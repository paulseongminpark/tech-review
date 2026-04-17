---
layout: post
title: "Claude Design 출시, Claude Code 품질 퇴화 논란, 미세플라스틱 98.5% 차단 세탁 필터"
date: 2026-04-18
lang: ko
permalink: /ko/2026/04/18/daily-tech-review/
pair: 2026-04-18-daily-tech-review
tags: ["ai-usecase", "enterprise", "adoption", "regulation"]
source_type: free-sources
---

## Today in One Line

Anthropic이 이번 주 AI를 새로운 사용자층으로 확장하는 도구를 출시했다. 동시에 기존 개발자들은 같은 회사의 코딩 도구가 조용히 퇴화하고 있다고 보고한다. 누구를 위해 도구가 만들어지고, 그 도구가 실제로 무엇을 해결하는지—오늘의 세 이야기가 같은 질문 앞에 서 있다.

---

## 1. Claude Design: 디자인 도구를 모르는 사람들을 위한 AI

Anthropic이 Claude Design을 출시했다. 프로토타입, 슬라이드, 원페이저 같은 시각 자료를 텍스트 프롬프트로 만들어주는 실험적 제품이다. 타깃이 명확하다. 디자인 배경이 없는 창업자, 제품 관리자처럼 아이디어를 빠르게 시각화해야 하지만 디자인 도구를 모르는 사람들이다. 사용자가 원하는 것을 설명하면 Claude가 초안을 만들고, 색상·타이포그래피·레이아웃을 직접 조정하거나 추가 요청으로 다듬을 수 있다. 결과물은 PDF, URL, PPTX로 내보내거나 Canva로 바로 전송된다. Anthropic은 Canva와 경쟁하는 것이 아니라 보완한다고 설명했다. 디자인 도구에서 시작하는 것이 아니라, 아이디어에서 시각물로 가는 첫 단계를 담당한다는 것이다. 팀 디자인 시스템을 코드베이스와 디자인 파일을 읽어 자동 적용하는 기능도 포함됐다. Claude Opus 4.7 기반이며, 현재 Claude Pro·Max·Team·Enterprise 구독자 대상 리서치 프리뷰로 제공된다.

**Why it matters:** AI가 "디자이너를 대체한다"는 거대 담론 대신, 아예 디자인 도구를 쓰지 않던 사람들에게 접근하는 방향이 눈에 띈다. 기존 Figma·Canva 사용자 흐름을 건드리지 않으면서 새 시장을 열려는 포지셔닝이다. 기업 도입 측면에서, 팀 디자인 시스템을 코드베이스 기반으로 자동 적용한다는 기능이 실용적인 진입점이 될 수 있다.

- 내보내기 옵션: PDF, URL, PPTX, Canva 직접 전송
- 팀 디자인 시스템을 코드베이스·디자인 파일 기반으로 자동 적용

**What's next:** 리서치 프리뷰 단계라 기능 범위와 안정성이 미지수다. 실시간 협업 기능이 없는 현재 상태에서 팀 단위 도입까지 얼마나 걸릴지가 관건이다.

**Source:** [Anthropic launches Claude Design, a new product for creating quick visuals](https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/)

---

새 사용자층을 향한 확장 시도와 달리, 기존 개발자 사용자들 사이에서는 다른 이야기가 나오고 있다.

## 2. Claude Code가 조용히 퇴화하고 있다

Opus 4.5(작년 11월)에서 Opus 4.6(올해 2월)을 거치며 쌓인 Claude Code에 대한 긍정적 평가가, 4.7 출시를 기점으로 흔들리고 있다. 한 개발자가 직접 경험한 변화들을 기록했다. 3월 말에는 plan 모드에서 컨텍스트를 정리하고 실행하는 옵션이 기본값 false로 변경됐다. Anthropic의 설명은 "1M 컨텍스트가 있으니 이제 필요 없다"였지만, 컨텍스트가 올라갈수록 성능이 저하되는 건 여전히 사실이다. 항의 끝에 결국 기본값이 복원됐다. 4월 초에는 Pro·Max 구독 토큰을 서드파티 프로그램이 사용하는 것이 금지됐고, 공식 공지 없이 이용 약관만 업데이트됐다. 캐시 TTL은 1시간에서 5분으로 단축됐다가 "버그였다"는 해명이 나왔다. 그리고 Opus 4.7에서는 extended thinking budget이 완전히 제거됐다. budget_tokens 파라미터를 설정하면 이제 400 에러가 반환된다. Anthropic은 adaptive thinking이 내부 평가에서 더 낫다고 했지만, 깃허브 이슈에 올라온 그래프는 그 주장을 직접 반박했다.

**Why it matters:** 문제는 개별 기능 변경이 아니다. 변경이 사전 공지 없이, 이유 설명 없이 이루어지고, 불만이 GitHub 이슈로 올라오면 closed 처리되는 패턴이 반복된다는 것이다. 급성장 국면에서 인프라 과부하를 관리하는 것은 이해할 수 있지만, 그 방식이 기존 사용자와의 신뢰를 소모하는 방식으로 이루어지고 있다.

- Extended thinking budget 제거: budget_tokens 설정 시 400 에러 반환, adaptive thinking만 지원
- 3월~4월 사이 사전 공지 없는 기능 변경이 연속으로 발생

**What's next:** 저자는 "enshittification 곡선"이라는 표현을 썼다. Anthropic이 성장 관리 방식을 어떻게 조정할지가 향후 개발자 신뢰의 분기점이 될 것이다.

**Source:** [The Claude Coding Vibes Are Getting Worse](https://blog.matthewbrunelle.com/the-claude-coding-vibes-are-getting-worse/)

---

소프트웨어 도구의 신뢰 문제와는 전혀 다른 맥락에서, 물리적 세계의 오래된 문제가 조용한 돌파구를 맞이했다.

## 3. 세탁 배수에서 미세플라스틱을 98.5% 잡아내는 필터

독일 DITF(섬유·섬유소재연구소)가 세탁 배수에서 미세플라스틱을 직접 포집하는 섬유 기반 캐스케이드 필터를 공개했다. 합성섬유 의류를 한 번 세탁할 때 섬유 1킬로그램당 최대 1,400밀리그램의 마이크로파이버가 배출된다. 기존 하수처리장은 미세플라스틱 제거율이 최대 99%에 달하지만, 처리 수량이 워낙 많아 상당량이 결국 강과 바다로 흘러들어간다. DITF의 필터는 문제의 발생 지점, 즉 세탁기 배수 라인에서 직접 차단하는 방식이다. 실험실 테스트와 산업용 세탁소·도시 하수처리장 현장 시험 모두에서 89.7~98.5%의 제거 효율을 확인했다. 저수압 환경에서도 효율적으로 작동하도록 설계됐으며, 1.5마이크론까지의 미세입자를 포집한다. 현재 세계 해양에는 약 171조 개의 미세플라스틱 입자가 존재하고, 2030년까지 3.2배, 세기 말까지 10배 증가할 것으로 예측된다.

**Why it matters:** 하수처리장 업그레이드나 제도적 규제를 기다리지 않고, 문제의 발생 지점을 직접 차단한다는 접근이 현실적이다. 산업용 세탁소와 도시 하수처리장 현장 검증까지 마쳤다는 점에서 연구 단계를 넘어선 실용화 수준이고, 저수압 설계는 가정용 확장에도 유리한 조건이다.

- 포집 대상: 1.5마이크론까지의 미세플라스틱 입자
- 현장 검증: 산업 세탁소 + 도시 하수처리장 실증 완료

**What's next:** 가정용 세탁기에 부착 가능한 버전으로 확장될 수 있는지가 실질적 확산의 관건이다.

**Source:** [New textile cascade filter removes up to 98.5% of microplastics from wastewater](https://interestingengineering.com/innovation/textile-cascade-filter-microplastics-wastewater)

---

## Comments