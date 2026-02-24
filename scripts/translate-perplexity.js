#!/usr/bin/env node
/**
 * translate-perplexity.js
 * KO 콘텐츠 파일을 Perplexity API로 EN 번역
 *
 * 환경변수:
 *   PERPLEXITY_API_KEY  - Perplexity API 키
 *   INPUT_FILE          - 번역할 KO 파일 경로 (기본: /tmp/perplexity-ko.md)
 *   OUTPUT_FILE         - 번역 결과 저장 경로 (기본: /tmp/perplexity-en.md)
 */

const https = require("https");
const fs = require("fs");

const API_KEY = process.env.PERPLEXITY_API_KEY;
const INPUT_FILE = process.env.INPUT_FILE || "/tmp/perplexity-ko.md";
const OUTPUT_FILE = process.env.OUTPUT_FILE || "/tmp/perplexity-en.md";

if (!API_KEY) {
  console.error("PERPLEXITY_API_KEY 환경변수가 필요합니다.");
  process.exit(1);
}

if (!fs.existsSync(INPUT_FILE)) {
  console.error(`입력 파일 없음: ${INPUT_FILE}`);
  process.exit(1);
}

const koContent = fs.readFileSync(INPUT_FILE, "utf8");

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
      console.error(`번역 시도 ${i + 1}/${retries + 1} 실패: ${err.message}`);
      if (i < retries) {
        console.log(`${delayMs / 1000}초 후 재시도...`);
        await sleep(delayMs);
      }
    }
  }
  throw lastError;
}

function callPerplexityTranslate(content) {
  return new Promise((resolve, reject) => {
    const systemMsg =
      "You are a professional technical translator. Translate Korean tech review content to English accurately. " +
      "Preserve all formatting markers exactly as-is: TOPIC_START, TOPIC_END, SPOTLIGHT_START, SPOTLIGHT_END, TITLE:, TAGS:. " +
      "Keep all URLs, code terms, product names, and proper nouns unchanged. " +
      "Output only the translated content with no additional commentary.";

    const userMsg =
      "Translate the following Korean tech review to English. " +
      "Keep all markers (TOPIC_START, TOPIC_END, SPOTLIGHT_START, SPOTLIGHT_END), TITLE: and TAGS: lines exactly as formatted.\n\n" +
      content;

    const body = JSON.stringify({
      model: "sonar-pro",
      messages: [
        { role: "system", content: systemMsg },
        { role: "user", content: userMsg },
      ],
      max_tokens: 10000,
      temperature: 0.1,
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
            let result = json.choices[0].message.content;
            // 인코딩 대체 문자 제거
            result = result.replace(/\ufffd+/g, "");
            resolve(result);
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
  console.log(`번역 중: ${INPUT_FILE} → ${OUTPUT_FILE}`);
  console.log(`입력 크기: ${koContent.length}자`);

  const translated = await callWithRetry(() => callPerplexityTranslate(koContent));

  if (!translated || translated.trim().length === 0) {
    console.error("경고: 번역 결과가 비어 있습니다.");
    process.exit(1);
  }
  console.log(`번역 완료 (${translated.length}자)`);

  fs.writeFileSync(OUTPUT_FILE, translated, "utf8");
  console.log(`저장 완료: ${OUTPUT_FILE}`);

  const out = process.env.GITHUB_OUTPUT;
  if (out) fs.appendFileSync(out, `output_file=${OUTPUT_FILE}\n`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
