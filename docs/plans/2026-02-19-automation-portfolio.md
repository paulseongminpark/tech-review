# Tech Review 자동화 + 포트폴리오 연동 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Perplexity API → Jekyll 포스트 자동 생성 파이프라인 완성 + 포트폴리오에 최신 포스트 카드 표시

**Architecture:**
- Perplexity API (`sonar-pro`) → `fetch-perplexity.js` → 프롬프트별 리서치 콘텐츠 생성
- `parse-content.js` → 전달받은 마크다운을 front matter + Comments 섹션 추가해 Jekyll 포스트로 저장
- Jekyll 빌드 시 `feed.json` 자동 생성 → Portfolio `TechReviewCards.tsx`가 fetch

**Tech Stack:** Jekyll (Liquid), Node.js, GitHub Actions, React/TypeScript (portfolio)

---

## 현재 상태 (As-Is)

| 항목 | 상태 | 문제 |
|------|------|------|
| Perplexity 프롬프트 | OLD 형식 | "Claude 실행 지침" 포함, TOPIC_START/END 미사용, 섹션 구조 불일치 |
| parse-content.js | TOPIC_START/END 파싱 | 전달 형식과 맞지 않음 |
| create-post.yml | 동작하나 버그 있음 | 파일명 `-daily.md` 하드코딩, generate_comments.py 자동 실행 (수동 추가 방침과 충돌) |
| feed.json | 없음 | TechReviewCards.tsx가 fetch 시 404 |
| Portfolio 연동 | 미완 | feed.json만 생성하면 자동 동작 |

---

## Task 1: feed.json 생성 (Jekyll Liquid 템플릿)

**파일:** `tech-review-blog/feed.json` (신규)

Liquid 템플릿으로 빌드 시마다 자동 생성. KO 포스트를 기준으로 EN 포스트를 pair 필드로 매칭.

**Step 1: feed.json 파일 생성**

```liquid
---
layout: null
---
{%- assign ko_posts = site.posts | where: "lang", "ko" | sort: "date" | reverse -%}
{
  "posts": [
    {%- assign count = 0 -%}
    {%- for ko in ko_posts -%}
      {%- if count < 10 -%}
        {%- assign en = site.posts | where: "pair", ko.pair | where: "lang", "en" | first -%}
        {%- if count > 0 -%},{%- endif -%}
        {
          "date": "{{ ko.date | date: '%Y-%m-%d' }}",
          "pair": "{{ ko.pair }}",
          "title": {
            "ko": "{{ ko.title | escape }}",
            "en": "{{ en.title | default: ko.title | escape }}"
          },
          "tags": [{% for tag in ko.tags %}"{{ tag }}"{% unless forloop.last %},{% endunless %}{% endfor %}],
          "url": {
            "ko": "{{ ko.url }}",
            "en": "{{ en.url | default: ko.url }}"
          }
        }
        {%- assign count = count | plus: 1 -%}
      {%- endif -%}
    {%- endfor -%}
  ]
}
```

**Step 2: 커밋 + 배포 후 검증**
```
curl https://paulseongminpark.github.io/tech-review/feed.json
```
기대값: `{"posts":[{"date":"2026-02-19",...}]}`

---

## Task 2: create-post.yml 수정

**파일:** `.github/workflows/create-post.yml`

**수정 내용:**
- `generate_comments.py` 두 스텝 제거 (user가 수동으로 comments 추가)
- Python 설치 / `pip install anthropic` 스텝 제거 (불필요)
- `ANTHROPIC_API_KEY` 환경변수 참조 제거

**Step 1: 수정된 workflow**

```yaml
name: Create Daily Post

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
    inputs:
      post_date:
        description: "날짜 (YYYY-MM-DD, 기본: 오늘)"
        required: false

permissions:
  contents: write

jobs:
  create-post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Set POST_DATE
        run: |
          if [ -n "${{ github.event.inputs.post_date }}" ]; then
            echo "POST_DATE=${{ github.event.inputs.post_date }}" >> $GITHUB_ENV
          else
            echo "POST_DATE=$(TZ=Asia/Seoul date +%Y-%m-%d)" >> $GITHUB_ENV
          fi

      - name: Fetch KO content from Perplexity
        env:
          PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
          LANG: ko
          OUTPUT_FILE: /tmp/perplexity-ko.md
        run: node scripts/fetch-perplexity.js

      - name: Parse KO content
        env:
          CONTENT_FILE: /tmp/perplexity-ko.md
          LANG: ko
        run: node scripts/parse-content.js

      - name: Fetch EN content from Perplexity
        env:
          PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
          LANG: en
          OUTPUT_FILE: /tmp/perplexity-en.md
        run: node scripts/fetch-perplexity.js

      - name: Parse EN content
        env:
          CONTENT_FILE: /tmp/perplexity-en.md
          LANG: en
        run: node scripts/parse-content.js

      - name: Commit and push
        run: |
          git config user.name "tech-review-bot"
          git config user.email "bot@tech-review.local"
          git add _posts/ko/ _posts/en/
          if git diff --cached --quiet; then
            echo "변경사항 없음"
          else
            git commit -m "[tech-review] ${POST_DATE} daily post 자동 생성"
            git push
          fi
```

---

## Task 3: parse-content.js 단순화

**파일:** `scripts/parse-content.js`

현재: TOPIC_START/END 파싱 후 재조합 → 복잡하고 프롬프트 형식에 의존적
목표: 콘텐츠를 그대로 통과시키고 front matter + Comments만 추가

**핵심 변경:** `main()` 함수에서 content를 그대로 사용.

```js
async function main() {
  let raw;
  if (CONTENT_FILE) {
    raw = fs.readFileSync(CONTENT_FILE, "utf8");
  } else {
    raw = await fetchGist(GIST_ID);
  }

  if (!raw || raw.trim().length === 0) {
    console.error("콘텐츠가 비어 있습니다.");
    process.exit(1);
  }

  const date = POST_DATE;
  const [y, m, d] = date.split("-");
  const permalink = `/${LANG}/${y}/${m}/${d}/daily-tech-review/`;

  const frontMatter = [
    "---",
    `layout: post`,
    `title: "${date} Daily Tech Review"`,
    `date: ${date}`,
    `lang: ${LANG}`,
    `permalink: ${permalink}`,
    `pair: ${date}-daily-tech-review`,
    `tags: [tech-review]`,
    "---"
  ].join("\n");

  const post = `${frontMatter}\n\n${raw.trim()}\n\n## Comments\n\n`;

  const dir = path.join("_posts", LANG);
  fs.mkdirSync(dir, { recursive: true });
  const filepath = path.join(dir, `${date}-daily-tech-review.md`);
  fs.writeFileSync(filepath, post, "utf8");
  console.log(`포스트 저장: ${filepath}`);

  const out = process.env.GITHUB_OUTPUT;
  if (out) fs.appendFileSync(out, `post_path=${filepath}\npost_date=${date}\npost_lang=${LANG}\n`);
}
```

---

## Task 4: Perplexity 프롬프트 업데이트 (14개 파일)

**대상:** `perplexity-prompts/ko/*.md` (7개), `perplexity-prompts/en/*.md` (7개)

현재 프롬프트 문제:
- "Claude 실행 지침" 섹션 출력 요구 → 불필요, 파싱 오염
- 번호/기호 위주 구조 → Jekyll 마크다운 헤딩 구조와 불일치

**KO 프롬프트 새 형식 (모든 요일 공통 구조):**

```markdown
# [테마] 글로벌 기술·AI 주요 동향

당신은 글로벌 기술·AI 동향 전문 리서처입니다.
오늘 기준 최근 7일간의 [테마] 중심 글로벌 핵심 기술·AI 동향을 아래 마크다운 형식으로 정확히 출력하세요.
실제 검증된 뉴스·공식 발표만 포함하세요. 미검증 내용은 [미검증]으로 표시하세요.

---

반드시 아래 구조를 그대로 사용하세요. 섹션 제목을 바꾸지 마세요:

## 오늘의 핵심 요약

이번 주 가장 중요한 트렌드 3-4개를 서술형 단락으로 요약. (3-5문장)

## 주요 발표 & 제품

### [제품/발표 제목]
서술형으로 무엇인지, 왜 중요한지, 어떻게 작동하는지 설명. (3-5문장)

### [제품/발표 제목 2]
...

(2-4개 항목)

## 기업 전략 & 파트너십

### [기업/이벤트 제목]
서술형 설명. (2-4문장)

(2-3개 항목)

## 트렌드 & 인사이트

### [트렌드 제목]
서술형 분석. (3-4문장)

(2-3개 항목)

## Source

- [제목](URL)
- [제목](URL)
(각 항목 당 1-2개 출처, 총 5-10개)
```

**EN 프롬프트 새 형식 (구조 동일, 영어):**

```markdown
# [Theme] Global Tech & AI Daily Digest

You are an expert researcher on global tech and AI trends.
Output today's key global tech and AI developments (past 7 days, [theme] focus) in the exact markdown format below.
Include only verified news and official announcements. Mark unverified content as [unverified].

---

Use exactly this structure. Do not change section titles:

## Today's Key Summary

Summarize the 3-4 most important trends of the week in narrative paragraphs. (3-5 sentences)

## Major Announcements & Products

### [Product/Announcement Title]
Narrative description: what it is, why it matters, how it works. (3-5 sentences)

### [Title 2]
...

(2-4 items)

## Business Strategy & Partnerships

### [Company/Event Title]
Narrative description. (2-4 sentences)

(2-3 items)

## Trends & Insights

### [Trend Title]
Narrative analysis. (3-4 sentences)

(2-3 items)

## Source

- [Title](URL)
(1-2 sources per item, 5-10 total)
```

**요일별 테마 (KO):**
- 월 (01): AI·ML 혁신, 모델·에이전트·기술 발표 중심
- 화 (02): 빅테크 전략, 파트너십·투자·플랫폼 중심
- 수 (03): 스타트업·펀딩, 신흥 기업·VC 동향 중심
- 목 (04): 오픈소스·개발툴, 커뮤니티·생태계 중심
- 금 (05): 하드웨어·인프라, 칩·데이터센터·엣지 중심
- 토 (06): 실사용 사례·산업 적용, 기업 도입·ROI 중심
- 일 (07): 주간 종합·트렌드 전망, 한 주 요약·다음 주 예상 중심

**Step 1:** Python으로 14개 파일 일괄 업데이트

---

## Task 5: 검증

**Step 1: workflow 수동 실행**
GitHub Actions → Create Daily Post → Run workflow

**Step 2: feed.json 확인**
```
curl https://paulseongminpark.github.io/tech-review/feed.json | python3 -m json.tool
```

**Step 3: 포트폴리오 로컬 확인**
```
cd C:\dev\01_projects\02_portfolio
npm run dev
```
포트폴리오에서 Tech Review 섹션 카드 4개 표시 확인

---

## 자동화 흐름 요약

```
매일 09:00 KST
    ↓
GitHub Actions (create-post.yml)
    ↓
fetch-perplexity.js × 2 (KO + EN)
    → Perplexity sonar-pro API 호출
    → 요일별 프롬프트 사용
    ↓
parse-content.js × 2
    → front matter + permalink + ## Comments 추가
    → _posts/ko/YYYY-MM-DD-daily-tech-review.md
    → _posts/en/YYYY-MM-DD-daily-tech-review.md
    ↓
git commit + push
    ↓
deploy.yml (자동 트리거)
    → Jekyll 빌드 + feed.json 생성
    ↓
paulseongminpark.github.io/tech-review  ← 포스트 게시
paulseongminpark.github.io/tech-review/feed.json  ← 포트폴리오용

사용자가 모바일에서 comments 추가 시:
    tech-review-comments 레포 comments.md 편집 + push
    → (미구현, 추후 Task)
```

## GitHub Secrets 필요 항목

| Secret | 용도 | 상태 |
|--------|------|------|
| `PERPLEXITY_API_KEY` | Perplexity sonar-pro API | 설정 필요 |
| `GITHUB_TOKEN` | 자동 커밋 push | 자동 제공 |
