#!/usr/bin/env python3
"""
reprocess-bookmarks.py — inbox/ raw 파일로 bookmarks.json 재처리
새 프롬프트 구조(whats_happening, why_it_matters, translation, apply_points) 적용

Usage: python scripts/reprocess-bookmarks.py
"""

import json, os, re, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR     = Path(__file__).parent
BLOG_DIR       = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

# add-bookmark.py와 동일한 프롬프트
PROMPT_TEMPLATE = """\
먼저 mcp-memory의 recall 도구를 호출해서 Paul의 현재 프로젝트 컨텍스트를 파악하라.
recall 쿼리: "Paul orchestration mcp-memory tech-review 프로젝트 현재 작업"

recall 결과를 바탕으로 아래 작업을 수행하라.

다음 트위터 게시글을 아래 JSON 형식으로 처리해라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

{{
  "whats_happening": "무슨 일인가 — 1-2문장, 핵심 사건·발표·발견을 구체적으로",
  "why_it_matters": "왜 중요한가 — 1-2문장, 임팩트와 의미 중심",
  "translation": "원문을 거의 그대로 한글로 번역. 요약 금지. 원문의 문장 구조·뉘앙스·어조를 최대한 살릴 것. 원문이 리스트면 리스트로, 문단이면 문단으로.",
  "tech_stack": ["언급된 실제 기술/도구/라이브러리명만"],
  "apply_points": ["recall로 파악한 Paul의 실제 프로젝트에 구체적으로 적용 가능한 것. 한 문장으로 간결하게. 파일 경로 금지. 일반론 금지."]
}}

규칙:
- whats_happening: 1-2문장. 사건 중심.
- why_it_matters: 1-2문장. 의미 중심.
- translation: 번역이지 요약이 아님. 원문 길이의 90% 이상 유지. 영어 고유명사는 영어 유지.
- tech_stack: 없으면 []
- apply_points: 한 문장씩, 최대 3개. 파일 경로·backtick 금지. 50자 이내.
- 전부 한국어. 단, 고유명사(라이브러리명, 회사명, 인명)는 영어 유지.

트위터 내용:
{text}
"""

def summarize_with_codex(text: str) -> dict | None:
    prompt = PROMPT_TEMPLATE.format(text=text[:8000])
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BLOG_DIR
    ) as tf:
        tf.write(prompt)
        tf_path = tf.name

    try:
        out_path = BLOG_DIR / "_codex_bm_out.json"
        result = subprocess.run(
            ["codex.cmd", "exec",
             f"파일 {tf_path} 을 읽고 지시대로 JSON을 만들어서 {out_path} 에 저장해라. 순수 JSON만.",
             "--full-auto"],
            capture_output=True, text=True, timeout=180, cwd=str(BLOG_DIR)
        )
        if out_path.exists():
            raw = out_path.read_text(encoding="utf-8").strip()
            out_path.unlink()
        else:
            raw = (result.stdout or "").strip()

        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        return json.loads(raw)
    except subprocess.TimeoutExpired:
        print("  Codex 타임아웃")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        print(f"  오류: {e}")
        return None
    finally:
        try:
            os.unlink(tf_path)
        except Exception:
            pass

def main():
    # inbox/ raw 파일에서 url→text 맵 구성
    inbox = BLOG_DIR / "inbox"
    url_to_text = {}
    for raw_file in sorted(inbox.glob("*.json")):
        try:
            items = json.loads(raw_file.read_text(encoding="utf-8"))
            if isinstance(items, list):
                for item in items:
                    url = item.get("url", "")
                    text = item.get("text", "") or item.get("full_text", "")
                    if url and text:
                        url_to_text[url] = text
        except Exception:
            pass

    print(f"raw 파일에서 {len(url_to_text)}개 트윗 원문 로드")

    with open(BOOKMARKS_JSON, encoding="utf-8") as f:
        bookmarks = json.load(f)

    updated = 0
    skipped = 0

    for bm in bookmarks:
        url = bm.get("url", "")
        # 이미 text 필드 있고 새 구조면 스킵
        existing_text = bm.get("text", "")
        if url in url_to_text:
            text = url_to_text[url]
        elif existing_text:
            text = existing_text
        else:
            print(f"  스킵 (원문 없음): {bm['id']} @{bm.get('author','?')}")
            skipped += 1
            continue

        print(f"  재처리 중: {bm['id']} @{bm.get('author','?')} ...", end="", flush=True)
        summary = summarize_with_codex(text)
        if not summary:
            print(" 실패")
            continue

        # 기존 필드 제거 후 새 구조로 교체
        for old_key in ["smart_brevity", "explore_points"]:
            bm.pop(old_key, None)

        bm["text"] = text
        bm["whats_happening"] = summary.get("whats_happening", "")
        bm["why_it_matters"] = summary.get("why_it_matters", "")
        bm["translation"] = summary.get("translation", "")
        bm["tech_stack"] = summary.get("tech_stack", [])
        bm["apply_points"] = summary.get("apply_points", [])

        updated += 1
        print(f" ✓  {bm['whats_happening'][:60]}")

    with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)

    print(f"\n완료 — 재처리 {updated}개, 스킵 {skipped}개")

if __name__ == "__main__":
    main()
