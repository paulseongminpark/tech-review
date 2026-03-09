#!/usr/bin/env node
/**
 * build-sources-feed.js
 * _data/bookmarks.json + _data/sources/youtube-*.json → sources.json (public)
 * 포트폴리오에서 fetch해서 3소스 카드 표시용
 */
const fs = require("fs");
const path = require("path");

const BLOG_DIR = path.join(__dirname, "..");
const DATA_DIR = path.join(BLOG_DIR, "_data");

// ── Twitter: bookmarks.json 최신 3개 ─────────────────────────────
const bmPath = path.join(DATA_DIR, "bookmarks.json");
const bookmarks = fs.existsSync(bmPath)
  ? JSON.parse(fs.readFileSync(bmPath, "utf-8"))
  : [];

const twitter = [...bookmarks]
  .sort((a, b) => {
    const da = a.added_at || a.date || "";
    const db = b.added_at || b.date || "";
    if (db !== da) return db.localeCompare(da);
    // added_at 같으면 id 역순 (bm-019 > bm-001)
    return (b.id || "").localeCompare(a.id || "");
  })
  .slice(0, 4)
  .map((b) => ({
  author: b.author || "",
  date: b.added_at || b.date || "",
  url: b.url || "",
  whats_happening: (b.whats_happening || b.smart_brevity?.why || "").slice(0, 80),
  apply_point: ((b.apply_points || [])[0] || "").slice(0, 80),
}));

// ── YouTube: 최신 파일에서 summary 있는 영상 1개 ──────────────────
const sourcesDir = path.join(DATA_DIR, "sources");
const ytFiles = fs
  .readdirSync(sourcesDir)
  .filter((f) => f.startsWith("youtube-"))
  .sort()
  .reverse();

let youtube = null;
for (const f of ytFiles) {
  const videos = JSON.parse(
    fs.readFileSync(path.join(sourcesDir, f), "utf-8")
  );
  const withSummary = videos.filter((v) => v.summary);
  if (withSummary.length > 0) {
    const v = withSummary[0];
    youtube = {
      title: v.title || "",
      channel: v.channel || "",
      video_id: v.video_id || "",
      url: v.url || "",
      why: v.summary?.smart_brevity?.why || "",
      section_count: (v.summary?.sections || []).length,
      published_at: (v.published_at || "").slice(0, 10),
    };
    break;
  }
}

const feed = {
  twitter,
  youtube: youtube ? [youtube] : [],
};

const outPath = path.join(BLOG_DIR, "sources.json");
fs.writeFileSync(outPath, JSON.stringify(feed, null, 2), "utf-8");
console.log(
  `sources.json 생성 완료 — twitter ${twitter.length}개, youtube ${youtube ? 1 : 0}개`
);
