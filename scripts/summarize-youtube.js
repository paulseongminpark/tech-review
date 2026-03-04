#!/usr/bin/env node
/**
 * summarize-youtube.js
 * yt-dlp로 자막만 추출 → JSON에 transcript 필드로 저장
 * AI 요약은 Claude Code 세션에서 수동으로 진행
 *
 * 환경변수:
 *   POST_DATE - YYYY-MM-DD (기본: 오늘)
 *   DRY_RUN   - "true"이면 파일 저장 생략
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const os = require("os");

const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const DRY_RUN = process.env.DRY_RUN === "true";

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");
const TMP_DIR = os.tmpdir();

// ─── VTT 파싱 ──────────────────────────────────────────────────
function parseVTT(content) {
  const lines = content.split("\n");
  const texts = [];
  let prev = "";

  for (const line of lines) {
    const t = line.trim();
    if (!t) continue;
    if (t.startsWith("WEBVTT")) continue;
    if (t.startsWith("NOTE")) continue;
    if (t.startsWith("Kind:")) continue;
    if (t.startsWith("Language:")) continue;
    if (/^\d+$/.test(t)) continue;
    if (/^\d{2}:\d{2}[:.]\d{2}/.test(t)) continue;
    if (/^-->/.test(t)) continue;

    const clean = t.replace(/<[^>]+>/g, "").trim();
    if (!clean) continue;

    // 중복 연속 문장 제거
    if (clean !== prev) {
      texts.push(clean);
      prev = clean;
    }
  }

  return texts.join(" ").replace(/\s+/g, " ").trim();
}

// ─── yt-dlp 자막 추출 ──────────────────────────────────────────
function extractTranscript(videoUrl, videoId) {
  const outPrefix = path.join(TMP_DIR, `yt_${videoId}`);
  const langs = ["ko", "en"];

  // 기존 파일 정리
  for (const f of fs.readdirSync(TMP_DIR)) {
    if (f.startsWith(`yt_${videoId}`)) {
      fs.unlinkSync(path.join(TMP_DIR, f));
    }
  }

  try {
    execSync(
      `yt-dlp --write-auto-subs --sub-langs ${langs.join(",")} --skip-download --output "${outPrefix}" "${videoUrl}"`,
      { stdio: "pipe", timeout: 60000 }
    );
  } catch (_) {
    return null;
  }

  // 파일 탐색: ko 우선, 없으면 en
  for (const lang of langs) {
    const candidates = [
      `${outPrefix}.${lang}.vtt`,
      `${outPrefix}.${lang}-orig.vtt`,
    ];
    for (const f of candidates) {
      if (fs.existsSync(f)) {
        const text = parseVTT(fs.readFileSync(f, "utf8"));
        if (text.length > 100) {
          console.log(`  자막 추출 성공 (${lang}, ${text.length}자)`);
          return text.slice(0, 80000);
        }
      }
    }
  }
  return null;
}

// ─── main ──────────────────────────────────────────────────────
async function main() {
  const inFile = path.join(DATA_DIR, `youtube-${POST_DATE}.json`);
  if (!fs.existsSync(inFile)) {
    console.error(`파일 없음: ${inFile}`);
    process.exit(1);
  }

  const videos = JSON.parse(fs.readFileSync(inFile, "utf8"));
  const pending = videos.filter((v) => !Object.prototype.hasOwnProperty.call(v, "transcript"));
  console.log(`자막 추출 대상: ${pending.length}개`);

  for (const video of pending) {
    console.log(`\n처리 중: ${video.title}`);
    const videoId = video.url.match(/[?&]v=([^&]+)/)?.[1] || video.video_id;

    if (!videoId) {
      console.log("  video_id 없음, transcript: null");
      video.transcript = null;
      continue;
    }

    const transcript = extractTranscript(video.url, videoId);
    if (transcript) {
      video.transcript = transcript;
    } else {
      console.log("  자막 없음, transcript: null");
      video.transcript = null;
    }
  }

  if (DRY_RUN) {
    console.log("\nDRY_RUN: 파일 저장 생략");
    return;
  }

  fs.writeFileSync(inFile, JSON.stringify(videos, null, 2));
  console.log(`\n저장: ${inFile}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
