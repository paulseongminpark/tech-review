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
에이전틱 AI가 연구자·직원·운영체제 수준으로 올라서고, 이를 측정·규율할 AGI 프레임워크와 GPU·오픈소스 인프라 패권 경쟁이 동시에 가속된 한 주였다.

---

## 1. 에이전틱 AI가 '연구원·직원·OS'로 산업 인프라에 편입되기 시작했다

OpenAI가 '완전 자동화된 AI 연구원'을 향한 중장기 로드맵을 공개하고, 동시에 Hugging Face·NVIDIA·스타트업들이 에이전틱 에이전트와 컴퓨터-유스 모델을 본격 제품화하는 주였다고 볼 수 있다. Holotron-12B, GTC 2026, 에이전틱 OS 스타트업 Eragon까지 합쳐지면서 "에이전트는 더 이상 데모가 아니라 인프라"라는 메시지가 명확해졌다.

**Why it matters:** 이번 흐름은 LLM이 단발성 채팅 도구에서, 장시간 자율로 문제를 풀고 UI를 조작하는 '장기 실행형 에이전트'로 중심축이 이동하고 있음을 보여준다. 이는 Anthropic가 최근 노동 보고서에서 지적한 것처럼, 프로그래머·애널리스트 등 화이트칼라 직무에서 실제 업무 범위의 70% 안팎을 덮는 자동화 시나리오를 앞당길 수 있다.

OpenAI는 MIT Technology Review 인터뷰에서 향후 몇 년간의 "북극성" 목표를 'AI 연구자(AI researcher)'로 설정하고, 2026년 9월까지 특정 수학·과학 연구 문제를 자율적으로 다루는 "AI 연구 인턴"을 만들고, 2028년에는 완전 자동 멀티에이전트 연구 시스템을 선보이겠다고 밝혔다.

Hugging Face 블로그는 3월 17일 H Company와의 협업 결과물인 멀티모달 컴퓨터-유스 모델 Holotron-12B를 공개했는데, 이 모델은 NVIDIA Nemotron-Nano-12B-v2-VL-BF16을 기반으로 하며 WebVoyager 벤치마크에서 Holo2-8B 대비 2배 이상의 처리량(단일 H100에서 동시성 100 기준 약 8.9k tokens/s vs 5.1k tokens/s)과 35.1%에서 80.5%로 크게 향상된 성공률을 기록했다.

NVIDIA는 GTC 2026 키노트와 자사 블로그에서 에이전틱 AI용 풀스택 플랫폼인 Vera Rubin(7개 칩·5개 랙스케일 시스템·1개 슈퍼컴퓨터)을 공개하고, Nemotron 3 오픈 모델과 로컬 에이전트를 위한 NemoClaw 스택을 소개했으며, 젠슨 황은 "모든 소프트웨어가 에이전틱이 될 것"이라고까지 언급했다.

TechCrunch는 같은 주 엔터프라이즈용 에이전틱 AI 운영체제를 표방하는 스타트업 Eragon이 설립 1년이 채 안 된 시점에 1,200만 달러 투자와 1억 달러 포스트머니 밸류에이션을 확보했다고 전하며, 창업자가 "버튼과 메뉴 대신 프롬프트가 업무 UI가 될 것"이라고 말한 내용을 전했다.

r/LocalLLaMA에서는 "NVIDIA와 함께 개발된 Holotron-12B가 기존 70B급 모델과 비슷한 성능에 2배 처리량을 제공하는 오픈 멀티모달 컴퓨터-유스 모델"이라는 게시글이 화제를 모았고, YouTube·요약 뉴스 채널들에서도 GTC 2026과 Holotron을 묶어 "에이전트가 인프라가 되는 전환점"으로 해석하는 콘텐츠가 등장했다.

**What's next:** 에이전틱 AI 스택을 누가 표준으로 장악하느냐(폐쇄형 OpenAI식 연구 에이전트 vs NVIDIA·Hugging Face·H Company가 주도하는 오픈·하이브리드 스택)가 향후 2~3년간 개발자와 엔터프라이즈 전략의 최대 변수가 될 가능성이 크다.

**Source:** [OpenAI is throwing everything into building a fully automated researcher](https://www.technologyreview.com/2026/03/20/1134438/openai-is-throwing-everything-into-building-a-fully-automated-researcher/)

---

## 2. AGI를 어떻게 측정·정의·규율할지에 대한 프레임워크와 정치 싸움이 동시에 구조화되고 있다

Google DeepMind가 AGI 진행도를 인지과학 기반으로 수치화하려는 프레임워크를 내놓았고, arXiv·커뮤니티에서는 대안적 AGI 지표와 비판이 쏟아지고 있다. 동시에 Anthropic·OpenAI·미국 규제·국방부 사이에서는 AI 안전 기준과 군사 활용을 둘러싼 줄다리기가 가시화되며, "AGI를 무엇으로 정의하고 어디까지 허용할 것인가"가 기술·정치 양쪽에서 열린 질문으로 던져진 주였다.

**Why it matters:** DeepMind의 Cognitive Taxonomy와 새로운 AGI 지표 논문은 "AGI냐 아니냐"를 둘러싼 감성적 논쟁을, 인간 인지 능력 10개 영역과 벤치마크 프로필이라는 데이터 구조로 옮기려는 시도라는 점에서 중요하다. 규제·군사·보험·거버넌스 영역에서는 결국 수치화된 임계값을 기준으로 규칙이 만들어지므로, 어떤 연구 집단의 프레임워크가 사실상 글로벌 표준이 되느냐에 따라 산업 룰 자체가 달라질 수 있다.

DeepMind는 3월 17일 블로그와 논문 "Measuring Progress Toward AGI: A Cognitive Taxonomy"를 통해 AGI를 10개의 핵심 인지 능력(작업 기억, 처리 속도, 유동·결정 지능 등)으로 분해해 '인지 프로필'을 만드는 프레임워크를 제안하고, 이를 구현할 평가를 모집하는 Kaggle 해커톤(총 상금 20만 달러)을 발표했다.

이 프레임워크는 2023년에 제시된 "Levels of AGI" 단계론을 잇는 작업으로, 구현 방식(트랜스포머냐, 하이브리드 아키텍처냐)에는 중립을 유지한 채 "무엇을 할 수 있는지"에만 초점을 두겠다고 밝힌다.

arXiv에는 FAST@AAAI 2026 채택 논문 "A Coherence-Based Measure of AGI"가 공개돼, 여러 벤치마크 점수를 산술 평균하는 대신, 일반화된 평균과 면적(AUC)을 이용해 특정 영역에서 심하게 뒤처지는 시스템에 더 큰 페널티를 주는 '일관성(coherence)' 기반 AGI 지표를 제안했다.

Hacker News와 Reddit에서는 DeepMind 프레임워크를 두고 "이런 벤치마크는 결국 실패 케이스를 데이터에 추가해 점수를 끌어올리는 게임으로 변질될 수 있다", "진짜 AGI라면 새로운 환경·로봇 플랫폼에의 적응력부터 보여줘야 한다"는 비판과 함께, 메타인지·설명가능성·로봇 통합이 빠져 있다는 지적이 이어졌다.

Anthropic는 3월 11일 AI 사이버보안·사회 영향·경제 연구를 통합한 'Anthropic Institute'를 출범시키며, 실제 Claude 사용 데이터에 기반한 노동·경제 영향 분석(예: 직군별 자동화율, 사용 성공률, 교육 수준별 성과 격차 등)을 체계적으로 공개하겠다고 밝혔다.

The Verge는 3월 18일 업데이트 기사에서, 미국 국방부가 Anthropic에 "어떠한 합법적 용도든 허용(any lawful use)" 조항 수용을 압박하며, 거부 시 '공급망 리스크'로 지정하는 방안을 검토 중이라고 보도했고, 같은 매체는 캘리포니아·콜로라도 등 주 단위 AI 법들이 2026년에 본격 발효되며 연방 정부와 충돌할 조짐을 전했다.

OpenAI 역시 2월 'Advancing independent research on AI alignment'에서 외부 독립 연구자들이 자사 모델의 정렬·위험을 평가할 수 있도록 지원을 늘리겠다고 밝히는 등, 각 랩이 자신들의 안전·평가 프레임워크를 전면에 내세우는 움직임을 보이고 있다.

**What's next:** OpenAI·Anthropic·DeepMind·규제기관이 서로 다른 AGI·안전 지표를 제시하고 각자 우군을 모으는 다극 체제가 될 공산이 크기 때문에, 하나의 'AGI 기준선'을 기다리기보다 여러 프레임워크 간 상충을 전제로 리스크·기회 분석을 해야 하는 국면이 열리고 있다고 봐야 한다.

**Source:** [Measuring progress toward AGI: A cognitive framework](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/measuring-agi-cognitive-framework/)

---

## 3. GPU·데이터센터·오픈소스·소버린 AI가 얽힌 'AI 인프라 패권 경쟁'이 한층 노골화되었다

NVIDIA GTC 2026과 여러 분석 기사, 그리고 Hugging Face의 오픈소스 동향 리포트는, 이제 모델 성능 경쟁만이 아니라 누가 어떤 인프라·라이선스·지리적 거점을 장악할지가 핵심 게임이 되고 있음을 보여준다. 동시에 Nemotron·Holotron-12B 같은 고성능 오픈 모델과 각국의 소버린 AI 이니셔티브는 "미국 빅테크 클라우드에 대한 의존을 얼마나 줄일 수 있느냐"를 둘러싼 새로운 축을 만들고 있다.

**Why it matters:** GPU·전력·냉각·부지·네트워크까지 통합한 'AI 팩토리' 개념이 부상하면서, AI는 더 이상 추상적인 소프트웨어가 아니라 물리 인프라와 같은 레이어에서 다뤄지고 있다. 여기에 오픈웨이트 모델과 국가 주도 소버린 AI 전략이 결합되면, 특정 클라우드·API에 대한 락인은 줄어드는 대신, 어떤 하드웨어·라이선스 조합을 채택하느냐가 국가·기업 단위의 전략 선택이 된다.

NVIDIA는 GTC 2026 키노트와 공식 블로그에서 Vera Rubin AI 플랫폼을 발표하며, 7개 칩·5개 랙스케일 시스템·1개 슈퍼컴퓨터로 구성된 '에이전틱 AI용 풀스택'이 토큰당 비용과 에너지 효율에서 "세계 최고" 수준의 추론 성능을 제공한다고 강조했다.

같은 행사에서 젠슨 황은 DLSS 5, Omniverse DSX 블루프린트, Vera Rubin DSX AI 팩토리 레퍼런스 디자인 등을 통해 "소프트웨어·GPU·CPU·네트워크를 코드-디자인(extreme codesign)으로 통합한 AI 공장" 비전을 제시했고, GTC 세션과 Hacker News 토론에서도 "그래픽스 회의가 아니라 AI 인프라 쇼에 가깝다"는 평가가 나왔다.

Constellation과 기타 분석 리포트는 NVIDIA를 "AI의 운영체제(operating system of AI)"로 부르며, Rubin GPU(이전 세대 대비 추론 성능 3배), Vera CPU, NVLink 6(3.6TB/s 대역폭) 조합이 향후 AI 팩토리 표준 중 하나가 될 수 있다고 평가했다.

Hugging Face는 3월 17일 "State of Open Source on Hugging Face: Spring 2026"에서, 지난 1년간 허브 데이터를 분석한 결과 미국 외 지역(특히 한국·유럽)에서 오픈웨이트 모델과 자체 LLM 채택이 빠르게 늘고 있으며, 한국 정부의 National Sovereign AI Initiative가 LG AI Research·SK텔레콤·네이버클라우드·NC AI·업스테이지를 국가 챔피언으로 지정했다고 정리했다.

같은 글에서는 한국과 미국 스타트업 Reflection AI 간의 데이터센터 파트너십처럼, 2026년 들어 AI용 데이터센터 투자가 국가 간·기업 간 제휴 형태로 등장하고 있다고 지적한다.

TechCrunch와 인프라 분석 글들은 구글·아마존·메타·마이크로소프트 네 곳이 올해 데이터센터에만 최대 6,500억 달러를 투입할 수 있다는 전망과 함께, 시카고 1.8GW급 캠퍼스 등 "AI용 메가 데이터센터" 프로젝트들을 잇달아 소개했다.

H Company와 NVIDIA는 3월 17일 Holotron-12B를 NVIDIA Open Model License로 공개해, Nemotron-Nano 기반의 고성능 컴퓨터-유스 에이전트를 누구나 Hugging Face에서 내려받아 사용할 수 있게 했고, 모델 카드와 블로그에는 WebVoyager 기준 기존 모델 대비 2배 이상의 토큰 처리량과 80.5% 성공률, 동시성 100에서 약 8.9k tokens/s까지 선형에 가까운 스케일링을 보여준 결과가 제시되었다.

r/LocalLLaMA에서는 Holotron-12B를 "로컬·온프렘 에이전틱 워크로드에 적합한 고처리량 오픈 모델"로 소개하는 글이 빠르게 상위에 올라, 고가의 폐쇄형 '컴퓨터-유스' 모델을 대체할 실질적인 선택지로 받아들이는 분위기가 감지된다.

**What's next:** 앞으로 AI를 도입하는 조직은 "어느 클라우드/코로케이션·어느 GPU/CPU 조합·어떤 오픈/클로즈드 모델 라이선스 위에서 에이전트와 데이터를 굴릴 것인가"가 전략 기획·보안·규제 준수·비용 구조를 동시에 결정하는 핵심 설계변수가 되는 환경을 전제로 해야 한다.

**Source:** [NVIDIA GTC 2026: Live Updates on What's Next in AI](https://blogs.nvidia.com/blog/gtc-2026-news/)

---

## This Week's Pattern
이번 주의 공통 키워드는 "에이전틱 AI의 산업화"라 할 수 있다. OpenAI의 AI 연구원 로드맵, DeepMind의 AGI 인지 프레임워크, NVIDIA·Hugging Face·H Company의 에이전틱 인프라·오픈 모델 발표는 모두 "오래 생각하고, 스스로 행동하며, 대규모 인프라 위에서 돌아가는 에이전트"를 전제하고 있다. 그 위에서 AGI를 어떻게 정의·측정·규율할지, 그리고 어떤 하드웨어·라이선스·국가 전략을 선택할지가 앞으로 몇 년간 AI/Tech 전체를 가르는 구조적 쟁점으로 부상하고 있다고 읽을 수 있다.

## Comments
