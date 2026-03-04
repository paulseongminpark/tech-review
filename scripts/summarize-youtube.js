#!/usr/bin/env node
/**
 * summarize-youtube.js
 * _data/sources/youtube-YYYY-MM-DD.json (summary 없는 항목)
 * → yt-dlp transcript 추출 → Gemini Smart Brevity 요약
 * → 같은 파일에 summary 필드 추가
 *
 * 환경변수:
 *   GEMINI_API_KEY  - Gemini API 키
 *   POST_DATE       - YYYY-MM-DD (기본: 오늘)
 *   DRY_RUN         - "true"이면 파일 저장 생략
 */

const { execSync } = require("child_process");
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

const SMART_BREVITY_PROMPT = `다음 유튜브 영상 트랜스크립트를 Smart Brevity 형식으로 요약하세요.

반드시 아래 JSON 형식으로만 응답하세요 (코드블록 없이 순수 JSON):
{
  "one_line": "한 문장 핵심 요약",
  "why_it_matters": "핵심 의미 1~2문장",
  "points": ["포인트 1", "포인트 2", "포인트 3"],
  "whats_next": "다음 전망 1문장"
}

트랜스크립트:
`;

function getTranscript(videoId) {
  const tmpBase = `/tmp/transcript-${videoId}`;
  const vttFile = `${tmpBase}.en.vtt`;

  // 기존 임시 파일 정리
  try { fs.unlinkSync(vttFile); } catch (_) {}

  try {
    execSync(
      `yt-dlp --write-auto-sub --sub-lang en --skip-download ` +
      `--sub-format vtt --output "${tmpBase}" ` +
      `"https://www.youtube.com/watch?v=${videoId}"`,
      { stdio: "pipe" }
    );
  } catch (e) {
    console.error(`  yt-dlp 실패 (${videoId}): ${e.message.slice(0, 100)}`);
    return null;
  }

  if (!fs.existsSync(vttFile)) {
    console.log(`  VTT 파일 없음 (자막 미제공 영상)`);
    return null;
  }

  const vtt = fs.readFileSync(vttFile, "utf8");
  const lines = vtt.split("\n").filter(
    (l) =>
      l.trim() &&
      !l.startsWith("WEBVTT") &&
      !/^\d{2}:\d{2}/.test(l) &&
      !/^NOTE/.test(l) &&
      !/^align:/.test(l) &&
      !/^position:/.test(l)
  );
  const unique = [...new Set(lines)];
  return unique.join(" ").slice(0, 8000);
}

async function summarize(transcript) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;
  const body = JSON.stringify({
    contents: [{ parts: [{ text: SMART_BREVITY_PROMPT + transcript }] }],
    generationConfig: { temperature: 0.3 },
  });

  const https = require("https");
  const urlObj = new URL(url);

  return new Promise((resolve, reject) => {
    const req = https.request(
      {
        hostname: urlObj.hostname,
        path: urlObj.pathname + urlObj.search,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (chunk) => (data += chunk));
        res.on("end", () => {
          const json = JSON.parse(data);
          if (json.error) return reject(new Error(json.error.message));
          const text = json.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
          if (!text) return reject(new Error("빈 응답"));
          const match = text.match(/\{[\s\S]*\}/);
          if (!match) return reject(new Error(`JSON 파싱 실패: ${text.slice(0, 100)}`));
          resolve(JSON.parse(match[0]));
        });
      }
    );
    req.on("error", reject);
    req.write(body);
    req.end();
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
    const transcript = getTranscript(video.video_id);
    if (!transcript) {
      console.log("  transcript 없음 — 건너뜀");
      continue;
    }
    console.log(`  transcript ${transcript.length}자 추출`);

    try {
      const summary = await summarize(transcript);
      video.summary = summary;
      console.log(`  요약 완료: ${summary.one_line}`);
    } catch (e) {
      console.error(`  요약 실패: ${e.message}`);
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
