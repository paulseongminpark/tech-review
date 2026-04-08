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
Meta의 차세대 모델 라인업이 공식 발표 전에 내부에서 새어나왔고, OpenAI는 자사 모델이 어떻게 행동해야 하는지를 처음으로 공개 문서로 정의했다. 같은 날, 단 3,164개의 파라미터로 훈련된 모델이 길이 100만의 시퀀스를 완벽하게 외삽했다. AI 개발의 방향을 공개하는 움직임과, AI가 얼마나 적은 자원으로 얼마나 먼 거리를 일반화할 수 있는지를 보여주는 결과가 같은 날 나란히 나왔다.

---

## 1. Meta Avocado 라인업 유출 — 에이전트 모델부터 멀티모달까지

공식 발표가 있기 전, Meta 내부 모델 선택기에서 Avocado 계열 전체 구성이 노출됐다. 확인된 변형은 최소 다섯 가지다. Avocado 9B는 소형 변형이고, Avocado Mango는 "agent"와 "sub-agent" 레이블을 함께 달고 있으며 이미지 생성까지 지원하는 멀티모달 변형으로 추정된다. TOMM은 "Tool of Many Models"의 약자로, 이름 자체가 다중 모델 조율 레이어의 존재를 시사한다. Avocado Thinking 5.6은 버전 번호가 명시된 추론 모델로, 이미 내부 반복이 상당히 진행된 상태임을 보여준다. 마지막으로 Paricado는 텍스트 전용 대화 모델이다. 아직 공식 발표는 없지만, 구체적인 명칭과 함께 내부 평가 단계에 있음이 드러났다.

**Why it matters:** 에이전트 특화 모델(Avocado Mango)과 다중 모델 조율 레이어(TOMM)가 같은 라인업 안에 동시에 존재한다는 것은, Meta가 단순히 더 큰 모델을 만드는 방향이 아니라 모델 간 협업 구조를 제품 수준에서 설계하고 있다는 뜻이다. 오픈소스로 공개될 경우 역할별 모델 할당 전략을 실제로 재설계할 근거가 생긴다.

- Avocado Thinking 5.6은 추론 모델의 버전 번호가 명시되어 있어 이미 내부 반복이 상당히 진행된 상태
- TOMM(Tool of Many Models)은 이름 자체가 다중 모델 조율 레이어의 존재를 시사함

**What's next:** Meta가 Llama 계열과 별개로 에이전트·멀티모달 특화 라인을 분리 공개할 가능성이 높다. 공식 발표 시점과 오픈소스 라이선스 범위가 핵심 변수다.

**Source:** [Meta new open source model is coming?](https://www.reddit.com/r/LocalLLaMA/comments/1s6v5n3/meta_new_open_source_model_is_coming/)

---

모델 라인업 유출이 아직 만들어지지 않은 것에 대한 이야기라면, 다음은 지금 존재하는 모델들이 어떻게 행동해야 하는지를 공개 문서로 정의하려는 시도에 관한 이야기다.

## 2. OpenAI Model Spec — 모델 행동의 공개 기준서

OpenAI가 Model Spec의 구조와 작성 철학을 공개했다. Model Spec은 모델이 지시를 따르고 충돌을 해소하며 사용자 자유를 존중하고 안전하게 동작하는 방식을 정의하는 공식 프레임워크다. 2024년 첫 버전 이후 지속적으로 진화해왔으며, 사용자·개발자·연구자·정책 입안자 누구나 읽고 검토할 수 있는 형태로 공개된다. OpenAI는 이 문서가 현재 모델 행동이 완벽하다는 주장이 아님을 분명히 했다. 목표 행동을 명시적으로 정의해 훈련과 평가의 기준으로 삼겠다는 의도다. Model Spec은 Preparedness Framework(프론티어 능력 위험 대응)와 보완 관계로 설계된 별도 레이어로, 공정성과 안전이라는 두 축에서 공개 가독성이 필수라고 명시했다. 사용자 자유, 지시 충돌 해소, 안전 행동이 핵심 정의 영역이다.

**Why it matters:** "의도한 행동을 명시적으로 기술한다"는 접근은 AI 개발 방식의 변화를 보여준다. 모델이 왜 그렇게 행동하는지를 외부에서 검토할 수 있도록 공개한다는 것은, AI 거버넌스 논의를 추상적 원칙에서 구체적 문서로 끌어내리려는 시도다. 이 선례가 다른 AI 기업들에게도 유사한 공개를 요구하는 압력으로 작용할 가능성이 있다.

- Model Spec은 Preparedness Framework(프론티어 능력 위험 대응)와 보완 관계로 설계된 별도 레이어임
- 공정성(AI가 왜 그렇게 행동하는지 이해할 권리)과 안전(예측 가능한 행동 기대) 두 축에서 공개 가독성이 필수라고 명시

**What's next:** Model Spec의 공개 검토 가능성은 AI 거버넌스 논의를 구체화할 기반이 된다. 다른 AI 기업들도 유사한 공개 문서를 요구받을 가능성이 높아졌다.

**Source:** [Inside our approach to the Model Spec](https://openai.com/index/our-approach-to-the-model-spec)

---

대형 모델들의 행동 기준을 공개하는 움직임과 대조적으로, 이쪽에서는 3천 개의 파라미터가 100만 길이를 완벽히 다루는 결과가 나왔다.

## 3. 3천 파라미터 모델이 길이 100만 시퀀스를 완벽히 외삽

Geometric Flow Networks(GFN)라는 새로운 시퀀스 모델링 아키텍처가 공개됐다. 기존의 어텐션 기반 모델이 통계적 상관을 계산하는 방식과 달리, GFN은 입력이 기하학적 다양체를 통과하는 파티클의 궤적을 왜곡시키는 방식으로 동작한다. 통계적 패턴이 아닌 구조적 불변량을 학습한다는 설계 철학이다. 결과는 놀랍다. 3,164 파라미터짜리 G-SSM 모델이 길이 20의 XOR 시퀀스로 훈련된 뒤, 길이 100만 시퀀스에서 100% 정확도를 달성했다. 학습에는 200회 미만의 스텝만 걸렸다. KV 캐시 없이 O(1) 상태 메모리를 유지한다. 8,109 파라미터 모델은 K=2 니들에서 길이 32,000까지 100% 정확도에 오탐 0%를 기록했다. 363K 파라미터 ISN 모델은 TinyShakespeare에서 perplexity 2.48을 달성했다. 모든 실험은 GTX 1650(4GB VRAM)에서 진행됐다.

**Why it matters:** 이 결과에서 진짜 주목할 점은 숫자의 크기가 아니라 일반화의 성격이다. 길이 20으로 훈련해서 길이 100만에서 동작한다는 것은, 이 모델이 패턴을 암기한 게 아니라 구조를 파악했다는 뜻이다. 실패 모드도 기하학적으로 추적 가능한 방식으로 발생한다는 점이 이를 뒷받침한다. K=3 니들에서는 두 번째 니들에서 일관되게 실패한다. 무작위 실패가 아니라 예측 가능한 실패다. 코드는 Apache 2.0으로, 모델은 HuggingFace에 공개되어 재현 장벽이 낮다.

- 8,109 파라미터 모델은 K=2 니들에서 길이 32,000까지 100% 정확도, 오탐 0% 달성
- 코드는 Apache 2.0, 모델은 HuggingFace 공개로 재현 장벽이 낮음

**What's next:** 저자는 cs.LG ArXiv 인도스먼트를 구하고 있어 공식 동료 검토는 아직 전이다. ISN이 길이 128 이상 학습 시 일관성을 유지하는지가 다음 핵심 검증 포인트다.

**Source:** [[R] I trained a 3k parameter model on XOR sequences of length 20](https://www.reddit.com/r/MachineLearning/comments/1s796pz/r_i_trained_a_3k_parameter_model_on_xor_sequences/)

---

## Comments
