---
layout: post
title: "Britannica-OpenAI 저작권 소송, GTC 2026 인프라 1조달러, Mistral Forge+Leanstral 동시 공개"
date: 2026-03-17
lang: ko
permalink: /ko/2026/03/17/daily-tech-review/
pair: 2026-03-17-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
source_type: perplexity
---

## Today in One Line
저작권 소송·인프라 투자·커스텀 모델 플랫폼이라는 세 축에서 LLM 산업의 법적·기술적·사업적 경계가 동시에 재편되고 있다.

---

## 1. Britannica·Merriam-Webster, OpenAI 상대 저작권·상표권 소송 제기

2026년 3월 16일 Encyclopedia Britannica와 자회사 Merriam-Webster가 뉴욕 맨해튼 연방법원에 OpenAI를 제소했다. 약 10만 건 기사를 허가 없이 GPT 학습에 사용하고, ChatGPT가 이를 near-verbatim 재현해 트래픽을 잠식했다는 주장이다.

**Why it matters:** tech-review 파이프라인이 의존하는 DR 서비스(Perplexity, ChatGPT)의 소스 접근 방식이 이 판결에 따라 달라진다. LLM 학습 데이터 전략의 선례가 된다.

- 소장: near-verbatim 재현 + 잘못된 AI 출력에 'Britannica' 출처 명시하는 상표권 침해까지 포함
- OpenAI: 공정 이용(fair use) 원칙 유지 입장. 구조적 시정조치(데이터셋 삭제·재훈련) 여부가 핵심
- 대형 레퍼런스·뉴스 출판사의 집단 라이선스 재편 가능성 대두

**What's next:** 법원이 '공정 이용' 범위와 모델 출력 유사도 기준을 판단하며, 모든 상업용 LLM 사업자의 데이터 전략 선례가 될 전망이다.

**Source:** [Britannica, Merriam-Webster sue OpenAI](https://www.reuters.com/technology/artificial-intelligence/britannica-merriam-webster-sue-openai-2026-03-16/)

---

## 2. NVIDIA GTC 2026 — AI 인프라 1조달러 전망, Vera Rubin·Groq 3 공개

2026년 3월 16일 산호세 GTC에서 젠슨 황 CEO가 Vera Rubin 플랫폼, Groq 3 LPU, Space-1 모듈을 공개하고 2025~2027 누적 AI 인프라 주문 규모 최대 1조 달러를 전망했다. '모델 전쟁'에서 '인프라·플랫폼 전쟁'으로의 전환을 선언했다.

**Why it matters:** 추론·에이전트 워크로드 중심 인프라 전환은 멀티AI 오케스트레이션의 비용 구조를 직접 바꾼다. Nemotron Coalition 오픈 모델은 Claude/Codex 의존도를 낮출 수 있는 로컬 대안 후보다.

- Google Cloud, IBM, Hugging Face 파트너십으로 'AI 인프라+오픈 모델 생태계' 확장
- Nemotron Coalition 출범: 오픈소스 연구소·스타트업이 참여하는 오픈 모델 컨소시엄
- ASUS + Hugging Face: '책상 위 AI 에이전트' 데모로 엣지 추론 대중화 비전 제시

**What's next:** GB200·Vera Rubin 출하와 함께 메모리·전력·냉각 동반 투자가 하이퍼스케일러 CAPEX를 크게 확대시킬 전망이다.

**Source:** [NVIDIA GTC 2026 Live Updates](https://blogs.nvidia.com/blog/gtc-2026/)

---

## 3. Mistral AI — 엔터프라이즈 'Forge' 플랫폼 + 오픈소스 형식 검증 에이전트 'Leanstral'

Mistral AI가 GTC 2026에서 기업 내부 데이터로 커스텀 모델을 훈련하는 'Forge' 플랫폼과, Lean 4 형식 검증용 오픈소스 에이전트 'Leanstral'(6B active, 120B급 성능, Apache 2.0)을 동시 공개했다. CEO 아르튀르 멩슈는 2026년 ARR 10억 달러 궤도를 밝혔다.

**Why it matters:** Forge의 '자기 데이터 모델 훈련'은 mcp-memory 지식그래프를 학습 소스로 전환할 가능성을 시사한다. Leanstral의 pass@2 $36/26.3점(Sonnet $549/23.7점)은 검증형 코딩의 비용 구조를 재정의한다.

- Forge: RAG·프롬프트 엔지니어링을 넘어 기업 데이터 기반 파인튜닝·강화학습 지원
- Leanstral: FLTEval pass@16 31.9점(Sonnet 대비 +8점), pass 횟수에 따라 선형 상승 패턴
- 오픈소스(Apache 2.0) + 엔터프라이즈 서비스 조합이 상용 비즈니스로 성립 가능함을 입증

**What's next:** Forge의 비영어권·규제 산업 채택 사례와 Leanstral의 Lean 4 외 증명 시스템(Coq, Isabelle) 확장 여부가 관전 포인트다.

**Source:** [Mistral Forge — TechCrunch](https://techcrunch.com/2026/03/16/mistral-forge-enterprise/)

## Comments
