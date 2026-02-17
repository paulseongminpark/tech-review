# Tech Review Daily Digest - Design Document

**Date**: 2026-02-18
**Status**: Approved
**Goal**: Perplexity 리서치를 Daily Digest 형식으로 변환하여 Jekyll 블로그에 게시

---

## 프로젝트 개요

### 문제점
- 현재 샘플 포스트: 단일 주제, 매우 간단 (각 섹션 1-2줄)
- Perplexity 리서치: 10-20개 주제, 매우 상세 (수천 단어)
- **격차**: 내용이 너무 적어서 Perplexity 리서치 가치를 활용하지 못함

### 해결책
- **Daily Digest 형식**: 하나의 포스트에 10-15개 핵심 뉴스
- **3-섹션 구조**: 주요 발표 & 제품, 기업 전략 & 파트너십, 트렌드 & 인사이트
- **적절한 밀도**: 각 뉴스당 3-5줄

---

## 핵심 결정사항

| 항목 | 결정 |
|------|------|
| **포스트 형식** | Daily Digest (하루에 하나) |
| **파일명** | `YYYY-MM-DD-daily-digest.md` |
| **섹션 구조** | 3-섹션 (주요 발표, 기업 전략, 트렌드) |
| **내용 밀도** | 각 뉴스당 3-5줄 |
| **뉴스 개수** | 10-15개 핵심 뉴스 |
| **다국어** | Perplexity에 KO/EN 각각 요청 |
| **Comments** | Claude API (Haiku) 자동 생성 (~$0.03/월) |
| **자동화** | 단계적 (Phase 1 → Phase 2 → Phase 3) |

---

## 시스템 흐름

```
Perplexity 리서치 (KO 3개 + EN 3개, 매일 8AM)
  ↓
수동/자동 파싱 (Perplexity → Markdown)
  ↓
Daily Tech Digest 포스트 생성
  - 파일: _posts/ko/YYYY-MM-DD-daily-digest.md
  - 파일: _posts/en/YYYY-MM-DD-daily-digest.md
  ↓
Comments 섹션 자동 생성 (Claude API)
  ↓
Jekyll 블로그 게시 (GitHub Pages)
  ↓
Portfolio 연동 (feed.json → TechReviewCards)
```

---

## 포스트 구조

### Front Matter

```yaml
---
layout: post
title: "Daily Tech Digest - Feb 18, 2026"  # EN
title: "데일리 테크 다이제스트 - 2월 18일"    # KO
date: 2026-02-18
lang: ko  # or en
pair: 2026-02-18-daily-digest
tags: [ai, tech, digest]
---
```

### 본문 템플릿

```markdown
## 오늘의 핵심 요약
[전체 요약 3-5줄]
- 핵심 축 1
- 핵심 축 2
- 핵심 축 3

## 주요 발표 & 제품

### [제품/서비스명]
[1줄] 핵심 발표/제품이 무엇인지
[2-3줄] 주요 기능/특징/의미
[1줄] 왜 중요한지 (So What?)

[... 4-6개 뉴스 ...]

## 기업 전략 & 파트너십

### [회사명 - 전략/파트너십]
[3-5줄 설명]

[... 3-4개 뉴스 ...]

## 트렌드 & 인사이트

### [트렌드명]
[3-5줄 설명]

[... 3-4개 뉴스 ...]

## Source
- [제목](URL)
- [제목](URL)
[... 모든 소스 URL ...]

## Comments
[Claude API 자동 생성]
- **산업 연관성**: [1-2문장]
- **직무 연관성**: [1-2문장]
- **자소서·면접**: [1-2문장]
```

---

## 내용 변환 전략

### 1. 콘텐츠 선별 기준 (우선순위)

```
높음  ✓ 실제 출시물 (모델, 제품, 플랫폼)
      ✓ 주요 파트너십/투자 (금액, 전략적 의미)
      ✓ 판도 변화 (가격 혁신, 새로운 패러다임)

중간  ○ 기업 전략 변화 (수익모델, 시장 진입)
      ○ 기술 트렌드 (에이전트, Edge AI, 거버넌스)

낮음  △ 일반 분석/예측 (시장 리포트, 컨퍼런스 발표)
      △ 반복 내용 (이미 알려진 뉴스)
```

### 2. 중복 제거 규칙

Perplexity 리서치 3개가 같은 뉴스를 다룰 경우:
- **가장 상세한 버전** 1개만 선택
- 나머지는 추가 정보만 통합

### 3. 3-5줄 요약 템플릿

```
[1줄] 핵심 발표/제품이 무엇인지
[2-3줄] 주요 기능/특징/의미
[1줄] 왜 중요한지 (So What?)
```

### 4. 섹션 배분 목표

- **주요 발표 & 제품**: 4-6개 뉴스
- **기업 전략 & 파트너십**: 3-4개 뉴스
- **트렌드 & 인사이트**: 3-4개 뉴스
- **총 10-15개** 핵심 뉴스

---

## Comments 자동 생성

### 방식
- **API**: Claude API (Haiku)
- **입력**: Daily Digest 전체 (~2,000 토큰)
- **출력**: Comments 3줄 (~200 토큰)
- **비용**: ~$0.001 per post → **~$0.03/월**

### 구조
```markdown
## Comments
- **산업 연관성**: [전체 흐름에 대한 인사이트]
- **직무 연관성**: [실무 관련성]
- **자소서·면접**: [면접 대비 포인트]
```

### 자동화 시점
GitHub Actions에서:
1. Perplexity 리서치 파싱
2. Daily Digest 생성
3. **Comments 자동 생성** (Claude API 호출)
4. 최종 포스트 커밋

---

## 다국어 & 자동화

### 다국어 처리

**방식**: Perplexity 프롬프트에 명시

```
"이번 주의 가장 중요한 기술 개발 분석...

**언어**: 한국어와 영어 각각 별도 응답 제공
- 첫 번째 응답: 한국어
- 두 번째 응답: 영어 (번역 아닌 원어 작성)
```

**결과**:
- Perplexity 리서치 6개 (KO 3개 + EN 3개)
- 번역 API 불필요
- 더 나은 품질

### 자동화 로드맵

**Phase 1** (현재): 수동 + API
- Perplexity 리서치 수동 복사
- Daily Digest 수동 작성
- Comments 자동 생성 (Claude API)
- Git commit + push 수동

**Phase 2** (단기): 반자동
- Perplexity 이메일 → 자동 파싱 (Google Apps Script)
- Daily Digest 자동 생성 (Claude API)
- Comments 자동 생성
- Git 자동 커밋 (GitHub Actions)

**Phase 3** (장기): 완전 자동
- E2E 자동화 + 오류 감지
- 수동 개입 최소화

---

## 기존 아키텍처와의 관계

### 변경 사항
| 항목 | 기존 | 변경 후 |
|------|------|---------|
| 파일명 | `YYYY-MM-DD-[topic].md` | `YYYY-MM-DD-daily-digest.md` |
| 포스트 형식 | 단일 주제 | Daily Digest (10-15개 뉴스) |
| 섹션 구조 | Industry/Who/What/When/Why/How/So? | 3-섹션 (주요 발표, 기업 전략, 트렌드) |
| 내용 밀도 | 각 섹션 1-2줄 | 각 뉴스 3-5줄 |

### 유지 사항
- Jekyll + GitHub Pages
- EN/KO 이중 언어
- feed.json → Portfolio 연동
- Comments 자동 생성

---

## Next Steps

1. **Perplexity 프롬프트 업데이트**
   - KO/EN 각각 요청 명시
   - Daily Digest 형식에 맞춘 출력 지시

2. **샘플 Daily Digest 작성** (Phase 1)
   - 제공받은 Perplexity 리서치 3개로 샘플 작성
   - KO/EN 각각 작성
   - Comments 수동 작성 (API 연동 전)

3. **Claude API 연동** (Phase 1)
   - API 키 발급
   - Comments 자동 생성 스크립트

4. **자동화 구현** (Phase 2)
   - Google Apps Script (이메일 파싱)
   - GitHub Actions (포스트 생성 + 커밋)

5. **E2E 테스트** (Phase 2)
   - 전체 파이프라인 검증
   - 오류 처리 로직 추가

6. **완전 자동화** (Phase 3)
   - 수동 개입 최소화
   - 모니터링 및 알림

---

## 산출물

- **디자인 문서**: `docs/plans/2026-02-18-daily-digest-design.md` (본 문서)
- **구현 계획**: TBD (writing-plans 스킬로 생성 예정)
- **샘플 포스트**: TBD (Phase 1에서 작성)

---

## 참고

- 기존 디자인: `docs/plans/2026-02-17-tech-review-design.md`
- 기존 구현 계획: `docs/plans/2026-02-17-tech-review-impl.md`
- Perplexity 리서치 3개: 사용자 제공 (2026-02-17)
