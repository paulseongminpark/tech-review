---
layout: post
title: "Meta Avocado 라인업 유출, OpenAI Model Spec 공개, 3K 파라미터로 100만 길이 외삽"
date: 2026-03-30
lang: ko
permalink: /ko/2026/03/30/daily-tech-review/
pair: 2026-03-30-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
source_type: free-sources
---

## Today in One Line
Meta의 차세대 오픈소스 모델 라인업이 내부에서 유출됐고, OpenAI는 모델 행동 기준을 공개 문서화했으며, 단 3천 개의 파라미터로 훈련된 모델이 길이 100만 시퀀스를 완벽히 외삽해냈다.

---

## 1. Meta Avocado 라인업 유출 — 에이전트 모델부터 멀티모달까지

Meta 내부 모델 선택기에서 Avocado 계열 구성이 노출됐다. 확인된 변형은 최소 다섯 가지다: Avocado 9B(소형), Avocado Mango(에이전트+서브에이전트 레이블, 이미지 생성 멀티모달 추정), Avocado TOMM("Tool of Many Models"), Avocado Thinking 5.6(추론 모델 최신 버전), Paricado(텍스트 전용 대화 모델). 아직 공식 발표는 없으나 내부 평가 단계임이 구체적 명칭과 함께 드러났다.

**Why it matters:** 멀티AI 조율 시스템을 운영하는 입장에서 에이전트 특화 모델(Avocado Mango)과 다중 모델 조율 레이어(TOMM)는 직접적으로 관련된다. 오픈소스로 공개될 경우 자동화 파이프라인에서 역할별 모델 할당 전략을 재설계할 근거가 생긴다.

- Avocado Mango는 "agent"와 "sub-agent" 레이블을 함께 달고 있으며 이미지 생성까지 지원하는 멀티모달 변형으로 추정됨
- TOMM(Tool of Many Models)은 이름 자체가 다중 모델 조율 레이어의 존재를 시사함
- Avocado Thinking 5.6은 추론 모델의 버전 번호가 명시되어 있어 이미 내부 반복이 상당히 진행된 상태

**What's next:** Meta가 Llama 계열과 별개로 에이전트·멀티모달 특화 라인을 분리 공개할 가능성이 높다. 공식 발표 시점과 오픈소스 라이선스 범위가 핵심 변수다.

**Source:** [Meta new open source model is coming?](https://www.reddit.com/r/LocalLLaMA/comments/1s6v5n3/meta_new_open_source_model_is_coming/)

---

## 2. OpenAI Model Spec — 모델 행동의 공개 기준서

OpenAI가 Model Spec의 구조와 작성 철학을 공개했다. Model Spec은 모델이 지시를 따르고 충돌을 해소하며 사용자 자유를 존중하고 안전하게 동작하는 방식을 정의하는 공식 프레임워크다. 2024년 첫 버전 이후 지속적으로 진화해왔으며, 사용자·개발자·연구자·정책 입안자 누구나 읽고 검토할 수 있는 형태로 공개된다. OpenAI는 이 문서가 현재 모델 행동이 완벽하다는 주장이 아니라 목표 행동을 명시적으로 정의해 훈련과 평가의 기준으로 삼겠다는 의도임을 분명히 했다.

**Why it matters:** AI 시스템을 직접 설계하고 조율하는 입장에서 모델 행동 규칙을 문서화하는 방법론은 실용적 참고가 된다. 지식그래프 기반 메모리 시스템에서 각 에이전트의 역할과 제약을 정의하는 방식과 구조적으로 유사하며, "의도한 행동을 명시적으로 기술한다"는 원칙은 멀티AI 조율 설계에서도 핵심 원칙이다.

- Model Spec은 Preparedness Framework(프론티어 능력 위험 대응)와 보완 관계로 설계된 별도 레이어임
- 공정성(AI가 왜 그렇게 행동하는지 이해할 권리)과 안전(예측 가능한 행동 기대) 두 축에서 공개 가독성이 필수라고 명시
- 사용자 자유, 지시 충돌 해소, 안전 행동이 핵심 정의 영역

**What's next:** Model Spec의 공개 검토 가능성은 AI 거버넌스 논의를 구체화할 기반이 된다. 다른 AI 기업들도 유사한 공개 문서를 요구받을 가능성이 높아졌다.

**Source:** [Inside our approach to the Model Spec](https://openai.com/index/our-approach-to-the-model-spec)

---

## 3. 3천 파라미터 모델이 길이 100만 시퀀스를 완벽히 외삽

Geometric Flow Networks(GFN)라는 새로운 시퀀스 모델링 아키텍처가 공개됐다. 어텐션 기반의 통계적 상관 계산 대신, 입력이 기하학적 다양체를 통과하는 파티클의 궤적을 왜곡시키는 방식으로 계산을 처리한다. 3,164 파라미터짜리 G-SSM 모델이 길이 20의 XOR 시퀀스로 훈련된 뒤 길이 100만 시퀀스에서 100% 정확도를 달성했으며, 200회 미만의 학습 스텝으로 수렴했다. KV 캐시 없이 O(1) 상태 메모리를 유지하고, 363K 파라미터 ISN 모델은 TinyShakespeare에서 perplexity 2.48을 기록했다. 모든 실험은 GTX 1650(4GB VRAM)에서 진행됐다.

**Why it matters:** 긴 컨텍스트를 다루는 AI 시스템을 설계할 때 KV 캐시 없이 O(1) 메모리로 임의 길이를 처리하는 아키텍처는 자동화 파이프라인의 컨텍스트 한계 문제를 근본적으로 다르게 접근하게 만든다. "통계적 패턴이 아닌 구조적 불변량을 학습한다"는 설계 철학은 장기 메모리 시스템에서 정보를 어떻게 표현하고 인출할 것인가에 대한 새로운 관점을 제시한다.

- 8,109 파라미터 모델은 K=2 니들에서 길이 32,000까지 100% 정확도, 오탐 0% 달성
- 실패 모드가 확률적이 아닌 기하학적으로 추적 가능한 방식으로 발생함 — K=3 니들에서는 두 번째 니들에서 일관되게 실패
- 코드는 Apache 2.0, 모델은 HuggingFace 공개로 재현 장벽이 낮음

**What's next:** 저자는 cs.LG ArXiv 인도스먼트를 구하고 있어 공식 동료 검토는 아직 전이다. ISN이 길이 128 이상 학습 시 일관성을 유지하는지가 다음 핵심 검증 포인트다.

**Source:** [[R] I trained a 3k parameter model on XOR sequences of length 20](https://www.reddit.com/r/MachineLearning/comments/1s796pz/r_i_trained_a_3k_parameter_model_on_xor_sequences/)

---

## Comments