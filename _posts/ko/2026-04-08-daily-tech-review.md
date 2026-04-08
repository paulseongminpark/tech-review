---
layout: post
title: "Project Glasswing; 아폴로 11호의 57년 버그; 콘크리트 노트북 스탠드"
date: 2026-04-08
lang: ko
permalink: /ko/2026/04/08/daily-tech-review/
pair: 2026-04-08-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line
Anthropic이 AI 사이버보안 동맹을 결성하고, AI 툴이 57년간 숨겨진 아폴로 버그를 끄집어냈다.

---

## 1. Project Glasswing: AI가 방어 사이버보안의 최전선에 선다

Anthropic이 오늘 Project Glasswing을 발표했다. AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks가 파트너로 이름을 올렸다. 핵심은 미공개 신규 프런티어 모델 Claude Mythos Preview로, 이 모델이 이미 모든 주요 운영체제와 웹 브라우저에서 수천 건의 고위험 취약점을 발견했다는 사실이다. Anthropic은 Mythos Preview 사용 크레딧 최대 $1억을 투입하고, 오픈소스 보안 단체에 $400만을 직접 기부한다.

**Why it matters:** AI로 뉴스를 수집·분석하는 자동화 파이프라인을 운영하는 입장에서, 이 수준의 코드 이해 능력은 단순 보안 도구를 넘어 소프트웨어 개발 전반을 재편할 신호다. 지식그래프 기반 메모리처럼 대규모 코드베이스를 구조적으로 파악하는 AI 능력이 방어적 목적으로 전환되는 첫 번째 대규모 실증이다.

- Mythos Preview는 가장 숙련된 인간 보안 전문가를 능가하는 취약점 탐지 능력을 보여줬다
- 1·2차 오픈소스 인프라를 포함한 40개 이상의 추가 조직이 스캔 목적의 접근권을 받았다
- 전 세계 사이버범죄 비용은 연간 약 $5000억으로 추정된다

**What's next:** AI 모델의 취약점 탐지 능력이 공격자보다 방어자에게 먼저 확산될 수 있을지가 관건이다. Anthropic은 "프런티어 AI 능력이 앞으로 몇 달 내에 급격히 발전할 것"이라며 지금 행동해야 한다고 밝혔다.

**Source:** [Project Glasswing: Securing critical software for the AI era](https://www.anthropic.com/glasswing)

---

## 2. 57년간 숨겨진 아폴로 11호 버그를 AI가 찾아냈다

영국 소프트웨어 컨설팅사 JUXT의 CTO Henry Garner 팀이 Apollo Guidance Computer(AGC) 코드에서 57년간 발견되지 않은 버그를 찾아냈다. Claude와 오픈소스 행동 명세 언어 Allium을 사용해 13만 줄의 AGC 어셈블리를 1만 2500줄의 명세로 증류했다. 버그는 자이로스코프 제어 코드의 LGYRO 리소스 락이 오류 경로(BADEND)에서 해제되지 않는 것으로, 수정에 필요한 코드는 단 4바이트다.

**Why it matters:** 멀티AI 조율 시스템을 운영하는 관점에서, 코드를 "읽고 에뮬레이션하는" 기존 방식과 "행동 명세로 증류하는" AI 방식의 차이는 단순 텍스트 검색과 구조화된 지식그래프의 차이와 같다. 소스코드가 2003년부터 공개되어 수천 명이 읽었음에도 발견하지 못한 버그를 명세 기반 접근이 곧바로 끄집어냈다는 점이 핵심이다.

- LGYRO 락이 BADEND 경로에서 해제되지 않으면 이후 모든 자이로 토크 시도가 영구 대기 상태에 빠진다
- 1969년 7월 21일 Armstrong과 Aldrin이 달 표면을 걷는 동안 Collins는 이 버그가 있는 코드로 달을 공전했다
- 역사상 가장 정밀하게 검토된 코드베이스 중 하나임에도, 형식 검증이나 정적 분석은 한 번도 적용된 적이 없었다

**What's next:** 행동 명세 기반 AI 분석이 레거시 코드베이스 감사의 새로운 표준이 될 가능성이 있다. "검증됐다"고 여겨진 시스템에 대한 재검토 수요가 생겨날 것이다.

**Source:** [We found an undocumented bug in the Apollo 11 guidance computer code](https://www.juxt.pro/blog/a-bug-on-the-dark-side-of-the-moon/)

---

## 3. 콘크리트로 노트북 스탠드를 직접 만들었다

개발자 Sam Burns가 순수 콘크리트로 노트북 스탠드를 제작했다. 브루탈리즘 건축 양식과 어반 익스플로레이션(urbex) 미학을 결합한 디자인으로, 2024년 포스트가 최근 HN에서 696점을 받으며 재조명됐다. "소프트웨어를 만드는 사람이 물리적 물건도 직접 만든다"는 메이커 감각이 개발자 커뮤니티의 공감을 얻었다.

**Why it matters:** 소프트웨어 인프라를 직접 설계하고 운영하는 개발자에게 도구에 대한 주도권은 중요한 가치다. 시중 제품을 사는 대신 직접 설계·제작하는 접근법은 소프트웨어 스타트업 문화의 셀프서브 DNA와 닿아 있다.

- 소재: 고형 콘크리트, 브루탈리즘 건축 양식 적용
- 어반 익스플로레이션 테마의 시각적 정체성
- 2024년 작성 후 시간차를 두고 HN 트렌딩에 재진입

**What's next:** 메이커 문화와 개발자 문화의 교차점은 계속 확장되고 있다. 하드웨어와 소프트웨어를 동시에 다루는 인디 개발자 층이 두터워질수록 이런 실험적 제작기가 더 자주 주목받을 것이다.

**Source:** [Show HN: Brutalist Concrete Laptop Stand (2024)](https://sam-burns.com/posts/concrete-laptop-stand/)

---

## Comments