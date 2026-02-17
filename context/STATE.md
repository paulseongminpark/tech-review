# Tech Review - Project State

**Last Updated**: 2026-02-18
**Status**: Phase 1 디자인 완료, 구현 대기

---

## Current State

### Phase 1: Jekyll 블로그 ✅
- 레포: https://github.com/paulseongminpark/tech-review
- 배포: https://paulseongminpark.github.io/tech-review/
- 샘플 포스트: 1개 (단일 주제, 간단)

### Phase 2: Daily Digest 디자인 ✅
- 디자인: `docs/plans/2026-02-18-daily-digest-design.md`
- 구현 계획: `docs/plans/2026-02-18-daily-digest-impl.md`
- 형식: Daily Digest (하루 10-15개 뉴스)
- 구조: 3-섹션 (주요 발표, 기업 전략, 트렌드)
- Comments: Claude API 자동 생성 (~$0.03/월)

### Phase 3: 구현 대기 ⏱
- Task 1-2: 샘플 Daily Digest (KO/EN)
- Task 3-4: Claude API 스크립트 + 테스트
- Task 5: Git commit
- Task 6: Perplexity 프롬프트 업데이트

---

## Architecture

```
Perplexity 리서치 (KO 3개 + EN 3개)
  ↓
Daily Digest 포스트 생성
  ↓
Comments 자동 생성 (Claude API)
  ↓
Jekyll 블로그 게시
  ↓
Portfolio 연동 (feed.json)
```

---

## Key Decisions

| 항목 | 결정 |
|------|------|
| 포스트 형식 | Daily Digest |
| 파일명 | `YYYY-MM-DD-daily-digest.md` |
| 섹션 구조 | 3-섹션 |
| 내용 밀도 | 각 뉴스 3-5줄 |
| 뉴스 개수 | 10-15개 |
| 다국어 | Perplexity KO/EN 각각 요청 |
| Comments | Claude API (Haiku) |
| 자동화 | Phase 1 → Phase 2 → Phase 3 |

---

## Next Steps

1. **새 세션 시작**: `cd /c/dev/tech-review`
2. **executing-plans 스킬**: 구현 계획 실행
3. **Perplexity 리서치**: 새 세션에 다시 제공
4. **API 키 설정**: `.env` 파일 생성

---

## Files

```
tech-review/
├── _posts/
│   ├── ko/2026-02-17-ai-agent-trends.md  (샘플, 단일 주제)
│   └── en/2026-02-17-ai-agent-trends.md  (샘플, 단일 주제)
├── docs/plans/
│   ├── 2026-02-18-daily-digest-design.md
│   └── 2026-02-18-daily-digest-impl.md
└── context/
    └── STATE.md  (this file)
```

---

## References

- 기존 디자인: `docs/plans/2026-02-17-tech-review-design.md` (Portfolio)
- 기존 구현: `docs/plans/2026-02-17-tech-review-impl.md` (Portfolio)
- Perplexity 리서치: 2026-02-17 (3개, 사용자 제공)
