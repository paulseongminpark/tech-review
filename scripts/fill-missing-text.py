#!/usr/bin/env python3
"""
fill-missing-text.py
raw json에서 text가 없는 항목들을 Playwright로 접속해서 텍스트 채우기.
기존 bookmarks.json의 URL 없는 항목도 raw와 매칭해서 URL 채우기.

Usage:
  python fill-missing-text.py
"""

import asyncio, json, re, sys
from pathlib import Path
from playwright.async_api import async_playwright

BLOG_DIR       = Path(__file__).parent.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"
RAW_JSON       = BLOG_DIR / "inbox" / "bookmarks-raw-2026-03-09.json"

# status ID 추출
def sid(url):
    m = re.search(r'status/(\d+)', url or '')
    return m.group(1) if m else None

# URL 정규화 (잘린 URL 복원)
def fix_url(url):
    if not url:
        return url
    if url.startswith('ttps://'):
        return 'h' + url
    if url.startswith('tps://'):
        return 'ht' + url
    if url.startswith('ps://'):
        return 'htt' + url
    if url.startswith('//'):
        return 'https:' + url
    return url

async def extract_text(page, url):
    """트윗 URL에서 텍스트 추출"""
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=15000)
        await page.wait_for_timeout(2500)

        text = await page.evaluate("""() => {
            const urlId = location.pathname.match(/status\\/(\\d+)/)?.[1];
            if (!urlId) return '';

            const articles = document.querySelectorAll('article[data-testid="tweet"]');

            // 1) URL ID가 포함된 time 링크의 article
            for (const a of articles) {
                const links = a.querySelectorAll('a[href*="/' + urlId + '"]');
                if (links.length) {
                    const tt = a.querySelector('[data-testid="tweetText"]');
                    if (tt) return tt.innerText.trim();
                    // Article 형식 fallback
                    const langDiv = a.querySelector('div[lang]');
                    if (langDiv) return langDiv.innerText.trim();
                }
            }

            // 2) 첫 번째 article의 tweetText
            for (const a of articles) {
                const tt = a.querySelector('[data-testid="tweetText"]');
                if (tt) return tt.innerText.trim();
            }

            // 3) div[lang] fallback
            const ld = document.querySelector('div[lang]');
            return ld ? ld.innerText.trim() : '';
        }""")
        return text.strip() if text else ''
    except Exception as e:
        print(f'  오류 ({url[:60]}): {e}')
        return ''

async def main():
    with open(RAW_JSON, encoding='utf-8') as f:
        raw = json.load(f)
    with open(BOOKMARKS_JSON, encoding='utf-8') as f:
        bookmarks = json.load(f)

    # 기존 bookmarks의 status ID 맵
    existing_sids = {}
    for bm in bookmarks:
        s = sid(bm.get('url', ''))
        if s:
            existing_sids[s] = bm

    # raw에서 빠진 항목 (status ID 기준)
    missing = []
    for r in raw:
        url = fix_url(r.get('url', ''))
        r['url'] = url
        s = sid(url)
        if s and s not in existing_sids and not r.get('text'):
            missing.append(r)

    # 기존 bookmarks 중 URL이 없는 것 → raw에서 매칭
    url_fixes = {}  # bm id → new url
    for bm in bookmarks:
        if not bm.get('url') or not sid(bm.get('url', '')):
            # raw에서 같은 author의 항목 찾기
            author_lower = bm.get('author', '').lower().replace('sysls', 'systematicls')
            for r in raw:
                r_author = r.get('author', '').lower()
                if r_author == author_lower or r_author == bm.get('author','').lower():
                    fixed = fix_url(r.get('url', ''))
                    if fixed:
                        url_fixes[bm['id']] = fixed
                        print(f"  URL 매칭: {bm['id']} @{bm.get('author')} → {fixed}")
                        break

    print(f"\n빠진 항목: {len(missing)}개, URL 수정: {len(url_fixes)}개")

    if not missing:
        print("텍스트 추출 불필요.")
    else:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            ctx = await browser.new_context()
            page = await ctx.new_page()

            # x.com 쿠키 로드 (Chrome 기존 세션 사용 안 됨 — 수동 로그인 필요)
            print("\n브라우저가 열렸습니다. x.com에 로그인되어 있는지 확인 중...")
            await page.goto('https://x.com', wait_until='domcontentloaded', timeout=15000)
            await page.wait_for_timeout(2000)
            url_now = page.url
            print(f"현재 URL: {url_now}")

            if 'login' in url_now or 'i/flow' in url_now:
                print("로그인이 필요합니다. 브라우저에서 로그인 후 Enter를 누르세요.")
                input()

            results = {}
            for i, r in enumerate(missing):
                url = r['url']
                author = r.get('author', '?')
                print(f"  [{i+1}/{len(missing)}] @{author} ...", end='', flush=True)
                text = await extract_text(page, url)
                results[url] = text
                if text:
                    print(f" OK ({len(text)}chars)")
                else:
                    print(" -- no text")

            await browser.close()

        # raw json 업데이트
        for r in raw:
            url = r.get('url', '')
            if url in results and results[url]:
                r['text'] = results[url]

    # raw json에 text 채워진 것 저장
    out_path = RAW_JSON.parent / (RAW_JSON.stem + '-filled.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)
    print(f"\nfilled raw 저장: {out_path.name}")

    # bookmarks.json URL 수정
    if url_fixes:
        for bm in bookmarks:
            if bm['id'] in url_fixes:
                bm['url'] = url_fixes[bm['id']]
        with open(BOOKMARKS_JSON, 'w', encoding='utf-8') as f:
            json.dump(bookmarks, f, ensure_ascii=False, indent=2)
        print(f"bookmarks.json URL {len(url_fixes)}개 수정 완료")

    print(f"\n다음 단계: python add-bookmark.py {out_path}")

if __name__ == '__main__':
    asyncio.run(main())
