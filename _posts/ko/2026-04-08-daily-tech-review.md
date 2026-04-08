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
Anthropic이 테크 업계 전체를 한 방에 모아 AI 사이버보안 동맹을 결성한 날, 다른 쪽에서는 AI가 57년간 아무도 찾지 못한 아폴로 11호의 버그를 4바이트로 고칠 수 있다는 걸 증명했다. AI가 현재의 코드를 지키는 동시에, 과거의 코드에서 우리가 놓친 것을 끄집어내고 있다.

---

## 1. Project Glasswing: Anthropic이 테크 전체를 한 방에 모았다

이런 파트너 목록은 흔치 않다. AWS, Apple, Broadcom, Cisco, CrowdStrike, Google, JPMorganChase, Linux Foundation, Microsoft, NVIDIA, Palo Alto Networks — 평소라면 서로 경쟁하는 이름들이 하나의 발표문에 나란히 올라왔다. Anthropic이 오늘 발표한 Project Glasswing의 핵심은 미공개 프런티어 모델 Claude Mythos Preview다. 이 모델은 이미 모든 주요 운영체제와 웹 브라우저에서 수천 건의 고위험 취약점을 발견했다. "가장 숙련된 인간 보안 전문가를 능가한다"는 Anthropic의 주장이 사실이라면, 사이버보안의 공격-방어 균형이 처음으로 방어 쪽으로 기울 수 있다. Anthropic은 Mythos Preview 사용 크레딧 최대 1억 달러를 투입하고, 오픈소스 보안 단체에 400만 달러를 직접 기부한다.

**Why it matters:** 연간 5,000억 달러 규모의 사이버범죄 시장에 AI가 방어자 편에서 먼저 대규모로 투입되는 첫 사례다. 그동안 AI 보안 논의는 "AI가 공격에 쓰이면 어쩌나"에 집중됐는데, Glasswing은 그 질문을 뒤집었다.

- 40개 이상의 추가 조직이 스캔 목적의 접근권을 이미 받았다
- 전 세계 사이버범죄 비용 연간 약 5,000억 달러 — Glasswing의 투입 규모가 이 숫자에 비례한다

**What's next:** AI 모델의 취약점 탐지 능력이 공격자보다 방어자에게 먼저 확산될 수 있을지가 관건이다. Anthropic은 "프런티어 AI 능력이 앞으로 몇 달 내에 급격히 발전할 것"이라며 지금 행동해야 한다고 밝혔다.

**Source:** [Project Glasswing: Securing critical software for the AI era](https://www.anthropic.com/glasswing)

---

Glasswing이 현재의 코드를 지키는 이야기라면, 다음은 과거의 코드에서 AI가 무엇을 찾아냈는지에 관한 이야기다.

## 2. 아폴로 11호에 57년간 숨어 있던 버그, 4바이트로 고친다

1969년 7월 20일, 닐 암스트롱과 버즈 올드린이 달 표면을 걸었다. 그 위를 마이클 콜린스가 사령선 컬럼비아호로 달을 공전하고 있었다. 콜린스의 비행을 제어한 것은 Apollo Guidance Computer — 13만 줄의 어셈블리로 작성된, 인류 역사상 가장 정밀하게 검토된 소프트웨어 중 하나다. 2003년에 소스가 공개된 이후 수천 명의 개발자가 읽었다. 아무도 찾지 못한 버그가 하나 있었다.

영국 소프트웨어 컨설팅사 JUXT의 CTO Henry Garner 팀이 Claude와 오픈소스 행동 명세 언어 Allium을 사용해, 13만 줄을 1만 2,500줄의 행동 명세로 증류했다. 그 과정에서 드러난 것: 자이로스코프 제어 코드의 LGYRO 리소스 락이 오류 경로(BADEND)에서 해제되지 않는다. 이 버그가 트리거되면 이후 모든 자이로 토크 시도가 영구 대기 상태에 빠진다. 수정에 필요한 코드는 단 4바이트. 콜린스는 이 버그가 있는 코드로 달의 뒷면을 날았다.

**Why it matters:** "충분히 많은 눈이 보면 모든 버그는 얕다"는 오픈소스의 격언이 57년 동안 틀렸다. 사람이 코드를 읽는 것과 AI가 행동 명세로 증류하는 것은 근본적으로 다른 검증이다. 형식 검증도, 정적 분석도 단 한 번 적용된 적 없는 코드베이스에서 AI가 첫 시도로 버그를 찾아냈다.

- 2003년 소스 공개 이후 23년간 공개 상태 — 발견자 없음
- LGYRO 락이 BADEND에서 해제되지 않으면 이후 모든 자이로 토크가 영구 대기에 빠진다

**What's next:** "검증됐다"고 여겨진 레거시 시스템에 대한 재검토 수요가 생겨날 것이다. 행동 명세 기반 AI 분석이 코드 감사의 새로운 표준이 되는 흐름의 시작이다.

**Source:** [We found an undocumented bug in the Apollo 11 guidance computer code](https://www.juxt.pro/blog/a-bug-on-the-dark-side-of-the-moon/)

---

코드에서 잠시 눈을 떼면, 손으로 만드는 감각도 여전히 살아 있다.

## 3. 콘크리트로 노트북 스탠드를 만든 개발자

개발자 Sam Burns는 순수 콘크리트로 노트북 스탠드를 만들었다. 브루탈리즘 건축의 거친 질감과 어반 익스플로레이션의 미학이 합쳐진 물건이다. 2024년에 올린 제작기가 2년 뒤인 지금 Hacker News에서 696점을 받으며 다시 떠올랐다는 것 자체가 흥미롭다. 소프트웨어를 만드는 사람이 물리적 물건도 직접 만든다는 사실이 개발자 커뮤니티에서 공감을 얻었고, 시중 제품을 사는 대신 직접 설계하고 직접 부어 만드는 감각은 코드를 쓰는 감각과 어딘가 닿아 있다.

**Why it matters:** 2년 전 글이 지금 다시 화제가 됐다는 것 자체가 신호다. AI 도구가 빠르게 발전할수록, 손으로 직접 만드는 것에 대한 향수와 존중이 동시에 커지고 있다.

- 소재: 고형 콘크리트, 브루탈리즘 건축 양식
- 2024년 작성 → 2026년 HN 트렌딩 재진입, 696점

**What's next:** 메이커 문화와 개발자 문화의 교차점은 계속 넓어지고 있다.

**Source:** [Show HN: Brutalist Concrete Laptop Stand (2024)](https://sam-burns.com/posts/concrete-laptop-stand/)

---

## Comments
