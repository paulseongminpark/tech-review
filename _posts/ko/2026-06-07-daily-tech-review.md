---
layout: post
title: "Google × SpaceX 월 $920M 컴퓨트 계약 / OpenAI가 AWS에 상륙하다 / AI 에이전트 용어, 다들 다르게 알고 있었다"
date: 2026-06-07
lang: ko
permalink: /ko/2026/06/07/daily-tech-review/
pair: 2026-06-07-daily-tech-review
tags: ["weekly-review", "ai-trends", "tech-summary"]
source_type: free-sources
---

## Today in One Line
이번 주 AI 업계를 관통한 신호는 하나다. 규모가 상상을 넘어서기 시작했다. Google이 경쟁사의 인프라에 월 $920M을 쓰기로 했고, OpenAI는 AWS 생태계 전체를 배포 채널로 확보했으며, 그 모든 것을 만드는 사람들은 정작 자신들이 쓰는 단어조차 통일하지 못했다는 것이 같은 주에 드러났다.

---

## 1. Google이 경쟁사 인프라에 월 $920M을 쓰기로 했다

SpaceX가 AI 컴퓨트 임대 사업자로 변신하고 있다. Google은 올해 10월부터 2029년 6월까지 32개월간 월 $920M을 지불하고, SpaceX 데이터센터에 있는 약 11만 개의 Nvidia GPU와 관련 하드웨어를 임차하기로 했다. Google 클라우드 측의 설명은 솔직하다. "Gemini Enterprise의 수요가 예상보다 훨씬 높아서 브리지 용량을 확보한 것"이다. 계약에는 날카로운 조건이 붙었다. SpaceX가 9월 30일까지 약속한 GPU 물량을 확보하지 못하면 Google은 즉시 해지할 수 있다. 이 딜이 발표되기 불과 한 달 전, Anthropic은 SpaceX의 멤피스 Colossus 1 데이터센터 전체 용량을 쓰는 유사한 계약을 먼저 맺었다. SpaceX는 올해 2월 xAI와 합병해 $1.25T 밸류에이션을 받은 뒤 IPO를 준비 중이다. 이 두 건의 딜은 IPO를 앞두고 가장 강력한 수익 근거가 됐다.

**Why it matters:** Google이 자체 TPU 인프라를 운영하면서도 경쟁사 인프라를 월 $920M에 빌려야 했다는 것은, Gemini Enterprise의 성장 속도가 Google의 내부 계획을 이미 앞질렀다는 의미다. 그 공급자가 Elon Musk의 xAI와 합병한 SpaceX라는 점은 AI 인프라 시장의 세력 지도가 얼마나 빠르게 뒤섞이고 있는지를 보여준다. 자체 칩을 만드는 회사도 외부 GPU를 사야 하는 수준이라면, AI 수요의 속도는 어떤 단일 공급망도 따라잡지 못하고 있다는 뜻이기도 하다.

- Anthropic과 Google 두 AI 회사가 SpaceX를 주요 컴퓨트 공급자로 확보 — xAI 합병 후 SpaceX의 전략적 위치가 급격히 강화됨
- 계약 기간은 32개월이지만 90일 사전 통보로 어느 쪽이든 해지 가능 — 수요 불확실성을 반영한 구조

**What's next:** SpaceX IPO 이후 AI 컴퓨트 공급자로서의 사업 규모가 공개 시장에서 평가받게 된다. Google이 자체 인프라 확장을 따라잡는 속도와 외부 임차 규모가 어떻게 균형을 맞추는지가 다음 관전 포인트다.

**Source:** [Google to pay SpaceX $920 million a month for compute capacity at xAI data centers](https://www.cnbc.com/2026/06/05/google-to-pay-spacex-920-million-a-month-for-xai-compute-capacity.html)

---

인프라 확보 전쟁이 거세지는 한편, 그 컴퓨트를 실제 기업 환경에 연결하는 배포 레이어에서도 같은 주에 눈에 띄는 문이 열렸다.

## 2. OpenAI가 AWS에 들어왔다

6월 1일, OpenAI의 프런티어 모델과 Codex가 AWS에서 공식 출시됐다. 기업들이 AI 도입을 주저하는 이유는 기술적 역량 부족이 아니라 기존 보안·컴플라이언스·조달·빌링 프로세스와의 충돌이었다. OpenAI는 Amazon Bedrock을 통해 이 마찰을 직접 제거했다. AWS를 이미 쓰는 기업이라면 별도 계약이나 보안 검토 없이 OpenAI 모델을 기존 워크플로우에 연결할 수 있게 됐다. "평가에서 실제 배포까지 더 빠르게"라는 문구가 이번 발표의 핵심을 압축한다. OpenAI 입장에서는 Microsoft Azure 외에 AWS 생태계로 유통 채널을 공식 확장하는 첫 번째 대형 행보다. Anthropic이 AWS와 깊은 파트너십을 맺고 Google이 GCP를 통해 Gemini를 배포하는 구조에서, OpenAI는 이번 행보로 세 클라우드 모두를 유통 채널로 쓰는 포지션에 가까워졌다.

**Why it matters:** 기업 AI 채택에서 가장 오래 걸리는 단계는 기술 검증이 아니라 조달 승인이다. AWS를 통한 배포는 그 단계를 없앤다. OpenAI가 자체 API 외에 클라우드 마켓플레이스 유통을 강화한다는 것은, Anthropic과 Google이 각자의 클라우드를 통해 쌓아온 기업 채널 우위를 정면으로 흔드는 행보다. 모델 품질 경쟁만큼이나 유통 경쟁이 기업 AI 시장의 실질적인 전선이 되고 있다.

- OpenAI 모델이 Amazon Bedrock을 통해 제공되며, 기업의 기존 AWS 보안·거버넌스 체계 안에서 사용 가능
- Codex도 함께 출시되어 개발 자동화 워크플로우와의 즉시 통합이 가능

**What's next:** OpenAI는 사이버 보안 분야 가용성을 포함한 다음 단계를 예고했다. 엔터프라이즈 AI 유통 경쟁이 클라우드 마켓플레이스 위에서 본격화될 것이다.

**Source:** [OpenAI frontier models and Codex are now available on AWS](https://openai.com/index/openai-frontier-models-and-codex-are-now-available-on-aws)

---

인프라부터 배포 채널까지 빠르게 층이 쌓이는 동안, 정작 우리가 만들고 있는 것이 무엇인지에 대한 공통 언어는 아직 따라오지 못하고 있다는 사실이 이번 주 드러났다.

## 3. "Harness"와 "Scaffold"가 뭔지 다들 다르게 알고 있었다

ICLR 2026 현장에서 연구자 Aritra Roy Gosthipaty가 던진 질문 하나가 HuggingFace 블로그 포스트를 만들었다. "harness와 scaffold에 대한 설명을 여러 명에게 들었는데 하나도 수렴하지 않았다." HuggingFace가 이에 대한 응답으로 공개한 AI 에이전트 용어집은 핵심 레이어를 이렇게 구분한다. 모델은 텍스트를 받아 텍스트를 내보내는 LLM 자체다. 스캐폴딩은 모델 주변의 행동 정의 레이어로, 시스템 프롬프트·툴 설명·컨텍스트 관리가 여기에 속한다. 하네스는 실행 레이어로, 모델이 툴 호출 의도를 표현하면 그것을 실제로 실행하는 부분이다. 흥미롭게도 Claude Code는 공식 문서에서 자신을 "Claude를 감싸는 에이전틱 하네스"라고 직접 표현하지만, 외부에서는 같은 것을 스캐폴드라고도 부른다. 이 용어집은 Context Engineering, Policy, Tool Use, Sub-agents까지 이어지면서도 "아직 보편적으로 합의된 정의가 없다"는 단서를 일관되게 달고 있다.

**Why it matters:** 에이전트 시스템이 프로덕션에 들어가기 시작한 지금, 팀 안에서 같은 단어를 다르게 이해하는 것은 단순한 소통 문제가 아니라 아키텍처 결정의 오해로 이어진다. 이 용어집이 최종 정의를 제시하지는 못해도, "우리는 같은 단어로 다른 것을 말하고 있다"는 사실을 공식화한 것 자체가 이 필드의 성숙도를 한 단계 올린다. 빠르게 성장하는 분야에서 어휘 혼란은 기술적 부채만큼 비싼 문제다.

- 모델·스캐폴딩·하네스·에이전트를 별개 레이어로 분리해 정의한 실용적 분류 체계 제시
- Claude Code, Codex, Hermes Agent 등 실제 제품을 예시로 사용해 추상 개념에 구체적 근거를 부여

**What's next:** 에이전트 시스템이 복잡해질수록 레이어 간 경계를 명확히 하는 공통 어휘의 필요성은 커진다. 이 필드에서 RFC나 표준 제안이 나올 타이밍이 가까워지고 있다.

**Source:** [Harness, Scaffold, and the AI Agent Terms Worth Getting Right](https://huggingface.co/blog/agent-glossary)

---

## Comments

