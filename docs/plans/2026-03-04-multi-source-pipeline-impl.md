# Multi-Source Pipeline Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Twitter/Threads/YouTube 소스 파이프라인 추가 + Daily Digest UI (기존 topics 대체)

**Architecture:** YouTube는 YouTube Data API v3 + yt-dlp + Gemini Smart Brevity 요약. Twitter/Threads는 Playwright 실제 로그인 + following 피드 스크래핑. UI는 Daily Digest 탭 (날짜 패널 + 태그 카드 그리드) + Twitter/Threads/YouTube 전용 페이지.

**Tech Stack:** Node.js (기존 패턴), Playwright, YouTube Data API v3, Gemini API (`@google/generative-ai`), yt-dlp (Python), Jekyll + Liquid

---

## Phase 1: YouTube 파이프라인

### Task 1: youtube-sources.json 초기화

**Files:**
- Create: `config/youtube-sources.json`
- Create: `config/youtube-processed.json`

**Step 1: 파일 생성**

```json
// config/youtube-sources.json
{
  "playlists": [
    {
      "id": "PLxxxxxxxxxxxxxxxx",
      "name": "AI Tech Picks",
      "lang": "en"
    }
  ]
}
```

```json
// config/youtube-processed.json
{
  "processed": []
}
```

**Step 2: 커밋**

```bash
git add config/youtube-sources.json config/youtube-processed.json
git commit -m "[tech-review] youtube sources 설정 파일 초기화"
```

---

### Task 2: fetch-youtube.js 작성

**Files:**
- Create: `scripts/fetch-youtube.js`

**Step 1: 의존성 확인**

```bash
cd /c/dev/01_projects/03_tech-review/blog
cat package.json  # 기존 의존성 확인
```

**Step 2: 스크립트 작성**

```javascript
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
      res.on("end", () => resolve(JSON.parse(data)));
    }).on("error", reject);
  });
}

async function getPlaylistItems(playlistId) {
  const url = `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=${playlistId}&key=${API_KEY}`;
  const data = await httpsGet(url);
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

  // _data/sources/ 디렉토리 생성
  fs.mkdirSync(DATA_DIR, { recursive: true });

  const outFile = path.join(DATA_DIR, `youtube-${POST_DATE}.json`);
  fs.writeFileSync(outFile, JSON.stringify(newVideos, null, 2));
  console.log(`저장: ${outFile}`);

  // processed ID 추가
  for (const v of newVideos) processed.add(v.video_id);
  processedData.processed = [...processed];
  fs.writeFileSync(PROCESSED_FILE, JSON.stringify(processedData, null, 2));
  console.log("youtube-processed.json 업데이트 완료");
}

main().catch((e) => { console.error(e); process.exit(1); });
```

**Step 3: 로컬 테스트 (DRY_RUN)**

```bash
YOUTUBE_API_KEY=실제키 DRY_RUN=true POST_DATE=2026-03-04 \
  node scripts/fetch-youtube.js
```

Expected: 신규 영상 목록 콘솔 출력, 파일 미생성

**Step 4: 실제 실행**

```bash
YOUTUBE_API_KEY=실제키 POST_DATE=2026-03-04 \
  node scripts/fetch-youtube.js
```

Expected: `_data/sources/youtube-2026-03-04.json` 생성

**Step 5: 커밋**

```bash
git add scripts/fetch-youtube.js config/youtube-processed.json
git commit -m "[tech-review] fetch-youtube.js 신규 영상 추출 스크립트"
```

---

### Task 3: summarize-youtube.js 작성

**Files:**
- Create: `scripts/summarize-youtube.js`

**Step 1: Gemini 패키지 설치**

```bash
cd /c/dev/01_projects/03_tech-review/blog
npm install @google/generative-ai
```

**Step 2: yt-dlp 설치 확인**

```bash
yt-dlp --version
# 없으면: pip install yt-dlp
```

**Step 3: 스크립트 작성**

```javascript
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
const { GoogleGenerativeAI } = require("@google/generative-ai");

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const DRY_RUN = process.env.DRY_RUN === "true";

if (!GEMINI_API_KEY) {
  console.error("GEMINI_API_KEY 환경변수가 필요합니다.");
  process.exit(1);
}

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

const SMART_BREVITY_PROMPT = `다음 유튜브 영상 트랜스크립트를 Smart Brevity 형식으로 요약하세요.

반드시 아래 JSON 형식으로만 응답하세요:
{
  "one_line": "한 문장 핵심 요약",
  "why_it_matters": "핵심 의미 1~2문장",
  "points": ["포인트 1", "포인트 2", "포인트 3"],
  "whats_next": "다음 전망 1문장"
}

트랜스크립트:
`;

function getTranscript(videoId) {
  try {
    const tmpFile = `/tmp/transcript-${videoId}.txt`;
    execSync(
      `yt-dlp --write-auto-sub --sub-lang en --skip-download ` +
      `--sub-format vtt --output /tmp/transcript-${videoId} ` +
      `https://www.youtube.com/watch?v=${videoId}`,
      { stdio: "pipe" }
    );
    // VTT → 텍스트 변환
    const vttFile = `/tmp/transcript-${videoId}.en.vtt`;
    if (!fs.existsSync(vttFile)) return null;
    const vtt = fs.readFileSync(vttFile, "utf8");
    // VTT 헤더/타임스탬프 제거, 텍스트만 추출
    const lines = vtt.split("\n").filter(
      (l) => l.trim() && !l.startsWith("WEBVTT") && !/^\d{2}:/.test(l) && !/^NOTE/.test(l)
    );
    // 중복 제거
    const unique = [...new Set(lines)];
    return unique.join(" ").slice(0, 8000); // Gemini 컨텍스트 제한
  } catch (e) {
    console.error(`  transcript 추출 실패 (${videoId}): ${e.message}`);
    return null;
  }
}

async function summarize(transcript, title) {
  const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
  const prompt = SMART_BREVITY_PROMPT + transcript;
  const result = await model.generateContent(prompt);
  const text = result.response.text().trim();
  // JSON 블록 파싱
  const match = text.match(/\{[\s\S]*\}/);
  if (!match) throw new Error("JSON 응답 파싱 실패");
  return JSON.parse(match[0]);
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
      const summary = await summarize(transcript, video.title);
      video.summary = summary;
      console.log(`  요약 완료: ${summary.one_line}`);
    } catch (e) {
      console.error(`  요약 실패: ${e.message}`);
    }

    // 속도 제한 방지
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
```

**Step 4: 테스트**

```bash
GEMINI_API_KEY=실제키 DRY_RUN=true POST_DATE=2026-03-04 \
  node scripts/summarize-youtube.js
```

Expected: 영상별 Smart Brevity 요약 콘솔 출력

**Step 5: 커밋**

```bash
git add scripts/summarize-youtube.js package.json package-lock.json
git commit -m "[tech-review] summarize-youtube.js yt-dlp+Gemini Smart Brevity 요약"
```

---

## Phase 2: Daily Digest UI

### Task 4: default.html에 탭 네비게이션 추가

**Files:**
- Modify: `_layouts/default.html`

**Step 1: 현재 default.html 확인 후 nav 추가**

`<body>` 내 `{% include lang-toggle.html %}` 바로 아래에 추가:

```html
<nav class="site-nav">
  <a href="{{ site.baseurl }}/{{ page.lang | default: 'ko' }}/"
     {% if page.url contains 'daily-digest' == false and page.url contains 'twitter' == false and page.url contains 'threads' == false and page.url contains 'youtube' == false %}class="active"{% endif %}>Home</a>
  <a href="{{ site.baseurl }}/{{ page.lang | default: 'ko' }}/daily-digest/"
     {% if page.url contains 'daily-digest' %}class="active"{% endif %}>Daily Digest</a>
  <a href="{{ site.baseurl }}/{{ page.lang | default: 'ko' }}/twitter/"
     {% if page.url contains '/twitter/' %}class="active"{% endif %}>Twitter</a>
  <a href="{{ site.baseurl }}/{{ page.lang | default: 'ko' }}/threads/"
     {% if page.url contains '/threads/' %}class="active"{% endif %}>Threads</a>
  <a href="{{ site.baseurl }}/{{ page.lang | default: 'ko' }}/youtube/"
     {% if page.url contains '/youtube/' %}class="active"{% endif %}>YouTube</a>
</nav>
```

`<style>` 블록에 추가:

```css
.site-nav { display:flex; gap:1rem; margin-bottom:2rem; border-bottom:1px solid #eee; padding-bottom:0.75rem; }
.site-nav a { color:#666; font-size:0.9rem; text-decoration:none; padding:0.25rem 0; }
.site-nav a.active { color:#1a1a1a; font-weight:600; border-bottom:2px solid #1a1a1a; }
```

**Step 2: 로컬 Jekyll 서버로 확인**

```bash
# 사용자가 Warp에서 직접 실행:
cd /c/dev/01_projects/03_tech-review/blog && bundle exec jekyll serve
```

**Step 3: 커밋**

```bash
git add _layouts/default.html
git commit -m "[tech-review] site-nav 탭 추가 (Daily Digest/Twitter/Threads/YouTube)"
```

---

### Task 5: Daily Digest 페이지 생성 (기존 topics 대체)

**Files:**
- Create: `ko/daily-digest.html`
- Create: `en/daily-digest.html`
- 기존 `ko/topics.html`, `en/topics.html` 삭제 (redirect로 대체)

**Step 1: ko/daily-digest.html 작성**

```html
---
layout: default
title: Daily Digest
lang: ko
permalink: /ko/daily-digest/
---

<div style="display:flex; gap:1.5rem; min-height:60vh;">

  <!-- 왼쪽: 날짜 패널 -->
  <div id="date-panel" style="width:120px; flex-shrink:0; border-right:1px solid #eee; padding-right:1rem;">
    <p style="font-size:0.75rem; color:#999; margin-bottom:0.75rem; text-transform:uppercase; letter-spacing:0.05em;">Dates</p>
    <div id="date-list"></div>
  </div>

  <!-- 오른쪽: 태그 토글 + 카드 그리드 -->
  <div style="flex:1; min-width:0;">
    <!-- 태그 토글 -->
    <div id="tag-toggle" style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:1.25rem;"></div>

    <!-- 카드 그리드 -->
    <div id="card-grid" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:0.75rem;"></div>
  </div>
</div>

<script>
// ── 데이터 수집 ──────────────────────────────────────────────
const SECTIONS = [];
{% for item in site.data.sections %}
  {% assign d = item[1] %}
  {% if d.lang == 'ko' %}
    {% for s in d.sections %}
SECTIONS.push({
  date: {{ d.date | jsonify }},
  post_url: {{ d.post_url | prepend: site.baseurl | jsonify }},
  index: {{ s.index }},
  title: {{ s.title | jsonify }},
  tags: {{ s.tags | jsonify }},
  anchor: {{ s.anchor | jsonify }}
});
    {% endfor %}
  {% endif %}
{% endfor %}

SECTIONS.sort((a, b) => b.date.localeCompare(a.date));

// ── 태그 집계 ────────────────────────────────────────────────
const tagMap = {}; // tag → { count, dates }
SECTIONS.forEach(s => {
  (s.tags || []).forEach(t => {
    if (!tagMap[t]) tagMap[t] = { count: 0, dates: new Set() };
    tagMap[t].count++;
    tagMap[t].dates.add(s.date);
  });
});
const allTags = Object.keys(tagMap).sort((a, b) => tagMap[b].count - tagMap[a].count);

// ── 날짜 목록 ────────────────────────────────────────────────
const allDates = [...new Set(SECTIONS.map(s => s.date))];

let activeDate = null;
let activeTag = null;

// ── 렌더링 ──────────────────────────────────────────────────
function renderDateList() {
  document.getElementById('date-list').innerHTML =
    ['all', ...allDates].map(d =>
      `<div onclick="selectDate('${d}')"
           style="padding:0.3rem 0; font-size:0.82rem; cursor:pointer; color:${d === (activeDate || 'all') ? '#1a1a1a' : '#999'}; font-weight:${d === (activeDate || 'all') ? '600' : '400'}">
         ${d === 'all' ? 'All' : d.slice(5)}
       </div>`
    ).join('');
}

function renderTagToggle() {
  document.getElementById('tag-toggle').innerHTML =
    ['all', ...allTags].map(t => {
      const count = t === 'all' ? SECTIONS.length : tagMap[t].count;
      const isActive = t === (activeTag || 'all');
      return `<button onclick="selectTag('${t}')"
        style="background:${isActive ? '#1a1a1a' : '#f0f0f0'}; color:${isActive ? '#fff' : '#444'};
               border:none; padding:0.3rem 0.65rem; border-radius:4px; font-size:0.8rem; cursor:pointer;">
        ${t === 'all' ? 'All' : t} <span style="opacity:0.6;">${count}</span>
      </button>`;
    }).join('');
}

function getFilteredTags() {
  let filtered = SECTIONS;
  if (activeDate) filtered = filtered.filter(s => s.date === activeDate);
  // 날짜 필터 후 태그 재집계
  const tMap = {};
  filtered.forEach(s => {
    (s.tags || []).forEach(t => {
      tMap[t] = (tMap[t] || 0) + 1;
    });
  });
  return Object.keys(tMap).sort((a, b) => tMap[b] - tMap[a]).map(t => ({ tag: t, count: tMap[t] }));
}

function renderCards() {
  let filtered = SECTIONS;
  if (activeDate) filtered = filtered.filter(s => s.date === activeDate);
  if (activeTag) filtered = filtered.filter(s => (s.tags || []).includes(activeTag));

  // 태그별 카드 (각 태그 1개 카드)
  const tagCounts = {};
  filtered.forEach(s => {
    (s.tags || []).forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; });
  });
  const tags = Object.keys(tagCounts).sort((a, b) => tagCounts[b] - tagCounts[a]);

  if (activeTag) {
    // 태그 선택 시 → 섹션 목록
    document.getElementById('card-grid').style.gridTemplateColumns = '1fr';
    document.getElementById('card-grid').innerHTML = filtered.map(s =>
      `<a href="${s.post_url}#${s.anchor}"
          style="display:block; padding:0.75rem; border:1px solid #eee; border-radius:6px; text-decoration:none; color:#1a1a1a;">
         <div style="font-size:0.75rem; color:#999; margin-bottom:0.3rem;">${s.date}</div>
         <div style="font-size:0.9rem; font-weight:600; line-height:1.4;">${s.title}</div>
         <div style="display:flex; gap:0.3rem; margin-top:0.5rem; flex-wrap:wrap;">
           ${(s.tags||[]).map(t => `<span style="background:#f0f0f0; padding:0.1rem 0.4rem; border-radius:3px; font-size:0.72rem;">${t}</span>`).join('')}
         </div>
       </a>`
    ).join('');
    return;
  }

  // 태그 카드 그리드
  document.getElementById('card-grid').style.gridTemplateColumns = 'repeat(auto-fill,minmax(140px,1fr))';
  document.getElementById('card-grid').innerHTML = tags.map(t =>
    `<div onclick="selectTag('${t}')"
         style="aspect-ratio:1; background:#f8f8f8; border-radius:8px; padding:1rem;
                display:flex; flex-direction:column; justify-content:space-between;
                cursor:pointer; border:1px solid #eee; transition:border-color 0.15s;"
         onmouseover="this.style.borderColor='#999'" onmouseout="this.style.borderColor='#eee'">
       <div style="font-size:1rem; font-weight:700; color:#1a1a1a;">#${t}</div>
       <div style="font-size:0.78rem; color:#888;">${tagCounts[t]}개 섹션</div>
     </div>`
  ).join('');
}

function selectDate(d) {
  activeDate = d === 'all' ? null : d;
  activeTag = null;
  renderDateList();
  renderTagToggle();
  renderCards();
}

function selectTag(t) {
  activeTag = t === 'all' ? null : t;
  renderTagToggle();
  renderCards();
}

// 초기화
renderDateList();
renderTagToggle();
renderCards();
</script>
```

**Step 2: en/daily-digest.html 작성**

같은 구조, `lang: en`, `permalink: /en/daily-digest/`, 텍스트만 영어로 변경:
- "Dates" → "Dates"
- `d.lang == 'en'` 조건
- `개 섹션` → ` sections`

**Step 3: ko/topics.html → redirect로 교체**

```html
---
layout: null
permalink: /ko/topics/
---
<meta http-equiv="refresh" content="0; url=/tech-review/ko/daily-digest/">
```

en/topics.html도 동일하게 `/en/daily-digest/` 로 redirect.

**Step 4: 로컬에서 확인**

```bash
# Warp에서: bundle exec jekyll serve
# 브라우저: http://localhost:4000/tech-review/ko/daily-digest/
# 확인: 날짜 패널 / 태그 토글 / 카드 그리드 동작
```

**Step 5: 커밋**

```bash
git add ko/daily-digest.html en/daily-digest.html ko/topics.html en/topics.html
git commit -m "[tech-review] Daily Digest 페이지 (날짜+태그 카드 그리드) — topics 대체"
```

---

### Task 6: Twitter/Threads/YouTube 전용 페이지

**Files:**
- Create: `ko/twitter.html`, `en/twitter.html`
- Create: `ko/threads.html`, `en/threads.html`
- Create: `ko/youtube.html`, `en/youtube.html`

**Step 1: ko/twitter.html**

```html
---
layout: default
title: Twitter
lang: ko
permalink: /ko/twitter/
---

<div id="feed"></div>

<script>
const ITEMS = [];
{% for file in site.static_files %}
  {% if file.path contains '_data/sources/twitter' %}
    // Jekyll static_files는 JSON 직접 로드 불가 → fetch 사용
  {% endif %}
{% endfor %}

// _data/sources/ 파일 목록을 Jekyll로 주입
const SOURCE_FILES = [
  {% for item in site.data.sources %}
    {% assign key = item[0] %}
    {% if key contains 'twitter' %}
      {{ key | jsonify }},
    {% endif %}
  {% endfor %}
];

// site.data.sources.twitter-YYYY-MM-DD 형태로 접근
const ALL_ITEMS = [];
{% for item in site.data.sources %}
  {% assign key = item[0] %}
  {% if key contains 'twitter' %}
    {% for entry in item[1] %}
ALL_ITEMS.push({
  author: {{ entry.author | jsonify }},
  text: {{ entry.text | jsonify }},
  url: {{ entry.url | jsonify }},
  timestamp: {{ entry.timestamp | jsonify }},
  is_thread: {{ entry.is_thread | jsonify }},
  has_external_link: {{ entry.has_external_link | jsonify }}
});
    {% endfor %}
  {% endif %}
{% endfor %}

ALL_ITEMS.sort((a, b) => b.timestamp.localeCompare(a.timestamp));

document.getElementById('feed').innerHTML = ALL_ITEMS.length === 0
  ? '<p style="color:#999;">아직 수집된 트윗이 없습니다.</p>'
  : ALL_ITEMS.map(item => `
    <div style="padding:1rem 0; border-bottom:1px solid #eee;">
      <div style="font-size:0.8rem; color:#999; margin-bottom:0.4rem;">
        <strong>${item.author}</strong> · ${item.timestamp.slice(0,10)}
        ${item.is_thread ? ' · <span style="color:#0066cc;">스레드</span>' : ''}
      </div>
      <p style="font-size:0.9rem; line-height:1.6; white-space:pre-wrap;">${item.text}</p>
      ${item.has_external_link ? `<a href="${item.url}" target="_blank" style="font-size:0.8rem; color:#0066cc;">→ 원문 보기</a>` : ''}
    </div>
  `).join('');
</script>
```

**Step 2: ko/youtube.html**

```html
---
layout: default
title: YouTube
lang: ko
permalink: /ko/youtube/
---

<div id="feed"></div>

<script>
const ALL_ITEMS = [];
{% for item in site.data.sources %}
  {% assign key = item[0] %}
  {% if key contains 'youtube' %}
    {% for entry in item[1] %}
ALL_ITEMS.push({
  title: {{ entry.title | jsonify }},
  channel: {{ entry.channel | jsonify }},
  url: {{ entry.url | jsonify }},
  playlist: {{ entry.playlist | jsonify }},
  published_at: {{ entry.published_at | jsonify }},
  summary: {{ entry.summary | jsonify }}
});
    {% endfor %}
  {% endif %}
{% endfor %}

ALL_ITEMS.sort((a, b) => b.published_at.localeCompare(a.published_at));

document.getElementById('feed').innerHTML = ALL_ITEMS.length === 0
  ? '<p style="color:#999;">아직 수집된 영상이 없습니다.</p>'
  : ALL_ITEMS.map(item => {
    const s = item.summary || {};
    return `
    <div style="padding:1.25rem 0; border-bottom:1px solid #eee;">
      <div style="font-size:0.78rem; color:#999; margin-bottom:0.4rem;">
        ${item.channel} · ${item.published_at.slice(0,10)} · ${item.playlist}
      </div>
      <a href="${item.url}" target="_blank"
         style="font-weight:700; font-size:1rem; color:#1a1a1a; display:block; margin-bottom:0.75rem;">
        ${item.title} ↗
      </a>
      ${s.one_line ? `<p style="font-weight:600; margin-bottom:0.5rem;">${s.one_line}</p>` : ''}
      ${s.why_it_matters ? `<p style="font-size:0.88rem; color:#444; margin-bottom:0.5rem;">${s.why_it_matters}</p>` : ''}
      ${s.points ? `<ul style="list-style:none; padding-left:1rem;">${s.points.map(p=>`<li style="font-size:0.88rem; color:#444; margin:0.2rem 0;">· ${p}</li>`).join('')}</ul>` : ''}
      ${s.whats_next ? `<p style="font-size:0.85rem; color:#666; margin-top:0.5rem; font-style:italic;">${s.whats_next}</p>` : ''}
    </div>
  `}).join('');
</script>
```

**Step 3:** `ko/threads.html` → `ko/twitter.html`과 동일 구조, `'twitter'` → `'threads'`, 텍스트 변경.

**Step 4:** `en/` 버전 3개도 동일 구조 (lang 변경).

**Step 5: _data/sources 디렉토리 초기화**

```bash
mkdir -p _data/sources
echo '[]' > _data/sources/.gitkeep
```

**Step 6: 커밋**

```bash
git add ko/twitter.html en/twitter.html ko/threads.html en/threads.html \
        ko/youtube.html en/youtube.html _data/sources/
git commit -m "[tech-review] Twitter/Threads/YouTube 전용 페이지 추가"
```

---

## Phase 3: Twitter 파이프라인

### Task 7: export-cookies.js 작성

**Files:**
- Create: `scripts/export-cookies.js`

**Step 1: 스크립트 작성**

```javascript
#!/usr/bin/env node
/**
 * export-cookies.js
 * 로컬 실행용: 브라우저 쿠키 저장 → GitHub Secret 갱신에 사용
 *
 * 사용:
 *   node scripts/export-cookies.js twitter
 *   node scripts/export-cookies.js threads
 *
 * 동작:
 *   1. Playwright로 브라우저 창 오픈
 *   2. 사용자가 직접 로그인
 *   3. Enter 입력 시 쿠키 추출 → cookies-{service}.json 출력
 *   4. 출력된 JSON을 GitHub Secret에 붙여넣기
 */

const { chromium } = require("playwright");
const readline = require("readline");

const SERVICE = process.argv[2];
if (!["twitter", "threads"].includes(SERVICE)) {
  console.error("사용법: node export-cookies.js twitter|threads");
  process.exit(1);
}

const URLS = {
  twitter: "https://x.com/login",
  threads: "https://www.threads.net/login",
};

async function main() {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(URLS[SERVICE]);
  console.log(`\n브라우저에서 ${SERVICE} 로그인을 완료하세요.`);
  console.log("완료 후 Enter를 누르세요...");

  await new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin });
    rl.once("line", () => { rl.close(); resolve(); });
  });

  const cookies = await context.cookies();
  const cookiesJson = JSON.stringify(cookies, null, 2);

  console.log("\n=== GitHub Secret에 복사하세요 ===");
  console.log(cookiesJson);
  console.log("===================================");
  console.log(`\nSecret 이름: ${SERVICE.toUpperCase()}_COOKIES`);

  await browser.close();
}

main().catch((e) => { console.error(e); process.exit(1); });
```

**Step 2: Playwright 설치 확인**

```bash
npx playwright install chromium
```

**Step 3: 로컬 실행 테스트**

```bash
node scripts/export-cookies.js twitter
# 브라우저 오픈 → 로그인 → Enter → 쿠키 출력 확인
```

**Step 4: 커밋**

```bash
git add scripts/export-cookies.js
git commit -m "[tech-review] export-cookies.js 로컬 쿠키 추출 도구"
```

---

### Task 8: fetch-twitter.js 작성

**Files:**
- Create: `scripts/fetch-twitter.js`

**Step 1: 스크립트 작성**

```javascript
#!/usr/bin/env node
/**
 * fetch-twitter.js
 * GitHub Actions / 로컬: Playwright 쿠키 로그인 → following 피드
 * → 필터(280자+ OR 스레드 OR 외부링크) → JSON 저장
 *
 * 환경변수:
 *   TWITTER_COOKIES  - GitHub Secret: 쿠키 JSON 문자열
 *   POST_DATE        - YYYY-MM-DD
 *   MAX_ITEMS        - 최대 수집 수 (기본: 30)
 *   DRY_RUN          - "true"이면 파일 저장 생략
 */

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const COOKIES_JSON = process.env.TWITTER_COOKIES;
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const MAX_ITEMS = parseInt(process.env.MAX_ITEMS || "30");
const DRY_RUN = process.env.DRY_RUN === "true";

if (!COOKIES_JSON) {
  console.error("TWITTER_COOKIES 환경변수가 필요합니다.");
  process.exit(1);
}

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

function shouldInclude(text, hasThread, hasLink) {
  if (text.length >= 280) return true;
  if (hasThread) return true;
  if (hasLink) return true;
  return false;
}

async function main() {
  const cookies = JSON.parse(COOKIES_JSON);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  await context.addCookies(cookies);
  const page = await context.newPage();

  console.log("following 피드 로딩...");
  await page.goto("https://x.com/following", { waitUntil: "networkidle", timeout: 30000 });

  // 세션 만료 감지
  if (page.url().includes("/login")) {
    console.error("세션 만료 — TWITTER_COOKIES Secret 갱신 필요");
    await browser.close();
    process.exit(1);
  }

  const items = [];
  let scrollCount = 0;

  while (items.length < MAX_ITEMS && scrollCount < 10) {
    const tweets = await page.$$eval('[data-testid="tweet"]', (els) =>
      els.map((el) => {
        const textEl = el.querySelector('[data-testid="tweetText"]');
        const text = textEl ? textEl.innerText : "";
        const timeEl = el.querySelector("time");
        const linkEls = el.querySelectorAll('a[href^="http"]');
        const userEl = el.querySelector('[data-testid="User-Name"]');
        const hasThread = /\d+\/\d+/.test(text) || el.querySelector('[aria-label*="Thread"]') !== null;
        const hasLink = linkEls.length > 0;
        const tweetLinkEl = el.querySelector('a[href*="/status/"]');
        return {
          text,
          timestamp: timeEl ? timeEl.getAttribute("datetime") : "",
          author: userEl ? "@" + userEl.innerText.split("\n")[1] : "",
          url: tweetLinkEl ? "https://x.com" + tweetLinkEl.getAttribute("href") : "",
          is_thread: hasThread,
          has_external_link: hasLink,
          source_type: "twitter",
        };
      })
    );

    for (const t of tweets) {
      if (!t.text) continue;
      if (!shouldInclude(t.text, t.is_thread, t.has_external_link)) continue;
      if (items.find((i) => i.url === t.url)) continue; // 중복 제거
      items.push(t);
      console.log(`  [${items.length}] ${t.author}: ${t.text.slice(0, 60)}...`);
      if (items.length >= MAX_ITEMS) break;
    }

    if (items.length < MAX_ITEMS) {
      await page.evaluate(() => window.scrollBy(0, 1500));
      await page.waitForTimeout(2000);
      scrollCount++;
    }
  }

  await browser.close();
  console.log(`\n수집: ${items.length}개`);

  if (DRY_RUN) {
    console.log("DRY_RUN: 파일 저장 생략");
    return;
  }

  fs.mkdirSync(DATA_DIR, { recursive: true });
  const outFile = path.join(DATA_DIR, `twitter-${POST_DATE}.json`);
  fs.writeFileSync(outFile, JSON.stringify(items, null, 2));
  console.log(`저장: ${outFile}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
```

**Step 2: 로컬 테스트 (쿠키 추출 후)**

```bash
TWITTER_COOKIES="$(cat /tmp/twitter-cookies.json)" DRY_RUN=true \
  node scripts/fetch-twitter.js
```

Expected: 트윗 목록 콘솔 출력

**Step 3: 커밋**

```bash
git add scripts/fetch-twitter.js
git commit -m "[tech-review] fetch-twitter.js Playwright following 피드 스크래퍼"
```

---

### Task 9: fetch-threads.js 작성

**Files:**
- Create: `scripts/fetch-threads.js`

**Step 1: 스크립트 작성** (fetch-twitter.js 구조 동일, URL/셀렉터만 변경)

```javascript
#!/usr/bin/env node
/**
 * fetch-threads.js
 * Playwright 쿠키 로그인 → Threads following 피드
 * → 필터(100자+) → JSON 저장
 *
 * 환경변수: THREADS_COOKIES, POST_DATE, MAX_ITEMS, DRY_RUN
 */

const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const COOKIES_JSON = process.env.THREADS_COOKIES;
const POST_DATE = process.env.POST_DATE || new Date().toISOString().slice(0, 10);
const MAX_ITEMS = parseInt(process.env.MAX_ITEMS || "20");
const DRY_RUN = process.env.DRY_RUN === "true";

if (!COOKIES_JSON) {
  console.error("THREADS_COOKIES 환경변수가 필요합니다.");
  process.exit(1);
}

const DATA_DIR = path.join(__dirname, "..", "_data", "sources");

async function main() {
  const cookies = JSON.parse(COOKIES_JSON);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  await context.addCookies(cookies);
  const page = await context.newPage();

  console.log("Threads 피드 로딩...");
  await page.goto("https://www.threads.net/", { waitUntil: "networkidle", timeout: 30000 });

  if (page.url().includes("/login")) {
    console.error("세션 만료 — THREADS_COOKIES Secret 갱신 필요");
    await browser.close();
    process.exit(1);
  }

  const items = [];
  let scrollCount = 0;

  while (items.length < MAX_ITEMS && scrollCount < 10) {
    const posts = await page.$$eval('article', (els) =>
      els.map((el) => {
        const textEl = el.querySelector('div[dir="auto"]');
        const text = textEl ? textEl.innerText : "";
        const timeEl = el.querySelector("time");
        const linkEl = el.querySelector('a[href*="/t/"]');
        const authorEl = el.querySelector('a[href*="/@"]');
        return {
          text,
          timestamp: timeEl ? timeEl.getAttribute("datetime") : "",
          author: authorEl ? authorEl.getAttribute("href").replace("/", "@") : "",
          url: linkEl ? "https://www.threads.net" + linkEl.getAttribute("href") : "",
          source_type: "threads",
        };
      }).filter(p => p.text.length >= 100)
    );

    for (const p of posts) {
      if (items.find((i) => i.url === p.url)) continue;
      items.push(p);
      console.log(`  [${items.length}] ${p.author}: ${p.text.slice(0, 60)}...`);
      if (items.length >= MAX_ITEMS) break;
    }

    await page.evaluate(() => window.scrollBy(0, 1500));
    await page.waitForTimeout(2000);
    scrollCount++;
  }

  await browser.close();
  console.log(`\n수집: ${items.length}개`);

  if (DRY_RUN) { console.log("DRY_RUN: 저장 생략"); return; }

  fs.mkdirSync(DATA_DIR, { recursive: true });
  const outFile = path.join(DATA_DIR, `threads-${POST_DATE}.json`);
  fs.writeFileSync(outFile, JSON.stringify(items, null, 2));
  console.log(`저장: ${outFile}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
```

**Step 2: 커밋**

```bash
git add scripts/fetch-threads.js
git commit -m "[tech-review] fetch-threads.js Playwright Threads 피드 스크래퍼"
```

---

## Phase 4: GitHub Actions 워크플로우

### Task 10: fetch-youtube.yml 작성

**Files:**
- Create: `.github/workflows/fetch-youtube.yml`

```yaml
name: Fetch YouTube

on:
  schedule:
    - cron: '0 22 * * *'  # 매일 07:00 KST
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        working-directory: blog
        run: npm ci

      - name: Install yt-dlp
        run: pip install yt-dlp

      - name: Fetch new videos
        working-directory: blog
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
          POST_DATE: ${{ env.POST_DATE }}
        run: |
          POST_DATE=$(TZ=Asia/Seoul date +%Y-%m-%d)
          echo "POST_DATE=$POST_DATE" >> $GITHUB_ENV
          YOUTUBE_API_KEY=${{ secrets.YOUTUBE_API_KEY }} POST_DATE=$POST_DATE \
            node scripts/fetch-youtube.js

      - name: Summarize with Gemini
        working-directory: blog
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }} POST_DATE=${{ env.POST_DATE }} \
            node scripts/summarize-youtube.js

      - name: Commit and push
        working-directory: blog
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add _data/sources/ config/youtube-processed.json
          git diff --cached --quiet || git commit -m "[auto] youtube picks ${{ env.POST_DATE }}"
          git push
```

**Step 2: 커밋**

```bash
git add .github/workflows/fetch-youtube.yml
git commit -m "[tech-review] fetch-youtube.yml GitHub Actions 워크플로우"
```

---

### Task 11: fetch-twitter.yml + fetch-threads.yml 작성

**Files:**
- Create: `.github/workflows/fetch-twitter.yml`
- Create: `.github/workflows/fetch-threads.yml`

**fetch-twitter.yml:**

```yaml
name: Fetch Twitter

on:
  schedule:
    - cron: '30 22 * * *'  # 매일 07:30 KST
  workflow_dispatch:

jobs:
  fetch:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - name: Install dependencies
        working-directory: blog
        run: npm ci && npx playwright install chromium --with-deps
      - name: Fetch Twitter
        working-directory: blog
        run: |
          POST_DATE=$(TZ=Asia/Seoul date +%Y-%m-%d)
          TWITTER_COOKIES='${{ secrets.TWITTER_COOKIES }}' POST_DATE=$POST_DATE \
            node scripts/fetch-twitter.js
      - name: Commit and push
        working-directory: blog
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add _data/sources/
          git diff --cached --quiet || git commit -m "[auto] twitter picks $(TZ=Asia/Seoul date +%Y-%m-%d)"
          git push
```

`fetch-threads.yml`: 동일 구조, `TWITTER_COOKIES` → `THREADS_COOKIES`, `fetch-twitter.js` → `fetch-threads.js`, cron `'0 23 * * *'` (08:00 KST).

**Step 2: 커밋**

```bash
git add .github/workflows/fetch-twitter.yml .github/workflows/fetch-threads.yml
git commit -m "[tech-review] fetch-twitter/threads GitHub Actions 워크플로우"
git push
```

---

## GitHub Secrets 설정 체크리스트

Actions 탭 → Settings → Secrets and variables → Actions:

| Secret | 값 |
|--------|-----|
| `YOUTUBE_API_KEY` | Google Cloud Console → YouTube Data API v3 키 |
| `GEMINI_API_KEY` | Google AI Studio → API 키 |
| `TWITTER_COOKIES` | `node scripts/export-cookies.js twitter` 출력 JSON |
| `THREADS_COOKIES` | `node scripts/export-cookies.js threads` 출력 JSON |

---

## 구현 완료 확인

- [ ] `_data/sources/youtube-YYYY-MM-DD.json` 생성되고 summary 필드 포함
- [ ] Daily Digest 페이지: 날짜 패널 + 태그 카드 그리드 동작
- [ ] Twitter/Threads/YouTube 전용 페이지 데이터 표시
- [ ] 탭 네비게이션 5개 탭 정상 동작
- [ ] 3개 GitHub Actions 워크플로우 수동 실행 성공
- [ ] `/ko/topics/` → `/ko/daily-digest/` redirect 동작
