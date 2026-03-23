---
layout: post
title: "AWS GPU 100만개 확약, 삼성 110조 AI 반도체 투자, NVIDIA H200 중국 공급 재개"
date: 2026-03-20
lang: ko
permalink: /ko/2026/03/20/daily-tech-review/
pair: 2026-03-20-daily-tech-review
tags: ["hardware", "infrastructure", "chips"]
source_type: perplexity
---

## Today in One Line
AWS가 NVIDIA GPU 100만개 이상을 확약하고, 삼성전자가 110조원 AI 반도체 투자를 선언하며, NVIDIA가 중국向 H200 생산을 재개해 글로벌 AI 인프라 확장이 다시 가속되고 있다.

---

## 1. AWS, NVIDIA GPU 100만개 이상 확약으로 AI 클라우드 캐파 전쟁 선도

NVIDIA와 AWS가 GTC 2026에서 발표한 확장 협력에 따라 AWS가 2026년부터 전 세계 리전에 걸쳐 Blackwell·Rubin 아키텍처 기반 NVIDIA GPU를 100만개 이상 도입하고, Groq LPU와 ConnectX·Spectrum X 네트워킹까지 포함한 풀스택 AI 인프라를 구축하기로 했다.

**Why it matters:** 단일 클라우드 사업자가 특정 벤더 GPU 100만개를 확약한 첫 사례다. AI 인프라 경쟁의 초점이 모델 성능에서 물리적 컴퓨트 확보력으로 이동하고 있다는 신호이며, 이는 세 가지 파급을 낳는다. 첫째, AWS 리전별 GPU 밀도 상승은 LLM 추론 비용 하락 압력을 가속시켜 API 기반 서비스의 가격 구조가 바뀐다. 둘째, Blackwell B200(192GB HBM3e, FP4 9,000 TFLOPS)과 Rubin까지 포함된 로드맵은 향후 2~3년간 GPU 세대 전환 주기에 따른 마이그레이션 리스크를 의미한다. 셋째, 개인 개발자·스타트업 입장에서 클라우드 GPU 가용성이 높아지면 로컬 GPU 대비 클라우드 추론의 경제성이 뒤집히는 시점이 앞당겨진다.

- AWS는 2026년부터 글로벌 리전에 걸쳐 Blackwell·Rubin GPU 아키텍처 기반 NVIDIA 가속기를 100만개 이상 추가 배치한다
- RTX PRO 4500 Blackwell Server Edition GPU가 탑재된 신규 Amazon EC2 인스턴스를 공개했으며, AWS가 해당 서버급 Blackwell GPU를 최초로 지원하는 클라우드 사업자가 됐다
- NVIDIA Groq 3 LPU(초저지연 추론용), ConnectX 및 Spectrum X 이더넷 네트워킹이 포함돼 있으며, AWS는 일부 워크로드에 대해 NVIDIA 네트워킹 스택을 공동 배치하는 방향으로 확대하고 있다

**What's next:** AWS와 NVIDIA는 2027년까지 Rubin·Blackwell 계열 칩 판매 누적 1조달러 규모를 목표로 하고 있어 향후 몇 년간 GPU·HBM·데이터센터 전력 수요가 추가로 급등할 가능성이 크다.

**Source:** [NVIDIA GTC 2026: Live Updates](https://blogs.nvidia.com/blog/gtc-2026-news/) · [AWS and NVIDIA deepen strategic collaboration](https://aws.amazon.com/blogs/machine-learning/aws-and-nvidia-deepen-strategic-collaboration-to-accelerate-ai-from-pilot-to-production/)

---

## 2. 삼성전자, 2026년 AI 반도체 설비·R&D에 110조원 투입으로 HBM·파운드리 역전 의지 천명

삼성전자가 2026년 한 해 동안 시설투자와 R&D에 총 110조원(약 732억달러) 이상을 집행해 AI 반도체 시대의 주도권을 확보하겠다는 기업가치 제고 계획을 공시했으며, 이는 2025년 90.4조원 대비 약 22% 증액된 역대 최대 수준이다.

**Why it matters:** 이 숫자의 의미는 비교에서 드러난다. TSMC의 2026년 설비투자 약 500억달러보다 많다. SK hynix가 HBM3E·HBM4로 NVIDIA 공급망을 선점한 상황에서, 삼성은 메모리(HBM4)와 로직(2nm 파운드리)을 동시에 밀어붙이는 전면전을 선택했다. 산업 차원에서 HBM 공급 듀얼소싱이 현실화되면 메모리 가격 협상력이 AI 칩 설계사(NVIDIA, AMD) 쪽으로 기울면서 GPU 단가와 최종 클라우드 추론 비용에 영향을 준다. 한국 반도체 산업 차원에서는 삼성·SK hynix가 HBM 양대 공급자로 동시에 풀캐파를 돌리는 시나리오가 글로벌 AI 메모리 공급의 지정학적 집중도를 심화시킨다.

- 평택·화성 라인과 미국 텍사스 테일러 신규 파운드리 팹(2nm 공정, 2027년 하반기 양산 예정)에 선제적 장비를 투입한다
- AMD MI455X용 HBM4 우선 공급업체로 지정되어 차세대 AI 가속기 메모리 공급에서도 점유율 확대를 노리고 있다
- 로봇·메디컬·자동차 전장·공조 솔루션 등 AI 연관 사업에서 의미 있는 M&A를 추진하겠다고 밝혔다

**What's next:** 삼성전자는 HBM4·GAAFET 기반 2nm 파운드리·차세대 AI SoC를 동시에 밀어붙여 2027년 이후 SK hynix·TSMC가 선점한 HBM·파운드리 구도를 뒤집겠다는 전략으로, 실제 수주·양산 성과에 따라 HBM 가격·AI 가속기 BOM 구조가 재조정될 가능성이 크다.

**Source:** [삼성전자, 시설·R&D에 110조원 투자](https://www.etnews.com/20260319000413) · [Samsung aims to invest record US$73 billion on AI chip thrust](https://www.businesstimes.com.sg/companies-markets/samsung-aims-invest-record-us73-billion-ai-chip-thrust)

---

## 3. NVIDIA, 중국向 H200 GPU 생산·출하 재개로 10개월 간 제동 걸린 AI 칩 공급 재가동

중국 정부가 NVIDIA의 H200 AI GPU 수입을 승인하면서, NVIDIA가 약 10개월간 중단됐던 H200 생산을 재개하고 중국 고객사들로부터 주문을 다시 받기 시작했다.

**Why it matters:** 이 결정은 기술 뉴스가 아니라 지정학 뉴스다. 미국이 고성능 AI 칩 수출을 제한하는 와중에 H200(141GB HBM3e, 4.8TB/s)이 중국에 들어간다는 것은 규제와 산업 현실 사이의 타협선이 새로 그어졌다는 의미다. 글로벌 AI 칩 수급 관점에서 중국 시장 재개방은 NVIDIA의 총 출하량을 늘려 규모의 경제를 강화하고 전체 GPU 단가를 낮추는 쪽으로 작용한다. 동시에 중국 AI 인프라가 다시 최신 GPU에 접근하게 되면 미중 AI 격차 내러티브가 수정되고, 오픈소스 모델 생태계(DeepSeek 등)의 학습 인프라가 한 단계 올라간다. 개발자 입장에서는 글로벌 GPU 공급 확대가 클라우드 API 가격 하락과 모델 다양성 확대로 이어지는 간접 수혜가 된다.

- H200는 141GB HBM3e 메모리와 4.8TB/s 대역폭, 최대 700W TGP를 제공하는 Hopper 계열 GPU로, H100 대비 메모리 용량을 거의 두 배로 늘렸다
- Jensen Huang CEO는 미국과 중국 양측에서 수출 라이선스를 확보함에 따라 10개월간 중단됐던 생산 라인이 재가동됐다고 밝혔다
- NVIDIA가 중국향 H200에 더해 Groq LPU 기반 추론 칩 변형까지 준비 중인 것으로 알려졌다

**What's next:** NVIDIA는 2026년 중으로 중국향 H200 공급을 점진적으로 확대하는 한편, Groq LPU 기반 추론 칩 변형과 Rubin·Vera 플랫폼을 포함한 차세대 제품군을 병행 공급한다는 방침이어서, 미국 수출 규제·중국 자립 전략·글로벌 AI 칩 가격 구조가 재조정될 가능성이 크다.

**Source:** [Nvidia gets Beijing's nod for H200 chip sales](https://www.reuters.com/world/china/chinese-authorities-approve-nvidias-h200-ai-chip-sales-source-says-2026-03-18/) · [NVIDIA Resumes H200 Production for Chinese Market](https://www.chosun.com/english/industry-en/2026/03/18/63U4KDDW7NG6JKWVXATLPGUIDY/)

## Comments


