#!/usr/bin/env node
/**
 * fetch-youtube.js
 * youtube-sources.json 플레이리스트 → 신규 영상 추출
 * → _data/sources/youtube-YYYY-MM-DD.json 저장
 *
 * 환경변수:
 *   YOUTUBE_API_KEY  - YouTube Data API v3 키
 *   POST_DATE        - YYYY-MM-DD (기본: 오늘)
 *   DRY_RUN          - "true"이면 파일 저장 생략
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

const API_KEY = process.env.YOUTUBE_API_KEY;
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const DRY_RUN = process.env.DRY_RUN === "true";

if (!API_KEY) {
  console.error("YOUTUBE_API_KEY 환경변수가 필요합니다.");
  process.exit(1);
}

const SOURCES_FILE = path.join(__dirname, "..", "config", "youtube-sources.json");
const PROCESSED_FILE = path.join(__dirname, "..", "config", "youtube-processed.json");
const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`JSON 파싱 실패: ${data.slice(0, 200)}`));
        }
      });
    }).on("error", reject);
  });
}

async function getPlaylistItems(playlistId) {
  const url = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=${playlistId}&key=${API_KEY}`;
  const data = await httpsGet(url);
  if (data.error) {
    throw new Error(`YouTube API 오류: ${data.error.message}`);
  }
  return (data.items || []).map((item) => ({
    video_id: item.snippet.resourceId.videoId,
    title: item.snippet.title,
    channel: item.snippet.channelTitle,
    published_at: item.snippet.publishedAt,
    thumbnail: item.snippet.thumbnails?.medium?.url || "",
    url: `https://www.youtube.com/watch?v=${item.snippet.resourceId.videoId}`,
  }));
}

async function main() {
  const sources = JSON.parse(fs.readFileSync(SOURCES_FILE, "utf8"));
  const processedData = JSON.parse(fs.readFileSync(PROCESSED_FILE, "utf8"));
  const processed = new Set(processedData.processed);

  const newVideos = [];

  for (const playlist of sources.playlists) {
    console.log(`플레이리스트 처리 중: ${playlist.name} (${playlist.id})`);
    const items = await getPlaylistItems(playlist.id);

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
  fs.writeFileSync(outFile, JSON.stringify(newVideos, null, 2));
  console.log(`저장: ${outFile}`);

  for (const v of newVideos) processed.add(v.video_id);
  processedData.processed = [...processed];
  fs.writeFileSync(PROCESSED_FILE, JSON.stringify(processedData, null, 2));
  console.log("youtube-processed.json 업데이트 완료");
}

main().catch((e) => { console.error(e); process.exit(1); });
