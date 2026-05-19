---
layout: post
title: "Karpathy, Anthropic 합류 선언 / LLM 6개월 레이스 총정리 / Gemini 3.5 Flash 공개"
date: 2026-05-20
lang: ko
permalink: /ko/2026/05/20/daily-tech-review/
pair: 2026-05-20-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line
Karpathy가 "I've joined Anthropic"이라는 한 줄을 올렸고, HN은 900점을 넘겼다. 같은 날 Simon Willison은 지난 6개월 LLM 레이스를 5분으로 압축해 PyCon 무대에 올렸고, Google은 Gemini 3.5 Flash를 공개했다. 인재, 속도, 플랫폼 — 오늘 세 개의 신호는 AI 스타트업 생태계의 다음 판이 어떻게 짜이고 있는지를 각각 다른 각도에서 보여준다.

---

## 1. Karpathy, Anthropic 합류 선언

Andrej Karpathy가 트위터에 "I've joined Anthropic"이라는 한 문장을 올렸다. Hacker News에서 이 트윗은 907점과 354개의 댓글을 기록했다. AI 분야에서 단일 트윗이 이 정도 반응을 끌어내는 경우는 거의 없다. Karpathy는 연구자이자 교육자로서 독보적인 존재감을 가진 인물이다. 수백만 명의 개발자가 그의 강의와 글을 통해 딥러닝을 처음 접했고, 그 무게가 지금 Anthropic 쪽으로 넘어갔다. 이것은 단순한 이직이 아니다. 커뮤니티 신뢰가 어느 회사를 향하고 있는지를 보여주는 사건이다.

**Why it matters:** Karpathy의 선택은 Anthropic이 연구 역량뿐 아니라 개발자 생태계 장악에도 본격적으로 진입하겠다는 신호로 읽힌다. 인재 유치 경쟁에서 AI 스타트업이 빅테크와 대등해졌다는 증거이기도 하고, 교육·커뮤니티 영향력이 모델 벤치마크만큼 중요한 자산이 된 시대의 반영이기도 하다. 장기적으로 이 한 건의 이동은 Claude 생태계 개발자 채택률에 직접 영향을 미칠 것이다.

- HN score 907, 댓글 354건 — 최근 AI 관련 단일 뉴스 중 최상위 반응
- Anthropic은 Claude 시리즈로 이미 코딩 에이전트 영역에서 선두를 달리고 있는 상황

**What's next:** Karpathy가 어떤 역할을 맡느냐에 따라 방향이 달라진다. 교육 인프라, 오픈소스 기여, 모델 해석가능성 중 어디에 집중하느냐가 향후 Anthropic의 포지셔닝을 결정할 것이다.

**Source:** [I've joined Anthropic](https://twitter.com/karpathy/status/2056753169888334312)

---

인재 이동이 업계 지형을 흔드는 동안, 지난 6개월간 LLM 레이스 자체는 얼마나 빠르게 돌아갔을까.

## 2. 지난 6개월 LLM 레이스, 5분 요약

Simon Willison이 PyCon US 2026 번개 발표에서 지난 6개월 LLM 동향을 5분에 압축했다. 그가 첫 번째로 꺼낸 키워드는 "November 2025 inflection point"였다. 11월 한 달 사이에 최강 모델 타이틀이 세 회사 사이에서 다섯 번 교체됐다. Claude Sonnet 4.5에서 GPT-5.1로, Gemini 3로, GPT-5.1 Codex Max로, 그리고 Claude Opus 4.5가 왕관을 되찾았다. Willison은 이 흐름을 "펠리컨이 자전거를 타는 그림 그리기" 테스트로 시각화했다. 어떤 모델이 가장 잘 그렸는지가 아니라, 최강 모델이 이 속도로 바뀐다는 사실 자체가 요점이다. 그리고 그는 11월의 진짜 뉴스는 순위 교체가 아니라 코딩 에이전트가 실제로 쓸 만해진 것이라고 짚었다. OpenAI와 Anthropic 모두 2025년 대부분을 코드 품질 향상을 위한 RLVR(Reinforcement Learning from Verifiable Rewards) 적용에 쏟았고, 그 성과가 11월에 동시에 터졌다.

**Why it matters:** 코딩 에이전트가 실제로 쓸 만해졌다는 11월의 변화는 AI 스타트업 비즈니스 모델을 근본적으로 흔들고 있다. "LLM 위에 앱을 쌓는다"는 레이어 전략이 통하던 시기가 끝나가고, 에이전트가 직접 개발 파이프라인에 진입하는 국면이다. Willison이 6개월을 5분으로 요약할 수 있었다는 사실 자체가, 이 레이스의 속도가 이미 인간의 처리 속도를 한참 초과하고 있다는 신호다.

- 최강 모델 교체 순서: Claude Sonnet 4.5 → GPT-5.1 → Gemini 3 → GPT-5.1 Codex Max → Claude Opus 4.5
- RLVR이 코딩 에이전트 급성장의 핵심 동인 — 2025년 한 해가 그 준비 기간이었다

**What's next:** Willison이 "Opus 4.5가 이후 몇 달간 왕관을 유지했다"고 표현했다. 그 몇 달이 이미 지나가고 있다. 다음 교체가 임박했을 가능성을 열어둬야 한다.

**Source:** [The last six months in LLMs in five minutes](https://simonwillison.net/2026/May/19/5-minute-llms/)

---

레이스의 다음 주자는 이미 출발선에 서 있었다.

## 3. Gemini 3.5 Flash, "행동하는 프런티어 인텔리전스"

Google DeepMind가 5월 19일 Gemini 3.5를 공개했다. 슬로건은 "frontier intelligence with action"이다. 기존 Gemini 시리즈가 이해와 생성에 집중했다면, 3.5는 행동 능력을 핵심으로 내세운다. 같은 날 Gemini Omni("create anything from anything"), Gemini Audio, Nano Banana 같은 특화 모델들도 함께 발표됐다. Google이 단일 범용 모델 전략에서 목적별 모델 군으로 이동하고 있다는 신호다. AI 스타트업 입장에서 이 발표의 의미는 새 벤치마크 숫자보다 플랫폼 전략에 있다. Gemini 3.5 Flash가 API로 접근 가능한 수준의 모델이라면, 도구 호출과 에이전트 체이닝의 기반이 또 한 번 업그레이드된다.

**Why it matters:** "action"을 슬로건에 올렸다는 것은 Google이 에이전트 경쟁에서 더 이상 후발주자임을 인정하지 않겠다는 선언이다. Willison이 정리한 11월 레이스에서 Gemini 3가 일시적으로 1위를 차지했던 전례가 있다. 3.5는 충분한 도전자다. 스타트업이 어떤 모델을 기반 인프라로 선택하느냐는 6개월 뒤 제품 경쟁력을 좌우하는 결정이 된다.

- 슬로건 "frontier intelligence with action" — 에이전트 실행 능력을 전면 강조
- 같은 날 Gemini Omni, Gemini Audio 등 특화 모델 군 동시 공개 — 포트폴리오 전략으로의 전환

**What's next:** Flash 버전의 실제 에이전트 성능과 API 접근성, 가격 정책이 공개되면 스타트업 채택 속도가 결정된다. 모델 선택은 이제 기술 결정이 아니라 생태계 베팅이다.

**Source:** [Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/)

## Comments
