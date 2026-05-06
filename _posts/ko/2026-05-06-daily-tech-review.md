---
layout: post
title: "Chrome의 무단 4GB AI 설치, AI 도입해도 조직은 못 배운다, 생물학적 컴퓨팅의 공포"
date: 2026-05-06
lang: ko
permalink: /ko/2026/05/06/daily-tech-review/
pair: 2026-05-06-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line

AI가 어디에나 스며드는 시대, 그 방식이 문제다. 빅테크는 동의 없이 수십억 기기에 모델을 심고, 기업들은 라이선스를 사도 조직 학습으로 이어지지 않는다고 토로하며, 개발자들은 다음 파도인 생물학적 컴퓨팅 앞에서 이미 두려움을 느낀다. 오늘의 세 이야기는 모두 같은 질문을 가리킨다: AI를 가진다는 것과 AI를 이해한다는 것은 다른 일인가.

---

## 1. Chrome이 4GB AI 모델을 몰래 설치하고 있다

Google Chrome은 현재 사용자 동의 없이 4GB 파일을 기기에 쓰고 있다. OptGuideOnDeviceModel 디렉토리 안의 weights.bin이 바로 Gemini Nano의 가중치 파일이다. 프라이버시 연구자 Alexander Hanff가 이를 발견했을 때 Chrome은 어떤 동의 다이얼로그도 표시하지 않았고, 사용자가 파일을 삭제하면 자동으로 재다운로드된다. 이미 Anthropic이 Claude Desktop 설치 시 7개 Chromium 기반 브라우저에 Native Messaging 브리지를 무단 등록한 사례가 있었는데, Google은 동일한 패턴을 훨씬 더 큰 규모로 반복하고 있다. Hanff는 이것이 ePrivacy 지침 제5조 3항, GDPR 제5조 1항의 합법성·공정성·투명성 원칙, 제25조의 설계에 의한 데이터 보호 위반이라고 분석한다. 더 충격적인 것은 환경 비용이다. Chrome의 10억 기기 규모에서 이 한 번의 모델 푸시로 발생하는 CO2 환산 배출량은 6,000~60,000톤 사이로 추산된다. 하나의 회사가 내린 결정이 지구 전체에 청구서를 날리는 셈이다.

**Why it matters:** 이것은 단순한 프라이버시 침해가 아니다. 빅테크가 수십억 기기를 모델 배포 인프라로 전용할 수 있는 힘을 이미 가졌다는 사실을 보여준다. 스타트업은 똑같은 행동을 할 수 없다. 동의 플로우, 투명성 의무, 규정 준수 비용이 그대로 적용되는 동안, 경쟁자는 이미 10억 기기에 자사 모델을 심어뒀다. 비대칭 게임의 새로운 층위다.

- 사용자 삭제 후에도 Chrome 재실행 시 weights.bin 자동 재다운로드
- 배출량 추산: 기기 수에 따라 6,000~60,000톤 CO2 환산

**What's next:** EU 규제 당국의 반응이 주목된다. ePrivacy 지침과 GDPR 위반이 명시적으로 지목된 만큼 과징금 또는 행동 교정 명령이 나올 가능성이 있다. 다만 Google이 이를 "기능 배포"로 재정의하면 법적 공방이 길어질 수 있다.

**Source:** [Google Chrome silently installs a 4 GB AI model on your device without consent](https://www.thatprivacyguy.com/blog/chrome-silent-nano-install/)

---

빅테크가 AI 모델을 일방적으로 심는 동안, 기업 내부에서는 정반대의 문제가 벌어지고 있다.

## 2. AI를 도입해도 기업은 아무것도 배우지 못한다

Ethan Mollick은 오래 전부터 이 역설을 경고해왔다. 개인의 AI 생산성 향상이 자동으로 조직 학습으로 이어지지 않는다는 것. Robert Glaser는 이 상태를 "지저분한 중간(messy middle)"이라고 부른다. GitHub Copilot 라이선스가 전사에 배포되고, ChatGPT Enterprise가 스택 어딘가에 있고, Claude나 Gemini나 Cursor가 팀 곳곳에서 쓰인다. 그런데 같은 회사 안에서 동시에 이런 일이 벌어진다: 한 팀은 Copilot을 자동완성으로만 쓰고, 다른 팀은 Claude Code를 테스트·리뷰와 함께 루프로 돌린다. 시니어 엔지니어는 에이전트에 2주짜리 근본원인 분석을 위임해 1시간 만에 결과를 받고, 주니어 개발자는 그 결과물의 아키텍처 가정이 무엇인지조차 모른다. 지원팀은 반복 티켓을 워크플로우 자동화로 바꿔버렸는데, 센터 오브 엑설런스는 한 번도 올바른 질문을 하지 않았다. Glaser가 주목하는 핵심 질문은 하나다: 그 학습이 어떻게 이동하는가. Leadership이 방향을 설정하고, Crowd가 실제 일을 하면서 쓰임새를 발견하고, Lab이 그것을 공유 관행과 도구로 전환해야 한다. 그런데 흥미로운 AI 작업은 다음 커뮤니티 미팅을 기다려주지 않는다. 코드 리뷰 안에서, 영업 제안서 안에서, 이미 일어나고 있다.

**Why it matters:** 이것은 AI 도입 ROI 논쟁이 아니다. AI가 조직 학습의 속도보다 빠르게 확산되면, 기업은 도구를 가졌어도 역량을 갖지 못한 상태가 된다. 스타트업은 대기업보다 이 루프를 빠르게 닫을 수 있는 구조적 이점이 있다. 그 이점을 의도적으로 설계하지 않으면 대기업과 같은 함정에 빠진다.

- Mollick의 Leadership/Lab/Crowd 프레임: 개인 발견이 조직 역량으로 이동하는 경로 설계가 핵심
- 채택 단위가 조직이나 팀이 아닌 "작업 내부의 루프"로 이동 중

**What's next:** AI 도입 2단계의 진짜 승자는 라이선스를 많이 산 기업이 아니라, 발견을 조직 역량으로 전환하는 시스템을 먼저 만든 기업이 될 것이다.

**Source:** [When everyone has AI and the company still learns nothing](https://www.robert-glaser.de/when-everyone-has-ai-and-the-company-still-learns-nothing/)

---

조직이 AI를 흡수하는 방법을 찾는 사이, 이미 다음 파도가 수평선에 나타나고 있다.

## 3. 생물학적 컴퓨팅이 두렵다

ChatGPT 출시부터 AI 공간에 있어온 한 개발자가 조용히 두려움을 고백했다. 여러 LLM을 직접 실험했고, 사이드 프로젝트를 만들었고, 직접 모델을 구현하며 수학까지 파고들었다. 그런데 생물학적 컴퓨팅 앞에서 처음으로 다른 종류의 두려움을 느꼈다고 한다. AI는 적어도 우리가 이해하는 연산 패러다임 안에 있었다. 실리콘, 트랜지스터, 행렬 곱셈. 생물학적 컴퓨팅은 다르다. 신경세포나 DNA 기반 연산이 실용화되면, 지금까지 쌓아온 직관과 이해의 기반이 통째로 바뀐다. AI가 이미 빠르다고 느꼈는데, 그 다음 파도는 지금 우리가 이해하는 범주 밖에서 온다는 이야기다. 기술의 속도가 이해의 속도를 앞지르기 시작할 때, 공포는 개인적 감상이 아니라 신호가 된다.

**Why it matters:** AI 초기 수용자들, 즉 스타트업 생태계를 실질적으로 움직이는 사람들이 다음 패러다임 앞에서 이미 불안을 표면화하고 있다. 이것은 기술 진보의 속도가 학습의 속도를 초과하기 시작했다는 뜻이다. 그 간극에서 어떤 종류의 회사를, 어떤 타임라인에서 만들어야 하는지에 대한 질문이 스타트업 앞에 다시 던져지고 있다.

- 생물학적 컴퓨팅은 실리콘 기반 패러다임 밖의 연산 영역
- AI 초기 수용자 사이에서 "다음 파도" 불안이 표면화되고 있음

**What's next:** 바이오컴퓨팅이 실용화되기까지는 아직 시간이 있다. 그러나 그 공포감이 지금 이 순간 AI 공간에서 활동하는 사람들에게 나타나고 있다는 사실 자체가, 스타트업이 어디에 베팅하고 무엇을 준비해야 하는지를 재고하게 만든다.

**Source:** [I'm scared about biological computing](https://kuber.studio/blog/Reflections/I%27m-Scared-About-Biological-Computing)

---

## Comments

