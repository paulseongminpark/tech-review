---
layout: post
title: "Anthropic 1M 토큰 표준 가격화 + $100M 파트너 투자, Mistral 675B MoE 공개"
date: 2026-03-16
lang: ko
permalink: /ko/2026/03/16/daily-tech-review/
pair: 2026-03-16-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
source_type: perplexity
---

## Today in One Line
Anthropic이 하루에 두 개의 선제적 행보를 내놨다. 1M 토큰 컨텍스트의 프리미엄 요금을 없애 긴 대화를 일반적인 일로 만들었고, 100M 달러를 파트너 생태계에 투입해 엔터프라이즈 시장을 선점하려 했다. 같은 날 Mistral은 675B 파라미터 MoE 모델을 Apache 2.0으로 풀어 "대형 모델은 독점"이라는 공식에 정면 도전했다. 비용 경쟁과 오픈소스 경쟁이 같은 날 동시에 달아올랐다.

---

## 1. Claude 1M 토큰 컨텍스트 표준 가격 제공 - 장문 컨텍스트 프리미엄 완전 폐지

Anthropic이 3월 13일 Claude Opus 4.6과 Sonnet 4.6의 1M 토큰 컨텍스트를 표준 가격으로 제공하기 시작했다. 이전까지는 200K 토큰을 넘어가면 요금이 2배로 뛰었다. 이 구조에서는 긴 컨텍스트를 쓰는 것 자체가 부담이었고, 개발자들은 토큰 창을 아끼기 위해 설계를 타협했다. 이번 변경으로 900K 토큰짜리 요청도 9K 토큰 요청과 동일한 요율로 청구된다. Opus 4.6은 전체 1M 윈도우에서 $5/$5/$25 per million tokens, Sonnet 4.6은 $3/$3/$15 per million tokens로 통일됐다. Claude Code Max, Team, Enterprise 사용자에게는 Opus 4.6에서 추가 비용 없이 기본 제공된다. 장문 컨텍스트가 특수 기능이 아닌 기본 기능으로 격이 내려간 순간이다.

**Why it matters:** 프리미엄 요금이 사라지면 개발자의 설계 논리가 바뀐다. 이전에는 "얼마나 잘라서 넣을까"를 고민했다면, 이제는 "무엇을 넣을까"만 고민하면 된다. 긴 대화, 대용량 문서 분석, 복잡한 에이전트 체인 같은 워크로드가 비용 계산 없이 시도 가능해진다. 장문 컨텍스트 활용의 심리적 장벽이 낮아지는 효과가 요금표보다 더 클 수 있다.

- Opus 4.6: 전체 1M 윈도우에서 통일된 $5/$5/$25 per million tokens 가격 적용, 프리미엄 요금 제거됨
- Sonnet 4.6: 통일된 $3/$3/$15 per million tokens 가격, 900K 토큰 요청도 9K 토큰과 동일 요율 청구
- Claude Code Max, Team, Enterprise 사용자에게 Opus 4.6에서 기본 제공, 추가 비용 없음

**What's next:** 다른 AI 제공업체들의 장문 컨텍스트 가격 경쟁 압박과 AI 에이전트 기반 자동화 워크플로우의 대중화가 가속될 전망이다.

**Source:** [Anthropic just announced 1M context GA at standard pricing](https://forum.cursor.com/t/anthropic-just-announced-1m-context-ga-at-standard-pricing-for-opus-4-6-sonnet-4-6-when-will-cursor-reflect-this/154701)

---

Anthropic의 두 번째 움직임은 모델 가격이 아닌 시장 구조에 관한 것이었다.

## 2. Anthropic Claude Partner Network에 100M 달러 투자 - 엔터프라이즈 배포 생태계 확대

Anthropic이 3월 12일 Claude 도입을 지원하는 파트너 기업들을 위해 2026년 초기 투자로 100M 달러를 약정했다. 자금은 교육, 기술 지원, 공동 마케팅에 배분되며 파트너 대면 팀을 5배 확대할 계획이다. 이 발표가 단순한 투자 선언처럼 보이지 않는 이유는 그 뒤에 붙은 숫자들 때문이다. Claude Code는 1월 1일 이후 연 매출 2.5B 달러를 넘어섰고 이는 2배 증가한 수치다. 비즈니스 구독은 같은 기간 4배 증가했으며, 100K 달러 이상 연간 지출 고객은 지난 1년간 7배 증가했고 1M 달러 이상 지출 고객도 500명을 넘었다. Accenture는 30,000명, Cognizant는 350,000명 직원에게 Claude 접근권을 열었고 Infosys는 전담 센터를 세웠다. 성장이 먼저 일어나고 있고, 파트너 투자는 그 성장을 잠가두려는 시도다.

**Why it matters:** 기업 AI 시장에서 모델 성능만큼 중요한 것이 배포 지원 역량이다. 파트너 생태계에 먼저 투자한 쪽이 엔터프라이즈 표준을 선점한다. 100K 달러 이상 고객 7배 증가라는 숫자는 Claude가 실험 단계를 넘어 실제 업무 흐름에 박혀 있다는 증거다.

- Claude Code 연 매출 2.5B 달러 이상, 1월 1일 이후 2배 증가; 비즈니스 구독은 4배 증가
- 100K 달러 이상 연간 지출 고객 과거 1년간 7배 증가, 1M 달러 이상 지출 고객 500명 이상
- Accenture 30,000명, Cognizant 350,000명 직원에게 Claude 접근권 개방, Infosys는 전담 센터 구축

**What's next:** 타 AI 제공업체(OpenAI, Google)도 유사한 파트너 투자로 엔터프라이즈 시장 경쟁을 심화할 것으로 예상되며, Anthropic의 AWS/GCP/Azure 멀티클라우드 가용성 전략이 파트너 채택에 핵심 경쟁 요소가 될 것으로 보인다.

**Source:** [Anthropic invests $100 million into the Claude Partner Network](https://www.anthropic.com/news/claude-partner-network)

---

Anthropic이 비용 장벽을 낮추고 생태계를 넓히는 동안, Mistral은 다른 방식으로 시장에 균열을 냈다.

## 3. Mistral 3 공개 - 최대 675B 파라미터 오픈 MoE 모델 Apache 2.0 라이선스

Mistral AI가 Mistral 3 모델군을 공개했다. 최상위 모델 Mistral Large 3는 675B 전체 파라미터 중 41B 활성 파라미터를 지닌 혼합 전문가(MoE) 아키텍처를 채용했다. 대규모 모델이 Apache 2.0으로 완전 공개된다는 것이 이번 발표의 핵심이다. NVIDIA H200 3000개 GPU로 처음부터 학습됐고, LMArena 오픈소스 비추론 모델 순위 2위를 기록했다. Ministral 3 시리즈(3B, 8B, 14B)는 비슷한 규모 모델 대비 최고 성능·비용 비율을 제공하며 생성 토큰 양을 대폭 줄였다. NVIDIA, vLLM, Red Hat 협력으로 Blackwell NVL72 및 A100/H100 단일 노드 추론도 지원한다. 675B 파라미터 모델을 클라우드 종속 없이 직접 실행할 수 있게 된 것은 오픈소스 생태계에서 전례 없는 규모다.

**Why it matters:** MoE 구조는 675B 파라미터를 전부 켜지 않고 필요한 41B만 활성화하기 때문에, 실제 추론 비용은 모델 크기와 다르다. Apache 2.0이라는 라이선스는 상업적 파생 제품에 제약이 없다는 뜻이다. 대형 상용 모델이 독점하던 성능 대역에 오픈 모델이 합법적으로, 상업적으로 진입한 사례가 생겼다.

- Mistral Large 3는 NVIDIA H200 3000개 GPU로 처음부터 학습되었고 LMArena 오픈소스 비추론 모델 순위 2위 달성
- Ministral 3 (3B, 8B, 14B)는 비슷한 규모 모델 대비 최고 성능/비용 비율 제공, 생성 토큰 양 대폭 감소
- NVIDIA, vLLM, Red Hat 협력으로 Blackwell NVL72 및 A100/H100 단일 노드 효율적 추론 지원

**What's next:** Mistral 3의 다양한 크기 옵션(3B~675B)이 엣지 디바이스부터 데이터센터까지 채택되면서 오픈 MoE 모델의 다운스트림 응용이 빠르게 확산될 것이며, NVIDIA 최적화 생태계 강화로 하드웨어-소프트웨어 통합 경쟁이 심화될 전망이다.

**Source:** [Introducing Mistral 3](https://mistral.ai/news/mistral-3)

## Comments


