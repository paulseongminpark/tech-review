---
layout: post
title: "엔비디아의 Vera Rubin AI 팩토리, Z.ai의 에이전트 특화 GLM-5-Turbo, Google Maps의 Gemini 기반 Ask Maps/Immersive Navigation 론칭으로 에이전트+물리 세계+실사용 워크플로 스택이 동시에 구체화되고 있다."
date: 2026-03-17
lang: ko
permalink: /ko/2026/03/17/daily-tech-review/
pair: 2026-03-17-daily-tech-review
tags: ["ai-ml", "hardware", "models", "agents"]
---

## Today in One Line
지난 48시간 동안 AI/ML 핵심 뉴스는 엔비디아의 Vera Rubin AI 팩토리 플랫폼, Z.ai의 에이전트 특화 모델 GLM-5-Turbo, Google Maps의 Gemini 기반 Ask Maps/Immersive Navigation 론칭으로 '에이전트+물리 세계+실사용 워크플로' 스택이 동시에 구체화되고 있다.

---

## 1. NVIDIA Vera Rubin AI 팩토리와 GTC 2026, 에이전트 시대용 인프라의 기준을 다시 쓴다

엔비디아가 GTC 2026에서 Vera CPU·Rubin GPU·NVLink 6·ConnectX-9·BlueField-4·Spectrum-6를 묶은 **Vera Rubin NVL72 AI 팩토리 플랫폼**을 공식 론칭하고, 에이전트 시대를 겨냥한 풀스택 하드웨어 전략을 공개했다.

**Why it matters:** 이 플랫폼은 한 랙당 3.6 엑사FLOPS NVFP4 추론 성능과 토큰당 비용 10배 절감을 목표로 하며, 대규모 Mixture-of-Experts 모델과 멀티-에이전트 워크로드를 전제로 설계된 최초의 상용 랙 스케일 AI 팩토리 중 하나다. 이는 단순 GPU 카드 추가가 아니라, 'AI 팩토리'라는 데이터센터 단위로 에이전트 인프라를 사고해야 하는 시대로의 전환 신호로 해석되며, 2027년까지 1조 달러 규모의 AI 수요를 겨냥한 엔비디아의 지배력 확대 전략의 핵심 축이다.

- Vera Rubin NVL72는 Rubin GPU 72개와 Vera CPU 36개를 NVLink 6 스위치로 풀-메시(all-to-all)로 묶어 랙 하나에서 3.6 엑사FLOPS FP4 추론·2.5 엑사FLOPS 학습 성능과 20.7TB HBM4(총 1.6PB/s 대역폭)를 제공하며, Blackwell NVL72 대비 추론 성능 5배·토큰당 비용 10분의 1을 표방한다.
- Rubin 플랫폼은 Vera CPU(에이전트 오케스트레이션·메모리), Rubin GPU(연산), NVLink 6 스위치(3.6TB/s 링크), ConnectX-9 SuperNIC, BlueField-4 DPU, Spectrum-6 이더넷 스위치, Groq 3 LPU까지 포함한 7개 칩 기반 풀스택으로, 엔비디아가 GPU 기업을 넘어 '에이전트용 추론 실리콘+네트워크+스토리지'까지 통합하는 전략을 분명히 했다.
- Wiwynn, ASUS, AHEAD 등 파트너들은 완전 액침/직결 수냉 기반 Vera Rubin NVL72 랙, 10MW급 액체 냉각 인티그레이션 팩토리, Rubin NVL72 기반 AI POD를 GTC 2026에서 동시에 발표하며, 랙당 100~250kW 이상 전력 밀도를 상정한 'AI 팩토리' 레퍼런스 아키텍처를 내놓았다.

**What's next:** GTC 2026에서 예고된 차차세대 Feynman 아키텍처(실리콘 포토닉스+에이전트 오케스트레이션 전용 ACU)까지 감안하면, 향후 2~3년간 AI 인프라 경쟁의 초점은 GPU 개수가 아니라 에이전트 추론 지연·토큰당 비용·랙 스케일 통합 설계로 이동할 가능성이 크다.

**Source:** [Nvidia GTC 2026: Nvidia's hardware strategy goes beyond GPU in AI inference pivot](https://www.constellationr.com/insights/news/nvidia-gtc-2026-nvidias-hardware-strategy-goes-beyond-gpu-ai-inference-pivot)

---

## 2. Z.ai GLM-5-Turbo, OpenClaw 에이전트 워크플로에 최적화된 첫 '에이전트-퍼스트' LLM을 공개하다

중국의 Z.ai(구 Zhipu AI)가 OpenClaw 시나리오에 특화된 대규모 언어 모델 GLM-5-Turbo를 2026년 3월 15~16일 공개하며, 기존 범용 LLM 위에 덧씌우는 방식이 아닌 '에이전트-퍼스트' 학습을 거친 상업용 모델을 선보였다.

**Why it matters:** GLM-5-Turbo는 7440억 매개변수(활성 400억) Mixture-of-Experts 구조와 약 20만 토큰 컨텍스트 윈도우, 에이전트용 reasoning 모드, 장기·예약 실행 기능을 결합해 OpenClaw 같은 멀티-툴·멀티-스텝 에이전트 워크플로를 전제로 설계된 점이 특징이다. 동시에 기본 모델 GLM-5는 MIT 라이선스 오픈소스, Turbo는 클로즈드 상용이라는 구조를 취해 '오픈 가중치 기반에서 수익성 높은 에이전트 특화 상단 계층을 쌓는 새로운 비즈니스 패턴'을 보여주었다.

- GLM-5-Turbo는 GLM-5(744B 총 파라미터, 40B 활성 MoE)를 기반으로, 20만+ 토큰 컨텍스트, DeepSeek 스타일 희소 어텐션, MCP v2, 함수 호출, 구조화 출력, reasoning 모드를 탑재해 긴 도구 호출 체인과 복잡한 지시 분해에 안정적으로 대응하도록 튜닝되었다.
- 공식·커뮤니티 문서에 따르면 이 모델은 OpenClaw 벤치마크와 실제 에이전트 로그를 이용해 'claw-bench-enhanced model'로 학습·최적화되었고, 길게 이어지는 툴 체인에서 실패율과 무한 루프를 줄이는 데 초점을 맞췄다는 평가가 많다.
- Z.ai는 Turbo를 실험적 클로즈드 모델로 운영하면서 여기서 얻은 성능·안정성 개선을 차기 오픈소스 GLM 계열에 반영하겠다고 명시했으며, 이미 Puter.js, Chutes 등에서 GLM-5-Turbo 지원이 추가되고 Hacker News와 r/LocalLLaMA 등 커뮤니티에서 가격·성능·에이전트 적합성 논의가 활발히 이뤄지고 있다.

**What's next:** Turbo가 상용·폐쇄임에도 핵심 개선점이 차기 오픈소스 GLM 릴리스에 합류한다고 명시된 만큼, '에이전트-퍼스트 학습+오픈 가중치' 조합이 2026년 이후 에이전트 생태계의 기본 패턴으로 확산될 가능성이 크다.

**Source:** [GLM-5 Turbo: Zhipu AI's agent model built for OpenClaw](https://www.buildfastwithai.com/blogs/glm-5-turbo-openclaw-agent-model)

---

## 3. Google Maps, Gemini 기반 Ask Maps와 Immersive Navigation으로 '대화형 내비게이션' 시대로 들어가다

Google이 Gemini 모델을 Google Maps에 본격 통합해 대화형 검색 기능 'Ask Maps'와 3D 'Immersive Navigation'을 론칭하며, 지도·길찾기 경험을 지난 10여 년 중 가장 큰 폭으로 개편했다.

**Why it matters:** Ask Maps는 단순 '장소 검색'이 아니라 "핸드폰 배터리가 거의 없는데 줄 오래 안 서고 충전할 수 있는 곳" 같은 복합 조건을 자연어로 물으면, Gemini가 3억 개 이상 POI와 5억 명 이상 사용자의 리뷰 데이터를 기반으로 맞춤 추천과 경로를 구성하는 인터페이스를 제공한다. 동시에 Immersive Navigation은 건물·지형·교차로·차선·횡단보도·신호등까지 3D로 시각화하고, 건물 뒤로 가려지는 구간을 반투명 처리하는 등 운전 화면 자체를 재설계해, 내비게이션 UX를 '지도 보기'에서 '현실에 가까운 3D 공간 인지'로 옮기고 있다.

- Google 공식 블로그에 따르면 Ask Maps는 Gemini가 Street View·항공 사진·리뷰·POI 메타데이터를 결합해 복잡한 질문에 대화형으로 응답하고, 결과를 커스텀 지도와 함께 보여주는 경험을 제공하며, 현재 미국·인도에서 Android·iOS 앱에 우선 롤아웃 중이다.
- Forbes·MacRumors·The Verge 등은 이번 업데이트를 "지난 10년간 Google Maps 내비게이션의 가장 큰 변화"로 평가하며, Ask Maps가 과거 검색·리뷰 탭을 오가며 정보를 찾던 과정을 줄이고, 과거 검색 이력·즐겨찾기·리뷰 패턴을 활용한 개인화 추천을 기본값으로 만들어 간다고 분석했다.
- Immersive Navigation은 Gemini가 Street View·항공 이미지에서 공간 구조를 추출해 경로를 따라 3D로 재구성하고, 복잡한 교차로·고가도로·터널 진입 시 카메라 각도와 투명 처리 등을 자동 조정해 운전자가 실제 전방 시야와 가장 비슷한 형태로 길을 인지하도록 돕는 것을 목표로 하며, 미국부터 iOS·Android·CarPlay·Android Auto에 순차 배포되고 있다.

**What's next:** Google은 Ask Maps와 Immersive Navigation을 먼저 미국·인도에 배포한 뒤 다른 국가·데스크톱·차량 내 시스템으로 확대할 계획이지만, Ask Maps 결과에 광고·스폰서 장소를 어떻게 통합할지는 아직 밝히지 않아 로컬 검색·광고 시장 전반에 적지 않은 변동성이 예상되는 상황이다.

**Source:** [How we're reimagining Maps with Gemini](https://blog.google/products-and-platforms/products/maps/ask-maps-immersive-navigation/)

## Comments

