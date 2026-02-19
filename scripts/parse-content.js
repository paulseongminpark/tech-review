#!/usr/bin/env node
/**
 * parse-content.js
 * 콘텐츠 소스(CONTENT_FILE 또는 GIST_ID) → TOPIC_START/END 파싱 → Jekyll 포스트 생성
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

function parseTopics(raw) {
  const topics = [];
  const re = /TOPIC_START\s*([\s\S]*?)\s*TOPIC_END/g;
  let m;
  while ((m = re.exec(raw)) !== null) topics.push(m[1].trim());
  return topics;
}

function parseSpotlight(raw) {
  const m = /SPOTLIGHT_START\s*([\s\S]*?)\s*SPOTLIGHT_END/.exec(raw);
  return m ? m[1].trim() : null;
}

function buildSummary(topics) {
  return topics.map((topic, i) => {
    const lines = topic.split("\n").filter((l) => l.trim());
    let title = "", sentence = "";
    for (const line of lines) {
      if (line.startsWith("## ")) title = line.slice(3).trim();
      else if (!sentence && !line.startsWith("**Source**")) {
        const sm = line.match(/^(.+?[.!?。])/);
        sentence = sm ? sm[1] : line.slice(0, 80) + "…";
      }
      if (title && sentence) break;
    }
    return `${i + 1}. **${title || `Topic ${i + 1}`}** — ${sentence}`;
  });
}

function buildPost(topics, spotlight, summaryLines, lang) {
  const sep = "\n\n---\n\n";
  const parts = [];

  const summaryHeader = lang === "en" ? "## Today's Highlights" : "## 오늘의 핵심";
  if (summaryLines.length > 0) parts.push(`${summaryHeader}\n${summaryLines.join("\n")}`);

  parts.push(topics.join(sep));

  if (spotlight) parts.push(`## 🤖 AI Agent & Dev Spotlight\n${spotlight}`);

  parts.push("## Comments\n");

  const frontMatter = `---\nlayout: post\ntitle: "${POST_DATE} Daily Tech Review"\ndate: ${POST_DATE}\nlang: ${lang}\npair: ${POST_DATE}-daily-tech-review\ntags: [daily, tech-review]\n---`;

  return `${frontMatter}\n\n${parts.join(sep)}\n`;
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

  const frontMatter = `---\nlayout: post\ntitle: "${POST_DATE} Daily Tech Review"\ndate: ${POST_DATE}\nlang: ${LANG}\npair: ${POST_DATE}-daily-tech-review\ntags: [daily, tech-review]\n---`;

  const post = `${frontMatter}\n\n${raw}\n\n---\n\n## Comments\n`;

  const dir = path.join("_posts", LANG);
  fs.mkdirSync(dir, { recursive: true });
  const filepath = path.join(dir, `${POST_DATE}-daily-tech-review.md`);
  fs.writeFileSync(filepath, post, "utf8");
  console.log(`포스트 저장: ${filepath}`);

  const out = process.env.GITHUB_OUTPUT;
  if (out) fs.appendFileSync(out, `post_path=${filepath}\npost_date=${POST_DATE}\npost_lang=${LANG}\n`);
}

main().catch((err) => { console.error(err.message); process.exit(1); });
