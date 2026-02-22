#!/usr/bin/env node
/**
 * fetch-perplexity.js
 * 오늘 요일에 맞는 프롬프트 파일을 읽어 Perplexity API 호출
 * → TOPIC_START/END 마커 포함 콘텐츠를 OUTPUT_FILE에 저장
 *
 * 환경변수:
 *   PERPLEXITY_API_KEY  - Perplexity API 키
 *   LANG                - "ko" 또는 "en"
 *   POST_DATE           - YYYY-MM-DD (기본: 오늘)
 *   OUTPUT_FILE         - 결과 저장 경로 (기본: /tmp/perplexity-{lang}.md)
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

const API_KEY = process.env.PERPLEXITY_API_KEY;
const LANG = process.env.LANG || "ko";
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const OUTPUT_FILE = process.env.OUTPUT_FILE || `/tmp/perplexity-${LANG}.md`;

if (!API_KEY) {
  console.error("PERPLEXITY_API_KEY 환경변수가 필요합니다.");
  process.exit(1);
}

// 요일 → 프롬프트 파일 매핑 (0=일, 1=월, ..., 6=토)
const PROMPT_FILES = {
  0: "07-sunday-weekly.md",
  1: "01-monday-ai-ml.md",
  2: "02-tuesday-bigtech.md",
  3: "03-wednesday-startup.md",
  4: "04-thursday-opensource.md",
  5: "05-friday-hardware.md",
  6: "06-saturday-usecase.md",
};

// 요일 인덱스(0=일~6=토) → keywords-log.md 섹션 헤더 매핑
const DAY_SECTION = {
  0: "## 일 (주간 종합)",
  1: "## 월 (AI/ML 혁신)",
  2: "## 화 (빅테크 동향)",
  3: "## 수 (AI × Industry: 비즈니스 모델)",
  4: "## 목 (오픈소스 & 개발자)",
  5: "## 금 (AI 하드웨어 & 인프라)",
  6: "## 토 (AI 실사용 사례)",
};

function getKeywordsBlock(day) {
  const logPath = path.join("perplexity-prompts", "keywords-log.md");
  if (!fs.existsSync(logPath)) return "";

  const log = fs.readFileSync(logPath, "utf8");
  const sectionHeader = DAY_SECTION[day];
  if (!sectionHeader) return "";

  // 해당 요일 섹션 추출
  const sectionStart = log.indexOf(sectionHeader);
  if (sectionStart === -1) return "";

  const nextSection = log.indexOf("\n## ", sectionStart + sectionHeader.length);
  const section = nextSection === -1
    ? log.slice(sectionStart)
    : log.slice(sectionStart, nextSection);

  // 테이블 행에서 날짜·키워드 추출 (최근 4주)
  const rows = [];
  const rowRegex = /\|\s*([\d-]+)\s*\|\s*([^|]+)\s*\|/g;
  let match;
  while ((match = rowRegex.exec(section)) !== null) {
    const date = match[1].trim();
    const keywords = match[2].trim();
    if (date && date !== "날짜") rows.push(`- ${date}: ${keywords}`);
  }

  if (rows.length === 0) return "";

  const recent = rows.slice(-4); // 최근 4주
  return [
    "[같은 요일 이전 키워드 — 아래와 실질적으로 겹치는 뉴스는 제외]",
    ...recent,
    "같은 기업이어도 다른 사건이면 포함 가능. 같은 기업 + 비슷한 사건이면 반드시 제외.",
  ].join("\n");
}

function getPromptFile() {
  // POST_DATE 기준 KST 요일 계산
  const date = new Date(POST_DATE + "T00:00:00+09:00");
  const day = date.getDay();
  const filename = PROMPT_FILES[day];
  const filepath = path.join("perplexity-prompts", LANG, filename);

  if (!fs.existsSync(filepath)) {
    throw new Error(`프롬프트 파일 없음: ${filepath}`);
  }

  console.log(`프롬프트 파일: ${filepath} (요일: ${day})`);
  let prompt = fs.readFileSync(filepath, "utf8");

  // {KEYWORDS_BLOCK} 치환 (ko만, en은 keywords-log 없음)
  if (LANG === "ko") {
    const keywordsBlock = getKeywordsBlock(day);
    prompt = prompt.replace("{KEYWORDS_BLOCK}", keywordsBlock);
  } else {
    prompt = prompt.replace("{KEYWORDS_BLOCK}", "");
  }

  // {DATE} 치환
  prompt = prompt.replace(/\{DATE\}/g, POST_DATE);

  return prompt;
}

function callPerplexityAPI(prompt) {
  return new Promise((resolve, reject) => {
    const systemMsg = LANG === "ko"
      ? "당신은 글로벌 기술·AI 동향 전문 리서처입니다. 반드시 한국어로 답변하세요."
      : "You are an expert researcher on global tech and AI trends. Always respond in English.";

    const body = JSON.stringify({
      model: "sonar-pro",
      messages: [
        { role: "system", content: systemMsg },
        { role: "user", content: prompt },
      ],
      max_tokens: 4000,
      temperature: 0.2,
      search_recency_filter: "week",
    });

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
            reject(new Error(`API 오류 ${res.statusCode}: ${data}`));
            return;
          }
          try {
            const json = JSON.parse(data);
            let content = json.choices[0].message.content;
            const citations = json.citations || [];

            // [title][n] → [title](url) 변환
            if (citations.length > 0) {
              content = content.replace(/\[([^\]]+)\]\[(\d+)\]/g, (_, title, n) => {
                const url = citations[parseInt(n, 10) - 1];
                return url ? `[${title}](${url})` : title;
              });
              // 본문 내 [n] 인용 마커 제거
              content = content.replace(/\[(\d+)\]/g, "");
            }

            // 인코딩 대체 문자(U+FFFD) 제거
            content = content.replace(/\ufffd+/g, "");

            // 한자(CJK) 제거 - 괄호 내 한자 패턴 포함
            content = content.replace(/（[\u4e00-\u9fff\u3400-\u4dbf]+）/g, "");
            content = content.replace(/\([\u4e00-\u9fff\u3400-\u4dbf]+\)/g, "");
            content = content.replace(/[\u4e00-\u9fff\u3400-\u4dbf]/g, "");

            resolve(content);
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

async function main() {
  console.log(`Perplexity API 호출 중... (lang: ${LANG}, date: ${POST_DATE})`);

  const prompt = getPromptFile();
  const content = await callPerplexityAPI(prompt);

  // 응답 확인
  if (!content || content.trim().length === 0) {
    console.error("경고: 빈 응답");
    process.exit(1);
  }
  console.log(`응답 수신 완료 (${content.length}자)`);

  fs.writeFileSync(OUTPUT_FILE, content, "utf8");
  console.log(`저장 완료: ${OUTPUT_FILE}`);

  // GitHub Actions output
  const out = process.env.GITHUB_OUTPUT;
  if (out) fs.appendFileSync(out, `output_file=${OUTPUT_FILE}\n`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
