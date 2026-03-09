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

다음 트위터 게시글을 아래 JSON 형식으로 요약해라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

{{
  "smart_brevity": {{
    "why": "한 문장 핵심 (왜 중요한가, 임팩트·의미 중심, 구체적 수치나 결과 포함)",
    "what": "2-3줄 설명 (무슨 일인가 — 핵심 메커니즘, 작동 방식, 차별점을 명확하게)"
  }},
  "tech_stack": ["실제 기술/도구/라이브러리명만"],
  "apply_points": ["recall로 파악한 Paul의 실제 프로젝트(orchestration, mcp-memory, tech-review 등)에 구체적으로 적용 가능한 것. 일반론 금지."],
  "explore_points": ["더 파볼 가치 있는 개념/구현/원리"]
}}

규칙:
- why: 한 문장, 핵심 임팩트만. 뻔한 표현 금지.
- what: 2-3줄. 구체적 숫자·기술명·작동 원리 포함.
- tech_stack: 실제 기술명만. 없으면 []
- apply_points: 반드시 recall 결과 기반 — Paul의 실제 프로젝트명·파일명·패턴을 언급. "자동화", "최적화" 같은 막연한 표현 금지.
- explore_points: 없으면 []
- 전부 한국어. 단, 고유명사(라이브러리명, 회사명)는 영어 유지.

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
            [
                "codex.cmd", "exec",
                f"파일 {tf_path} 을 읽고 지시대로 JSON을 만들어서 {out_path} 에 저장해라. 순수 JSON만.",
                "--full-auto",
            ],
            capture_output=True, text=True, timeout=180,
            cwd=str(BLOG_DIR)
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
        print("  Codex 타임아웃 (3분 초과)")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON 파싱 실패: {e}")
        print(f"  출력: {raw[:300]}")
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

    for tw in tweets:
        key = tw["url"] or tw["id"]
        if key and key in seen:
            print(f"  스킵 (중복): @{tw['author']}")
            continue

        print(f"  요약 중 (Codex): @{tw['author']} ...", end="", flush=True)
        summary = summarize_with_codex(tw["text"])
        if not summary:
            print(" 오류")
            continue

        bm = {
            "id": f"bm-{next_num:03d}",
            "author": tw["author"],
            "date": tw["date"],
            "added_at": datetime.now().strftime("%Y-%m-%d"),
            "url": tw["url"],
            **summary,
        }
        if tw["id"]:
            bm["tweet_id"] = tw["id"]

        bookmarks.append(bm)
        seen.add(key)
        next_num += 1
        added += 1
        print(f" ✓  {summary.get('smart_brevity', {}).get('why', '')[:60]}")

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
