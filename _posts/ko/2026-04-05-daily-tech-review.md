---
layout: post
title: "이란 미사일 AWS 중동 직격, 오라클 3만 명 이메일 해고, MS Copilot '오락용' 선언"
date: 2026-04-05
lang: ko
permalink: /ko/2026/04/05/daily-tech-review/
pair: 2026-04-05-daily-tech-review
tags: ["weekly-review", "ai-trends", "tech-summary"]
source_type: free-sources
---

## Today in One Line
이란의 미사일이 AWS 바레인·두바이 데이터센터를 직격해 복수 가용 영역이 동시에 "hard down" 상태에 빠졌다. 같은 날, 오라클은 95% 이익 급등을 발표한 직후 직원 최대 3만 명을 이메일 한 통으로 해고했다. 그리고 Microsoft는 그동안 공격적으로 판매해온 Copilot을 "오락용이니 중요한 결정에 쓰지 마라"고 공식 선언했다. 지정학, 고용, 신뢰라는 세 개의 균열이 하루 안에 동시에 드러난 날이다.

---

## 1. 이란 미사일 공격, AWS 중동 데이터센터 다운

Tom's Hardware가 보도한 이 사건은 클라우드 인프라를 둘러싼 논의에서 쉽게 빠지는 한 가지를 정면으로 드러냈다. 이란의 미사일이 바레인과 두바이 두 곳에 위치한 AWS 데이터센터를 직격했고, Amazon은 해당 지역의 복수 가용 영역에 대해 "hard down" 상태를 공식 선언했다. 단일 존 장애가 아니라 복수 가용 영역이 동시에 다운됐다는 점이 핵심이다. 가용 영역 설계가 물리적 공격 앞에서는 작동하지 않는다는 것을 실증한 사례다.

중동 AWS 리전을 기반으로 서비스를 운영하던 기업들은 즉각적인 가용성 장애에 직면했다. 멀티 AZ 아키텍처를 갖췄더라도, 물리적으로 근접한 두 존이 동시에 피격되면 설계의 전제 자체가 무너진다. 클라우드 SLA가 보장하는 99.99%는 지정학적 위협을 가정하지 않는다.

**Why it matters:** 클라우드 아키텍처 논의에서 "멀티 AZ면 충분하다"는 전제가 여기서 깨졌다. 지정학적 리스크는 소프트웨어 레이어로 해결되지 않는다. 물리적 인프라가 공격을 받으면 클라우드 SLA 자체가 무력화된다는 것을 이 사건은 실증했다.

- 이란의 미사일이 바레인과 두바이 두 곳의 AWS 시설을 동시에 타격했다
- Amazon이 "hard down" 상태를 공식 선언한 가용 영역이 복수였다

**What's next:** 클라우드 사업자들의 중동 지역 재해복구 설계와 지정학적 리스크 반영 여부가 기업 고객들의 리전 선택 기준에 직접 영향을 미칠 것이다. 지역 분산 아키텍처에 대한 수요가 급속히 높아질 가능성이 크다.

**Source:** [Iranian missile blitz takes down AWS data centers in Bahrain and Dubai](https://www.tomshardware.com/tech-industry/iranian-missile-blitz-takes-down-aws-data-centers-in-bahrain-and-dubai-amazon-declares-hard-down-status-for-multiple-zones)

---

인프라가 외부 충격으로 무너지는 동안, 기업 내부에서는 다른 방식의 충격이 진행되고 있었다.

## 2. 오라클, 95% 이익 급등 후 직원 3만 명 이메일 해고

오라클이 전 분기 대비 95% 이익 급등을 발표한 직후, 최대 3만 명의 직원에게 이메일로 해고 통보를 보냈다. 이익이 두 배 가까이 늘어나는 시점에 단행된 대규모 감원이다. 같은 기간 테크 업계 전반에서는 하루 평균 약 1,000명의 일자리가 사라지고 있는 것으로 집계됐다.

이 두 숫자를 나란히 놓으면 구조가 보인다. 이익은 급등하고, 고용은 급감한다. 감원이 비용 절감의 결과가 아니라 이익 극대화의 수단으로 작동하기 시작했다는 것을 수치가 직접 보여준다. 이메일 한 통으로 수만 명에게 해고를 통보하는 방식 자체도, 속도와 규모 앞에서 절차가 어떻게 압축되는지를 드러낸다.

**Why it matters:** 테크 기업의 이익과 고용이 반대 방향으로 움직이기 시작했다. AI 인프라에 대한 투자가 이익으로 전환되는 속도가 빨라질수록, 인건비 감축을 통한 마진 극대화 압력도 함께 커진다. 이 흐름은 오라클 한 곳의 문제가 아니다.

- 오라클의 이익은 전 분기 대비 95% 급등했다
- 이익 급등과 동시에 최대 3만 명을 이메일 한 통으로 해고했다
- 테크 기업들 전체로는 하루 약 1,000명 규모의 감원이 진행 중이다

**What's next:** AI 인프라 투자가 이익으로 이어지는 속도가 빨라질수록 기업들은 인건비 감축을 통한 마진 극대화 압력을 더 강하게 받게 된다. 업계 전반의 고용 구조 재편이 앞으로 12~18개월 사이에 가속화될 가능성이 높다.

**Source:** [Oracle fired up to 30,000 workers via email after a 95% profit surge](https://finance.yahoo.com/markets/stocks/articles/oracle-fired-30-000-workers-174000364.html)

---

고용이 무너지는 동안, AI 도구를 팔아온 기업이 그 도구에 대해 스스로 선을 그었다.

## 3. Microsoft "Copilot은 오락용 — 중요한 결정에 쓰지 마세요"

Tom's Hardware에 따르면 Microsoft는 Copilot을 엔터테인먼트 목적 전용으로 규정하고, 중요한 용도에는 사용하지 말 것을 공식 권고했다. 소비자와 기업 모두를 대상으로 Copilot을 공격적으로 판매하면서, 동시에 중요한 조언에는 의존하지 말라고 경고한다. 제품을 팔면서 그 제품을 믿지 말라고 하는 것이다.

이 선언은 법적 면책 조항의 성격이 강하다. 제품의 실제 신뢰 수준과 판매 방식 사이의 모순이 공개 문서로 드러났다. 기업 고객 입장에서는 계약서에 서명한 제품이 "오락용"으로 분류된다는 것이 무엇을 의미하는지, 그리고 SLA와 책임 범위 조항을 어떻게 해석해야 하는지 다시 검토해야 하는 상황이 됐다.

**Why it matters:** 제조사가 스스로 "중요한 결정에 쓰지 마라"고 말하는 AI 도구를 어디까지 믿을 것인지, 그 경계는 사용자가 직접 그어야 한다. 도구를 파이프라인에 연결하기 전에 어떤 판단을 위임할 수 있고 어떤 판단은 사람이 직접 내려야 하는지 설계 단계에서 명확히 해야 한다는 것을 제조사 스스로 인정한 셈이다.

- Microsoft는 Copilot을 소비자와 기업 모두에게 적극적으로 판매하고 있다
- 동시에 중요한 조언에 의존하지 말라고 공식적으로 권고했다
- 제품의 실제 신뢰 수준과 판매 방식 사이의 모순이 공개 문서로 드러났다

**What's next:** 이 면책 선언이 EU AI Act의 고위험 AI 시스템 요건과 충돌하는지 규제 당국의 검토가 이어질 수 있다. 기업용 Copilot 계약에서 SLA와 책임 범위 조항을 재협상하려는 움직임이 나타날 것이다.

**Source:** [Microsoft says Copilot is for entertainment purposes only, not serious use](https://www.tomshardware.com/tech-industry/artificial-intelligence/microsoft-says-copilot-is-for-entertainment-purposes-only-not-serious-use-firm-pushing-ai-hard-to-consumers-tells-users-not-to-rely-on-it-for-important-advice)

---

## Comments
