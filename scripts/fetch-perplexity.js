#!/usr/bin/env node
/**
 * fetch-perplexity.js
 * sonar-deep-research + sonar-pro 폴백 파이프라인
 * URL 검증, 분량 검증, 요일별 도메인 필터 포함
 *
 * 환경변수:
 *   PERPLEXITY_API_KEY   - Perplexity API 키
 *   LANG                 - "ko" 또는 "en"
 *   POST_DATE            - YYYY-MM-DD (기본: 오늘)
 *   OUTPUT_FILE          - 결과 저장 경로
 *   USE_DEEP_RESEARCH    - "true"이면 sonar-deep-research 사용 (기본: "true")
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");

const API_KEY = process.env.PERPLEXITY_API_KEY;
// 주의: Linux의 LANG은 locale 값(en_US.UTF-8 등)이 기본 설정됨
// 워크플로우에서 반드시 LANG=ko를 명시적으로 전달해야 함
const LANG = process.env.LANG || "ko";
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const OUTPUT_FILE = process.env.OUTPUT_FILE || `/tmp/perplexity-${LANG}.md`;
const USE_DEEP_RESEARCH = process.env.USE_DEEP_RESEARCH !== "false";

if (!API_KEY) {
  console.error("PERPLEXITY_API_KEY 환경변수가 필요합니다.");
  process.exit(1);
}

// ─── 요일 → 프롬프트 파일 매핑 (0=일, 1=월, ..., 6=토) ─────────
const PROMPT_FILES = {
  0: "07-sunday-weekly.md",
  1: "01-monday-ai-ml.md",
  2: "02-tuesday-bigtech.md",
  3: "03-wednesday-startup.md",
  4: "04-thursday-opensource.md",
  5: "05-friday-hardware.md",
  6: "06-saturday-usecase.md",
};

const DAY_SECTION = {
  0: "## 일 (주간 종합)",
  1: "## 월 (AI/ML 혁신)",
  2: "## 화 (빅테크 동향)",
  3: "## 수 (AI × Industry: 비즈니스 모델)",
  4: "## 목 (오픈소스 & 개발자)",
  5: "## 금 (AI 하드웨어 & 인프라)",
  6: "## 토 (AI 실사용 사례)",
};

// ─── 요일별 도메인 필터 ──────────────────────────────────────────
const DOMAIN_FILTERS = {
  0: [], // 일: 글로벌 AI 현장 — 제한 없음
  1: [   // 월: AI/ML 혁신
    "arxiv.org", "paperswithcode.com", "scholar.google.com",
    "nature.com", "science.org", "spectrum.ieee.org", "acm.org",
    "openai.com", "anthropic.com", "deepmind.google", "ai.meta.com",
    "mistral.ai", "huggingface.co", "stability.ai", "cohere.com",
    "venturebeat.com", "theverge.com", "techcrunch.com", "arstechnica.com",
    "wired.com", "thenewstack.io", "infoq.com", "zdnet.com",
    "technologyreview.com", "newscientist.com",
    "reuters.com", "apnews.com", "bloomberg.com",
    "reddit.com", "news.ycombinator.com", "dev.to", "lobste.rs",
    "zdnet.co.kr", "itworld.co.kr", "etnews.com", "aitimes.com",
    "bensbites.co", "therundown.ai", "importai.net",
  ],
  2: [   // 화: 빅테크 동향
    "about.google", "blog.google", "blogs.microsoft.com",
    "engineering.fb.com", "developer.nvidia.com", "newsroom.apple.com",
    "aws.amazon.com", "developer.samsung.com",
    "bloomberg.com", "reuters.com", "cnbc.com", "ft.com", "wsj.com",
    "nytimes.com", "washingtonpost.com", "economist.com",
    "theverge.com", "techcrunch.com", "arstechnica.com", "wired.com",
    "theinformation.com", "semafor.com", "platformer.news",
    "zdnet.com", "cnet.com", "engadget.com",
    "fortune.com", "fastcompany.com", "businessinsider.com",
    "axios.com", "protocol.com",
    "reddit.com", "news.ycombinator.com",
    "zdnet.co.kr", "etnews.com", "mk.co.kr", "edaily.co.kr",
    "seekingalpha.com", "finance.yahoo.com", "barrons.com",
  ],
  3: [   // 수: AI × Industry
    "a16z.com", "sequoiacap.com", "ycombinator.com", "techcrunch.com",
    "cbinsights.com", "crunchbase.com", "pitchbook.com",
    "hbr.org", "mckinsey.com", "sloanreview.mit.edu", "bcg.com",
    "gartner.com", "forrester.com",
    "theinformation.com", "fortune.com", "fastcompany.com",
    "bloomberg.com", "ft.com", "wsj.com",
    "venturebeat.com", "semafor.com", "axios.com",
    "healthcareitnews.com", "americanbanker.com", "supplychaindive.com",
    "retaildive.com", "educationdive.com",
    "reddit.com", "news.ycombinator.com",
    "platum.kr", "venturesquare.net", "zdnet.co.kr", "etnews.com",
    "arxiv.org", "ssrn.com",
  ],
  4: [   // 목: 오픈소스 & 개발자
    "github.com", "github.blog", "gitlab.com", "stackoverflow.com",
    "dev.to", "hashnode.dev", "medium.com",
    "pytorch.org", "tensorflow.org", "huggingface.co", "langchain.com",
    "docs.anthropic.com", "platform.openai.com",
    "thenewstack.io", "infoq.com", "theregister.com",
    "techcrunch.com", "venturebeat.com", "zdnet.com",
    "devops.com", "dzone.com",
    "reddit.com", "news.ycombinator.com", "lobste.rs",
    "producthunt.com",
    "velog.io", "zdnet.co.kr", "44bits.io",
    "tldr.tech", "changelog.com", "thisweekinrust.org",
  ],
  5: [   // 금: AI 하드웨어 & 인프라
    "tomshardware.com", "semianalysis.com", "servethehome.com",
    "anandtech.com", "techpowerup.com", "videocardz.com",
    "spectrum.ieee.org", "eetimes.com", "semiengineering.com",
    "nextplatform.com", "hpcwire.com",
    "datacenterknowledge.com", "cloudflare.com", "aws.amazon.com",
    "bloomberg.com", "reuters.com", "cnbc.com", "ft.com",
    "theregister.com", "arstechnica.com", "wired.com",
    "techcrunch.com",
    "reddit.com", "news.ycombinator.com",
    "etnews.com", "zdnet.co.kr", "sedaily.com",
    "stratechery.com", "trendforce.com",
  ],
  6: [   // 토: AI 실사용 사례
    "technologyreview.com", "mckinsey.com", "gartner.com",
    "hbr.org", "bcg.com", "forrester.com",
    "nytimes.com", "washingtonpost.com", "theatlantic.com",
    "newyorker.com", "wired.com", "economist.com",
    "venturebeat.com", "fortune.com", "fastcompany.com",
    "bloomberg.com", "reuters.com", "axios.com",
    "whitehouse.gov", "ec.europa.eu", "oecd.org",
    "reddit.com", "news.ycombinator.com",
    "zdnet.co.kr", "etnews.com", "hani.co.kr", "donga.com",
    "healthcareitnews.com", "edtechmagazine.com", "retaildive.com",
  ],
};

// ─── 유틸리티 ────────────────────────────────────────────────────
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function callWithRetry(fn, retries = 2, delayMs = 10000) {
  let lastError;
  for (let i = 0; i <= retries; i++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      console.error(`시도 ${i + 1}/${retries + 1} 실패: ${err.message}`);
      if (i < retries) {
        console.log(`${delayMs / 1000}초 후 재시도...`);
        await sleep(delayMs);
      }
    }
  }
  throw lastError;
}

// ─── 키워드 ──────────────────────────────────────────────────────
function extractSectionKeywords(log, sectionHeader, filterFn) {
  const sectionStart = log.indexOf(sectionHeader);
  if (sectionStart === -1) return [];

  const nextSection = log.indexOf("\n## ", sectionStart + sectionHeader.length);
  const section = nextSection === -1
    ? log.slice(sectionStart)
    : log.slice(sectionStart, nextSection);

  const rows = [];
  const rowRegex = /\|\s*([\d-]+)\s*\|\s*([^|]+)\s*\|/g;
  let match;
  while ((match = rowRegex.exec(section)) !== null) {
    const date = match[1].trim();
    const keywords = match[2].trim();
    if (date && date !== "날짜" && filterFn(date)) {
      rows.push(`- ${date}: ${keywords}`);
    }
  }
  return rows;
}

function getSameDayKeywords(day) {
  const logPath = path.join("perplexity-prompts", "keywords-log.md");
  if (!fs.existsSync(logPath)) return "";

  const log = fs.readFileSync(logPath, "utf8");
  const sectionHeader = DAY_SECTION[day];
  if (!sectionHeader) return "";

  const rows = extractSectionKeywords(log, sectionHeader, () => true);
  if (rows.length === 0) return "";

  const recent = rows.slice(-4);
  return [
    "[같은 요일 이전 키워드 — 아래와 실질적으로 겹치는 뉴스는 제외]",
    ...recent,
    "같은 기업이어도 다른 사건이면 포함 가능. 같은 기업 + 비슷한 사건이면 반드시 제외.",
  ].join("\n");
}

function getThisWeekAllKeywords() {
  const logPath = path.join("perplexity-prompts", "keywords-log.md");
  if (!fs.existsSync(logPath)) return "";

  const log = fs.readFileSync(logPath, "utf8");

  // POST_DATE (일요일) 기준 이번 주 월~토 날짜 범위
  const [y, m, d] = POST_DATE.split("-").map(Number);
  const sunday = new Date(Date.UTC(y, m - 1, d));
  const monday = new Date(sunday);
  monday.setUTCDate(sunday.getUTCDate() - 6);
  const saturday = new Date(sunday);
  saturday.setUTCDate(sunday.getUTCDate() - 1);

  const mondayStr = monday.toISOString().slice(0, 10);
  const saturdayStr = saturday.toISOString().slice(0, 10);

  const allKeywords = [];
  for (let day = 1; day <= 6; day++) {
    const sectionHeader = DAY_SECTION[day];
    const rows = extractSectionKeywords(log, sectionHeader, (date) =>
      date >= mondayStr && date <= saturdayStr
    );
    allKeywords.push(...rows);
  }

  if (allKeywords.length === 0) return "";

  return [
    "[이번 주 월~토 사용 키워드 — 동일 뉴스 제외. 새로운 사건이면 포함]",
    ...allKeywords,
    "같은 기업이어도 다른 사건이면 포함 가능. 같은 기업 + 비슷한 사건이면 반드시 제외.",
  ].join("\n");
}

function getKeywordsBlock(day) {
  if (day === 0) return getThisWeekAllKeywords();
  return getSameDayKeywords(day);
}

// ─── 프롬프트 로드 ───────────────────────────────────────────────
function getPromptFile() {
  const [y, m, d] = POST_DATE.split("-").map(Number);
  const date = new Date(Date.UTC(y, m - 1, d));
  const day = date.getUTCDay();
  const filename = PROMPT_FILES[day];
  const filepath = path.join("perplexity-prompts", LANG, filename);

  if (!fs.existsSync(filepath)) {
    throw new Error(`프롬프트 파일 없음: ${filepath}`);
  }

  console.log(`프롬프트 파일: ${filepath} (요일: ${day})`);
  let prompt = fs.readFileSync(filepath, "utf8");

  let titleLine = "";
  let tagsLine = "";
  const lines = prompt.split("\n");
  const promptLines = [];
  for (const line of lines) {
    if (line.startsWith("TITLE:")) {
      titleLine = line;
    } else if (line.startsWith("TAGS:")) {
      tagsLine = line;
    } else {
      promptLines.push(line);
    }
  }
  prompt = promptLines.join("\n").trim();

  if (LANG === "ko") {
    const keywordsBlock = getKeywordsBlock(day);
    prompt = prompt.replace("{KEYWORDS_BLOCK}", keywordsBlock);
  } else {
    prompt = prompt.replace("{KEYWORDS_BLOCK}", "");
  }

  titleLine = titleLine.replace(/\{DATE\}/g, POST_DATE);
  prompt = prompt.replace(/\{DATE\}/g, POST_DATE);

  return { prompt, titleLine, tagsLine, day };
}

// ─── 공통 후처리 ─────────────────────────────────────────────────
function postProcess(content, citations = []) {
  // [title][n] → [title](url) 변환
  if (citations.length > 0) {
    content = content.replace(/\[([^\]]+)\]\[(\d+)\]/g, (_, title, n) => {
      const url = citations[parseInt(n, 10) - 1];
      return url ? `[${title}](${url})` : title;
    });
    content = content.replace(/\[(\d+)\]/g, "");
  }

  // 인코딩 대체 문자(U+FFFD) 제거
  content = content.replace(/\ufffd+/g, "");

  // 한자(CJK) 제거
  content = content.replace(/（[\u4e00-\u9fff\u3400-\u4dbf]+）/g, "");
  content = content.replace(/\([\u4e00-\u9fff\u3400-\u4dbf]+\)/g, "");
  content = content.replace(/[\u4e00-\u9fff\u3400-\u4dbf]/g, "");

  return content;
}

// ─── API: sonar-pro (동기) ───────────────────────────────────────
function callSonarPro(prompt, domainFilter = []) {
  return new Promise((resolve, reject) => {
    const systemMsg = LANG === "ko"
      ? "당신은 글로벌 기술·AI 동향 전문 리서처입니다. 반드시 한국어로 답변하세요."
      : "You are an expert researcher on global tech and AI trends. Always respond in English.";

    const requestBody = {
      model: "sonar-pro",
      messages: [
        { role: "system", content: systemMsg },
        { role: "user", content: prompt },
      ],
      max_tokens: 10000,
      temperature: 0.2,
      search_recency_filter: "week",
    };

    // Perplexity API: search_domain_filter 최대 20개
    if (domainFilter.length > 0) {
      requestBody.search_domain_filter = domainFilter.slice(0, 20);
    }

    const body = JSON.stringify(requestBody);

    const req = https.request(
      {
        hostname: "api.perplexity.ai",
        path: "/chat/completions",
        method: "POST",
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode !== 200) {
            reject(new Error(`sonar-pro API 오류 ${res.statusCode}: ${data}`));
            return;
          }
          try {
            const json = JSON.parse(data);
            const choice = json.choices?.[0];
            if (!choice) {
              reject(new Error("API 응답에 choices가 없음"));
              return;
            }
            const content = choice.message.content;
            const citations = json.citations || [];
            resolve(postProcess(content, citations));
          } catch (e) {
            reject(new Error(`응답 파싱 실패: ${data.slice(0, 200)}`));
          }
        });
      }
    );
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ─── API: sonar-deep-research ────────────────────────────────────
function submitDeepResearch(prompt, domainFilter = []) {
  return new Promise((resolve, reject) => {
    const systemMsg = LANG === "ko"
      ? "당신은 글로벌 기술·AI 동향 전문 리서처입니다. 반드시 한국어로 답변하세요."
      : "You are an expert researcher on global tech and AI trends. Always respond in English.";

    // deep research는 도메인 필터 미지원 — 자체 검색으로 소스 결정
    const requestBody = {
      model: "sonar-deep-research",
      messages: [
        { role: "system", content: systemMsg },
        { role: "user", content: prompt },
      ],
      temperature: 0.2,
    };

    const body = JSON.stringify(requestBody);

    console.log("sonar-deep-research 요청 중... (최대 15분 대기)");

    const req = https.request(
      {
        hostname: "api.perplexity.ai",
        path: "/chat/completions",
        method: "POST",
        headers: {
          Authorization: `Bearer ${API_KEY}`,
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          if (res.statusCode !== 200) {
            reject(new Error(`Deep Research API 오류 ${res.statusCode}: ${data}`));
            return;
          }
          try {
            const json = JSON.parse(data);
            const choice = json.choices?.[0];
            if (!choice) {
              reject(new Error("Deep Research 응답에 choices가 없음"));
              return;
            }
            const content = choice.message.content;
            const citations = json.citations || [];
            console.log("sonar-deep-research 응답 수신 완료");
            resolve(postProcess(content, citations));
          } catch (e) {
            reject(new Error(`응답 파싱 실패: ${data.slice(0, 200)}`));
          }
        });
      }
    );

    // 15분 타임아웃
    req.setTimeout(900000, () => {
      req.destroy();
      reject(new Error("Deep Research 요청 타임아웃 (15분)"));
    });

    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ─── 후처리: 브라켓 제목 제거 ────────────────────────────────────
function removeBracketHeadlines(content) {
  // ## 1. [제목] → ## 1. 제목
  // ## 1. [제목 — 부제] → ## 1. 제목 — 부제
  return content.replace(/^(##\s*\d+\.?\s*)\[([^\]]+)\]/gm, "$1$2");
}

// ─── URL 검증 ────────────────────────────────────────────────────
function checkUrl(urlStr) {
  return new Promise((resolve) => {
    try {
      const parsed = new URL(urlStr);
      const client = parsed.protocol === "https:" ? https : http;

      const req = client.request(
        {
          hostname: parsed.hostname,
          path: parsed.pathname + parsed.search,
          method: "HEAD",
          headers: {
            "User-Agent": "Mozilla/5.0 (compatible; tech-review-bot/1.0)",
          },
        },
        (res) => {
          resolve(res.statusCode >= 200 && res.statusCode < 400);
        }
      );

      req.setTimeout(5000, () => {
        req.destroy();
        resolve(false);
      });

      req.on("error", () => resolve(false));
      req.end();
    } catch {
      resolve(false);
    }
  });
}

async function validateUrls(content) {
  const linkRegex = /\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g;
  const links = [];
  let match;
  while ((match = linkRegex.exec(content)) !== null) {
    links.push({ full: match[0], text: match[1], url: match[2] });
  }

  if (links.length === 0) return content;

  console.log(`URL 검증 중... (${links.length}개)`);

  const results = await Promise.allSettled(
    links.map(async (link) => {
      const valid = await checkUrl(link.url);
      return { ...link, valid };
    })
  );

  let result = content;
  let invalidCount = 0;
  for (const r of results) {
    if (r.status === "fulfilled" && !r.value.valid) {
      invalidCount++;
      result = result.replaceAll(r.value.full, r.value.text);
      console.log(`  무효 URL 제거: ${r.value.url}`);
    }
  }

  console.log(`URL 검증 완료: ${links.length - invalidCount}/${links.length} 유효`);
  return result;
}

// ─── 분량 검증 (Node.js 로컬) ────────────────────────────────────
function validateContent(content) {
  const errors = [];

  if (content.length < 2500) {
    errors.push(`분량 부족: ${content.length}자 (최소 2500자)`);
  }

  const sections = content.match(/^##\s+\d+\./gm) || [];
  if (sections.length < 4) {
    errors.push(`섹션 부족: ${sections.length}개 (최소 4개)`);
  }

  if (!/Today in One Line/i.test(content)) {
    errors.push('"Today in One Line" 섹션 없음');
  }

  const wim = content.match(/Why it matters/gi) || [];
  if (wim.length < 4) {
    errors.push(`"Why it matters" 부족: ${wim.length}개 (최소 4개)`);
  }

  if (errors.length > 0) {
    console.warn("분량 검증 경고:");
    errors.forEach((e) => console.warn(`  - ${e}`));
    return false;
  }

  console.log("분량 검증 통과");
  return true;
}

// ─── 거부 패턴 검사 ──────────────────────────────────────────────
const REJECT_PATTERNS = [
  "죄송하지만", "죄송합니다", "작성할 수 없습니다",
  "제공된 검색 결과로는", "요청하신 형식의", "검색 결과의 성격",
  "권장사항:", "I apologize", "I cannot", "I'm unable to", "prompt injection",
  "이 요청을 수행할 수 없습니다", "실시간 데이터 접근 불가",
];

function isRejected(content) {
  if (!content || content.trim().length === 0) return true;
  const lower = content.toLowerCase();
  return REJECT_PATTERNS.some((p) => lower.includes(p.toLowerCase()));
}

// ─── main ────────────────────────────────────────────────────────
async function main() {
  console.log(`Perplexity 파이프라인 시작 (lang: ${LANG}, date: ${POST_DATE}, deep: ${USE_DEEP_RESEARCH})`);

  const { prompt, titleLine, tagsLine, day } = getPromptFile();
  const domainFilter = DOMAIN_FILTERS[day] || [];

  let content;

  if (USE_DEEP_RESEARCH) {
    try {
      content = await submitDeepResearch(prompt, domainFilter);
      if (isRejected(content)) {
        console.warn("Deep Research 응답이 거부됨:");
        console.warn(content.slice(0, 200));
        content = null;
      }
    } catch (err) {
      console.warn(`Deep Research 실패: ${err.message}`);
      content = null;
    }

    if (!content) {
      console.log("sonar-pro 폴백으로 전환...");
      content = await callWithRetry(
        () => callSonarPro(prompt, domainFilter), 2, 10000
      );
    }
  } else {
    content = await callWithRetry(
      () => callSonarPro(prompt, domainFilter), 2, 10000
    );
  }

  // 최종 응답 확인
  if (!content || content.trim().length === 0) {
    console.error("빈 응답");
    process.exit(1);
  }

  if (isRejected(content)) {
    console.error("최종 응답도 거부됨:");
    console.error(content.slice(0, 300));
    process.exit(1);
  }

  // 후처리
  content = removeBracketHeadlines(content);
  content = await validateUrls(content);

  // 분량 검증 (경고만, 저장은 진행)
  validateContent(content);

  console.log(`응답 완료 (${content.length}자)`);

  // 저장
  const header = [titleLine, tagsLine].filter(Boolean).join("\n");
  const output = header ? `${header}\n\n${content}` : content;
  fs.writeFileSync(OUTPUT_FILE, output, "utf8");
  console.log(`저장 완료: ${OUTPUT_FILE}`);

  const out = process.env.GITHUB_OUTPUT;
  if (out) fs.appendFileSync(out, `output_file=${OUTPUT_FILE}\n`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
