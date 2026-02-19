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
  return fs.readFileSync(filepath, "utf8");
}

function callPerplexityAPI(prompt) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model: "sonar-pro",
      messages: [{ role: "user", content: prompt }],
      max_tokens: 2000,
      temperature: 0.2,
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
            resolve(json.choices[0].message.content);
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

  // TOPIC_START 마커 확인
  if (!content.includes("TOPIC_START")) {
    console.error("경고: TOPIC_START 마커 없음. 응답 앞 500자:");
    console.error(content.slice(0, 500));
    // 마커 없이도 저장 (parse-content.js에서 에러 처리)
  } else {
    const topicCount = (content.match(/TOPIC_START/g) || []).length;
    console.log(`토픽 ${topicCount}건 감지`);
  }

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
