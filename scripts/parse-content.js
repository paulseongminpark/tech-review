#!/usr/bin/env node
/**
 * parse-content.js
 * 콘텐츠 소스(CONTENT_FILE 또는 GIST_ID) → front matter 추가 → Jekyll 포스트 저장
 *
 * 환경변수:
 *   CONTENT_FILE  - 로컬 콘텐츠 파일 경로 (fetch-perplexity.js 출력)
 *   GIST_ID       - Gist ID (CONTENT_FILE 없을 때 fallback)
 *   GITHUB_TOKEN  - Gist 접근 토큰 (GIST_ID 사용 시 필요)
 *   LANG          - "ko" 또는 "en" (기본: "ko")
 *   POST_DATE     - YYYY-MM-DD (기본: 오늘)
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

const CONTENT_FILE = process.env.CONTENT_FILE;
const GIST_ID = process.env.GIST_ID;
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const LANG = process.env.LANG || "ko";
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);

if (!CONTENT_FILE && !GIST_ID) {
  console.error("CONTENT_FILE 또는 GIST_ID 환경변수가 필요합니다.");
  process.exit(1);
}

function httpsRequest(options) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, body: data }); }
      });
    });
    req.on("error", reject);
    req.end();
  });
}

async function fetchGist(gistId) {
  const res = await httpsRequest({
    hostname: "api.github.com",
    path: `/gists/${gistId}`,
    method: "GET",
    headers: {
      Authorization: `token ${GITHUB_TOKEN}`,
      "User-Agent": "tech-review-bot",
      Accept: "application/vnd.github.v3+json",
    },
  });
  if (res.status !== 200) throw new Error(`Gist fetch 실패: ${res.status}`);
  return Object.values(res.body.files)[0].content;
}

async function main() {
  let raw;
  if (CONTENT_FILE) {
    console.log(`로컬 파일 로드: ${CONTENT_FILE}`);
    raw = fs.readFileSync(CONTENT_FILE, "utf8");
  } else {
    console.log(`Gist ${GIST_ID} 로드 중...`);
    raw = await fetchGist(GIST_ID);
  }

  if (!raw || raw.trim().length === 0) {
    console.error("콘텐츠가 비어 있습니다.");
    process.exit(1);
  }

  // TAGS: 추출 + Today in One Line에서 제목 추출
  let title = `${POST_DATE} Daily Tech Review`;
  let tags = ["tech-review"];
  const lines = raw.trim().split("\n");
  let bodyStart = 0;

  // 헤더에서 TITLE:/TAGS: 추출 (fetch-perplexity.js가 붙여준 것)
  for (let i = 0; i < Math.min(5, lines.length); i++) {
    if (lines[i].startsWith("TITLE:")) {
      // TITLE은 fallback용으로만 보관 (Today in One Line 우선)
      title = lines[i].replace(/^TITLE:\s*/, "").trim().replace(/"/g, "'");
      bodyStart = i + 1;
    } else if (lines[i].startsWith("TAGS:")) {
      tags = lines[i].replace(/^TAGS:\s*/, "").split(",").map(t => t.trim().toLowerCase().replace(/\s+/g, "-")).filter(Boolean);
      bodyStart = Math.max(bodyStart, i + 1);
    }
  }
  raw = lines.slice(bodyStart).join("\n").trim();

  // 브라켓 헤드라인 제거: ## 1. [제목] → ## 1. 제목
  raw = raw.replace(/^(##\s*\d+\.?\s*)\[([^\]]+)\]/gm, "$1$2");

  // 본문에서 "## Today in One Line" 다음 비어있지 않은 줄을 제목으로 사용
  const bodyLines = raw.split("\n");
  for (let i = 0; i < bodyLines.length; i++) {
    if (bodyLines[i].match(/^##\s*Today in One Line/i)) {
      // 다음 비어있지 않은 줄 찾기
      for (let j = i + 1; j < bodyLines.length; j++) {
        const candidate = bodyLines[j].trim();
        if (candidate && !candidate.startsWith("#") && !candidate.startsWith("---")) {
          title = candidate.replace(/"/g, "'");
          console.log(`제목 추출 (Today in One Line): ${title}`);
          break;
        }
      }
      break;
    }
  }

  const [y, m, d] = POST_DATE.split("-");
  const permalink = `/${LANG}/${y}/${m}/${d}/daily-tech-review/`;
  const tagsStr = tags.map(t => `"${t}"`).join(", ");

  const frontMatter = [
    "---",
    `layout: post`,
    `title: "${title}"`,
    `date: ${POST_DATE}`,
    `lang: ${LANG}`,
    `permalink: ${permalink}`,
    `pair: ${POST_DATE}-daily-tech-review`,
    `tags: [${tagsStr}]`,
    "---",
  ].join("\n");

  const post = `${frontMatter}\n\n${raw.trim()}\n\n## Comments\n\n`;

  const dir = path.join("_posts", LANG);
  fs.mkdirSync(dir, { recursive: true });
  const filepath = path.join(dir, `${POST_DATE}-daily-tech-review.md`);

  // 이미 존재하는 파일은 덮어쓰지 않음 (comments 보호)
  if (fs.existsSync(filepath)) {
    console.log(`이미 존재함, 건너뜀: ${filepath}`);
    return;
  }

  fs.writeFileSync(filepath, post, "utf8");
  console.log(`포스트 저장: ${filepath}`);

  const out = process.env.GITHUB_OUTPUT;
  if (out) fs.appendFileSync(out, `post_path=${filepath}\npost_date=${POST_DATE}\npost_lang=${LANG}\n`);
}

main().catch((err) => { console.error(err.message); process.exit(1); });
