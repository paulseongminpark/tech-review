# Multi-Source Pipeline Design
_Date: 2026-03-04_

## 개요

Perplexity 외 3개 소스(Twitter, Threads, YouTube)를 추가하고,
기존 topics 페이지를 Daily Digest로 전면 재설계한다.

---

## 1. 데이터 파이프라인

### 파일 구조

```
blog/
  scripts/
    fetch-twitter.js        ← Playwright 로그인 → following 피드 스크래핑
    fetch-threads.js        ← Playwright 로그인 → following 피드 스크래핑
    fetch-youtube.js        ← YouTube Data API → 신규 영상 추출
    summarize-youtube.js    ← yt-dlp transcript → Gemini Smart Brevity 요약
    export-cookies.js       ← 로컬: 브라우저 쿠키 추출 → GitHub Secret 갱신용
  _data/
    sources/
      twitter-YYYY-MM-DD.json
      threads-YYYY-MM-DD.json
      youtube-YYYY-MM-DD.json
  config/
    youtube-sources.json    ← 플레이리스트 ID 목록 (수동 관리)
    youtube-processed.json  ← 처리 완료된 video ID (중복 방지)
```

### Twitter / Threads JSON 스키마

```json
[{
  "source_type": "twitter",
  "author": "@username",
  "text": "트윗 원문",
  "url": "https://x.com/...",
  "timestamp": "2026-03-04T06:30:00Z",
  "is_thread": true,
  "has_external_link": false
}]
```

### YouTube JSON 스키마

```json
[{
  "source_type": "youtube",
  "title": "영상 제목",
  "channel": "채널명",
  "url": "https://youtube.com/watch?v=...",
  "video_id": "abc123",
  "playlist": "플레이리스트명",
  "published_at": "2026-03-04T00:00:00Z",
  "summary": {
    "one_line": "한 문장 요약",
    "why_it_matters": "핵심 의미",
    "points": ["포인트 1", "포인트 2", "포인트 3"],
    "whats_next": "다음 전망"
  }
}]
```

### 필터 기준

| 소스 | 필터 |
|------|------|
| Twitter | 텍스트 280자+ OR 스레드(1/N 포함) OR 외부링크 포함 |
| Threads | 텍스트 100자+ (단순 반응 제외) |
| YouTube | 플레이리스트 내 미처리 신규 영상 (youtube-processed.json 기준) |

### YouTube 처리 흐름

```
youtube-sources.json 읽기
  → YouTube Data API: 플레이리스트 영상 목록
  → youtube-processed.json와 비교 → 신규 ID만 추출
  → yt-dlp: transcript 추출
  → Gemini AI Studio: Smart Brevity 요약
  → youtube-YYYY-MM-DD.json 저장
  → youtube-processed.json에 ID 추가
```

---

## 2. GitHub Actions 워크플로우

### 워크플로우 구조 (3개 독립)

```
.github/workflows/
  fetch-twitter.yml    ← cron 매일, Playwright + TWITTER_COOKIES
  fetch-threads.yml    ← cron 매일, Playwright + THREADS_COOKIES
  fetch-youtube.yml    ← cron 매일, YouTube API + Gemini API
```

각 워크플로우가 독립 실행 → 한 소스 실패해도 나머지 영향 없음.

### GitHub Secrets

| Secret | 용도 |
|--------|------|
| `TWITTER_COOKIES` | Playwright 세션 쿠키 JSON |
| `THREADS_COOKIES` | Playwright 세션 쿠키 JSON |
| `YOUTUBE_API_KEY` | YouTube Data API v3 키 |
| `GEMINI_API_KEY` | Gemini AI Studio 요약용 |

### 쿠키 관리 전략

- 로컬에서 `scripts/export-cookies.js` 실행 → 쿠키 JSON 출력
- GitHub Secret 수동 업데이트
- 세션 만료 주기: 보통 30~90일
- 만료 감지: workflow 실패 시 GitHub Actions 이메일 알림으로 확인

---

## 3. UI 구조

### 네비게이션

```
[Home] [Daily Digest] [Twitter] [Threads] [YouTube]
```

기존 `[Topics]` 탭 → `[Daily Digest]` 로 대체.

### Daily Digest 페이지 (기존 topics 전면 재설계)

```
┌──────────────┬──────────────────────────────────────┐
│ 날짜 목록    │ [All] [AI] [GPU] [Apple] ...  ← 태그 토글 │
│              │ ─────────────────────────────────────│
│ 2026-03-04   │ ┌────────┐ ┌────────┐ ┌────────┐    │
│ 2026-03-03   │ │        │ │        │ │        │    │
│ 2026-03-02   │ │  #AI   │ │  #GPU  │ │ #Apple │    │
│   ...        │ │  (12)  │ │  (8)   │ │  (5)   │    │
│              │ └────────┘ └────────┘ └────────┘    │
└──────────────┴──────────────────────────────────────┘
```

- **왼쪽 패널**: 날짜 목록 — 클릭 시 오른쪽 해당 날짜 카드로 필터
- **오른쪽 상단**: 태그 토글 버튼 — 클릭 시 해당 태그 카드만 표시
- **카드**: 태그 1개 단위, 해당 태그 섹션 수 표시, 클릭 시 섹션 목록 표시

페이지: `ko/daily-digest.html` + `en/daily-digest.html`
기존 `ko/topics.html` + `en/topics.html` 대체.

### Twitter / Threads 페이지

- 카드 리스트 (날짜 역순)
- 원본 텍스트, 작성자, 타임스탬프, 외부링크 표시

### YouTube 페이지

- 카드 리스트 (날짜 역순)
- Smart Brevity 요약 + 영상 링크

---

## 4. 구현 순서

1. YouTube 파이프라인 (API 기반, 가장 안정적)
2. Daily Digest UI 재설계
3. Twitter 파이프라인 (Playwright)
4. Threads 파이프라인 (Playwright)
