#!/usr/bin/env node
/**
 * extract-sections.js
 * _posts/ko/, _posts/en/ 포스트에서 섹션 추출
 * → _data/sections/YYYY-MM-DD-{lang}.json 저장
 *
 * 사용:
 *   node scripts/extract-sections.js           (전체 소급 처리)
 *   node scripts/extract-sections.js --date 2026-03-04  (특정 날짜만)
 */

const fs = require("fs");
const path = require("path");

const POSTS_DIR = path.join(__dirname, "..", "_posts");
const DATA_DIR = path.join(__dirname, "..", "_data", "sections");
const TAXONOMY_FILE = path.join(
  __dirname,
  "..",
  "perplexity-prompts",
  "taxonomy.json"
);

const taxonomy = JSON.parse(fs.readFileSync(TAXONOMY_FILE, "utf8"));

// tier2 전체 Set
const tier2All = new Set(Object.values(taxonomy.tier2).flat());

// tier2 → tier1 역매핑
const tier2ToTier1 = {};
for (const [cat, tags] of Object.entries(taxonomy.tier2)) {
  for (const tag of tags) {
    tier2ToTier1[tag] = cat;
  }
}

// ─── 태그 정규화 ──────────────────────────────────────────────
function normalizeTags(rawTags) {
  const result = new Set();

  for (const raw of (rawTags || [])) {
    const t = raw.trim().toLowerCase().replace(/^["']|["']$/g, "");
    if (!t) continue;

    if (tier2All.has(t)) {
      result.add(t);
      continue;
    }
    if (taxonomy.fallback_map[t]) {
      taxonomy.fallback_map[t].forEach((m) => result.add(m));
      continue;
    }
    // tier1 카테고리 자체이면 그대로 통과
    if (taxonomy.tier1[t]) {
      result.add(t);
      continue;
    }
    console.warn(`  ⚠️  unknown tag: "${t}" → misc`);
    result.add("misc");
  }

  return [...result];
}

// misc 제거: 다른 유효 태그가 있으면 misc 불필요
function cleanMisc(tags) {
  if (tags.length > 1 && tags.includes("misc")) {
    return tags.filter((t) => t !== "misc");
  }
  return tags;
}

// ─── 섹션 제목에서 tier2 키워드 감지 ────────────────────────
function detectTagsFromTitle(title) {
  const found = new Set();
  const lower = title.toLowerCase();

  for (const tag of tier2All) {
    // 하이픈 제거한 버전도 비교 ("ai-models" → "ai models")
    const tagPlain = tag.replace(/-/g, " ");
    const tagParts = tag.split("-");

    if (
      lower.includes(tag) ||
      lower.includes(tagPlain) ||
      (tagParts.length === 1 && new RegExp(`\\b${tagParts[0]}\\b`).test(lower))
    ) {
      found.add(tag);
    }
  }
  return [...found];
}

// ─── front matter 파싱 ──────────────────────────────────────
function parseFrontMatter(content) {
  content = content.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return { meta: {}, body: content };

  const meta = {};
  for (const line of match[1].split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let val = line.slice(colonIdx + 1).trim();

    if (key === "tags") {
      meta[key] = val
        .replace(/[\[\]]/g, "")
        .split(",")
        .map((t) => t.trim().replace(/^["']|["']$/g, ""))
        .filter(Boolean);
    } else {
      meta[key] = val.replace(/^["']|["']$/g, "");
    }
  }

  const body = content.slice(match[0].length).trim();
  return { meta, body };
}

// ─── 섹션 추출 ───────────────────────────────────────────────
function extractSections(body, postTags) {
  const sections = [];
  const sectionRegex = /^## (\d+)\.\s+(.+)$/gm;
  const matches = [];
  let m;

  while ((m = sectionRegex.exec(body)) !== null) {
    matches.push({
      index: parseInt(m[1]),
      title: m[2].trim(),
      pos: m.index,
      fullMatch: m[0],
    });
  }

  for (let i = 0; i < matches.length; i++) {
    const bodyStart = matches[i].pos + matches[i].fullMatch.length;
    const bodyEnd =
      i + 1 < matches.length ? matches[i + 1].pos : body.length;
    const sectionBody = body.slice(bodyStart, bodyEnd).trim();

    // 리드: 첫 번째 의미 있는 단락 (볼드/불릿/헤더 제외)
    const lead =
      sectionBody
        .split("\n")
        .map((l) => l.trim())
        .find(
          (l) =>
            l.length > 10 &&
            !l.startsWith("**") &&
            !l.startsWith("-") &&
            !l.startsWith("#") &&
            !l.startsWith(">")
        ) || "";

    // 태그: 포스트 태그 정규화 + 섹션 제목 키워드 감지
    const tagSet = new Set([
      ...normalizeTags(postTags),
      ...detectTagsFromTitle(matches[i].title),
    ]);

    sections.push({
      index: matches[i].index,
      title: matches[i].title,
      lead: lead.slice(0, 250),
      tags: cleanMisc([...tagSet]),
      anchor: matches[i].title
        .toLowerCase()
        .replace(/[^\w\s가-힣·\-]/g, "")
        .replace(/\s+/g, "-")
        .slice(0, 60),
    });
  }

  return sections;
}

// ─── 포스트 처리 ─────────────────────────────────────────────
function processPost(filepath) {
  const content = fs.readFileSync(filepath, "utf8");
  const { meta, body } = parseFrontMatter(content);

  if (!meta.date || !meta.lang) return null;

  const sections = extractSections(body, meta.tags || []);
  if (sections.length === 0) return null;

  return {
    date: meta.date,
    lang: meta.lang,
    post_url: meta.permalink || "",
    post_title: meta.title || "",
    source_type: "perplexity",
    sections,
  };
}

// ─── main ────────────────────────────────────────────────────
function main() {
  fs.mkdirSync(DATA_DIR, { recursive: true });

  const targetDate = process.argv.includes("--date")
    ? process.argv[process.argv.indexOf("--date") + 1]
    : null;

  let processed = 0;
  let skipped = 0;

  for (const lang of ["ko", "en"]) {
    const langDir = path.join(POSTS_DIR, lang);
    if (!fs.existsSync(langDir)) continue;

    const files = fs
      .readdirSync(langDir)
      .filter((f) => f.endsWith(".md"))
      .filter((f) => !targetDate || f.startsWith(targetDate))
      .sort();

    for (const file of files) {
      const result = processPost(path.join(langDir, file));

      if (!result) {
        skipped++;
        continue;
      }

      const outFile = path.join(DATA_DIR, `${result.date}-${lang}.json`);
      fs.writeFileSync(outFile, JSON.stringify(result, null, 2), "utf8");
      console.log(
        `✓ ${result.date}-${lang}: ${result.sections.length}섹션 | 태그: ${[
          ...new Set(result.sections.flatMap((s) => s.tags)),
        ].join(", ")}`
      );
      processed++;
    }
  }

  console.log(`\n완료: ${processed}개 처리, ${skipped}개 스킵`);
}

main();
