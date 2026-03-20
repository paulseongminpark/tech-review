#!/usr/bin/env python3
"""bm-045~055 재분석 — Codex GPT-5.4 + mcp-memory recall"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

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


def summarize_with_codex(text, bm_id):
    prompt = PROMPT_TEMPLATE.format(text=text[:8000])

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BLOG_DIR
    ) as tf:
        tf.write(prompt)
        tf_path = tf.name

    try:
        out_path = BLOG_DIR / f"_codex_reprocess_{bm_id}.json"
        result = subprocess.run(
            [
                "codex.cmd", "exec",
                f"파일 {tf_path} 을 읽고 지시대로 JSON을 만들어서 {out_path} 에 저장해라. 순수 JSON만.",
                "--full-auto",
            ],
            capture_output=True, text=True, timeout=300,
            encoding="utf-8", errors="replace",
            cwd=str(BLOG_DIR)
        )

        if out_path.exists():
            raw = out_path.read_text(encoding="utf-8").strip()
            out_path.unlink()
        else:
            raw = (result.stdout or "").strip()

        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())

        json_match = re.search(r"\{[\s\S]*\}", raw)
        if json_match:
            raw = json_match.group(0)

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
    bm = json.load(open(BOOKMARKS_JSON, encoding="utf-8"))
    targets = [b for b in bm if b["id"] >= "bm-045"]
    print(f"재분석 대상: {len(targets)}개")

    updated = 0
    for b in targets:
        text = b.get("text", "")
        if not text or len(text) < 50:
            print(f"  {b['id']} @{b['author']}: 본문 없음 — 스킵")
            continue

        print(f"\n[{b['id']}] @{b['author']} ({len(text)}자)...", end="", flush=True)
        summary = summarize_with_codex(text, b["id"])
        if not summary:
            print(" FAIL")
            continue

        for key in ["whats_happening", "why_it_matters", "translation", "tech_stack", "apply_points"]:
            if key in summary:
                b[key] = summary[key]

        updated += 1
        print(f" OK — {summary.get('whats_happening', '')[:50]}")

        # 건마다 저장
        with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
            json.dump(bm, f, ensure_ascii=False, indent=2)

    print(f"\n{updated}/{len(targets)}개 재분석 완료")

    if updated > 0:
        os.chdir(BLOG_DIR)
        os.system("git add _data/bookmarks.json")
        os.system(f'git commit -m "[tech-review] bm-045~055 Codex 재분석 ({updated}개)"')
        os.system("git push")
        print("push 완료")


if __name__ == "__main__":
    main()
