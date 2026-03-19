---
layout: post
title: "지난 48시간 동안 GitHub Copilot의 GPT-5.3-Codex LTS 도입, NVIDIA의 오픈소스 추론 OS Dynamo 1.0, Mistral의 Forge 출시가 AI 개발 인프라 지형을 새로 그리고 있다."
date: 2026-03-19
lang: ko
permalink: /ko/2026/03/19/daily-tech-review/
pair: 2026-03-19-daily-tech-review
tags: ["ai-industry", "startups", "business"]
---

규칙 6 "마크다운만 출력. 코드블록 없이" — 직접 출력한다.

---
layout: post
title: "GitHub Copilot 첫 LTS 모델 GPT-5.3-Codex, NVIDIA Dynamo 1.0, Mistral Forge 출시"
date: 2026-03-19
lang: ko
permalink: /ko/2026/03/19/daily-tech-review/
pair: 2026-03-19-daily-tech-review
tags: ["ai-industry", "startups", "business"]
source_type: perplexity
---

## Today in One Line
지난 48시간 동안 GitHub Copilot의 GPT-5.3-Codex LTS 도입, NVIDIA의 오픈소스 추론 OS Dynamo 1.0, Mistral의 Forge 출시가 AI 개발 인프라 지형을 새로 그리고 있다.

---

## 1. GitHub Copilot, GPT-5.3-Codex를 첫 LTS 모델이자 기본 모델로 채택해 엔터프라이즈 AI 코딩 기준을 고정한다

GitHub가 GPT-5.3-Codex를 GitHub Copilot의 첫 장기 지원(LTS) 모델로 지정하고, 2026년 5월 17일부터 Copilot Business·Enterprise의 기본(base) 모델로 전환하겠다고 발표했다.

**Why it matters:** 우리 orchestration이 Claude(설계)·Codex(추출)·Gemini(검증)로 모델을 위임하는 구조에서, Copilot의 LTS 12개월 보장은 Codex 위임 파이프라인의 프롬프트·비용 설계를 연 단위로 안정화할 수 있는 기준점이 된다.

- GPT-5.3-Codex는 2026년 2월 5일 출시, 2027년 2월 4일까지 12개월 유지 지원
- 발표 시점(3월 18일)으로부터 60일 안에 모든 Business·Enterprise 조직에서 자동 활성화
- GPT-5.3-Codex는 1× 프리미엄 요청 단위, 기존 GPT-4.1은 0×로 유지해 점진적 전환 유도

**What's next:** 각 조직은 60일 안에 GPT-5.3-Codex 기준으로 내부 보안·품질 가이드와 코드 리뷰 정책을 재정의하고, 매해 1회 LTS 모델 교체 주기에 맞춘 검토 프로세스를 갖춰야 할 것이다.

**Source:** GPT-5.3-Codex long-term support in GitHub Copilot

---

## 2. NVIDIA, 오픈소스 추론 OS 'Dynamo 1.0'으로 AI 팩토리 스택의 공용 인프라를 연다

NVIDIA가 GTC 2026에서 대규모 AI 추론을 위한 오픈소스 운영체제 격 소프트웨어인 'NVIDIA Dynamo 1.0'을 발표해, LangChain·llm-d·LMCache·SGLang·vLLM 같은 프레임워크와 긴밀히 통합되는 AI 팩토리용 추론 레이어를 공식화했다.

**Why it matters:** Context Engineering에서 Gate B/C 대규모 추론 위임 시 토큰당 비용이 핵심 변수인데, Dynamo의 Blackwell 기반 7배 추론 성능 향상은 동일 예산으로 더 복잡한 에이전트 워크플로를 돌릴 수 있는 인프라 조건을 만든다.

- Blackwell GPU 기반 추론에서 최대 7배 속도 향상
- LangChain, vLLM, SGLang 등 OSS 프레임워크와 네이티브 통합
- KVBM(메모리 관리), NIXL(GPU 간 전송), Grove(클러스터 스케일링) 코어 모듈 별도 OSS 제공

**What's next:** LangChain·vLLM·SGLang이 Dynamo 전용 최적화를 노출하기 시작하면, "Dynamo 대응 여부"가 대규모 에이전트/서빙 스택 선택의 필수 체크리스트가 될 가능성이 크다.

**Source:** NVIDIA Enters Production With Dynamo, the Broadly Adopted Inference Operating System for AI Factories

---

## 3. Mistral AI, Forge 플랫폼으로 기업이 자체 데이터로 프런티어급 모델을 재학습하는 시대를 연다

Mistral AI가 GTC 2026에서 기업 전용 모델 학습 플랫폼 'Forge'를 공개해, 단순 파인튜닝이 아닌 사내 데이터로 프런티어급 모델을 pre-training부터 RL까지 재학습할 수 있는 서비스를 내놓았다.

**Why it matters:** mcp-memory에 축적된 관찰→시그널→패턴→원칙 지식 그래프를 RAG만으로는 모델에 온전히 전달하기 어려운데, Forge식 자체 학습 경로는 도메인 지식을 모델 가중치에 직접 주입하는 대안을 열어준다.

- pre-training, supervised fine-tuning, DPO/ODPO, RL 파이프라인까지 모델 전 라이프사이클 지원
- 초기 고객으로 ASML, Ericsson, 유럽우주국(ESA) 등 확보
- CEO Arthur Mensch: 2026년 내 연간 매출 10억 달러 규모 궤도 진입 언급

**What's next:** Forge가 실제 성공 사례를 만들면, 호스티드 파인튜닝 API vs 자가 학습 공장 구축이 2026~2027년 엔터프라이즈 AI 전략의 핵심 갈림길이 될 전망이다.

**Source:** Mistral launches Forge to help enterprises build their own AI models

## Comments