---
layout: post
title: "LiteLLM 공급망 공격 탐지, Tesla 보안 연구, Mac Pro 단종"
date: 2026-03-25
lang: ko
permalink: /ko/2026/03/25/daily-tech-review/
pair: 2026-03-25-daily-tech-review
tags: ["security", "supply-chain", "apple", "hardware", "ai-tooling"]
source_type: free-sources
---

## Today in One Line
AI 도구 생태계를 노린 PyPI 공급망 공격이 Claude Code로 탐지되었고, Apple은 Mac Pro를 공식 단종했다.

---

## 1. LiteLLM 1.82.8 PyPI 공급망 공격 — Claude Code로 분석·신고까지

2026년 3월 24일 10:52, litellm v1.82.8이 PyPI에 업로드되었다. 해당 버전에는 대응하는 GitHub 태그가 없었고 — 공식 최신 버전은 v1.82.6이었다. 피해자 엔지니어 Callum McMahon은 노트북이 멈추는 현상을 시작으로 조사에 착수했고, Claude Code 단일 대화 세션 안에서 악성코드를 분석한 뒤 PyPI 측에 격리를 요청하는 전 과정을 완료했다. 악성코드는 ~/.config/sysmon/sysmon.py 영속성 설치를 시도했고, 11k 프로세스 포크 폭탄으로 강제 재부팅을 유발했다. litellm_init.pth (34 KB) 파일에는 자격증명 탈취, Kubernetes 횡적 이동, 외부 유출 코드가 포함되어 있었다.

**Why it matters:** Paul의 orchestration 스택은 litellm을 LLM 라우터로 사용할 가능성이 있고, mcp-memory 서버 및 futuresearch-mcp-legacy 같은 MCP 의존성 체인이 동일한 취약점을 공유할 수 있다. 공격 탐지 자체가 Claude Code 대화 로그로 공개되었다는 점은 tech-review 파이프라인 자동화에서 LLM-assisted security monitoring 패턴의 실증 사례다.

- 10:52 업로드 → 11:13 Claude Code 조사 시작 → 11:40 악성코드 확인 → 11:58 Docker 격리 환경에서 재검증 → 12:00 PyPI 신고: 총 68분
- futuresearch-mcp-legacy가 의존성으로 litellm을 당겨오면서 Cursor 실행 시 감염 — MCP 서버 간접 의존성이 공격 경로가 됨
- 엔지니어 본인 표현: "AI 툴링이 악성코드 생성만이 아니라 탐지 속도도 높였다"

**What's next:** PyPI 공급망 공격은 이번이 처음이 아니다. MCP 생태계가 빠르게 성장하는 지금, 간접 의존성 자동 검증 도구나 버전 핀 전략이 표준 관행이 될 가능성이 높다.

**Source:** [My minute-by-minute response to the LiteLLM malware attack](https://futuresearch.ai/blog/litellm-attack-transcript/)

---

## 2. 충돌 차량 부품으로 Tesla Model 3 컴퓨터를 책상에서 부팅하기

보안 연구자 xdavidhu는 Tesla 버그 바운티 참가를 위해 eBay에서 충돌 차량 부품을 구매해 Model 3 컴퓨터를 책상 위에서 구동하는 데 성공했다. 핵심 부품인 MCU(Media Control Unit)와 Autopilot 컴퓨터는 iPad 크기, 약 500쪽 책 두께의 수냉식 케이스 형태로 eBay에서 $200–$300에 구할 수 있었다. 터치스크린은 별도로 $175에 구입했고, 전원 공급은 0–30V 가변 DC 파워 서플라이를 사용했으며 최대 8A까지 소비했다. 가장 난관은 케이블이었다 — 대부분의 판매자가 커넥터 직후에서 케이블을 절단해두었기 때문이다. Tesla가 공개한 Electrical Reference 서비스 문서에서 디스플레이 케이블이 6핀(12V·GND 2핀 + 데이터 4핀), Rosenberger 99K10D-1D5A5-D 커넥터를 사용함을 확인했다.

**Why it matters:** Tesla가 배선 다이어그램을 공개 서비스 사이트에 게시한다는 사실은 하드웨어 보안 연구자에게 강력한 레버리지가 된다. orchestration 파이프라인 관점에서, "충돌 차량 → eBay → 책상 위 OS 부팅"이라는 물리적 공격 표면이 소프트웨어 버그 바운티와 교차하는 방식은 embedded system 보안의 현실적 접근법을 보여준다.

- MCU + AP 컴퓨터는 조수석 앞, 글로브박스 뒤편에 위치 — 크기는 iPad, 두께는 ~500쪽 책
- Tesla 공식 서비스 사이트에서 특정 차종·부품 검색 시 배선도·핀맵 공개 확인 가능
- 충돌 차량 부품 재판매 업체들은 동일 차량 부품만 필터링하는 기능까지 제공

**What's next:** 연구자는 실제 버그 바운티 제출 단계로 진행 중이다. Tesla MCU에서 발견될 취약점은 OTA 업데이트 메커니즘이나 Autopilot 연동 부분에서 나올 가능성이 높다.

**Source:** [Running Tesla Model 3's computer on my desk using parts from crashed cars](https://bugs.xdavidhu.me/tesla/2026/03/23/running-tesla-model-3s-computer-on-my-desk-using-parts-from-crashed-cars/)

---

## 3. Apple, Mac Pro 공식 단종 — 후속 제품 계획 없음

Apple이 Mac Pro를 공식 단종했다. 9to5Mac에 따르면 Mac Pro 구매 페이지는 Mac 홈페이지로 리다이렉트되며 모든 관련 항목이 삭제되었고, Apple은 향후 Mac Pro 하드웨어 계획이 없음을 직접 확인했다. 현행 Mac Pro 디자인은 2019년 Pro Display XDR과 함께 출시되었으며, 2023년 6월 M2 Ultra로 업데이트된 이후 M3 Ultra가 탑재된 Mac Studio가 등장할 때까지 $6,999 가격 그대로 방치되었다. Apple의 현재 데스크톱 라인업은 24인치 iMac M4, Mac mini M4/M4 Pro, Mac Studio 세 모델이다. macOS Tahoe 26.2에서 추가된 Thunderbolt 5 기반 RDMA 저지연 기능으로 여러 Mac을 연결하는 방식이 Mac Pro를 대체하는 방향으로 자리잡을 것으로 보인다.

**Why it matters:** portfolio 및 tech-review 사이트 개발 환경으로 Mac Studio M3 Ultra가 사실상의 최상위 Mac이 되었다. Mac Pro가 지원하던 PCIe 확장 슬롯 기반 워크플로우(고성능 GPU, 전문 I/O 카드)는 대안 없이 사라졌으며, 이는 특정 프로덕션 파이프라인에서 Apple Silicon 전환 비용을 높이는 요인이다.

- Mac Studio 최고 사양: M3 Ultra, 32코어 CPU, 80코어 GPU, 256GB 통합 메모리, 16TB SSD
- Pro Display XDR은 Mac Pro보다 먼저 이달 초 단종
- 현재 판매 중인 노트북: MacBook Neo(신규 엔트리), MacBook Air, MacBook Pro

**What's next:** PCIe 확장이 필요한 전문가 시장에서 공백이 생겼다. Thunderbolt 5 RDMA 클러스터링이 고성능 컴퓨팅 수요를 흡수할 수 있는지가 향후 Mac 전략의 핵심 변수다.

**Source:** [Apple discontinues the Mac Pro](https://9to5mac.com/2026/03/26/apple-discontinues-the-mac-pro/)

---

## Comments