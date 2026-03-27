선택 기준: Hardware 주제 우선 → Mac Pro 단종(1위), Tesla MCU 분해(2위), iOS 26 Memory Integrity Enforcement(3위, 하드웨어 보안 기능).

---

```markdown
---
layout: post
title: "Mac Pro 단종, Tesla MCU 책상 위 부팅, iOS 26 메모리 보안"
date: 2026-03-27
lang: ko
permalink: /ko/2026/03/27/daily-tech-review/
pair: 2026-03-27-daily-tech-review
tags: ["hardware", "chips", "datacenter", "cloud", "infrastructure"]
source_type: free-sources
---

## Today in One Line
Apple이 Mac Pro를 조용히 단종시키면서 프로 데스크탑 시장에서 Mac Studio로 라인업을 완전히 재편했다.

---

## 1. Apple, Mac Pro 공식 단종 — "향후 하드웨어 계획 없음"

Apple이 9to5Mac에 Mac Pro 단종을 공식 확인했다. Mac Pro 구매 페이지는 Mac 홈페이지로 리디렉션되며, 모든 제품 레퍼런스가 삭제됐다. Apple은 미래 Mac Pro 하드웨어에 대한 계획이 없다고 명시했다. 현재 Mac Pro 디자인은 2019년 Pro Display XDR과 함께 출시됐고 2023년 6월에 M2 Ultra로 업그레이드됐으나, 이후 M3 Ultra 탑재 Mac Studio가 출시되는 동안에도 $6,999 가격표를 유지하며 방치됐다.

**Why it matters:** tech-review 블로그가 추적하는 하드웨어 라인업 전략의 핵심 변화다. Apple 데스크탑이 iMac(M4), Mac mini(M4/M4 Pro), Mac Studio 3종으로 정리되면서 "확장성 대신 통합 메모리"라는 Apple Silicon 방향성이 최종 확인됐다. 포트폴리오 Tech Review 섹션에서 Apple 칩 전략 흐름을 다룰 때 이 단종을 분기점으로 쓸 수 있다.

- Mac Studio 최상위 사양: M3 Ultra, 32코어 CPU, 80코어 GPU, 256GB 통합 메모리, 16TB SSD
- macOS Tahoe 26.2에서 Thunderbolt 5 RDMA로 복수 Mac 연결 지원 — Mac Pro 역할 대체 수단
- 랩탑 라인업도 MacBook Neo / Air / Pro 3종으로 정리, 역대 가장 명확한 Mac 제품 구조

**What's next:** Mac Studio가 프로 데스크탑 포지션을 흡수하면서 다음 M4 Ultra 탑재 여부가 주목된다. Mac Pro 충성 사용자들의 이탈 방향(Linux 워크스테이션, Windows)도 관전 포인트다.

**Source:** [Apple discontinues the Mac Pro](https://9to5mac.com/2026/03/26/apple-discontinues-the-mac-pro/)

---

## 2. Tesla Model 3 MCU를 $500 미만으로 책상 위에서 부팅하다

보안 연구자 David Hu가 eBay에서 사고 차량 부품을 모아 Tesla Model 3의 차량용 컴퓨터를 책상 위에서 부팅하는 데 성공했다. MCU(Media Control Unit)와 오토파일럿 컴퓨터(AP)가 적층된 이 유닛은 iPad 크기에 500페이지 두께 책 정도로, eBay에서 $200~$300에 구할 수 있었다. 전체 세팅은 12V DC 파워서플라이, $175짜리 터치스크린, 디스플레이 케이블로 구성됐으며 피크 시 최대 8A를 소비했다.

**Why it matters:** Tesla가 모든 차량의 배선 "Electrical Reference"를 공개 서비스 사이트에서 제공한다는 사실 자체가 흥미롭다. 디스플레이 연결에 6핀 케이블(12V/GND 2핀 + 데이터 4핀, Rosenberger 99K10D-1D5A5-D 커넥터)을 쓴다는 스펙까지 공개돼 있다. 차량 보안 연구의 진입 장벽이 하드웨어 접근성과 직결된다는 점에서, 임베디드·보안 하드웨어 방향에 관심 있는 Paul 프로젝트의 아이디에이션 소재가 된다.

- MCU 단독 부팅 후 화면 없이도 차량 OS가 기동됨 — 레드 LED 점등으로 확인
- Rosenberger 커넥터는 소량 구매 불가, BMW LVDS 케이블이 핀 호환 대안으로 발견됨
- 연구 목적은 Tesla 버그 바운티 프로그램 참여 — 실제 하드웨어 없이는 취약점 발견 불가

**What's next:** MCU 부팅 이후 오토파일럿 컴퓨터와 통신하는 프로토콜 분석 및 실제 취약점 발굴이 이어질 전망이다. 차량용 임베디드 보안 연구의 저비용 진입 방법론으로 주목받을 것이다.

**Source:** [Running Tesla Model 3's computer on my desk using parts from crashed cars](https://bugs.xdavidhu.me/tesla/2026/03/23/running-tesla-model-3s-computer-on-my-desk-using-parts-from-crashed-cars/)

---

## 3. iOS 26 Memory Integrity Enforcement vs. 유출된 스파이웨어 툴

Google, iVerify, Lookout의 연구자들이 Coruna와 DarkSword라는 해킹 툴이 전 세계 피해자를 광범위하게 노리고 있음을 문서화했다. 이 툴들이 최근 온라인에 유출돼 누구나 구버전 iOS 사용자를 공격할 수 있는 상황이 됐다. 공격자에는 러시아 스파이와 중국 사이버 범죄자가 포함되며, 해킹된 웹사이트나 가짜 페이지를 통해 대량 피해자를 노린다.

**Why it matters:** 하드웨어 수준의 보안 분기가 시작됐다. iPhone 17 + iOS 26의 Memory Integrity Enforcement는 메모리 손상 버그를 차단하도록 설계됐으며, DarkSword가 바로 이 메모리 손상 버그에 의존했다. 즉, 최신 하드웨어를 쓰는 사용자와 구형 기기 사용자 사이에 사실상 보안 계층이 두 개로 나뉜다. 하드웨어-소프트웨어 통합 보안 설계의 중요성을 보여주는 사례로, Apple Silicon 전략 분석에서 직접 인용할 수 있다.

- Memory Integrity Enforcement: iOS 26 + iPhone 17 전용 — 이전 모델은 동일 OS 업데이트에도 미적용
- iOS 18 이하 또는 구형 기기 사용자는 메모리 기반 익스플로잇에 여전히 노출
- Apple의 대응 전략: 최신 모델용 메모리 안전 코드 + Lockdown Mode (제한적 적용)

**What's next:** 구형 iPhone 보유자가 많은 시장에서 Coruna/DarkSword 파생 공격이 확산될 위험이 있다. Apple이 구형 기기 지원 종료를 언제 공식화하느냐가 다음 변수다.

**Source:** [Apple made strides with iOS 26 security, but leaked hacking tools still leave millions exposed to spyware attacks](https://techcrunch.com/2026/03/26/apple-made-strides-with-ios-26-security-but-leaked-hacking-tools-still-leave-millions-exposed-to-spyware-attacks/)

---

## Comments