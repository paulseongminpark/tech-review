#!/usr/bin/env node
/**
 * remap-tags.js
 * 포스트 front matter tags를 taxonomy 기반으로 재매핑
 *
 * 사용:
 *   node scripts/remap-tags.js           (dry-run, 변경 미리보기)
 *   node scripts/remap-tags.js --apply   (실제 적용)
 */

const fs = require("fs");
const path = require("path");

const POSTS_DIR = path.join(__dirname, "..", "_posts");
const TAXONOMY_FILE = path.join(
  __dirname,
  "..",
  "perplexity-prompts",
  "taxonomy.json"
);

const taxonomy = JSON.parse(fs.readFileSync(TAXONOMY_FILE, "utf8"));
const tier2All = new Set(Object.values(taxonomy.tier2).flat());
const tier1All = new Set(Object.keys(taxonomy.tier1));

const APPLY = process.argv.includes("--apply");

function normalizeTags(rawTags) {
  const result = new Set();
  for (const raw of rawTags || []) {
    const t = raw.trim().toLowerCase().replace(/^["']|["']$/g, "");
    if (!t) continue;

    if (tier2All.has(t)) { result.add(t); continue; }
    if (taxonomy.tier1[t]) continue; // tier1 카테고리는 포스트 태그에서도 제외
    if (taxonomy.fallback_map[t]) {
      taxonomy.fallback_map[t]
        .filter((m) => !taxonomy.tier1[m])
        .forEach((m) => result.add(m));
      continue;
    }
    // misc는 버림 — 재매핑 후에는 misc 없어야 함
    console.warn(`  ⚠️  매핑 없음: "${t}" → 제거`);
  }
  // misc 제거
  result.delete("misc");
  return [...result].sort();
}

function processFile(filepath) {
  let content = fs.readFileSync(filepath, "utf8");
  const crlf = content.includes("\r\n");
  content = content.replace(/\r\n/g, "\n").replace(/\r/g, "\n");

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) return null;

  // tags 라인 파싱
  const tagsMatch = fmMatch[1].match(/^tags:\s*(.+)$/m);
  if (!tagsMatch) return null;

  const rawTagStr = tagsMatch[1];
  const rawTags = rawTagStr
    .replace(/[\[\]]/g, "")
    .split(",")
    .map((t) => t.trim().replace(/^["']|["']$/g, ""))
    .filter(Boolean);

  const newTags = normalizeTags(rawTags);
  const newTagStr = `["${newTags.join('", "')}"]`;

  if (rawTagStr.trim() === newTagStr) return null; // 변경 없음

  const newContent = content.replace(
    /^tags:\s*.+$/m,
    `tags: ${newTagStr}`
  );

  return {
    filepath,
    before: rawTags,
    after: newTags,
    newContent: crlf ? newContent.replace(/\n/g, "\r\n") : newContent,
  };
}

function main() {
  const changes = [];

  for (const lang of ["ko", "en"]) {
    const langDir = path.join(POSTS_DIR, lang);
    if (!fs.existsSync(langDir)) continue;

    const files = fs.readdirSync(langDir).filter((f) => f.endsWith(".md")).sort();
    for (const file of files) {
      const result = processFile(path.join(langDir, file));
      if (!result) continue;
      changes.push({ file: `${lang}/${file}`, ...result });
    }
  }

  if (changes.length === 0) {
    console.log("변경 없음");
    return;
  }

  console.log(`\n변경 대상: ${changes.length}개 파일\n${"─".repeat(60)}`);
  for (const c of changes) {
    console.log(`\n📄 ${c.file}`);
    console.log(`  이전: [${c.before.join(", ")}]`);
    console.log(`  이후: [${c.after.join(", ")}]`);
  }

  if (!APPLY) {
    console.log(`\n${"─".repeat(60)}`);
    console.log("dry-run 완료. 적용하려면: node scripts/remap-tags.js --apply");
    return;
  }

  // 실제 적용
  for (const c of changes) {
    fs.writeFileSync(c.filepath, c.newContent, "utf8");
  }
  console.log(`\n✅ ${changes.length}개 파일 적용 완료`);
}

main();
