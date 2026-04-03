---
layout: post
title: "LinkedIn 브라우저 익스텐션 무단 스캔 폭로, 아르테미스 우주선 Outlook 2개 실행 미스터리, 프로덕션 디스크 풀 사태 실전기"
date: 2026-04-03
lang: ko
permalink: /ko/2026/04/03/daily-tech-review/
pair: 2026-04-03-daily-tech-review
tags: ["hardware", "chips", "datacenter", "cloud", "infrastructure"]
source_type: free-sources
---

## Today in One Line
LinkedIn이 10억 사용자의 브라우저 익스텐션을 무단 스캔해 경쟁사 고객 리스트를 추출하고 있다는 사실이 폭로됐고, NASA 아르테미스 우주선에서는 Outlook이 두 개 동시에 실행 중인 것이 확인됐다.

---

## 1. LinkedIn이 당신의 브라우저를 몰래 스캔하고 있다

Fairlinked e.V.가 운영하는 BrowserGate 캠페인에 따르면, LinkedIn은 사용자가 linkedin.com을 방문할 때마다 숨겨진 코드가 컴퓨터에 설치된 소프트웨어를 검색하고 그 결과를 LinkedIn 서버와 미국-이스라엘 사이버보안 기업을 포함한 제3자에게 전송하고 있다. 사용자는 이를 알지 못하며 동의를 구하지도 않는다. 스캔 대상에는 509개의 구직 도구, 무슬림 신자를 식별하는 익스텐션, 정치 성향을 드러내는 익스텐션, 신경다양성 사용자용 익스텐션이 포함된다.

**Why it matters:** 자동화된 워크플로우와 AI 도구를 브라우저에서 운용하는 개발자라면, 지금 이 순간 LinkedIn이 어떤 도구를 쓰는지 추적하고 있을 가능성이 크다. Apollo, Lusha, ZoomInfo 등 200개 이상의 경쟁 제품을 스캔해 고객사 목록을 수집한다는 것은 단순 프라이버시 침해가 아니라 영업 정보 탈취다. 자동화 파이프라인에서 브라우저 기반 수집 도구를 쓴다면 직접적인 노출 대상이다.

- LinkedIn의 내부 API Voyager는 초당 163,000건을 처리하는 반면, EU에 공개 제출한 규정 준수 API는 초당 0.07건 수준이다
- EU 디지털시장법(DMA) 위반으로 법적 절차가 시작됐다
- LinkedIn은 이미 수집한 데이터를 이용해 서드파티 도구 사용자들에게 직접 경고장을 보낸 바 있다

**What's next:** EU DMA 소송 결과에 따라 플랫폼의 브라우저 접근 범위 전반이 규제 대상이 될 수 있다. Microsoft가 LinkedIn을 통해 어떤 수준의 경쟁사 인텔리전스를 수집해왔는지 전면 감사로 이어질 가능성이 있다.

**Source:** [LinkedIn BrowserGate](https://browsergate.eu/)

---

## 2. 아르테미스 우주선 컴퓨터에서 Outlook 2개가 실행 중 — 이유를 모른다

우주비행사들이 우주선 탑재 컴퓨터에서 Microsoft Outlook 인스턴스가 두 개 동시에 실행되고 있어 휴스턴에 연락했다. NASA는 원격으로 컴퓨터에 접속해 원인을 파악 중이다. 블루스카이에 올라온 Niki Grayson의 게시글로 알려졌으며, 게시 시각은 2026년 4월 2일이다.

**Why it matters:** 우주선 탑재 컴퓨터에서 상용 소프트웨어가 예상치 못한 방식으로 동작하는 사례는 임베디드 시스템의 프로세스 격리 문제를 다시 환기시킨다. 자동화 시스템을 운용할 때도 프로세스 인스턴스 관리는 소프트웨어 레이어가 아닌 하드웨어 수준에서 검증돼야 한다는 것을 극단적으로 보여주는 사례다.

- 우주비행사가 직접 Houston에 보고할 만큼 예상 밖의 상황이었다
- NASA가 원격 접속으로 즉각 대응에 나섰다
- 왜 두 인스턴스가 실행됐는지 원인은 아직 파악되지 않았다

**What's next:** 원인이 소프트웨어 버그인지, 설정 오류인지, 하드웨어 이상인지에 따라 NASA의 우주선 소프트웨어 검증 프로세스 전반이 재검토 대상이 될 수 있다.

**Source:** [Artemis computer running two instances of MS Outlook](https://bsky.app/profile/nikigrayson.com/post/3miik2wzosk25)

---

## 3. 프로덕션 출시 당일 디스크 100% — NixOS 서버 실전 복구기

Hetzner에서 운영하는 4GB RAM, 40GB 디스크의 NixOS 서버가 출시 직후 디스크를 100% 소진해 다운됐다. 2.2GB짜리 디지털 파일을 제공하는 서버였는데, 출시 공지 직후 수백 명이 동시에 접속하면서 공간이 가득 찼다. 주범은 8.5GB의 Plausible Analytics clickhouse 데이터베이스와 15GB의 /nix/store였다.

**Why it matters:** 지식그래프 기반 데이터나 자동화 파이프라인의 로그를 서버에 축적할 때 초기 용량 설계가 얼마나 중요한지를 보여준다. 소규모 VPS에서 여러 서비스를 동시에 운영하면 분석 도구나 빌드 아티팩트가 예상보다 훨씬 빠르게 디스크를 소모한다.

- nix-collect-garbage -d 실행 시 "No space left on device" 오류로 가비지 컬렉션 자체가 불가능한 상황이 됐다
- journalctl --vacuum-time=1s 로 로그를 먼저 정리해 공간을 확보한 뒤 nix store를 정리하는 순서로 복구했다
- Hetzner가 더 큰 인스턴스를 즉시 제공하지 못해 별도 Volume을 추가 구매해 /nix/store를 마운트하는 방식으로 해결했다

**What's next:** 저자는 /nix/store를 별도 볼륨에 마운트하는 구성으로 전환했다. Plausible Analytics 같은 데이터베이스 기반 분석 도구를 소규모 프로덕션 서버에 함께 올릴 때는 별도 스토리지 전략이 필수임을 확인했다.

**Source:** [Running out of Disk Space in Production](https://alt-romes.github.io/posts/2026-04-01-running-out-of-disk-space-on-launch.html)

---

## Comments