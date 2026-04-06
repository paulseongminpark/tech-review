---
layout: post
title: "OpenAI Model Spec 공개 철학 / Anthropic-OpenClaw 구독 분리 / nanocode로 Claude Code 직접 훈련"
date: 2026-04-06
lang: ko
permalink: /ko/2026/04/06/daily-tech-review/
pair: 2026-04-06-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
source_type: free-sources
---

## Today in One Line
OpenAI는 모델 행동 설계 철학을 공개 문서로 정리했고, Anthropic은 서드파티 도구의 구독 공유를 차단했으며, 한 개발자는 $200짜리 TPU로 Claude Code를 처음부터 훈련하는 방법을 오픈소스로 풀었다.

---

## 1. OpenAI Model Spec: "이건 우리 모델이 이미 이렇게 행동한다는 주장이 아니다"

OpenAI가 Model Spec의 설계 철학과 운영 방식을 상세히 공개했다. Model Spec은 모델이 지시를 따르고, 충돌을 해결하고, 사용자의 자유를 존중하며, 광범위한 쿼리에서 안전하게 행동하는 방식을 정의하는 공식 프레임워크다. OpenAI는 이 문서가 "우리 모델이 이미 완벽하게 이렇게 행동한다는 주장이 아니다"라고 명확히 밝히며, 서술적이기도 하지만 동시에 훈련 목표로 삼는 기준점이라고 설명했다. 2024년 첫 버전 이후 사용자 선호와 필요를 학습하며 상당 폭 진화해왔다.

**Why it matters:** 멀티AI 시스템을 조율할 때 각 모델이 어떤 원칙으로 행동하는지를 이해하는 것은 에이전트 간 갈등 해결과 오케스트레이션 설계의 기반이 된다. Preparedness Framework가 프론티어 위험에 집중한다면, Model Spec은 그보다 훨씬 넓은 일상적 행동 기준을 다룬다. 자동화 파이프라인에서 Claude나 GPT를 혼용할 때 각 모델의 공개 행동 원칙을 참조 문서로 활용할 수 있다.

- Model Spec과 Preparedness Framework는 상호 보완적이며 서로 다른 질문을 다룬다
- 사용자·개발자·연구자·정책 입안자 모두가 읽고 검토하고 토론할 수 있는 형태로 공개된 것이 핵심
- "민주화된 AI 접근성"이 Model Spec 존재의 근본 이유라고 OpenAI는 설명했다

**What's next:** OpenAI는 식별된 갭을 추적하고 업데이트를 주도하는 과정도 공개했다. Model Spec을 기반으로 한 평가 기준이 외부 감사나 규제 논의에서 참조될 가능성이 높아질 것이다.

**Source:** [Inside our approach to the Model Spec](https://openai.com/index/our-approach-to-the-model-spec)

---

## 2. Anthropic, Claude Code 구독으로 OpenClaw 사용 차단 — "구독은 이런 사용 패턴을 위해 설계되지 않았다"

Anthropic이 4월 4일 정오(태평양 시간)부터 Claude 구독 한도를 OpenClaw 등 서드파티 하네스에 사용하는 것을 차단했다. 이후 별도 종량제(pay-as-you-go)로만 서드파티 도구에서 Claude를 사용할 수 있다. 이 정책은 OpenClaw에서 시작해 "모든 서드파티 하네스로 순차 확대"될 예정이다. Claude Code 책임자 Boris Cherny는 "구독은 이런 도구들의 사용 패턴을 위해 설계된 것이 아니다"라며 지속 가능한 성장 관리 차원이라고 설명했고, 환불도 제공하겠다고 밝혔다.

**Why it matters:** 자동화 파이프라인에 Claude API를 통합할 때 비용 구조가 직접 달라진다. 구독 요금제를 전제로 설계된 도구 체인이 있다면 종량제 전환에 따른 비용 재산정이 필요하다. 특히 배치 작업이나 지속적 에이전트 루프처럼 높은 토큰 소비 패턴을 가진 시스템은 영향을 더 크게 받는다.

- OpenClaw 창업자 Peter Steinberger는 이 발표 직전 경쟁사 OpenAI에 합류했으며, 타이밍이 맞아떨어진다고 공개적으로 비판했다
- Steinberger는 "먼저 인기 기능을 자체 도구에 복사하고, 그다음 오픈소스를 잠근다"고 말했다
- Cherny는 이를 "엔지니어링 제약 문제"라고 반박하며 OpenClaw의 프롬프트 캐시 효율 개선 PR을 직접 올렸다고 밝혔다

**What's next:** Anthropic이 어떤 서드파티 하네스를 다음으로 지정할지, 그리고 종량제 가격 구조가 구체적으로 어떻게 책정될지가 관건이다. 오픈소스 AI 도구 생태계와 플랫폼 정책 간 긴장은 계속될 것이다.

**Source:** [Anthropic says Claude Code subscribers will need to pay extra for OpenClaw usage](https://techcrunch.com/2026/04/04/anthropic-says-claude-code-subscribers-will-need-to-pay-extra-for-openclaw-support/)

---

## 3. nanocode: $200 TPU로 처음부터 훈련하는 나만의 Claude Code

개발자 Salman Mohammadi가 Constitutional AI 방식으로 코딩 에이전트를 처음부터 훈련하는 오픈소스 라이브러리 nanocode를 공개했다. Anthropic이 Claude 훈련에 사용하는 방법론과 동일하게, SOUL.md를 직접 작성하고, 에이전트의 세계 인터페이스를 정의하고, 합성 데이터를 생성한 뒤 선호도 최적화로 모델을 SOUL에 정렬하는 전체 파이프라인을 보여준다. 코드는 전부 JAX로 작성되었고 TPU 훈련을 위해 설계되었으며, Karpathy의 nanochat 프로젝트에서 훈련 인프라와 철학을 차용했다.

**Why it matters:** 지식그래프 기반 메모리나 멀티AI 에이전트처럼 커스텀 동작이 필요한 시스템을 만들 때, 일반 목적 LLM을 프롬프트로 조율하는 것과 도메인에 맞게 정렬된 소형 모델을 직접 훈련하는 것은 근본적으로 다른 선택지다. nanocode는 Constitutional AI의 실제 작동 방식을 $200 수준에서 실험 가능한 형태로 번역했다는 점에서, 커스텀 에이전트 설계의 참조 구현으로 쓸 수 있다.

- SOUL.md = Claude의 행동 헌법에 해당하는 개인화 가능한 정렬 문서
- 합성 데이터 생성 + 선호도 최적화(preference optimisation)가 훈련의 두 축
- JAX + TPU 조합으로 $200 예산 내 엔드투엔드 훈련을 목표로 설계

**What's next:** nanochat이 그랬듯 nanocode도 커뮤니티 기여를 통해 다양한 도메인 특화 SOUL 구현이 등장할 가능성이 높다. Constitutional AI 훈련 방법론의 실험 접근 장벽이 낮아지는 흐름이다.

**Source:** [Nanocode: The best Claude Code that $200 can buy in pure JAX on TPUs](https://github.com/salmanmohammadi/nanocode/discussions/1)

---

## Comments