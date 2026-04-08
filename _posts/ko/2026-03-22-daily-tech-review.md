---
layout: post
title: "에이전틱 AI가 연구자·직원·운영체제 수준으로 올라서고, 이를 측정·규율할 AGI 프레임워크와 GPU·오픈소스 인프라 패권 경쟁이 동시에 가속된 한 주였다"
date: 2026-03-22
lang: ko
permalink: /ko/2026/03/22/daily-tech-review/
pair: 2026-03-22-daily-tech-review
tags: ["weekly-recap"]
source_type: perplexity
---

## Today in One Line
한 주 동안 에이전틱 AI는 데모 영역을 벗어나 산업 인프라 안에 자리를 잡기 시작했다. OpenAI는 AI 연구원 로드맵을 공개하고, Hugging Face와 NVIDIA는 오픈 멀티모달 컴퓨터-유스 모델을 쏟아냈으며, 에이전틱 OS 스타트업은 1억 달러 밸류에이션을 받았다. 그 한편에서는 이 전환을 어떻게 측정하고 규율할지를 두고 DeepMind·Anthropic·미국 국방부가 각자의 프레임워크를 꺼내 들었고, 인프라 패권을 둘러싼 GPU·데이터센터·소버린 AI 경쟁은 더욱 노골화됐다.

---

## 1. 에이전틱 AI가 '연구원·직원·OS'로 산업 인프라에 편입되기 시작했다

OpenAI가 'AI 연구원'이라는 중장기 목표를 구체적인 일정과 함께 공개했다. MIT Technology Review 인터뷰에서 밝힌 내용에 따르면, 2026년 9월까지 수학·과학 연구 문제를 자율적으로 다루는 "AI 연구 인턴"을 만들고, 2028년에는 완전 자동 멀티에이전트 연구 시스템을 선보이겠다는 로드맵이다. 이 인터뷰는 OpenAI가 자사의 "북극성" 목표를 처음으로 명시적 일정표와 함께 제시했다는 점에서 주목받았다.

같은 주에 Hugging Face와 H Company는 멀티모달 컴퓨터-유스 모델 Holotron-12B를 공개했다. NVIDIA Nemotron-Nano-12B-v2-VL-BF16을 기반으로 하는 이 모델은 WebVoyager 벤치마크에서 35.1%에서 80.5%로 성공률을 끌어올렸다. 단일 H100에서 동시성 100 기준 약 8.9k tokens/s로, 이전 모델인 Holo2-8B의 5.1k tokens/s 대비 2배 이상의 처리량이다. r/LocalLLaMA에서는 "기존 70B급 모델과 비슷한 성능에 2배 처리량"이라는 평가가 빠르게 퍼졌다.

엔터프라이즈 시장에서도 움직임이 있었다. TechCrunch에 따르면 에이전틱 AI 운영체제를 표방하는 스타트업 Eragon이 설립 1년이 채 안 된 시점에 1,200만 달러 투자와 1억 달러 포스트머니 밸류에이션을 확보했다. 창업자는 "버튼과 메뉴 대신 프롬프트가 업무 UI가 될 것"이라고 밝혔다. NVIDIA는 GTC 2026 키노트에서 Nemotron 3 오픈 모델과 로컬 에이전트를 위한 NemoClaw 스택을 소개하며 젠슨 황이 "모든 소프트웨어가 에이전틱이 될 것"이라고 언급했다.

**Why it matters:** 에이전트가 데모에서 인프라로 넘어가는 전환점은, 선언이 아니라 수치로 확인된다. Holotron-12B의 WebVoyager 80.5%와 Eragon의 1억 달러 밸류에이션은 같은 방향을 가리킨다. "오래 실행되고, 스스로 행동하며, 대규모 인프라 위에서 돌아가는 에이전트"가 이미 제품과 투자의 언어로 번역된 것이다. 지금 에이전트 스택을 설계하는 쪽이 2~3년 후 플랫폼 주도권을 갖는다.

**What's next:** 에이전틱 AI 스택을 누가 표준으로 장악하느냐 — 폐쇄형 OpenAI식 연구 에이전트인지, NVIDIA·Hugging Face·H Company가 주도하는 오픈·하이브리드 스택인지 — 가 향후 2~3년간 개발자와 엔터프라이즈 전략의 최대 변수가 될 가능성이 크다.

**Source:** [OpenAI is throwing everything into building a fully automated researcher](https://www.technologyreview.com/2026/03/20/1134438/openai-is-throwing-everything-into-building-a-fully-automated-researcher/)

---

에이전트가 인프라로 자리 잡는 속도만큼, 그것을 어떻게 측정하고 규율할지에 대한 싸움도 빠르게 구조화되고 있다.

## 2. AGI를 어떻게 측정·정의·규율할지에 대한 프레임워크와 정치 싸움이 동시에 구조화되고 있다

Google DeepMind가 3월 17일 블로그와 논문 "Measuring Progress Toward AGI: A Cognitive Taxonomy"를 통해 AGI를 작업 기억·처리 속도·유동 지능·결정 지능 등 10개의 핵심 인지 능력으로 분해해 '인지 프로필'을 만드는 프레임워크를 제안했다. 이를 구현할 평가를 모집하는 Kaggle 해커톤은 총 상금 20만 달러다. 2023년에 제시된 "Levels of AGI" 단계론을 잇는 작업으로, 구현 방식에 중립을 유지한 채 "무엇을 할 수 있는지"에만 초점을 둔다.

arXiv에는 FAST@AAAI 2026 채택 논문 "A Coherence-Based Measure of AGI"가 공개됐다. 여러 벤치마크 점수를 산술 평균하는 대신, 일반화된 평균과 면적(AUC)을 이용해 특정 영역에서 심하게 뒤처지는 시스템에 더 큰 페널티를 주는 '일관성(coherence)' 기반 AGI 지표다. Hacker News와 Reddit에서는 DeepMind 프레임워크를 두고 "벤치마크는 결국 실패 케이스를 데이터에 추가해 점수를 끌어올리는 게임으로 변질될 수 있다"는 비판과 함께 메타인지·설명가능성·로봇 통합이 빠져 있다는 지적이 이어졌다.

기술 바깥에서도 움직임이 가시화됐다. Anthropic는 3월 11일 AI 사이버보안·사회 영향·경제 연구를 통합한 'Anthropic Institute'를 출범시키며, 실제 Claude 사용 데이터에 기반한 노동·경제 영향 분석을 체계적으로 공개하겠다고 밝혔다. The Verge는 3월 18일 업데이트 기사에서 미국 국방부가 Anthropic에 "어떠한 합법적 용도든 허용" 조항 수용을 압박하며, 거부 시 '공급망 리스크'로 지정하는 방안을 검토 중이라고 보도했다. 같은 매체는 캘리포니아·콜로라도 등 주 단위 AI 법들이 2026년에 본격 발효되며 연방 정부와 충돌할 조짐을 전했다.

**Why it matters:** "AGI냐 아니냐"를 감성이 아닌 인지 능력 10개 영역의 수치 프로필로 바꾸는 시도가 시작됐다는 것 자체가 중요하다. 어떤 프레임워크가 글로벌 표준이 되느냐에 따라 규제·보험·거버넌스 임계값이 달라지므로, 지금 나오는 논문 하나하나가 산업 룰의 초안이다. 단일 AGI 기준선을 기다리기보다, DeepMind·Anthropic·OpenAI 각각의 프레임워크 간 상충을 전제로 리스크를 분석해야 하는 국면이다.

**What's next:** OpenAI·Anthropic·DeepMind·규제기관이 서로 다른 AGI·안전 지표를 제시하고 각자 우군을 모으는 다극 체제가 될 공산이 크다. 하나의 'AGI 기준선'을 기다리기보다 여러 프레임워크 간 상충을 전제로 리스크·기회 분석을 해야 하는 국면이 열리고 있다.

**Source:** [Measuring progress toward AGI: A cognitive framework](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/)

---

측정과 규율 논쟁이 벌어지는 동안, 실제 인프라 자원을 누가 쥐느냐를 둘러싼 경쟁은 훨씬 더 구체적으로 진행 중이다.

## 3. GPU·데이터센터·오픈소스·소버린 AI가 얽힌 'AI 인프라 패권 경쟁'이 한층 노골화되었다

NVIDIA는 GTC 2026에서 Vera Rubin AI 플랫폼을 발표했다. 7개 칩·5개 랙스케일 시스템·1개 슈퍼컴퓨터로 구성된 이 플랫폼은 이전 세대 대비 추론 성능 3배, NVLink 6에서 3.6TB/s 대역폭을 내세운다. 젠슨 황은 DLSS 5, Omniverse DSX 블루프린트, Vera Rubin DSX AI 팩토리 레퍼런스 디자인을 통해 "소프트웨어·GPU·CPU·네트워크를 코드-디자인으로 통합한 AI 공장" 비전을 제시했다. GTC 세션과 Hacker News 토론에서 "그래픽스 회의가 아니라 AI 인프라 쇼에 가깝다"는 평가가 나온 것은 무리가 아니었다.

빅테크 차원의 투자 규모도 가시화됐다. 구글·아마존·메타·마이크로소프트 네 곳이 올해 데이터센터에만 최대 6,500억 달러를 투입할 수 있다는 전망이 나왔고, 시카고 1.8GW급 캠퍼스 등 "AI용 메가 데이터센터" 프로젝트들이 잇달아 등장했다.

오픈소스 진영도 움직였다. H Company와 NVIDIA는 3월 17일 Holotron-12B를 NVIDIA Open Model License로 공개해, Nemotron-Nano 기반의 고성능 컴퓨터-유스 에이전트를 누구나 Hugging Face에서 내려받아 사용할 수 있게 했다. 동시성 100에서 약 8.9k tokens/s까지 선형에 가까운 스케일링은 고가의 폐쇄형 컴퓨터-유스 모델을 대체할 실질적 선택지로 받아들여지는 분위기다.

Hugging Face의 "State of Open Source on Hugging Face: Spring 2026"에 따르면 한국 정부의 National Sovereign AI Initiative가 LG AI Research·SK텔레콤·네이버클라우드·NC AI·업스테이지를 국가 챔피언으로 지정했고, 한국과 미국 스타트업 Reflection AI 간의 데이터센터 파트너십처럼 AI용 데이터센터 투자가 국가 간·기업 간 제휴 형태로 등장하고 있다고 지적했다.

**Why it matters:** AI가 추상적 소프트웨어에서 GPU·전력·냉각까지 통합한 물리 인프라 레이어로 이동하면서, 어떤 하드웨어·라이선스·지리적 거점을 선택하느냐가 국가와 기업 전략의 핵심 설계변수가 됐다. 빅4가 6,500억 달러를 쏟아붓는 동안, Holotron-12B 같은 오픈웨이트 모델과 한국 소버린 AI 이니셔티브의 조합은 빅테크 API 락인 없이 자체 에이전트 스택을 구축하는 경로를 현실화하고 있다.

**What's next:** AI를 도입하는 조직은 "어느 클라우드/코로케이션·어느 GPU/CPU 조합·어떤 오픈/클로즈드 모델 라이선스 위에서 에이전트와 데이터를 굴릴 것인가"가 전략·보안·규제·비용 구조를 동시에 결정하는 핵심 설계변수가 되는 환경을 전제로 해야 한다.

**Source:** [NVIDIA GTC 2026: Live Updates on What's Next in AI](https://blogs.nvidia.com/blog/gtc-2026-news/)

---

## This Week's Pattern
이번 주의 공통 키워드는 "에이전틱 AI의 산업화"라 할 수 있다. OpenAI의 AI 연구원 로드맵, DeepMind의 AGI 인지 프레임워크, NVIDIA·Hugging Face·H Company의 에이전틱 인프라·오픈 모델 발표는 모두 "오래 생각하고, 스스로 행동하며, 대규모 인프라 위에서 돌아가는 에이전트"를 전제하고 있다. 그 위에서 AGI를 어떻게 정의·측정·규율할지, 그리고 어떤 하드웨어·라이선스·국가 전략을 선택할지가 앞으로 몇 년간 AI/Tech 전체를 가르는 구조적 쟁점으로 부상하고 있다고 읽을 수 있다.

## Comments
