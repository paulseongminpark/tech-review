#!/usr/bin/env python3
"""
add-bookmark.py — prinsss/twitter-web-exporter JSON → bookmarks.json 자동 추가

Usage:
  python add-bookmark.py <bookmarks-raw.json>

Setup:
  pip install anthropic python-dotenv
  .env에 ANTHROPIC_API_KEY=your_key_here 추가
"""

import json, os, re, sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR     = Path(__file__).parent
BLOG_DIR       = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

load_dotenv(BLOG_DIR / ".env")
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Prompt ─────────────────────────────────────────────────────────────────
SYSTEM = "You are a concise tech summarizer. Output ONLY valid JSON, no markdown, no explanation."

PROMPT = """\
다음 트위터 스레드/게시글을 아래 JSON 포맷으로 요약해줘.
반드시 JSON만 출력해. 마크다운 코드블록 없이 순수 JSON만.

{
  "smart_brevity": {
    "why": "한 문장 핵심 (왜 중요한가, 임팩트·의미 중심, 구체적 수치나 결과 포함)",
    "what": "2-3줄 설명 (무슨 일인가 — 핵심 메커니즘, 작동 방식, 차별점을 명확하게)"
  },
  "tech_stack": ["실제 기술/도구/라이브러리명만"],
  "apply_points": ["내 프로젝트에 실제로 적용 가능한 구체적인 것 (추상적 표현 금지)"],
  "explore_points": ["더 파볼 가치 있는 개념/구현/원리"]
}

규칙:
- why: 한 문장, 핵심 임팩트만. "~가 중요하다" 같은 뻔한 표현 금지. 독자가 왜 읽어야 하는지 즉시 알게.
- what: 2-3줄. 구체적 숫자·기술명·작동 원리 포함. "소개됩니다" "됩니다" 같은 수동형 금지.
- tech_stack: 실제 기술명만. "비즈니스 모델 프레임워크" 같은 추상 표현 제외. 없으면 []
- apply_points: "자동화", "최적화" 같은 막연한 표현 금지. "XXX 패턴을 YYY에 적용" 수준으로 구체적으로.
- explore_points: 없으면 []
- 전부 한국어. 단, 고유명사(라이브러리명, 회사명)는 영어 유지.

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


# ── Claude Haiku ────────────────────────────────────────────────────────────
def summarize(text):
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM,
        messages=[
            {"role": "user", "content": PROMPT + text},
        ],
    )
    raw = resp.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw.strip())
    return json.loads(raw)


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) >= 2:
        raw_path = Path(sys.argv[1])
    else:
        # inbox/ 폴더에서 최신 파일 자동 선택
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
