# Tech Review Pipeline Specification v3

> Updated: 2026-03-31 | SoT: 이 문서가 파이프라인 구조의 단일 진실

## 시스템 개요

```
Windows Task Scheduler (05:03 KST)
  └─ TechReview-MasterPipeline
       └─ run-all-pipelines.py
            ├─ [1] run-daily-v3.py     (Daily Post)
            ├─ [2] analyze-youtube-v3.py (YouTube)
            └─ [3] run-twitter-pipeline.py (Twitter)
       → deploy.yml → GitHub Pages
       → feed.json → Portfolio TechReviewCards
```

**비용**: $0/월 (전부 무료 API/구독 내)

---

## 1. Daily Post (`run-daily-v3.py`)

### 흐름

```
[Step 1] 소스 수집 (RSS/Reddit/HN/arXiv → 100~150건)
[Step 2] 규칙 기반 선별 (교차 출현+도메인+키워드 → 상위 10건)
[Step 3] 본문 추출 (curl, 4000자 캡)
[Step 4] Claude Sonnet 가공 (Smart Brevity + WIM)
[Step 5] 후처리 (날짜/tags/백틱 강제 교정)
[Step 6] extract-sections.js → _data/sections/ 생성
[Step 7] 검증 → git commit → push
```

### 모델 배정

| 단계 | 모델 | 용도 | 비용 |
|---|---|---|---|
| Step 4 | Claude Sonnet 4.6 (`claude -p`) | 10건 → 3건 선별 + Smart Brevity 작성 | Pro 구독 내 |

### 요일별 소스 (COMMON + DAY_SOURCES)

**공통 (매일)**:
- HN API (`hacker-news.firebaseio.com`)
- TechCrunch RSS
- Lobsters JSON

**요일별**:

| 요일 | 주제 | 추가 소스 |
|---|---|---|
| 월 | AI/ML | arXiv cs.AI, arXiv cs.CL, r/MachineLearning, r/LocalLLaMA, r/ClaudeAI, OpenAI Blog, HuggingFace Blog, DeepMind Blog, VentureBeat |
| 화 | BigTech | The Verge, Ars Technica, r/technology |
| 수 | Startup | Product Hunt, r/startups |
| 목 | OpenSource | r/programming, r/SelfHosted, The New Stack, InfoQ, Dev.to, GitHub Blog |
| 금 | Hardware | Ars Technica, The Verge, VentureBeat |
| 토 | UseCase | MIT Tech Review, VentureBeat, r/artificial, r/Futurology |
| 일 | Weekly | 월~토 전체 합산 |

### Claude Sonnet 프롬프트 (Step 4 — 전문)

```
너는 tech-review 블로그의 Daily Post 작성자다. 한국어로 작성한다.

오늘은 {요일}요일이다. 주제: {DAY_TOPIC}.

## 입력
아래 JSON은 오늘 수집한 테크 뉴스 상위 10건이다.
각 항목에 title, url, body(기사 본문 일부)가 있다.

```json
{selected JSON, 15000자 캡}
```

## 작성자(Paul)의 프로젝트 컨텍스트 (Why it matters 작성용 — 독자에게 노출 금지)
멀티AI 조율 시스템, 외부 메모리 지식그래프(4685+ 노드), 자동 뉴스 수집 파이프라인,
Next.js 포트폴리오, 컨텍스트 엔지니어링 전략. 개인 지식그래프 기반 AI 시스템을 운영하는 개발자.
주의: Why it matters에서 내부 프로젝트명(orchestration, mcp-memory 등)을 직접 쓰지 마라.
"멀티AI 조율 시스템", "지식그래프 기반 메모리", "자동화 파이프라인" 등
독자가 이해할 수 있는 일반 표현으로 풀어 써라.

## 작업
1. 10건 중 가장 중요한 3건을 선택 ({DAY_TOPIC} 주제 우선)
2. 각 3건에 대해 Smart Brevity 형식으로 작성

## 출력 형식 (정확히 지켜라)
---
layout: post
title: "3건 제목 나열"
date: {POST_DATE}
lang: ko
permalink: /ko/{YYYY/MM/DD}/daily-tech-review/
pair: {POST_DATE}-daily-tech-review
tags: [{요일별 태그}]
source_type: free-sources
---

## Today in One Line
한 문장 요약

---

## 1. 제목
본문 설명 (최소 3문장, body의 구체적 팩트/수치/인용)
**Why it matters:** 위 Paul 프로젝트 컨텍스트를 참고해 구체적으로 연결. 일반론 금지.
- 불릿 1 (body에서 추출)
- 불릿 2
- 불릿 3
**What's next:** 전망 1-2문장
**Source:** [제목](URL)

---
(2, 3도 동일)

## Comments

## 규칙
- body의 실제 내용만 사용. 없는 팩트 지어내기 금지.
- 인라인 코드 백틱 사용 금지. 기술 용어도 일반 텍스트.
- ~다 체.
- front matter는 위 형식 그대로. 수정하지 마라.
- 마크다운 파일 전체를 출력. 설명/부연 없이 파일 내용만.
```

### 검증 기준 (Step 6)

| 항목 | 기준 |
|---|---|
| 파일 존재 | `_posts/ko/{date}-daily-tech-review.md` |
| 최소 분량 | 500자 이상 |
| Today in One Line | 존재 |
| Why it matters | 각 항목에 존재 |
| Source URL | 각 항목에 존재 |
| 날짜 일치 | frontmatter date = POST_DATE |

---

## 2. YouTube (`analyze-youtube-v3.py`)

### 흐름

```
[Step 1] 신규 영상 감지 (yt-dlp --flat-playlist, 5개 플레이리스트)
[Step 2] Transcript 추출 (yt-dlp 자막 1차 → Groq Whisper 2차)
[Step 3] 구조화 (Codex CLI gpt-5.4)
[Step 4] Apply Points (Claude Sonnet + mcp-memory recall)
[Step 5] 번역 (OpenAI gpt-4.1-mini API)
[Step 6] Quote 검증 + 저장
[Step 7] git commit → push
```

### 모델 배정

| 단계 | 모델 | 용도 | 비용 |
|---|---|---|---|
| Step 2 fallback | Groq Whisper | 음성→텍스트 (자막 없을 때) | 무료 |
| Step 3 | Codex CLI gpt-5.4 | transcript → Smart Brevity 구조화 JSON | Plus 구독 내 |
| Step 4 | Claude Sonnet 4.6 (`claude -p`) | 5W1H apply_points + mcp-memory recall | Pro 구독 내 |
| Step 5 | OpenAI gpt-4.1-mini API | 영어→한국어 번역 | 무료 토큰 (소형 2.5M/일) |

### 플레이리스트

| 이름 | ID |
|---|---|
| claude | PLUeFkXBkSX_bxzWza71Mdb7JlOOg5xDDS |
| build | PLUeFkXBkSX_Znh-9HE9iIEzq23h3Y2eBw |
| design | PLUeFkXBkSX_aH1TmJ1iOolxwkJsP6DwXf |
| insight | PLUeFkXBkSX_bhASv37IvjLnXfCVwqQT8h |
| ontology | PLUeFkXBkSX_ZFCfP8j0peOCeOlKVhwfFx |

### Codex CLI 구조화 프롬프트 (Step 3)

`config/structuring-prompt.md` 참조 — Smart Brevity 방법론 기반:

- **core_4**: Muscular Tease, Single Lede, Why It Matters, Go Deeper
- **12 Axiom 레이블**: Why it matters (필수) + 11개 선택
- 자막 → 주제별 재구성 (발화 순서 아님)
- sections 최소 6개, body 최소 5문장
- highlights는 body에서 복사, quote는 자막 원문 그대로

**출력 JSON 구조**:
```json
{
  "sections": [
    {
      "heading": "Muscular Tease 헤드라인",
      "body": "최소 5문장 Go Deeper",
      "highlights": ["body에서 복사"],
      "quote": "자막 원문 그대로"
    }
  ],
  "key_takeaways": ["5개"],
  "tech_stack": ["실제 언급된 기술만"],
  "smart_brevity": {
    "why": "WIM 1-2문장",
    "what": "Single Lede + 핵심 주장",
    "axioms": [{"label": "...", "content": "..."}]
  }
}
```

### Claude Sonnet AP 프롬프트 (Step 4)

```
mcp-memory에서 recall('Paul 프로젝트 시스템')로 현재 상태를 조회해라.

아래 YouTube 영상 분석 결과를 보고, Paul의 프로젝트에 적용할 수 있는
포인트를 1개만 5W1H 형식으로 작성해라.

영상 분석:
{title, key_takeaways, tech_stack, sections headings — compact JSON}

출력 형식 (순수 JSON만, 설명 없이):
{
  "level": 1,
  "where": "대상 프로젝트/시스템",
  "what": "구체적 액션",
  "why": "근거",
  "how": "실행 방법",
  "when": "시점"
}

규칙:
- Level 1(시스템 액션): 5필드 전부. 즉시 적용.
- Level 2(설계 참고): where/what/why만. 당장 아님.
- Level 3(사고 자극): what/why만.
- 가장 높은 레벨 우선. 억지 L1 금지.
- 1개만.
```

### 번역 프롬프트 (Step 5)

```
system: Translate English to natural Korean. Keep proper nouns/tech terms
        in English. Output only translated text.
user:   {transcript}
```

### 검증 기준

| 항목 | 기준 |
|---|---|
| 파일 존재 | `_data/sources/youtube-{date}.json` |
| sections | 6개 이상 |
| key_takeaways | 5개 |
| transcript | 500자 이상 |
| apply_points | 존재 (없으면 경고, 치명적 아님) |

---

## 3. Twitter (`run-twitter-pipeline.py`)

### 흐름

```
[Step 1] CDP Chrome 연결 확인 (미실행 시 자동 시작)
[Step 2] 북마크 수집 (fetch-twitter-pw.py → inbox/)
[Step 3] 분석 (add-bookmark.py → OpenAI gpt-4.1-mini 구조화 + Claude CLI WIM)
[Step 4] sources.json 갱신 (build-sources-feed.js)
[Step 5] git commit → push
```

### 모델 배정

| 단계 | 모델 | 용도 | 비용 |
|---|---|---|---|
| Step 3-A | OpenAI gpt-4.1-mini API | 트윗 구조화 (whats_happening, translation, tech_stack) | 무료 토큰 |
| Step 3-B | Claude CLI (`claude -p`) | Why It Matters 생성 (7-Lens wim-prompt.md) | Pro 구독 내 |

### 구조화 프롬프트 (Step 3-A — OpenAI)

```
다음 트위터 게시글을 아래 JSON 형식으로 처리해라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

주의: why_it_matters 필드는 생성하지 마라. Why It Matters는 별도 단계에서 처리된다.

{
  "whats_happening": "무슨 일인가 — 1-2문장, 핵심 사건·발표·발견을 구체적으로",
  "translation": "원문을 거의 그대로 한글로 번역. 요약 금지.",
  "tech_stack": ["언급된 실제 기술/도구/라이브러리명만"],
  "apply_points": ["적용 가능한 포인트. 한 문장으로 간결하게."]
}

규칙:
- whats_happening: 1-2문장. 사건 중심.
- translation: 원문 길이의 90% 이상 유지. 영어 고유명사 유지.
- tech_stack: 없으면 []
- apply_points: 최대 3개. 50자 이내.
- 전부 한국어. 고유명사는 영어 유지.
```

### WIM 프롬프트 (Step 3-B — Claude CLI)

`config/wim-prompt.md` 참조:

- **독자 프로필**: Paul의 사고방식, 프로젝트, 관심사 상세 기술
- **7가지 렌즈**: 시스템 임팩트, 이색적 접합, 외부화 진전, 조건 설계, 빼기의 관점, 수렴/분기, 메타인지
- **Smart Brevity**: 1-2문장 선언적 판단 + 해당 axiom 레이블
- **금지**: "이 영상은~" 시작, 추상적 일반론, 이모지, 렌즈 번호 직접 언급

### 검증 기준

| 항목 | 기준 |
|---|---|
| bookmarks.json | 파일 존재 + JSON 유효 |
| 신규 북마크 | why_it_matters ≠ 에러 메시지 |
| sources.json | 파일 존재 + twitter 항목 포함 |
| category | 비어있지 않음 |

---

## 공통 인프라

### Task Scheduler

| 태스크 | 상태 | 설명 |
|---|---|---|
| TechReview-MasterPipeline | **Ready** | 05:03 KST, 3개 순차 실행 |
| TechReview-DailyV3 | Disabled | (MasterPipeline이 대체) |
| TechReview-YoutubeV3 | Disabled | (MasterPipeline이 대체) |
| TechReview-Twitter | Disabled | (MasterPipeline이 대체) |

**설정**: WakeToRun=True, StartWhenAvailable=True, LogonType=Interactive, 3시간 제한

### Git 전략

모든 파이프라인은 commit → pull --rebase → push 순서:
1. 변경 파일 `git add`
2. `git commit -m "[auto] ..."`
3. `git pull --rebase origin master`
4. `git push` (실패 시 pull + 재시도 1회)

### 로그

| 파이프라인 | 로그 위치 |
|---|---|
| Master | `scripts/_logs/master-{date}.log` |
| Daily | `scripts/_logs/daily-v3-{date}.log` |
| YouTube | `scripts/_logs/youtube-v3-{date}.log` |
| Twitter | `_tmp/twitter-pipeline-{date}.log` |
| 실패 알림 | `_tmp/alert-{date}.txt` |

### 환경 변수

| 변수 | 출처 | 용도 |
|---|---|---|
| GROQ_API_KEY | blog/.env | Whisper fallback |
| GEMINI_API_KEY | blog/.env | (미사용, 레거시) |
| ANTHROPIC_API_KEY | blog/.env | (미사용, 만료 — Claude CLI는 OAuth) |
| OPENAI_API_KEY | mcp-memory/.env | gpt-4.1-mini 번역/분석 |
