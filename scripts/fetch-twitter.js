#!/usr/bin/env node
/**
 * fetch-twitter.js
 * GitHub Actions / 로컬: Playwright 쿠키 로그인 → following 피드
 * → 필터(280자+ OR 스레드 OR 외부링크) → JSON 저장
 *
 * 환경변수:
 *   TWITTER_COOKIES  - GitHub Secret: 쿠키 JSON 문자열
 *   POST_DATE        - YYYY-MM-DD (기본: 오늘 KST)
 *   MAX_ITEMS        - 최대 수집 수 (기본: 30)
 *   DRY_RUN          - "true"이면 파일 저장 생략
 *
 * 사전 설치:
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require("playwright-extra");
const StealthPlugin = require("playwright-extra-plugin-stealth");
chromium.use(StealthPlugin());
const fs = require("fs");
const path = require("path");

const COOKIES_JSON = process.env.TWITTER_COOKIES;
const POST_DATE = process.env.POST_DATE ||
  new Date(Date.now() + 9 * 60 * 60 * 1000).toISOString().slice(0, 10); // KST
const MAX_ITEMS = parseInt(process.env.MAX_ITEMS || "30");
const DRY_RUN = process.env.DRY_RUN === "true";

if (!COOKIES_JSON) {
  console.error("TWITTER_COOKIES 환경변수가 필요합니다.");
  console.error("로컬: node scripts/export-cookies.js twitter 실행 후 출력값 사용");
  process.exit(1);
}

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

function shouldInclude(text, hasThread, hasLink) {
  if (text.length >= 280) return true;
  if (hasThread) return true;
  if (hasLink) return true;
  return false;
}

async function main() {
  let cookies;
  try {
    cookies = JSON.parse(COOKIES_JSON);
  } catch (e) {
    console.error("TWITTER_COOKIES JSON 파싱 실패:", e.message);
    process.exit(1);
  }

  // Cookie-Editor 내보내기 sameSite 값 정규화 (Chrome 내부 → Playwright 허용값)
  const sameSiteMap = {
    no_restriction: "None",
    lax: "Lax",
    strict: "Strict",
    unspecified: "None",
  };
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

  console.log("following 피드 로딩...");
  try {
    await page.goto("https://x.com/following", { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(5000); // JS 초기 렌더링 대기
    await page.waitForSelector('[data-testid="tweet"]', { timeout: 30000 }).catch(() => {});
    await page.waitForTimeout(2000);
  } catch (e) {
    console.error("페이지 로딩 실패:", e.message);
    await browser.close();
    process.exit(1);
  }

  console.log(`  현재 URL: ${page.url()}`);

  // 세션 만료 감지
  if (page.url().includes("/login") || page.url().includes("/i/flow")) {
    console.error("세션 만료 — TWITTER_COOKIES Secret 갱신 필요");
    console.error("로컬에서: node scripts/export-cookies.js twitter");
    await browser.close();
    process.exit(1);
  }

  // 디버그: 실제 존재하는 data-testid 목록 확인
  const foundTestIds = await page.evaluate(() => {
    const els = document.querySelectorAll("[data-testid]");
    const ids = [...new Set([...els].map((e) => e.getAttribute("data-testid")))];
    return ids.slice(0, 30).join(", ");
  });
  console.log(`  발견된 testIds: ${foundTestIds || "(없음)"}`);
  console.log(`  tweet 셀렉터 존재: ${foundTestIds.includes("tweet")}`);

  const items = [];
  const seen = new Set();
  let scrollCount = 0;

  while (items.length < MAX_ITEMS && scrollCount < 10) {
    const tweets = await page.$$eval('[data-testid="tweet"]', (els) =>
      els.map((el) => {
        const textEl = el.querySelector('[data-testid="tweetText"]');
        const text = textEl ? textEl.innerText : "";
        const timeEl = el.querySelector("time");
        const userEl = el.querySelector('[data-testid="User-Name"]');
        const tweetLinkEl = el.querySelector('a[href*="/status/"]');
        const hasThread = /\d+\/\d+/.test(text) || el.querySelector('[aria-label*="Thread"]') !== null;
        const externalLinks = [...el.querySelectorAll('a[href^="http"]')]
          .filter(a => !a.href.includes("x.com") && !a.href.includes("twitter.com"));
        const hasLink = externalLinks.length > 0;
        const userText = userEl ? userEl.innerText : "";
        const userLines = userText.split("\n").filter(Boolean);

        return {
          text,
          timestamp: timeEl ? timeEl.getAttribute("datetime") : "",
          author: userLines.length >= 2 ? "@" + userLines[1] : (userLines[0] || ""),
          url: tweetLinkEl ? "https://x.com" + tweetLinkEl.getAttribute("href") : "",
          is_thread: hasThread,
          has_external_link: hasLink,
          source_type: "twitter",
        };
      })
    );

    for (const t of tweets) {
      if (!t.text || !t.url) continue;
      if (seen.has(t.url)) continue;
      if (!shouldInclude(t.text, t.is_thread, t.has_external_link)) continue;
      seen.add(t.url);
      items.push(t);
      console.log(`  [${items.length}] ${t.author}: ${t.text.slice(0, 60)}...`);
      if (items.length >= MAX_ITEMS) break;
    }

    if (items.length < MAX_ITEMS) {
      await page.evaluate(() => window.scrollBy(0, 1500));
      await page.waitForTimeout(2000);
      scrollCount++;
    }
  }

  await browser.close();
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
