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
LinkedIn이 10억 사용자의 브라우저를 무단으로 스캔해 경쟁사 고객 리스트를 추출하고 있다는 사실이 BrowserGate 캠페인으로 폭로됐다. 같은 날, NASA 아르테미스 우주선 탑재 컴퓨터에서는 Microsoft Outlook 인스턴스 두 개가 동시에 실행 중인 것이 확인돼 우주비행사가 휴스턴에 직접 보고했다. 감시와 예측 불가능성이라는 두 가지 불편한 진실이 하루에 겹쳐 드러난 날이다.

---

## 1. LinkedIn이 당신의 브라우저를 몰래 스캔하고 있다

Fairlinked e.V.가 운영하는 BrowserGate 캠페인은 LinkedIn이 사용자 모르게 수행해온 것을 문서로 정리해 공개했다. linkedin.com을 방문하는 순간, 숨겨진 코드가 컴퓨터에 설치된 소프트웨어를 조용히 훑는다. 그 결과는 LinkedIn 서버와 미국-이스라엘 사이버보안 기업을 포함한 제3자에게 전송되며, 사용자에게는 동의를 구하지 않는다.

스캔 대상 목록은 509개의 구직 도구에서 시작해 무슬림 신자를 식별하는 익스텐션, 정치 성향을 드러내는 익스텐션, 신경다양성 사용자용 익스텐션까지 포함한다. Apollo, Lusha, ZoomInfo를 비롯한 200개 이상의 경쟁 제품이 타깃이다. LinkedIn의 내부 API인 Voyager는 초당 163,000건을 처리하는 반면, EU에 규정 준수용으로 공개 제출한 API는 초당 0.07건 수준이다. 숫자가 말해주는 격차는 API 성능 차이가 아니라 의도의 차이다. LinkedIn은 이미 수집한 데이터를 이용해 서드파티 도구 사용자들에게 직접 경고장을 보낸 바 있으며, EU 디지털시장법(DMA) 위반으로 법적 절차가 시작됐다.

**Why it matters:** 이것은 단순한 프라이버시 침해가 아니다. 경쟁사 도구를 쓰는 사용자를 식별해 그 데이터를 영업 인텔리전스로 활용하는 것은 정보 탈취에 가깝다. 플랫폼이 사용자의 브라우저를 감시 도구로 전용할 수 있다는 사실은, 어떤 서비스에 로그인하는 순간 어떤 데이터가 빠져나가는지 사용자 스스로 알 수 없다는 구조적 문제를 드러낸다.

- EU DMA 위반으로 법적 절차가 시작됐으며, 소송 결과에 따라 플랫폼의 브라우저 접근 범위 전반이 규제 대상이 될 수 있다
- Microsoft가 LinkedIn을 통해 어떤 수준의 경쟁사 인텔리전스를 수집해왔는지 전면 감사로 이어질 가능성이 있다

**What's next:** EU DMA 소송 결과에 따라 플랫폼의 브라우저 접근 범위 전반이 규제 대상이 될 수 있다. Microsoft가 LinkedIn을 통해 어떤 수준의 경쟁사 인텔리전스를 수집해왔는지 전면 감사로 이어질 가능성이 있다.

**Source:** [LinkedIn BrowserGate](https://browsergate.eu/)

---

브라우저 스캔이 상업적 감시라면, 다음 이야기는 예측 불가능한 소프트웨어 동작이 지구 밖에서 발생한 경우다.

## 2. 아르테미스 우주선 컴퓨터에서 Outlook 2개가 실행 중 — 이유를 모른다

2026년 4월 2일, 블루스카이에 Niki Grayson의 게시글이 올라왔다. 아르테미스 우주선 탑재 컴퓨터에서 Microsoft Outlook 인스턴스가 두 개 동시에 실행 중이라는 내용이었다. 우주비행사들은 직접 Houston에 연락해 상황을 보고했고, NASA는 원격으로 컴퓨터에 접속해 원인 파악에 나섰다.

이 사건이 주목받는 이유는 단순히 소프트웨어가 오작동했기 때문이 아니다. 우주선 탑재 컴퓨터에서 상용 소프트웨어 인스턴스가 두 개 떠 있다는 사실 자체보다, 그것이 왜 그렇게 됐는지 아직 아무도 모른다는 점이 더 중요하다. 소프트웨어 버그인지, 설정 오류인지, 하드웨어 이상인지 원인은 여전히 파악되지 않았다. 우주비행사가 직접 Houston에 보고할 만큼 예상 밖의 상황이었다.

**Why it matters:** 검증된 환경에서도 예상치 못한 프로세스 동작이 발생할 수 있다는 것은, 어디서나 통하는 교훈이다. 프로세스 상태를 소프트웨어 레이어가 아닌 외부 관찰 수단으로 검증해야 한다는 원칙이 지구 밖에서도 동일하게 적용된다.

- 원인이 소프트웨어 버그인지, 설정 오류인지, 하드웨어 이상인지 아직 파악되지 않았다
- NASA가 원격 접속으로 즉각 대응에 나섰다

**What's next:** 원인 분석 결과에 따라 NASA의 우주선 소프트웨어 검증 프로세스 전반이 재검토 대상이 될 수 있다.

**Source:** [Artemis computer running two instances of MS Outlook](https://bsky.app/profile/nikigrayson.com/post/3miik2wzosk25)

---

예측 불가능성은 우주에서만 일어나는 일이 아니다. 출시 당일, 지상의 서버에서도 완전히 다른 형태의 위기가 터졌다.

## 3. 프로덕션 출시 당일 디스크 100% — NixOS 서버 실전 복구기

Hetzner에서 운영하는 NixOS 서버의 스펙은 4GB RAM, 40GB 디스크였다. 이 서버의 역할은 2.2GB짜리 디지털 파일을 제공하는 것이었고, 출시 공지가 올라가자 수백 명이 동시에 접속했다. 디스크는 순식간에 100%를 찍었다. 주범은 두 곳이었다. 8.5GB에 달하는 Plausible Analytics의 clickhouse 데이터베이스와 15GB를 차지한 /nix/store였다.

문제는 디스크가 가득 찼다는 것 자체가 아니라, 그 상태에서 복구 도구 자체가 작동하지 않는다는 점이었다. nix-collect-garbage -d를 실행하면 "No space left on device" 오류가 떴다. 가비지 컬렉션을 돌릴 공간이 없어서 공간을 확보할 수 없는 순환이었다. 해법은 순서에 있었다. journalctl --vacuum-time=1s로 로그를 먼저 정리해 최소한의 공간을 확보한 뒤, nix store를 정리하는 순서로 복구했다. Hetzner가 더 큰 인스턴스를 즉시 제공하지 못한 상황에서, 결국 별도 Volume을 추가 구매해 /nix/store를 마운트하는 방식으로 해결했다.

**Why it matters:** 디스크 복구에 디스크 공간이 필요한 상황은 처음 마주하면 당황스럽다. 소규모 VPS에서 여러 서비스를 동시에 올릴 때 분석 도구나 빌드 아티팩트가 예상보다 훨씬 빠르게 디스크를 소모한다는 것, 그리고 그 상황에서 복구 순서가 틀리면 도구가 먹통이 된다는 것은 한 번 겪어야 체감이 된다.

- nix-collect-garbage -d가 "No space left on device"로 막혔을 때, journalctl --vacuum-time=1s로 로그를 먼저 정리해 공간을 확보하는 순서가 핵심이었다
- Plausible Analytics 같은 데이터베이스 기반 분석 도구를 소규모 프로덕션 서버에 함께 올릴 때는 별도 스토리지 전략이 필수다

**What's next:** 저자는 /nix/store를 별도 볼륨에 마운트하는 구성으로 전환했다. 출시 전 용량 설계와 스토리지 분리 전략이 소규모 프로덕션 환경에서도 선택이 아닌 필수임을 확인했다.

**Source:** [Running out of Disk Space in Production](https://alt-romes.github.io/posts/2026-04-01-running-out-of-disk-space-on-launch.html)

---

## Comments
