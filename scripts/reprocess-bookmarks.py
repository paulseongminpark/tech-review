#!/usr/bin/env python3
"""깨진 북마크 재분석 — OpenAI gpt-4.1-mini + Claude WIM

Usage:
  python reprocess-bookmarks.py                    # "Credit balance" 깨진 것만
  python reprocess-bookmarks.py --ids bm-064,bm-065  # 특정 ID 지정
"""
import json, os, re, subprocess, sys, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

from dotenv import load_dotenv
load_dotenv(BLOG_DIR / ".env")
load_dotenv(Path("C:/dev/01_projects/06_mcp-memory/.env"))

CLAUDE_PATH = "C:/Users/pauls/AppData/Roaming/npm/claude.cmd"
WIM_PROMPT_PATH = BLOG_DIR / "config" / "wim-prompt.md"

PROMPT_TEMPLATE = """\
다음 트위터 게시글을 아래 JSON 형식으로 처리해라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

주의: why_it_matters 필드는 생성하지 마라.

{{
  "whats_happening": "무슨 일인가 — 1-2문장, 핵심 사건·발표·발견을 구체적으로",
  "translation": "원문을 거의 그대로 한글로 번역. 요약 금지.",
  "tech_stack": ["언급된 실제 기술/도구/라이브러리명만"],
  "apply_points": ["적용 가능한 포인트. 한 문장으로 간결하게."]
}}

규칙:
- whats_happening: 1-2문장. 사건 중심.
- translation: 원문 길이의 90% 이상 유지. 영어 고유명사 유지.
- tech_stack: 없으면 []
- apply_points: 최대 3개. 50자 이내.
- 전부 한국어. 고유명사(라이브러리명, 회사명, 인명)는 영어 유지.

트위터 내용:
{text}
"""


def summarize_openai(text):
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("  OPENAI_API_KEY 없음")
        return None
    prompt = PROMPT_TEMPLATE.format(text=text[:8000])
    try:
        body = json.dumps({
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "You are a tweet analyzer. Output ONLY valid JSON, no markdown code blocks."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_completion_tokens": 4096,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        )
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read().decode("utf-8"))
        raw = data["choices"][0]["message"]["content"].strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            raw = m.group(0)
        return json.loads(raw)
    except Exception as e:
        print(f"  OpenAI 실패: {e}")
        return None


def generate_wim(summary):
    if not WIM_PROMPT_PATH.exists():
        return None
    wim_prompt = WIM_PROMPT_PATH.read_text(encoding="utf-8")
    compact = json.dumps({
        "title": summary.get("whats_happening", ""),
        "key_takeaways": [summary.get("whats_happening", "")],
        "tech_stack": summary.get("tech_stack", []),
        "apply_points": summary.get("apply_points", []),
        "sections": [],
    }, indent=2, ensure_ascii=False)
    try:
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        result = subprocess.run(
            [CLAUDE_PATH, "-p", "--setting-sources", "user"],
            input=(wim_prompt + "\n" + compact).encode("utf-8"),
            capture_output=True, timeout=120,
            cwd="C:/windows/temp", env=env,
        )
        if result.returncode != 0:
            return None
        wim_text = result.stdout.decode("utf-8", errors="replace").strip()
        if not wim_text or len(wim_text) < 20:
            return None
        if any(err in wim_text.lower() for err in ["credit balance", "rate limit", "unauthorized"]):
            return None
        m = re.search(r"\*\*Why it matters:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)", wim_text, re.DOTALL)
        return m.group(1).strip() if m else wim_text[:200]
    except Exception:
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", help="쉼표 구분 ID (예: bm-064,bm-065)")
    args = parser.parse_args()

    bm = json.load(open(BOOKMARKS_JSON, encoding="utf-8"))

    if args.ids:
        target_ids = set(args.ids.split(","))
        targets = [b for b in bm if b["id"] in target_ids]
    else:
        targets = [b for b in bm if b.get("why_it_matters") == "Credit balance is too low"
                    or b.get("category") == ""]

    print(f"재분석 대상: {len(targets)}개")

    updated = 0
    for b in targets:
        text = b.get("text", "")
        if not text or len(text) < 20:
            print(f"  {b['id']}: 본문 부족 — 스킵")
            continue

        print(f"[{b['id']}] @{b.get('author','')}...", end="", flush=True)

        summary = summarize_openai(text)
        if not summary:
            print(" FAIL (OpenAI)")
            continue

        wim = generate_wim(summary)

        for key in ["whats_happening", "translation", "tech_stack", "apply_points"]:
            if key in summary:
                b[key] = summary[key]
        if wim:
            b["why_it_matters"] = wim
            print(f" OK+WIM")
        else:
            b.pop("why_it_matters", None)
            print(f" OK (WIM 없음)")

        updated += 1
        with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
            json.dump(bm, f, ensure_ascii=False, indent=2)

    print(f"\n{updated}/{len(targets)}개 완료")

    if updated > 0:
        os.chdir(BLOG_DIR)
        os.system("git add _data/bookmarks.json")
        os.system(f'git commit -m "[tech-review] 깨진 북마크 {updated}개 재분석 (OpenAI+WIM)"')
        os.system("git push")
        print("push 완료")


if __name__ == "__main__":
    main()
