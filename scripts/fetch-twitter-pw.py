#!/usr/bin/env python3
"""
fetch-twitter-pw.py — CDP로 기존 Chrome에 연결하여 X 북마크 자동 수집

사전 준비 (1회):
  Chrome 바로가기 대상에 --remote-debugging-port=9222 추가
  또는: chrome.exe --remote-debugging-port=9222

실행:
  python scripts/fetch-twitter-pw.py

동작:
  1. 기존 Chrome의 CDP 포트에 연결 (로그인 불필요)
  2. 새 탭에서 x.com/i/bookmarks 이동
  3. GraphQL 응답 가로채기 → 트윗 데이터 추출
  4. inbox/bookmarks-raw-YYYY-MM-DD.json 저장
  5. add-bookmark.py 체인 가능
"""

import json, os, re, sys, time, random
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
INBOX_DIR = BLOG_DIR / "inbox"
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

CDP_URL = "http://127.0.0.1:9222"
TODAY = datetime.now().strftime("%Y-%m-%d")
MAX_SCROLLS = 30
SCROLL_DELAY = (1.5, 3.0)
IDLE_LIMIT = 3


def load_existing_urls():
    if not BOOKMARKS_JSON.exists():
        return set()
    with open(BOOKMARKS_JSON, encoding="utf-8") as f:
        bms = json.load(f)
    return {bm["url"] for bm in bms if bm.get("url")}


def extract_tweets_from_graphql(data):
    tweets = []

    def walk(obj):
        if isinstance(obj, dict):
            if "tweet_results" in obj:
                result = obj["tweet_results"].get("result", {})
                parse_tweet_result(result, tweets)
            elif obj.get("__typename") == "Tweet":
                parse_tweet_result(obj, tweets)
            else:
                for v in obj.values():
                    walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return tweets


def parse_card(result):
    """트윗의 card 데이터 (링크 프리뷰, 영상 임베드) 추출"""
    card = result.get("card", {})
    if not card:
        return None

    legacy_card = card.get("legacy", {})
    card_name = legacy_card.get("name", "")
    bindings = legacy_card.get("binding_values", [])

    vals = {}
    for b in bindings:
        if not isinstance(b, dict):
            continue
        key = b.get("key", "")
        value = b.get("value", {})
        sv = value.get("string_value")
        iv = value.get("image_value", {})
        if sv:
            vals[key] = sv
        elif iv.get("url"):
            vals[key] = iv["url"]

    if not vals:
        return None

    parsed = {"type": card_name}
    if vals.get("title"):
        parsed["title"] = vals["title"]
    if vals.get("description"):
        parsed["description"] = vals["description"]
    if vals.get("vanity_url"):
        parsed["domain"] = vals["vanity_url"]
    if vals.get("card_url"):
        parsed["url"] = vals["card_url"]
    if vals.get("thumbnail_image_original"):
        parsed["thumbnail"] = vals["thumbnail_image_original"]
    elif vals.get("photo_image_full_size_original"):
        parsed["thumbnail"] = vals["photo_image_full_size_original"]
    if vals.get("player_url"):
        parsed["player_url"] = vals["player_url"]

    return parsed


def parse_media(legacy):
    """트윗의 미디어 (이미지, 영상) 추출"""
    media_list = legacy.get("extended_entities", {}).get("media", [])
    if not media_list:
        media_list = legacy.get("entities", {}).get("media", [])
    if not media_list:
        return []

    items = []
    for m in media_list:
        mtype = m.get("type", "photo")  # photo, video, animated_gif
        item = {"type": mtype, "url": m.get("media_url_https", "")}
        if mtype in ("video", "animated_gif"):
            variants = m.get("video_info", {}).get("variants", [])
            mp4s = [v for v in variants if v.get("content_type") == "video/mp4"]
            if mp4s:
                best = max(mp4s, key=lambda v: v.get("bitrate", 0))
                item["video_url"] = best["url"]
        items.append(item)
    return items


def parse_tweet_result(result, tweets):
    if not isinstance(result, dict):
        return
    if "tweet" in result:
        result = result["tweet"]

    user_result = result.get("core", {}).get("user_results", {}).get("result", {})
    legacy = result.get("legacy", {})
    # screen_name/name: user_result.core に（legacy ではなく）
    user_core = user_result.get("core", {})
    user_legacy = user_result.get("legacy", {})

    # note_tweet (280자 넘는 긴 트윗 전문)
    note = result.get("note_tweet", {}).get("note_tweet_results", {}).get("result", {})
    text = note.get("text") or legacy.get("full_text", "")
    if not text:
        return

    tweet_id = legacy.get("id_str") or result.get("rest_id", "")
    screen_name = user_core.get("screen_name") or user_legacy.get("screen_name", "")
    name = user_core.get("name") or user_legacy.get("name", "")
    created = legacy.get("created_at", "")

    # t.co → 실제 URL (note_tweet entities 우선, legacy fallback)
    note_entities = note.get("entity_set", {}).get("urls", [])
    legacy_entities = legacy.get("entities", {}).get("urls", [])
    for u in (note_entities or legacy_entities):
        text = text.replace(u.get("url", ""), u.get("expanded_url", ""))

    # 미디어 URL 제거 (텍스트에서만, 미디어는 별도 저장)
    for m in legacy.get("entities", {}).get("media", []):
        text = text.replace(m.get("url", ""), "").strip()

    tweet_url = f"https://x.com/{screen_name}/status/{tweet_id}" if screen_name and tweet_id else ""

    # X Article 감지 — GraphQL에 article 본문이 있는지 기록
    is_article = bool(re.match(r'^https?://(x\.com|twitter\.com)/i/article/\d+$', text.strip()))
    article_keys = []
    if is_article:
        for key in ("article", "article_results", "unified_card"):
            if key in result:
                article_keys.append(key)

    tweet_data = {
        "id": tweet_id,
        "text": text.strip(),
        "user": {"screen_name": screen_name, "name": name},
        "url": tweet_url,
        "created_at": created,
    }
    if is_article:
        tweet_data["is_article"] = True
        if article_keys:
            tweet_data["article_graphql_keys"] = article_keys

    # card 데이터 (링크 프리뷰, 영상 임베드)
    card = parse_card(result)
    if card:
        tweet_data["card"] = card

    # 미디어 (이미지, 영상)
    media = parse_media(legacy)
    if media:
        tweet_data["media"] = media

    tweets.append(tweet_data)


def fetch_bookmarks():
    existing_urls = load_existing_urls()
    captured_tweets = []
    seen_ids = set()

    def handle_response(response):
        url = response.url
        if "/graphql/" not in url or "Bookmark" not in url:
            return
        try:
            data = response.json()
            tweets = extract_tweets_from_graphql(data)
            for tw in tweets:
                if tw["id"] and tw["id"] not in seen_ids:
                    seen_ids.add(tw["id"])
                    captured_tweets.append(tw)
        except Exception as e:
            print(f"  [WARN] GraphQL 파싱 오류: {e}")

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            print(f"Chrome CDP 연결 성공 ({CDP_URL})")
        except Exception as e:
            print(f"Chrome CDP 연결 실패: {e}")
            print(f"\nChrome을 --remote-debugging-port=9222 로 시작하세요:")
            print(f'  chrome.exe --remote-debugging-port=9222')
            sys.exit(1)

        # 기존 context 사용 (로그인 세션 포함)
        context = browser.contexts[0]
        page = context.new_page()
        page.on("response", handle_response)

        print("북마크 페이지 이동 중...")
        page.goto("https://x.com/i/bookmarks", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        if "login" in page.url.lower():
            print("X에 로그인되어 있지 않습니다. Chrome에서 먼저 로그인하세요.")
            page.close()
            browser.close()
            sys.exit(1)

        print(f"초기 로드: {len(captured_tweets)}개 캡처\n")

        retry_count = 0

        for i in range(MAX_SCROLLS):
            prev_count = len(captured_tweets)

            # 랜덤 딜레이 (인간적 행동)
            time.sleep(random.uniform(*SCROLL_DELAY))

            # 콘텐츠 맨 아래로 스크롤
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # GraphQL Bookmark 응답 대기 (응답 기반)
            try:
                page.wait_for_response(
                    lambda r: "/graphql/" in r.url and "Bookmark" in r.url,
                    timeout=8000,
                )
            except Exception:
                pass  # 타임아웃 — 아래에서 retry 처리

            # 응답 처리 시간 확보
            page.wait_for_timeout(1000)

            current = len(captured_tweets)
            new_this_scroll = current - prev_count

            if new_this_scroll > 0:
                print(f"  스크롤 {i+1}/{MAX_SCROLLS}: +{new_this_scroll}개 (총 {current}개)")
                retry_count = 0
            else:
                retry_count += 1
                if retry_count >= 2:
                    print(f"  2회 연속 응답 없음 -> 종료")
                    break

        # 탭만 닫기 (Chrome 유지)
        page.close()
        browser.close()

    new_tweets = [t for t in captured_tweets if t["url"] not in existing_urls]
    print(f"\n캡처: {len(captured_tweets)}개 (신규: {len(new_tweets)}개, 기존: {len(captured_tweets) - len(new_tweets)}개)")

    if not captured_tweets:
        print("캡처된 트윗 없음.")
        return None

    INBOX_DIR.mkdir(exist_ok=True)
    out_path = INBOX_DIR / f"bookmarks-raw-{TODAY}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(captured_tweets, f, ensure_ascii=False, indent=2)
    print(f"저장: {out_path} ({len(captured_tweets)}개)")
    return out_path


def main():
    os.chdir(BLOG_DIR)
    fetch_bookmarks()


if __name__ == "__main__":
    main()
