#!/usr/bin/env python3
"""
add-bookmark.py — prinsss/twitter-web-exporter JSON → bookmarks.json 자동 추가

Usage:
  python add-bookmark.py <bookmarks-raw.json>

Setup:
  pip install groq python-dotenv
  .env에 GROQ_API_KEY=your_key_here 추가
"""

import json, os, re, sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR     = Path(__file__).parent
BLOG_DIR       = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

load_dotenv(BLOG_DIR / ".env")
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Prompt ─────────────────────────────────────────────────────────────────
SYSTEM = "You are a concise tech summarizer. Output ONLY valid JSON, no markdown, no explanation."

PROMPT = """\
다음 트위터 스레드/게시글을 아래 JSON 포맷으로 요약해줘.
반드시 JSON만 출력해. 마크다운 코드블록 없이 순수 JSON만.

{
  "smart_brevity": {
    "why": "한 문장 핵심 (왜 중요한가, 임팩트 중심)",
    "what": "2-3줄 설명 (무슨 일인가, Smart Brevity 스타일)"
  },
  "tech_stack": ["기술/도구명만"],
  "apply_points": ["실제 프로젝트 적용 가능한 것"],
  "explore_points": ["더 파볼 가치 있는 것"]
}

규칙:
- why: 한 문장, 핵심만
- what: 2-3줄, 짧고 명확하게
- tech_stack: 실제 기술명만, 없으면 []
- apply_points: 구체적으로, 없으면 []
- explore_points: 없으면 []
- 전부 한국어

트위터 내용:
"""

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
        if isinstance(user, dict):
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


# ── Groq ───────────────────────────────────────────────────────────────────
def summarize(text):
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT + text},
        ],
        temperature=0.3,
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw.strip())
    return json.loads(raw)


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python add-bookmark.py <bookmarks-raw.json>")
        sys.exit(1)

    raw_path = Path(sys.argv[1])
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

    for tw in tweets:
        key = tw["url"] or tw["id"]
        if key and key in seen:
            print(f"  스킵 (중복): @{tw['author']}")
            continue

        print(f"  요약 중: @{tw['author']} ...", end="", flush=True)
        try:
            summary = summarize(tw["text"])
        except Exception as e:
            print(f" 오류: {e}")
            continue

        bm = {
            "id": f"bm-{next_num:03d}",
            "author": tw["author"],
            "date": tw["date"],
            "url": tw["url"],
            **summary,
        }
        if tw["id"]:
            bm["tweet_id"] = tw["id"]

        bookmarks.append(bm)
        seen.add(key)
        next_num += 1
        added += 1
        print(f" ✓  {summary['smart_brevity']['why'][:60]}")

    if added == 0:
        print("새 북마크 없음.")
        return

    with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    print(f"\n{added}개 추가 → {BOOKMARKS_JSON}")

    os.chdir(BLOG_DIR)
    os.system("git add _data/bookmarks.json")
    os.system(f'git commit -m "[tech-review] Twitter Bookmarks {added}개 자동 추가"')
    os.system("git push")
    print("git push 완료")


if __name__ == "__main__":
    main()
