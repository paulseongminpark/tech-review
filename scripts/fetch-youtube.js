#!/usr/bin/env node
/**
 * fetch-youtube.js
 * youtube-sources.json 플레이리스트 → yt-dlp로 신규 영상 추출
 * → _data/sources/youtube-YYYY-MM-DD.json 저장
 *
 * YouTube Data API 불필요 — yt-dlp로 플레이리스트 직접 조회
 * 환경변수:
 *   POST_DATE - YYYY-MM-DD (기본: 오늘)
 *   DRY_RUN   - "true"이면 파일 저장 생략
 */

const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const DRY_RUN = process.env.DRY_RUN === "true";

const SOURCES_FILE = path.join(__dirname, "..", "config", "youtube-sources.json");
const PROCESSED_FILE = path.join(__dirname, "..", "config", "youtube-processed.json");
const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

function getPlaylistItems(playlistId) {
  const url = `https://www.youtube.com/playlist?list=${playlistId}`;
  console.log(`  yt-dlp 플레이리스트 조회: ${url}`);
  const output = execSync(
    `yt-dlp --flat-playlist -J "${url}"`,
    { encoding: "utf-8", maxBuffer: 10 * 1024 * 1024 }
  );
  const data = JSON.parse(output);
  return (data.entries || []).map((item) => ({
    video_id: item.id,
    title: item.title || "",
    channel: item.channel || item.uploader || "",
    published_at: item.upload_date
      ? `${item.upload_date.slice(0,4)}-${item.upload_date.slice(4,6)}-${item.upload_date.slice(6,8)}`
      : "",
    fetched_at: POST_DATE,
    url: `https://www.youtube.com/watch?v=${item.id}`,
  }));
}

function main() {
  const sources = JSON.parse(fs.readFileSync(SOURCES_FILE, "utf8"));
  const processedData = JSON.parse(fs.readFileSync(PROCESSED_FILE, "utf8"));
  const processed = new Set(processedData.processed);

  const newVideos = [];

  for (const playlist of sources.playlists) {
    console.log(`플레이리스트 처리 중: ${playlist.name} (${playlist.id})`);
    const items = getPlaylistItems(playlist.id);

    for (const item of items) {
      if (processed.has(item.video_id)) {
        console.log(`  건너뜀 (처리 완료): ${item.video_id}`);
        continue;
      }
      newVideos.push({ ...item, playlist: playlist.name, source_type: "youtube" });
      console.log(`  신규: ${item.title}`);
    }
  }

  console.log(`\n신규 영상: ${newVideos.length}개`);

  if (newVideos.length === 0) {
    console.log("처리할 신규 영상 없음.");
    return;
  }

  if (DRY_RUN) {
    console.log("DRY_RUN: 파일 저장 생략");
    console.log(JSON.stringify(newVideos, null, 2));
    return;
  }

  fs.mkdirSync(DATA_DIR, { recursive: true });

  const outFile = path.join(DATA_DIR, `youtube-${POST_DATE}.json`);

  // 기존 파일이 있으면 읽고 append (덮어쓰기 방지)
  let existing = [];
  if (fs.existsSync(outFile)) {
    try {
      existing = JSON.parse(fs.readFileSync(outFile, "utf8"));
      console.log(`기존 파일 로드: ${existing.length}개`);
    } catch (e) {
      console.warn(`기존 파일 파싱 실패, 새로 생성: ${e.message}`);
    }
  }
  const existingIds = new Set(existing.map((v) => v.video_id));
  const merged = [...existing];
  for (const v of newVideos) {
    if (!existingIds.has(v.video_id)) merged.push(v);
  }

  fs.writeFileSync(outFile, JSON.stringify(merged, null, 2));
  console.log(`저장: ${outFile} (${merged.length}개, 신규 ${newVideos.length}개)`);

  for (const v of newVideos) processed.add(v.video_id);
  processedData.processed = [...processed];
  fs.writeFileSync(PROCESSED_FILE, JSON.stringify(processedData, null, 2));
  console.log("youtube-processed.json 업데이트 완료");
}

main();
