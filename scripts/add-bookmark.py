#!/usr/bin/env python3
"""
add-bookmark.py — prinsss/twitter-web-exporter JSON → bookmarks.json 자동 추가
Codex CLI (gpt-5.4 xhigh) + mcp-memory recall로 apply_points 개인화

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
def summarize_with_claude(text: str) -> dict | None:
    """Claude CLI (-p) 비대화 모드로 트윗 분석. stdin으로 프롬프트 전달."""
    prompt = PROMPT_TEMPLATE.format(text=text[:8000])

    try:
        result = subprocess.run(
            "claude -p --output-format text",
            input=prompt, capture_output=True, text=True, timeout=120,
            encoding="utf-8", errors="replace",
            shell=True, cwd=str(BLOG_DIR),
        )

        raw = (result.stdout or "").strip()

        # 코드블록 제거
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())

        # JSON 부분만 추출
        json_match = re.search(r"\{[\s\S]*\}", raw)
        if json_match:
            raw = json_match.group(0)

        return json.loads(raw)

    except subprocess.TimeoutExpired:
        print("  Claude 타임아웃 (2분 초과)")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        print(f"  오류: {e}")
        return None


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
        summary = summarize_with_claude(tw["text"])
        if not summary:
            print(" FAIL")
            continue
        print(f" OK  {summary.get('whats_happening', '')[:50]}")
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
