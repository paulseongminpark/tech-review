#!/usr/bin/env node
/**
 * fetch-twitter.js
 * page.route()로 X.com GraphQL API 응답 인터셉트 → following 피드 수집
 *
 * 환경변수:
 *   TWITTER_COOKIES  - GitHub Secret: 쿠키 JSON 문자열
 *   POST_DATE        - YYYY-MM-DD (기본: 오늘 KST)
 *   MAX_ITEMS        - 최대 수집 수 (기본: 30)
 *   DRY_RUN          - "true"이면 파일 저장 생략
 */

const { chromium } = require("playwright-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
chromium.use(StealthPlugin());
const fs = require("fs");
const path = require("path");

const COOKIES_JSON = process.env.TWITTER_COOKIES;
const POST_DATE = process.env.POST_DATE ||
  new Date(Date.now() + 9 * 60 * 60 * 1000).toISOString().slice(0, 10);
const MAX_ITEMS = parseInt(process.env.MAX_ITEMS || "30");
const DRY_RUN = process.env.DRY_RUN === "true";

if (!COOKIES_JSON) {
  console.error("TWITTER_COOKIES 환경변수가 필요합니다.");
  process.exit(1);
}

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

function shouldInclude(text, hasThread, hasLink) {
  if (text.length >= 280) return true;
  if (hasThread) return true;
  if (hasLink) return true;
  return false;
}

function parseTweetsFromGraphQL(json) {
  const tweets = [];
  try {
    const instructions =
      json?.data?.home?.home_timeline_urt?.instructions ||
      json?.data?.timeline_by_id?.timeline?.instructions ||
      json?.data?.timeline?.instructions ||
      json?.data?.user?.result?.timeline_v2?.timeline?.instructions ||
      json?.data?.user_result?.result?.timeline_v2?.timeline?.instructions ||
      [];

    for (const inst of instructions) {
      if (inst.type !== "TimelineAddEntries") continue;
      for (const entry of (inst.entries || [])) {
        const result =
          entry.content?.itemContent?.tweet_results?.result ||
          entry.content?.items?.[0]?.item?.itemContent?.tweet_results?.result;
        if (!result) continue;

        const tweet = result.tweet || result;
        const legacy = tweet.legacy;
        const userLegacy =
          tweet.core?.user_results?.result?.legacy ||
          tweet.core?.user_results?.result?.user?.legacy;
        if (!legacy || !userLegacy) continue;

        const tweetId = legacy.id_str || tweet.rest_id;
        const screenName = userLegacy.screen_name;
        if (!tweetId || !screenName) continue;

        const text = legacy.full_text.replace(/https:\/\/t\.co\/\S+/g, "").trim();
        const urls = legacy.entities?.urls || [];
        const externalLinks = urls.filter(
          (u) => u.expanded_url &&
            !u.expanded_url.includes("twitter.com") &&
            !u.expanded_url.includes("x.com")
        );

        tweets.push({
          text,
          timestamp: legacy.created_at,
          author: "@" + screenName,
          url: `https://x.com/${screenName}/status/${tweetId}`,
          is_thread: /\d+\/\d+/.test(legacy.full_text),
          has_external_link: externalLinks.length > 0,
          source_type: "twitter",
        });
      }
    }
  } catch (_) {}
  return tweets;
}

async function main() {
  let cookies;
  try {
    cookies = JSON.parse(COOKIES_JSON);
  } catch (e) {
    console.error("TWITTER_COOKIES JSON 파싱 실패:", e.message);
    process.exit(1);
  }

  const sameSiteMap = { no_restriction: "None", lax: "Lax", strict: "Strict", unspecified: "None" };
  cookies = cookies.map((c) => ({
    ...c,
    sameSite: sameSiteMap[c.sameSite?.toLowerCase()] || "None",
  }));

  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const context = await browser.newContext({
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    locale: "en-US",
  });
  await context.addCookies(cookies);
  const page = await context.newPage();

  const items = [];
  const seen = new Set();
  const capturedJSON = [];

  // 모든 GraphQL 응답 캡처 (엔드포인트 무관)
  await page.route("**/graphql/**", async (route) => {
    try {
      const response = await route.fetch();
      const body = await response.text();
      const reqUrl = route.request().url();
      const epMatch = reqUrl.match(/graphql\/[^/]+\/([^?]+)/);
      const endpoint = epMatch ? epMatch[1] : "unknown";
      if (body.length > 500) {
        console.log(`  GraphQL: ${endpoint} (${body.length}자)`);
        try { capturedJSON.push({ endpoint, json: JSON.parse(body) }); } catch (_) {}
      }
      await route.fulfill({ response });
    } catch (_) {
      await route.continue();
    }
  });

  console.log("홈 피드 로딩...");
  try {
    await page.goto("https://x.com/home", { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(4000);
  } catch (e) {
    console.error("페이지 로딩 실패:", e.message);
    await browser.close();
    process.exit(1);
  }

  console.log(`  현재 URL: ${page.url()}`);
  if (page.url().includes("/login") || page.url().includes("/i/flow")) {
    console.error("세션 만료 — TWITTER_COOKIES Secret 갱신 필요");
    await browser.close();
    process.exit(1);
  }

  // "Following" 탭 클릭 → HomeLatestTimeline 트리거
  console.log("  Following 탭 클릭...");
  const tabSelectors = [
    '[aria-label="Following"]',
    '[aria-label="Latest tweets"]',
    '[data-testid="ScrollSnap-SwipeableList"] a:last-child',
    'nav[aria-label="Primary"] a[href="/following"]',
    'a[href="/following"]',
  ];
  let tabClicked = false;
  for (const sel of tabSelectors) {
    try {
      await page.click(sel, { timeout: 3000 });
      console.log(`  탭 클릭 성공: ${sel}`);
      tabClicked = true;
      break;
    } catch (_) {
      console.log(`  탭 클릭 실패: ${sel}`);
    }
  }
  if (!tabClicked) {
    console.log("  모든 selector 실패 → x.com/following 직접 접근");
    await page.goto("https://x.com/following", { waitUntil: "domcontentloaded", timeout: 60000 });
  }
  await page.waitForTimeout(6000);

  // 스크롤로 추가 트윗 로드
  for (let i = 0; i < 8; i++) {
    await page.evaluate(() => window.scrollBy(0, 2000));
    await page.waitForTimeout(3000);
  }

  await browser.close();

  // 캡처된 GraphQL 응답에서 트윗 파싱
  console.log(`\n캡처된 graphql 응답: ${capturedJSON.length}개`);
  for (const { endpoint, json } of capturedJSON) {
    const tweets = parseTweetsFromGraphQL(json);
    if (tweets.length > 0) console.log(`  [${endpoint}] ${tweets.length}개 트윗 파싱됨`);

    for (const t of tweets) {
      if (!t.text || !t.url) continue;
      if (seen.has(t.url)) continue;
      if (!shouldInclude(t.text, t.is_thread, t.has_external_link)) continue;
      seen.add(t.url);
      items.push(t);
      console.log(`  [${items.length}] ${t.author}: ${t.text.slice(0, 60)}...`);
      if (items.length >= MAX_ITEMS) break;
    }
  }

  console.log(`\n수집 완료: ${items.length}개`);

  if (DRY_RUN) {
    console.log("DRY_RUN: 파일 저장 생략");
    console.log(JSON.stringify(items.slice(0, 3), null, 2));
    return;
  }

  fs.mkdirSync(DATA_DIR, { recursive: true });
  const outFile = path.join(DATA_DIR, `twitter-${POST_DATE}.json`);
  fs.writeFileSync(outFile, JSON.stringify(items, null, 2));
  console.log(`저장: ${outFile}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
