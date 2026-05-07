---
layout: post
title: "SpaceX 5.5조 칩 공장 Terafab, Anthropic-Colossus 전면 계약, 인도 Skyroot 유니콘 등극"
date: 2026-05-08
lang: ko
permalink: /ko/2026/05/08/daily-tech-review/
pair: 2026-05-08-daily-tech-review
tags: ["hardware", "chips", "datacenter", "cloud", "infrastructure"]
source_type: free-sources
---

## Today in One Line
AI 경쟁이 소프트웨어를 넘어 실리콘과 콘크리트의 영역으로 내려왔다. 로켓 회사가 칩 공장을 짓고, 그 데이터센터가 이미 대형 AI 계약의 중심에 있으며, 지구 반대편 인도에서는 민간 로켓 스타트업이 유니콘에 오르며 궤도 발사를 앞두고 있다 — 하드웨어가 다시 전략의 중심이 되는 한 주다.

---

## 1. SpaceX, 텍사스에 55조 원 규모 AI 칩 공장 "Terafab" 건설

로켓 회사가 반도체를 만든다는 발상은 1년 전만 해도 농담에 가까웠다. 그런데 그게 현실이 됐다. SpaceX는 텍사스주 오스틴에 최소 550억 달러를 투자해 AI 칩 생산 공장 Terafab을 건설할 계획이다. Grimes County에 제출된 공개 청문회 신청서 — 세금 감면 요청을 위한 — 에서 이 숫자가 공개됐고, 추가 단계가 완공될 경우 총투자액은 1,190억 달러까지 늘어날 수 있다고 명시됐다. Musk가 3월에 처음 발표했을 때 제시한 목표는 구체적이었다 — 지구에서 연간 200기가와트, 우주에서는 1테라와트의 연산 능력을 지원하는 칩을 생산하는 것. Intel이 설계·패키징 파트너로 공식 합류해 이 야심을 현실로 끌어내리는 역할을 맡는다. 생산된 칩은 SpaceX와 Tesla 양쪽에서 AI, 로봇공학, 우주 기반 데이터센터에 활용된다. SpaceX는 이미 테네시주 멤피스에 Colossus라는 자체 데이터센터를 운영 중이며, 이 인프라는 점점 더 광범위한 AI 생태계의 물리적 척추가 되어가고 있다.

**Why it matters:** 칩 설계를 팹리스 기업에 맡기고 제조를 TSMC에 위탁하던 기존 구조에 균열이 생기고 있다. 수직 통합으로 칩부터 우주 데이터센터까지 쥐겠다는 SpaceX의 전략은 단순한 비용 절감이 아니라 공급망 자주권의 문제다. Terafab이 실제로 가동된다면 AI 칩 시장의 공급 구조 자체가 바뀔 수 있다.

- 총투자액 최대 1,190억 달러: 추가 단계 완공 시 기준, 청문회 신청서에 명시
- Intel: 설계·제조·패키징 전 과정 파트너로 참여 공식화

**What's next:** 세금 감면 협상이 관건이다. 규모가 규모인 만큼 텍사스주 측의 결정이 착공 일정에 직접 영향을 미친다.

**Source:** [SpaceX has a $55 billion plan to build AI chips in Texas](https://www.theverge.com/ai-artificial-intelligence/926356/spacex-terafab-plant-cost-ai-chips)

---

Terafab이 먼 미래처럼 들린다면, SpaceX의 현재 데이터센터가 이미 대형 AI 계약의 중심에 있다는 사실이 그 거리를 좁혀준다.

## 2. Anthropic, SpaceX Colossus 전체 용량 계약 — Claude Code 한도 즉시 두 배

Anthropic CEO Dario Amodei는 샌프란시스코에서 열린 Code with Claude 컨퍼런스에서 SpaceX와의 계약을 발표했다 — 멤피스 Colossus 데이터센터의 전체 컴퓨트 용량을 Anthropic이 사용한다는 내용이다. 발표는 즉각적인 효과와 함께 왔다. Claude Code의 5시간 창 한도가 Pro와 Max 구독자 기준으로 두 배가 됐고, 피크 타임 한도 축소 조치가 완전히 사라졌다. Opus 모델의 API 한도도 함께 올랐다. 공급이 수요를 따라잡지 못하는 구조에서 컴퓨트를 확보하는 방식 — 직접 짓거나, 남의 것을 통째로 계약하거나 — 이 AI 기업의 핵심 역량이 되어가고 있다. Anthropic은 Microsoft, Amazon과의 선행 계약에 이어 이번 SpaceX 딜로 물리적 인프라 확보 경쟁에서 한 발 더 나아갔다.

**Why it matters:** 모델 성능 경쟁이 수렴하기 시작하면 다음 차별화 요소는 가용성이다. 개발자가 Claude Code를 쓰다 한도에 막히는 경험이 사라지는 것은 단순한 편의가 아니라 툴 선택의 이유가 된다. Anthropic이 컴퓨트 조달을 전략적으로 다각화하고 있다는 신호이기도 하다.

- 피크 타임 한도 제한 완전 철폐: Pro·Max 플랜 모두 해당
- Colossus: 이번 계약 이전에도 SpaceX가 자체 AI 연산에 활용하던 시설

**What's next:** Colossus 용량으로 수요를 얼마나 흡수할 수 있는지가 변수다. 사용자 기반이 계속 커지면 다음 데이터센터 계약 발표까지의 간격이 점점 짧아질 것이다.

**Source:** [Anthropic raises Claude Code usage limits, credits new deal with SpaceX](https://arstechnica.com/ai/2026/05/anthropic-raises-claude-code-usage-limits-credits-new-deal-with-spacex/)

---

대형 테크 기업들이 지구 위에서 인프라를 쌓는 동안, 지구 밖으로 나가는 길을 민간이 여는 움직임도 빨라지고 있다.

## 3. 인도 최초 우주 스타트업 유니콘 Skyroot, Vikram-1 궤도 발사 초읽기

Skyroot Aerospace가 인도 최초의 우주 테크 유니콘이 됐다. 6,000만 달러 신규 투자로 기업 가치가 11억 달러(프리머니 기준)에 달했다 — 2023년 5억 달러 대비 두 배 이상이다. Sherpalo Ventures와 GIC가 약 5,000만 달러의 프라이머리 에쿼티를 공동 리드했고, BlackRock 계열 펀드가 약 1,000만 달러의 구조화 부채를 맡았다. 타이밍이 우연이 아니다. Vikram-1 로켓은 이미 스리하리코타 우주 발사장으로 이송됐고, 비행 자격 시험 완료 후 6월 발사를 목표로 하고 있다. Vikram-1은 저궤도에 최대 350kg 페이로드를 투입하는 소형 위성 발사체로, Rocket Lab이나 Firefly Aerospace와 직접 경쟁하는 포지션이다. ISRO 출신 엔지니어들이 2018년 창업한 이 회사는 2022년 11월 서브오비탈 로켓 Vikram-S로 인도 최초 민간 로켓 발사를 성공시킨 바 있다. 예상 수요의 약 3분의 1은 인도 내, 나머지는 국제 고객에게서 나온다.

**Why it matters:** 인도의 민간 우주 산업은 저비용 제조와 풍부한 공학 인재를 등에 업고 글로벌 소형 위성 발사 시장에 현실적인 대안으로 부상하고 있다. 6월 궤도 발사 성공 여부가 Skyroot가 단순 유니콘인지 실질적 발사 서비스 기업인지를 가르는 분기점이 된다.

- Ram Shriram (Sherpalo Ventures 창업자, Alphabet 이사): Skyroot 이사회 합류
- Vikram-2: 크리오제닉 스테이지 탑재 1톤급 발사체, 2027년 데뷔 예정

**What's next:** 6월 Vikram-1 발사 시도가 이 모든 것의 시험대다. 궤도 진입 성공 시 인도 민간 우주 산업의 상업화 속도는 한 단계 올라간다.

**Source:** [India's first space tech unicorn emerges as Skyroot gears up for orbital launch](https://techcrunch.com/2026/05/07/indias-first-space-tech-unicorn-emerges-as-skyroot-gears-up-for-orbital-launch/)

---

## Comments

