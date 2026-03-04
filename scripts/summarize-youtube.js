#!/usr/bin/env node
/**
 * summarize-youtube.js
 * _data/sources/youtube-YYYY-MM-DD.json (summary 없는 항목)
 * → Gemini에 YouTube URL 직접 전달 → Smart Brevity 요약
 * → 실패 시 제목+설명 텍스트로 폴백
 * → 같은 파일에 summary 필드 추가
 *
 * 환경변수:
 *   GEMINI_API_KEY  - Gemini API 키
 *   POST_DATE       - YYYY-MM-DD (기본: 오늘)
 *   DRY_RUN         - "true"이면 파일 저장 생략
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const DRY_RUN = process.env.DRY_RUN === "true";

if (!GEMINI_API_KEY) {
  console.error("GEMINI_API_KEY 환경변수가 필요합니다.");
  process.exit(1);
}

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

const BREVITY_FORMAT = `반드시 아래 JSON 형식으로만 응답하세요 (코드블록 없이 순수 JSON):
{
  "one_line": "한 문장 핵심 요약",
  "why_it_matters": "핵심 의미 1~2문장",
  "points": ["포인트 1", "포인트 2", "포인트 3"],
  "whats_next": "다음 전망 1문장"
}`;

async function geminiRequest(body, retries = 3) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`;
  const urlObj = new URL(url);
  const bodyStr = JSON.stringify(body);

  const result = await new Promise((resolve, reject) => {
    const req = https.request(
      {
        hostname: urlObj.hostname,
        path: urlObj.pathname + urlObj.search,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(bodyStr),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          try {
            const json = JSON.parse(data);
            if (json.error) {
              return reject(Object.assign(new Error(`Gemini API 오류 [${json.error.code}]: ${json.error.message}`), { code: json.error.code, raw: json.error.message }));
            }
            const candidate = json.candidates?.[0];
            if (!candidate) {
              return reject(new Error(`후보 없음. promptFeedback: ${JSON.stringify(json.promptFeedback)}`));
            }
            const text = candidate.content?.parts?.[0]?.text?.trim();
            if (!text) {
              return reject(new Error(`빈 응답. finishReason: ${candidate.finishReason}`));
            }
            const match = text.match(/\{[\s\S]*\}/);
            if (!match) return reject(new Error(`JSON 없음: ${text.slice(0, 150)}`));
            resolve(JSON.parse(match[0]));
          } catch (e) {
            reject(new Error(`파싱 실패: ${e.message} | raw: ${data.slice(0, 300)}`));
          }
        });
      }
    );
    req.on("error", reject);
    req.write(bodyStr);
    req.end();
  }).catch(async (e) => {
    if (e.code === 429 && retries > 0) {
      const match = (e.raw || "").match(/retry in ([\d.]+)s/);
      const waitMs = match ? (parseFloat(match[1]) + 3) * 1000 : 65000;
      console.log(`  Rate limit — ${Math.round(waitMs / 1000)}s 후 재시도 (남은 횟수: ${retries - 1})`);
      await new Promise((r) => setTimeout(r, waitMs));
      return geminiRequest(body, retries - 1);
    }
    throw e;
  });

  return result;
}

// 1차: Gemini가 YouTube 영상 직접 시청
async function summarizeByVideo(video) {
  return geminiRequest({
    contents: [{
      parts: [
        {
          file_data: {
            mime_type: "video/youtube",
            file_uri: video.url,
          },
        },
        { text: `이 유튜브 영상을 보고 Smart Brevity 형식으로 요약하세요.\n\n${BREVITY_FORMAT}` },
      ],
    }],
    generationConfig: { temperature: 0.3 },
  });
}

// 2차 폴백: 제목 + 설명 텍스트 기반 요약
async function summarizeByText(video) {
  const prompt = `YouTube 영상 정보를 보고 Smart Brevity 형식으로 요약하세요.

제목: ${video.title}
채널: ${video.channel}
설명: ${video.description || "(없음)"}

${BREVITY_FORMAT}`;
  return geminiRequest({
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.3 },
  });
}

async function main() {
  const inFile = path.join(DATA_DIR, `youtube-${POST_DATE}.json`);
  if (!fs.existsSync(inFile)) {
    console.error(`파일 없음: ${inFile}\nfetch-youtube.js를 먼저 실행하세요.`);
    process.exit(1);
  }

  const videos = JSON.parse(fs.readFileSync(inFile, "utf8"));
  const pending = videos.filter((v) => !v.summary);
  console.log(`요약 대상: ${pending.length}개`);

  for (const video of pending) {
    console.log(`\n처리 중: ${video.title}`);
    try {
      const summary = await summarizeByVideo(video);
      video.summary = summary;
      console.log(`  [영상] 요약 완료: ${summary.one_line}`);
    } catch (e) {
      console.error(`  [영상] 실패: ${e.message}`);
      console.log(`  [텍스트] 폴백 시도...`);
      try {
        const summary = await summarizeByText(video);
        video.summary = summary;
        console.log(`  [텍스트] 요약 완료: ${summary.one_line}`);
      } catch (e2) {
        console.error(`  [텍스트] 폴백도 실패: ${e2.message}`);
      }
    }
    await new Promise((r) => setTimeout(r, 1000));
  }

  if (DRY_RUN) {
    console.log("\nDRY_RUN: 파일 저장 생략");
    return;
  }

  fs.writeFileSync(inFile, JSON.stringify(videos, null, 2));
  console.log(`\n저장: ${inFile}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
