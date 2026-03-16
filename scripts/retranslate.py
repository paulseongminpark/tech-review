#!/usr/bin/env python3
"""
retranslate.py — 지정된 북마크 ID의 text를 Codex로 한국어 번역
Usage: python scripts/retranslate.py bm-011 bm-018 bm-030 bm-036 bm-037
"""

import json, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

PROMPT_TEMPLATE = """\
아래 영문 트윗을 한국어로 번역하라.
규칙:
- 요약이 아니라 번역이다. 원문의 모든 내용을 빠짐없이 번역할 것.
- 원문 길이의 90% 이상을 유지할 것.
- 문장 구조, 뉘앙스, 어조를 최대한 살릴 것.
- 리스트면 리스트로, 문단이면 문단으로 구조 유지.
- 고유명사(라이브러리명, 회사명, 인명, URL)는 영어 유지.
- 번역문만 출력. 설명이나 마크다운 없이 순수 텍스트만.

원문:
{text}
"""

def translate_with_codex(text: str) -> str | None:
    prompt = PROMPT_TEMPLATE.format(text=text[:12000])

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BLOG_DIR
    ) as tf:
        tf.write(prompt)
        tf_path = tf.name

    try:
        out_path = BLOG_DIR / "_codex_trans_out.txt"
        result = subprocess.run(
            [
                "codex.cmd", "exec",
                f"파일 {tf_path} 을 읽고 지시대로 번역해서 {out_path} 에 저장해라. 순수 텍스트만.",
                "--full-auto",
            ],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300, cwd=str(BLOG_DIR),
        )

        if out_path.exists():
            trans = out_path.read_text(encoding="utf-8").strip()
            out_path.unlink()
            return trans
        else:
            return (result.stdout or "").strip()

    except subprocess.TimeoutExpired:
        print("  Codex 타임아웃")
        return None
    except Exception as e:
        print(f"  오류: {e}")
        return None
    finally:
        try:
            os.unlink(tf_path)
        except:
            pass


def main():
    target_ids = sys.argv[1:] if len(sys.argv) > 1 else []
    if not target_ids:
        print("Usage: python retranslate.py bm-011 bm-018 ...")
        sys.exit(1)

    os.chdir(BLOG_DIR)

    with open(BOOKMARKS_JSON, encoding="utf-8") as f:
        bookmarks = json.load(f)

    updated = 0
    for bm in bookmarks:
        if bm["id"] not in target_ids:
            continue

        text = bm.get("text", "")
        if not text:
            print(f"  {bm['id']}: text 없음, 스킵")
            continue

        print(f"  번역 중: {bm['id']} @{bm.get('author','')} ({len(text)}자)...", end="", flush=True)
        trans = translate_with_codex(text)

        if trans and len(trans) > len(text) * 0.3:
            bm["translation"] = trans
            updated += 1
            print(f" OK ({len(trans)}자)")
        else:
            print(f" 실패 (결과: {len(trans) if trans else 0}자)")

    with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

    print(f"\n{updated}개 번역 업데이트 완료")


if __name__ == "__main__":
    main()
