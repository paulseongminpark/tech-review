---
layout: post
title: "NVIDIA가 광학 기술 강화에 $4B 투자하는 동안 Amazon이 OpenAI에 $50B 투여로 AI 인프라 경쟁 심화."
date: 2026-03-06
lang: ko
permalink: /ko/2026/03/06/daily-tech-review/
pair: 2026-03-06-daily-tech-review
tags: ["hardware", "chips", "datacenter", "cloud", "infrastructure"]
---

## Today in One Line

NVIDIA가 광학 기술 강화에 $4B 투자하는 동안 Amazon이 OpenAI에 $50B 투여로 AI 인프라 경쟁 심화.

---

## 1. NVIDIA, 광학 기술에 $40억 투자…데이터센터 확장 본격화

NVIDIA가 Lumentum과 Coherent에 각각 $20억씩 투자하며 다중 기가와트급 AI 팩토리 구축을 가속화한다.

**Why it matters:** AI 데이터센터의 대역폭 병목을 해결하는 광학 상호연결(optical interconnect) 기술이 Vera Rubin 이후 세대의 핵심 경쟁 요소로 부상했다. NVIDIA가 직접 공급망에 투자하는 것은 Co-Packaged Optics(CPO) 기술이 단순 선택이 아닌 필수 사항임을 시사한다.

- Lumentum은 미국 내 신규 반도체 팹 건설을 위해 NVIDIA 자금을 활용하며, Coherent도 20년간의 NVIDIA 파트너십을 확장하는 형태로 진행
- 양사 모두 다중 기가와트 규모의 구매 약정과 향후 용량 확보 권리를 NVIDIA로부터 획득
- 광학 기술 고도화는 AI 팩토리의 에너지 효율성과 신뢰성을 동시에 개선하는 필수 기술로 평가됨

**What's next:** NVIDIA는 GTC 2026(3월 16-19)에서 CPO 기반 신규 인프라 아키텍처를 공개할 예정이다.

**Source:** [NVIDIA Announces Strategic Partnership With Lumentum](http://nvidianews.nvidia.com/news/nvidia-announces-strategic-partnership-with-lumentum-to-develop-state-of-the-art-optics-technology)

---

## 2. Amazon, OpenAI에 $500억 투자…AWS 독점 지위 강화

Amazon이 OpenAI에 초기 $150억 투자를 시작으로 총 $500억까지 투입하며, OpenAI는 AWS의 커스텀 AI 칩 Trainium 약 2GW를 2027년까지 소비하기로 약정했다.

**Why it matters:** Microsoft의 장기 독점권 하에서도 Amazon이 OpenAI와 직접 클라우드 계약을 체결한 것은 AI 인프라 시장의 패러다임 변화를 의미한다. OpenAI의 Stateful Runtime Environment를 Amazon Bedrock에서 독점 제공하는 조건으로, Amazon은 Microsoft와의 기존 라이선 관계 내에서 제3자 클라우드 제공자로 포지셔닝했다.

- 계약금 $150억 + 추가 $350억은 특정 마일스톤(AI 칩셋 출하량 등) 달성 시 분할 지급 구조
- OpenAI가 Trainium3 및 차세대 Trainium4 칩에 총 2GW 전력 소비 약정은 AWS의 커스텀 실리콘 전략 성공의 직접적 증거
- Microsoft는 상태 기반 API를 제외한 모든 OpenAI 서비스에서 Azure를 통한 독점 호스팅 유지

**What's next:** OpenAI의 Stateful Runtime Environment는 향후 몇 개월 내 Amazon Bedrock을 통해 출시될 예정이다.

**Source:** [OpenAI and Amazon announce strategic partnership](https://www.aboutamazon.com/news/aws/amazon-open-ai-strategic-partnership-investment)

---

## 3. NVIDIA, Vera Rubin HBM4 대역폭 22.2TB/s로 업그레이드…AMD와의 경쟁 심화

NVIDIA가 Vera Rubin NVL72 서버의 HBM4 메모리 대역폭을 기존 대비 10% 상향조정한 22.2TB/s로 설정하여 AMD의 Instinct MI455X(19.6TB/s)를 압도하기로 결정했다.

**Why it matters:** AMD가 12-Hi 스택으로 19.6TB/s를 달성하는 와중에 NVIDIA가 8-Hi 스택으로 22.2TB/s를 구현한 것은 HBM4 핀 속도 경쟁이 본격화되었음을 의미한다. 이는 단순 성능 수치를 넘어 메모리 병목 해소라는 AI 모델 스케일링의 핵심 과제를 둘러 경쟁이 심화되고 있음을 보여준다.

- NVIDIA의 8-Hi HBM4 스택은 핀당 최대 11Gbps 속도로 작동하며, Samsung이 이를 양산 가능한 수준으로 검증 중
- AMD의 MI450X는 더 높은 메모리 용량(12-Hi)을 선택하는 대신 대역폭에서 NVIDIA에 양보하는 아키텍처 트레이드오프 선택
- Vera Rubin NVL72 한 대 기준 20.7TB의 총 HBM4 메모리와 260TB/s의 랙 수준 스케일업 대역폭은 Blackwell 대비 약 2.8배 향상

**What's next:** GTC 2026(3월 16-19)에서 NVIDIA가 Vera Rubin의 정식 스펙 및 성능 벤치마크를 공개할 것으로 예상된다.

**Source:** [NVIDIA upgrades Vera Rubin HBM4 bandwidth by 10 percent](https://www.tweaktown.com/news/109820/nvidia-upgrades-vera-rubin-hbm4-bandwidth-by-10-percent-in-order-to-stay-ahead-of-amd-instinct-mi455x/index.html)

## Comments

