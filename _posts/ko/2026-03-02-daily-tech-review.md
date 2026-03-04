---
layout: post
title: "미국 국방부의 AI 정책 격변이 산업을 뒤흔들고 있으며, OpenAI와 Anthropic 간 대립으로 미국 AI 진영의 균이 심화되는 한편 중국의 모델 추출 공격이 국제 AI 경쟁의 긴장을 가중시키고 있다."
date: 2026-03-02
lang: ko
permalink: /ko/2026/03/02/daily-tech-review/
pair: 2026-03-02-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
---


## Today in One Line
미국 국방부의 AI 정책 격변이 산업을 뒤흔들고 있으며, OpenAI와 Anthropic 간 대립으로 미국 AI 진영의 균이 심화되는 한편 중국의 모델 추출 공격이 국제 AI 경쟁의 긴장을 가중시키고 있다.

---

## 1. 미국 국방부의 선택: OpenAI와 계약, Anthropic은 공급망 위험으로 지정

OpenAI가 미국 국방부와 분류된 환경(classified systems)에서의 AI 모델 배포 계약을 체결했으며, 직후 트럼프 정부는 Anthropic을 "공급망 위험(supply chain risk)"으로 지정하고 모든 연방기관에 6개월 내 사용 중단을 명령했다.

**Why it matters:** 이는 미국 국방 AI 전략의 근본적 전환을 의미한다. 이전까지 Anthropic의 Claude만이 국방부의 최고 기밀 네트워크에 배포된 유일한 frontier LLM이었으나, 안전장치 해제 요구를 거부한 Anthropic이 제재를 받으면서 OpenAI와 xAI 등 다른 기업들이 국방 AI 시장을 놓고 경쟁하는 구도로 급변했다.

- 2월 28일 밤(현지시간) Sam Altman이 X를 통해 Pentagon 계약 체결 발표; OpenAI는 자체 안전장치(safety stack) 완전 통제권 유지 조건으로 합의했으며, 배포를 클라우드 환경으로 제한하고 OpenAI 인원이 현장에 상주하는 다층 방어구조 구성
- 트럼프 대통령이 2월 27일 Anthropic에 "공급망 위험" 지정 지시; 국방부는 6개월 유예기간 동안 Claude 대체재로 전환해야 며, 계약 규모는 최대 2억 달러로 추정됨
- Pentagon의 요구사항은 AI 모델을 "모든 합법적 목적"으로 사용 가능하도록 제한하지 말 것이었으나, Anthropic은 대규모 국내 감시와 완전 자율 무기에 대한 두 가지 예외를 고수; 반면 OpenAI는 같은 조건을 받아들임

**What's next:** xAI의 Grok도 이미 Pentagon 분류 시스템 승인을 받았으며, Google과 OpenAI의 협상이 가속화되어 향후 수주 내 추가 계약이 체결될 것으로 예상된다.

**Source:** OpenAI announces deal with the Pentagon

---

## 2. 중국 AI 기업들, 16백만 건 이상의 Claude 대화 불법 추출 적발

Anthropic이 DeepSeek, Moonshot AI, MiniMax 3개사가 약 24,000개의 가짜 계정을 통해 16백만 건 이상의 Claude 대화를 무단으로 수집했음을 공식 발표했으며, 이는 중국이 미국의 frontier AI 기술을 대규모로 "증류(distillation)" 기법으로 복제했다는 증거로 기록된다.

**Why it matters:** 이번 폭로는 미국과 중국 간 AI 패권 경쟁이 단순 기술 개발에서 적극적 산업 스파이 수준으로 심화됐음을 보여준다. 중국의 AI 기업들이 합법적 경로를 우회하여 미국의 안전장치가 포함된 첨단 모델의 핵심 능력을 대규모로 추출했다면, 미국의 수출통제 정책과 국가 안보 전략의 실효성에 직결된 문제다.

- DeepSeek는 150,000건 이상의 동기화된 트래픽으로 Claude의 추론 능력과 "검열에 안전한 대체 경로 생성"을 표적; Moonshot AI는 3.4백만 건 이상의 대화로 에이전트 추론, 툴 사용, 코딩을 수집; MiniMax는 13백만 건 이상으로 에이전트 코딩과 도구 조율을 집중 추출
- Anthropic은 이들이 "hydra cluster" 아키텍처(대규모 가짜 계정 네트워크를 프록시 서비스 통해 분산 운영)를 사용했으며, 한 프록시 네트워크만 동시에 20,000개 이상의 가짜 계정을 관리했다고 보고
- 증류된 모델은 필수 안전장치를 상실하여 생화학 무기 개발, 악성 사이버 활동 등에 악용될 국가 안보 위험을 초래함; Anthropic은 OpenAI도 비슷한 공격을 받았으며, 이는 "칩 수출통제의 정당성을 재확인시킨다"고 주장

**What's next:** 미국 정부와 AI 산업이 대형 프록시 네트워크 탐지, 교차 산업 정보 공유, 접근 통제 강화 등 다층 방어를 구축할 것으로 예상되며, 특히 중국의 에이전트 모델 개발(GLM-5, MiniMax-M2.1 등)이 이번 전술을 통해 급속도로 고도화되고 있다.

**Source:** [Anthropic: Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)

---

## 3. Frontier LLM 성능 경쟁 고조: Anthropic의 새 모델 연쇄 출시로 업계 기준 재정의

Anthropic이 2월 5일 Claude Opus 4.6(1M 토큰 컨텍스트, β 공개), 2월 말 Claude Sonnet 4.6을 잇따라 출시하면서, OpenAI의 GPT-5.2와의 성능 격차를 급격히 좁혔고 또한 가격 대비 성능에서 새로운 산업 표준을 제시했다.

**Why it matters:** Claude Opus 4.6이 GDPval-AA 벤치마크에서 GPT-5.2를 약 144 Elo 포인트(약 70% 확률로 더 높은 점수)로 앞질렀으며, Sonnet 4.6은 이전 Opus 수준의 성능을 훨씬 저렴하게 제공함으로써 "모델 선택의 경제성"을 완전히 뒤바꿨다. 이는 곧 기업과 정부의 AI 도입 의사결정에 즉시 영향을 미친다.

- Claude Opus 4.6은 1M 토큰 컨텍스트(약 300만 단어), 128K 출력 토큰, 에이전트 팀 기능(parallel multi-agent coordination), Terminal-Bench 2.0에서 최고 점수 달성; Humanity's Last Exam에서 industry-leading 성능으로 GPT-5.2를 능가
- Claude Sonnet 4.6은 가격이 이전과 동일($3/$15 per 1M tokens)하면서 이전 Opus 4.5와 비교해 사용자 선호도 약 70%, OfficeQA에서 Opus 4.6과 동등 수준 달성; 또한 컨텍스트 컴팩션(자동 요약으로 효과적 컨텍스트 확장)과 adaptive thinking 기능 추가
- 동시에 Meta의 Llama 4 Scout(10M 토큰 컨텍스트, 17B active parameters)와 GLM-5(744B MoE, MIT 라이센스, Huawei Ascend 칩 전용 훈련), MiniMax-M2.1(230B total/10B active, 다국어 코딩 우수) 등이 오픈 소스 진영에서 경쟁을 촉발

**What's next:** 이번 성능 도약은 각 기업의 투자 회수 방식(frontier vs. 오픈 소스)을 재구성하고 있으며, 가트너와 같은 기관의 LLM 평가 기준도 2026년 상반기 중 대폭 수정될 것으로 전망되며, 아울러 기업의 AI 벤더 선택 기준이 "최고 성능"에서 "성능-가격-안전성" 트라이앵글로 이동할 가능성이 높다.

**Source:** [Anthropic: Introducing Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6) | OpenAI: Introducing GPT-5.2

## Comments

