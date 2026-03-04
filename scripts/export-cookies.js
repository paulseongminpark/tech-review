#!/usr/bin/env node
/**
 * export-cookies.js
 * 로컬 실행용: 브라우저 쿠키 저장 → GitHub Secret 갱신에 사용
 *
 * 사용:
 *   node scripts/export-cookies.js twitter
 *   node scripts/export-cookies.js threads
 *
 * 동작:
 *   1. Playwright로 브라우저 창 오픈
 *   2. 사용자가 직접 로그인
 *   3. Enter 입력 시 쿠키 추출 → JSON 출력
 *   4. 출력된 JSON을 GitHub Secret에 붙여넣기
 *
 * 사전 설치:
 *   npm install playwright
 *   npx playwright install chromium
 */

const { chromium } = require("playwright");
const readline = require("readline");
const fs = require("fs");
const path = require("path");

const SERVICE = process.argv[2];
if (!["twitter"].includes(SERVICE)) {
  console.error("사용법: node scripts/export-cookies.js twitter");
  process.exit(1);
}

const URLS = {
  twitter: "https://x.com/login",
};

async function main() {
  console.log(`\n${SERVICE.toUpperCase()} 쿠키 추출 시작...`);
  const browser = await chromium.launch({ headless: false, channel: 'chrome' });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(URLS[SERVICE]);
  console.log(`\n브라우저에서 ${SERVICE} 로그인을 완료하세요.`);
  console.log("로그인 완료 후 이 터미널에서 Enter를 누르세요...\n");

  await new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin });
    rl.once("line", () => { rl.close(); resolve(); });
  });

  const cookies = await context.cookies();
  const cookiesJson = JSON.stringify(cookies, null, 2);

  // 로컬 임시 저장
  const outFile = path.join(__dirname, `..`, `cookies-${SERVICE}.json`);
  fs.writeFileSync(outFile, cookiesJson);

  console.log("\n=== GitHub Secret에 복사하세요 ===");
  console.log(cookiesJson);
  console.log("===================================");
  console.log(`\nSecret 이름: ${SERVICE.toUpperCase()}_COOKIES`);
  console.log(`로컬 저장: ${outFile}`);
  console.log("\n⚠️  cookies-*.json은 .gitignore에 포함되어 있어야 합니다.");

  await browser.close();
}

main().catch((e) => { console.error(e); process.exit(1); });
