#!/usr/bin/env node
/**
 * fetch-twitter.js
 * X.com GraphQL API 직접 HTTP 호출 → following 피드 수집
 * Playwright/headless browser 불필요 — Node.js 내장 https 모듈만 사용
 *
 * 환경변수:
 *   TWITTER_COOKIES  - GitHub Secret: 쿠키 JSON 문자열
 *   POST_DATE        - YYYY-MM-DD (기본: 오늘 KST)
 *   MAX_ITEMS        - 최대 수집 수 (기본: 30)
 *   DRY_RUN          - "true"이면 파일 저장 생략
 */

const https = require("https");
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

// ─── HTTP 헬퍼 ────────────────────────────────────────────────────────────────

function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const parsedUrl = new URL(url);
    const options = {
      hostname: parsedUrl.hostname,
      path: parsedUrl.pathname + parsedUrl.search,
      method: "GET",
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ko,en;q=0.9",
        ...headers,
      },
    };

    const req = https.request(options, (res) => {
      // 리다이렉트 처리 (최대 3회)
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const redirectUrl = res.headers.location.startsWith("http")
          ? res.headers.location
          : `https://${parsedUrl.hostname}${res.headers.location}`;
        return httpGet(redirectUrl, headers).then(resolve).catch(reject);
      }

      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        const body = Buffer.concat(chunks).toString("utf8");
        if (res.statusCode >= 400) {
          reject(new Error(`HTTP ${res.statusCode} for ${url}\n${body.slice(0, 500)}`));
        } else {
          resolve(body);
        }
      });
    });

    req.on("error", reject);
    req.setTimeout(30000, () => {
      req.destroy(new Error(`Timeout: ${url}`));
    });
    req.end();
  });
}

// ─── Bearer Token 동적 추출 ──────────────────────────────────────────────────

async function getBearerToken() {
  console.log("Bearer token 추출 중 (x.com JS 번들에서)...");

  // x.com 메인 페이지에서 JS 번들 URL 목록 수집
  let html;
  try {
    html = await httpGet("https://x.com");
  } catch (e) {
    throw new Error(`x.com 메인 페이지 로딩 실패: ${e.message}`);
  }

  // abs.twimg.com 번들 URL 추출
  const bundlePattern = /https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/main\.[^"'\s]+\.js/g;
  const bundleUrls = [...new Set([...html.matchAll(bundlePattern)].map((m) => m[0]))];

  // 번들 없을 경우 일반 JS URL도 시도
  if (bundleUrls.length === 0) {
    const fallbackPattern = /https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/[^"'\s]+\.js/g;
    const fallbackUrls = [...new Set([...html.matchAll(fallbackPattern)].map((m) => m[0]))];
    bundleUrls.push(...fallbackUrls.slice(0, 5));
  }

  console.log(`  JS 번들 후보: ${bundleUrls.length}개`);

  if (bundleUrls.length === 0) {
    throw new Error("Bearer token을 찾을 수 없음: JS 번들 URL을 x.com에서 찾지 못했습니다.");
  }

  for (const url of bundleUrls.slice(0, 3)) {
    console.log(`  번들 스캔: ${url.slice(0, 80)}...`);
    let js;
    try {
      js = await httpGet(url);
    } catch (e) {
      console.log(`  번들 로딩 실패: ${e.message}`);
      continue;
    }

    const match = js.match(/Bearer (AAAA[A-Za-z0-9%+/=]{40,})/);
    if (match) {
      console.log("  Bearer token 추출 성공");
      return "Bearer " + match[1];
    }
  }

  throw new Error("Bearer token을 찾을 수 없음: 스캔한 모든 JS 번들에서 패턴 미발견");
}

// ─── QueryId 동적 추출 ───────────────────────────────────────────────────────

async function getQueryId() {
  console.log("HomeLatestTimeline queryId 추출 중...");

  let html;
  try {
    html = await httpGet("https://x.com");
  } catch (e) {
    throw new Error(`x.com 메인 페이지 로딩 실패: ${e.message}`);
  }

  // api.js 또는 GraphQL 관련 번들에서 queryId 검색
  const bundlePattern = /https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/[^"'\s]+\.js/g;
  const allBundleUrls = [...new Set([...html.matchAll(bundlePattern)].map((m) => m[0]))];

  console.log(`  전체 번들: ${allBundleUrls.length}개 — queryId 검색 중`);

  for (const url of allBundleUrls.slice(0, 8)) {
    let js;
    try {
      js = await httpGet(url);
    } catch (_) {
      continue;
    }

    if (!js.includes("HomeLatestTimeline")) continue;

    console.log(`  HomeLatestTimeline 포함 번들 발견: ${url.slice(0, 80)}...`);

    // 패턴 1: queryId:"xxx"...operationName:"HomeLatestTimeline"
    const m1 = js.match(/queryId:"([^"]+)"[^}]{0,200}operationName:"HomeLatestTimeline"/);
    if (m1) {
      console.log(`  queryId 추출 성공 (패턴1): ${m1[1]}`);
      return m1[1];
    }

    // 패턴 2: "HomeLatestTimeline"...queryId:"xxx"
    const m2 = js.match(/"HomeLatestTimeline"[^}]{0,200}queryId:"([^"]+)"/);
    if (m2) {
      console.log(`  queryId 추출 성공 (패턴2): ${m2[1]}`);
      return m2[1];
    }

    // 패턴 3: {queryId:"xxx",operationName:"HomeLatestTimeline"
    const m3 = js.match(/\{queryId:"([^"]+)",operationName:"HomeLatestTimeline"/);
    if (m3) {
      console.log(`  queryId 추출 성공 (패턴3): ${m3[1]}`);
      return m3[1];
    }
  }

  throw new Error("HomeLatestTimeline queryId를 찾을 수 없음: 모든 번들 스캔 실패");
}

// ─── 쿠키 파싱 ───────────────────────────────────────────────────────────────

function extractCookieFields(cookies) {
  const ct0 = (cookies.find((c) => c.name === "ct0") || {}).value;
  const authToken = (cookies.find((c) => c.name === "auth_token") || {}).value;
  const cookieStr = cookies.map((c) => `${c.name}=${c.value}`).join("; ");
  return { ct0, authToken, cookieStr };
}

// ─── HomeLatestTimeline API 호출 ─────────────────────────────────────────────

async function fetchHomeLatestTimeline(queryId, bearerToken, ct0, cookieStr) {
  const variables = JSON.stringify({
    count: 40,
    includePromotedContent: true,
    latestControlAvailable: true,
    requestContext: "launch",
  });

  const features = JSON.stringify({
    rweb_tipjar_consumption_enabled: true,
    responsive_web_graphql_exclude_directive_enabled: true,
    verified_phone_label_enabled: false,
    creator_subscriptions_tweet_preview_api_enabled: true,
    responsive_web_graphql_timeline_navigation_enabled: true,
    responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
    communities_web_enable_tweet_community_results_fetch: true,
    c9s_tweet_anatomy_moderator_badge_enabled: true,
    articles_preview_enabled: true,
    tweetypie_unmention_optimization_enabled: true,
    responsive_web_edit_tweet_api_enabled: true,
    graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
    view_counts_everywhere_api_enabled: true,
    longform_notetweets_consumption_enabled: true,
    responsive_web_twitter_article_tweet_consumption_enabled: true,
    tweet_awards_web_tipping_enabled: false,
    creator_subscriptions_quote_tweet_preview_enabled: false,
    freedom_of_speech_not_reach_fetch_enabled: true,
    standardized_nudges_misinfo: true,
    tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
    rweb_video_timestamps_enabled: true,
    longform_notetweets_rich_text_read_enabled: true,
    longform_notetweets_inline_media_enabled: true,
    responsive_web_enhance_cards_enabled: false,
  });

  const params = new URLSearchParams({ variables, features });
  const url = `https://x.com/i/api/graphql/${queryId}/HomeLatestTimeline?${params}`;

  console.log(`HomeLatestTimeline API 호출 중...`);
  console.log(`  URL: https://x.com/i/api/graphql/${queryId}/HomeLatestTimeline`);

  const body = await httpGet(url, {
    Authorization: bearerToken,
    Cookie: cookieStr,
    "x-csrf-token": ct0,
    "x-twitter-active-user": "yes",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-client-language": "ko",
    Referer: "https://x.com/home",
    "Content-Type": "application/json",
  });

  return JSON.parse(body);
}

// ─── 트윗 파싱 (기존 로직 유지) ──────────────────────────────────────────────

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
      for (const entry of inst.entries || []) {
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
          (u) =>
            u.expanded_url &&
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

// ─── main ─────────────────────────────────────────────────────────────────────

async function main() {
  let cookies;
  try {
    cookies = JSON.parse(COOKIES_JSON);
  } catch (e) {
    console.error("TWITTER_COOKIES JSON 파싱 실패:", e.message);
    process.exit(1);
  }

  // Bearer token 추출
  let bearerToken;
  try {
    bearerToken = await getBearerToken();
  } catch (e) {
    console.error("[단계 1 실패] Bearer token 추출 오류:", e.message);
    process.exit(1);
  }

  // queryId 추출
  let queryId;
  try {
    queryId = await getQueryId();
  } catch (e) {
    console.error("[단계 2 실패] queryId 추출 오류:", e.message);
    process.exit(1);
  }

  // 쿠키 필드 추출
  const { ct0, authToken, cookieStr } = extractCookieFields(cookies);
  if (!ct0) {
    console.error("[단계 3 실패] 쿠키에서 ct0를 찾을 수 없습니다. TWITTER_COOKIES Secret을 갱신하세요.");
    process.exit(1);
  }
  if (!authToken) {
    console.error("[단계 3 실패] 쿠키에서 auth_token을 찾을 수 없습니다. TWITTER_COOKIES Secret을 갱신하세요.");
    process.exit(1);
  }
  console.log("쿠키 필드 확인: ct0 ✓, auth_token ✓");

  // API 호출
  let responseJson;
  try {
    responseJson = await fetchHomeLatestTimeline(queryId, bearerToken, ct0, cookieStr);
  } catch (e) {
    console.error("[단계 4 실패] HomeLatestTimeline API 호출 오류:", e.message);
    process.exit(1);
  }

  // 트윗 파싱
  const tweets = parseTweetsFromGraphQL(responseJson);
  console.log(`\nGraphQL 응답에서 트윗 파싱: ${tweets.length}개`);

  const items = [];
  const seen = new Set();

  for (const t of tweets) {
    if (!t.text || !t.url) continue;
    if (seen.has(t.url)) continue;
    if (!shouldInclude(t.text, t.is_thread, t.has_external_link)) continue;
    seen.add(t.url);
    items.push(t);
    console.log(`  [${items.length}] ${t.author}: ${t.text.slice(0, 60)}...`);
    if (items.length >= MAX_ITEMS) break;
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

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
