#!/usr/bin/env python3
"""
add-bookmark.py — prinsss/twitter-web-exporter JSON → bookmarks.json 자동 추가

3-stage: Codex 구조화 → Claude -p WIM (Smart Brevity axiom)

Usage:
  python add-bookmark.py <bookmarks-raw.json>
  python add-bookmark.py  # inbox/ 폴더 최신 파일 자동 선택

Setup:
  pip install python-dotenv
"""

import json, os, re, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR     = Path(__file__).parent
BLOG_DIR       = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

load_dotenv(BLOG_DIR / ".env")

# ── Prompt ─────────────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """\
다음 트위터 게시글을 아래 JSON 형식으로 처리해라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

주의: why_it_matters 필드는 생성하지 마라. Why It Matters는 별도 단계에서 처리된다.

{{
  "whats_happening": "무슨 일인가 — 1-2문장, 핵심 사건·발표·발견을 구체적으로",
  "translation": "원문을 거의 그대로 한글로 번역. 요약 금지. 원문의 문장 구조·뉘앙스·어조를 최대한 살릴 것. 원문이 리스트면 리스트로, 문단이면 문단으로.",
  "tech_stack": ["언급된 실제 기술/도구/라이브러리명만"],
  "apply_points": ["Paul의 프로젝트(orchestration, mcp-memory, tech-review, portfolio)에 적용 가능한 것. 한 문장으로 간결하게. 파일 경로 금지. 일반론 금지."]
}}

규칙:
- whats_happening: 1-2문장. 사건 중심.
- translation: 번역이지 요약이 아님. 원문 길이의 90% 이상 유지. 영어 고유명사는 영어 유지.
- tech_stack: 없으면 []
- apply_points: 한 문장씩, 최대 3개. 파일 경로·backtick 금지. 50자 이내.
- 전부 한국어. 단, 고유명사(라이브러리명, 회사명, 인명)는 영어 유지.

트위터 내용:
{text}
"""

CLAUDE_PATH = "C:/Users/pauls/AppData/Roaming/npm/claude.cmd"
WIM_PROMPT_PATH = BLOG_DIR / "config" / "wim-prompt.md"


def generate_wim_twitter(summary: dict) -> str | None:
    """Claude -p로 Twitter 북마크 WIM 생성."""
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
    full_prompt = wim_prompt + "\n" + compact
    try:
        result = subprocess.run(
            [CLAUDE_PATH, "-p", "--setting-sources", "user"],
            input=full_prompt.encode("utf-8"),
            capture_output=True, timeout=120,
            cwd="C:/windows/temp", env={**os.environ}
        )
        wim_text = result.stdout.decode("utf-8", errors="replace").strip()
        if not wim_text or len(wim_text) < 20:
            return None
        # Why it matters 추출
        why_match = re.search(
            r"\*\*Why it matters:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)",
            wim_text, re.DOTALL
        )
        return why_match.group(1).strip() if why_match else wim_text[:200]
    except Exception:
        return None

# ── Tweet extraction ────────────────────────────────────────────────────────
def extract_tweets(raw):
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        items = raw.get("data") or raw.get("tweets") or raw.get("bookmarks") or []
    else:
        return []

    tweets = []
    for item in items:
        if not isinstance(item, dict):
            continue

        text = (
            item.get("full_text")
            or item.get("text")
            or item.get("legacy", {}).get("full_text", "")
        ).strip()
        if not text:
            continue

        user = item.get("user") or item.get("author") or {}
        if isinstance(user, str):
            author = user or "unknown"
        elif isinstance(user, dict):
            author = (
                user.get("screen_name")
                or user.get("username")
                or user.get("legacy", {}).get("screen_name", "unknown")
            )
        else:
            author = item.get("screen_name") or "unknown"

        tweet_id = item.get("rest_id") or item.get("id_str") or item.get("id") or ""

        url = (
            item.get("url")
            or item.get("tweet_url")
            or (f"https://x.com/{author}/status/{tweet_id}" if tweet_id else "")
        )

        created = item.get("created_at") or item.get("timestamp") or ""
        try:
            dt = datetime.strptime(created, "%a %b %d %H:%M:%S +0000 %Y")
            date = dt.strftime("%Y-%m-%d")
        except Exception:
            date = created[:10] if len(created) >= 10 else datetime.now().strftime("%Y-%m-%d")

        tweets.append({"id": tweet_id, "author": author, "text": text, "url": url, "date": date})

    return tweets


# ── Dedup ──────────────────────────────────────────────────────────────────
def load_existing(path):
    if not path.exists():
        return [], set()
    with open(path, encoding="utf-8") as f:
        bms = json.load(f)
    seen = set()
    for bm in bms:
        if bm.get("url"):
            seen.add(bm["url"])
        if bm.get("tweet_id"):
            seen.add(bm["tweet_id"])
    return bms, seen


# ── Codex CLI ────────────────────────────────────────────────────────────────
def summarize_with_codex(text: str) -> dict | None:
    """Codex CLI (GPT-5.4 xhigh) + mcp-memory recall로 분석"""
    prompt = PROMPT_TEMPLATE.format(text=text[:8000])

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BLOG_DIR
    ) as tf:
        tf.write(prompt)
        tf_path = tf.name

    try:
        out_path = BLOG_DIR / "_codex_bm_out.json"
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
        print("  Codex 타임아웃 (5분 초과)")
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


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) >= 2:
        raw_path = Path(sys.argv[1])
    else:
        inbox = BLOG_DIR / "inbox"
        files = sorted(inbox.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not files:
            print("inbox/ 폴더에 JSON 파일 없음. bookmarks-raw.json을 inbox/에 넣어주세요.")
            sys.exit(1)
        raw_path = files[0]
        print(f"파일 자동 선택: {raw_path.name}")

    if not raw_path.exists():
        print(f"파일 없음: {raw_path}")
        sys.exit(1)

    with open(raw_path, encoding="utf-8") as f:
        raw = json.load(f)

    tweets = extract_tweets(raw)
    print(f"로드: {len(tweets)}개 트윗")

    bookmarks, seen = load_existing(BOOKMARKS_JSON)
    next_num = len(bookmarks) + 1
    added = 0

    # 신규 트윗 필터
    new_tweets = []
    for tw in tweets:
        key = tw["url"] or tw["id"]
        if key and key in seen:
            print(f"  스킵 (중복): @{tw['author']}")
            continue
        new_tweets.append(tw)

    if not new_tweets:
        print("새 북마크 없음.")
        return

    print(f"신규 {len(new_tweets)}개 → Claude CLI 순차 분석...")

    for tw in new_tweets:
        print(f"  분석 중: @{tw['author']} ...", end="", flush=True)
        summary = summarize_with_codex(tw["text"])
        if not summary:
            print(" FAIL")
            continue
        # Stage 2: Claude WIM
        wim = generate_wim_twitter(summary)
        if wim:
            summary["why_it_matters"] = wim
            print(f" OK  WIM✓ {summary.get('whats_happening', '')[:40]}")
        else:
            print(f" OK  WIM✗ {summary.get('whats_happening', '')[:40]}")
        bm = {
            "id": f"bm-{next_num:03d}",
            "author": tw["author"],
            "date": tw["date"],
            "added_at": datetime.now().strftime("%Y-%m-%d"),
            "url": tw["url"],
            "text": tw["text"],
            **summary,
        }
        if tw["id"]:
            bm["tweet_id"] = tw["id"]

        bookmarks.append(bm)
        key = tw["url"] or tw["id"]
        seen.add(key)
        next_num += 1
        added += 1

    if added == 0:
        print("새 북마크 없음.")
        return

    with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    print(f"\n{added}개 추가 → {BOOKMARKS_JSON}")

    os.chdir(BLOG_DIR)
    os.system("git add _data/bookmarks.json")
    os.system(f'git commit -m "[tech-review] Twitter Bookmarks {added}개 추가 (Codex)"')
    os.system("git push")
    print("git push 완료")


if __name__ == "__main__":
    main()
