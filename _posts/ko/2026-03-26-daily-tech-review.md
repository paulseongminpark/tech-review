---
layout: post
title: "GitHub Actions의 치명적 결함, Redox OS 캐퍼빌리티 보안, 750페이지 셀프호스팅 가이드"
date: 2026-03-26
lang: ko
permalink: /ko/2026/03/26/daily-tech-review/
pair: 2026-03-26-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
source_type: free-sources
---

## Today in One Line
전직 CircleCI 직원이 GitHub Actions를 정면 비판하고, Redox OS는 캐퍼빌리티로 커널 의존성을 줄이며, 750페이지짜리 인간 작성 셀프호스팅 가이드가 커뮤니티를 달궜다.

---

## 1. GitHub Actions가 엔지니어링 팀을 서서히 죽이고 있다

전직 CircleCI 초기 직원 Ian Duncan이 GitHub Actions를 직격 비판한 글이다. Jenkins, Travis, CircleCI, Semaphore, Drone, Concourse, TeamCity, Bamboo, GitLab CI, CodeBuild 등 거의 모든 CI 시스템을 실전 사용한 경험을 바탕으로 "GitHub Actions는 좋지 않다. 그냥 평범하지도 않다. 인기의 유일한 이유는 레포지토리에 바로 붙어있다는 것"이라고 단언한다. 특히 로그 뷰어가 크롬을 반복적·안정적으로 크래시시키며, 대용량 로그에서는 스크롤바 자체가 작동하지 않아 raw 로그를 텍스트 에디터로 열어야 하는 상황을 "2025년에 세계에서 가장 부유한 기업 중 하나가 만든 제품"이라며 꼬집는다.

**Why it matters:** 자동화 파이프라인을 직접 구축·운영하는 Paul의 관점에서 UI 구조 하나가 디버깅 비용을 어떻게 올리는지 보여주는 사례다. 자동 뉴스 파이프라인이나 메모리 서버 자동 실행처럼 지속적으로 돌아가는 시스템에서 빌드 실패 원인을 추적하려면 체크 요약 → 워크플로우 런 → 잡 → 스텝까지 4번 클릭해야 하는 구조는 실질적인 운영 비용이다.

- 로그 뷰어가 크롬을 크래시시키는 것은 한 번이 아니라 반복적·안정적으로 발생한다
- 뒤로가기 버튼은 "룰렛 휠"이다 — PR로 돌아가지 않고 무작위 페이지로 이동한다
- Nix 환경에는 YAML 설정이 필요 없는 Garnix를 대안으로 제시한다 — flake를 보고 빌드할 것을 자동 판단한다

**What's next:** 저자는 Buildkite를 "CI가 느껴져야 하는 것"으로 추천한다. GitHub Actions 점유율이 편의성에 기반한 것인 만큼, 대안 생태계로의 이동이 본격화될 가능성이 있다.

**Source:** [GitHub Actions Is Slowly Killing Your Engineering Team](https://www.iankduncan.com/engineering/2026-02-05-github-actions-killing-your-team)

---

## 2. Redox OS, 캐퍼빌리티로 네임스페이스를 커널 밖으로 꺼냈다

Ibuki Omatsu가 NGI Zero Commons와 NLnet 지원으로 진행 중인 "Redox OS 캐퍼빌리티 기반 보안" 프로젝트 업데이트다. 기존에 커널이 정수 ID로 바인딩해 관리하던 네임스페이스를 유저스페이스로 이전하고, 문자열 기반이던 CWD를 캐퍼빌리티로 재구현했다. Redox OS는 마이크로커널 OS로 파일시스템·프로세스 매니저 등 대부분 컴포넌트가 유저스페이스 별도 프로그램으로 실행되며, 모든 리소스는 /scheme/{scheme-name}/{resource-name} 형식의 Scheme 경로로 접근한다.

**Why it matters:** 지식그래프 메모리의 4685개 이상 노드처럼 복잡한 권한 경계를 다루는 시스템에서 캐퍼빌리티 모델은 중요한 설계 원칙이다. Redox의 네임스페이스 가시성 제어 방식 — file과 uds 네임스페이스에 속하면 네트워크 스택에는 접근 불가 — 은 Paul이 파이프라인에서 각 에이전트의 접근 범위를 명시적으로 정의하는 방식과 구조적으로 유사하다.

- Scheme은 유저스페이스 서비스로, 모든 리소스 접근이 scheme/{scheme-name}/{resource-name} 경로를 통해 이뤄진다
- 네임스페이스가 Scheme 가시성을 제어한다 — file, uds 네임스페이스라면 네트워크 스택에는 접근 불가다
- relibc의 redox-rt가 POSIX 호환 레이어를 제공하며, Redox에서 스레드와 프로세스는 파일 디스크립터로 관리된다

**What's next:** 커널에서 유저스페이스로의 권한 이전이 완성되면 프로세스 격리가 강화될 전망이다. 마이크로커널 OS의 실용적 구현 사례로 학술적·산업적 주목도 모두 높다.

**Source:** [Capability-Based Security for Redox: Namespace and CWD as Capabilities](https://www.redox-os.org/news/nlnet-cap-nsmgr-cwd/)

---

## 3. "AI 슬롭 없음" — 750페이지 프로덕션 셀프호스팅 가이드

r/SelfHosted에 등장한 750페이지짜리 프로덕션 셀프호스팅 가이드가 스코어 1498, 153개 댓글을 기록하며 폭발적 반응을 이끌어냈다. 제목에 "NO AI SLOP"을 명시한 점이 핵심이다 — AI 생성 콘텐츠 홍수 속에서 인간이 직접 작성한 고품질 기술 문서에 대한 수요가 여전히 강하다는 신호다.

**Why it matters:** 자동 뉴스 파이프라인에서 소스 신뢰도를 평가할 때 "NO AI SLOP" 같은 명시적 태그가 커뮤니티 큐레이션 신호로 기능하기 시작했다는 점이 중요하다. 현재 파이프라인의 소스 필터링 기준에 콘텐츠 출처 신뢰도 지표를 추가하는 근거가 된다.

- 750페이지 분량으로 프로덕션 앱 셀프호스팅 전반을 다루는 종합 가이드다
- r/SelfHosted에서 스코어 1498, 153개 댓글로 높은 참여율을 기록했다
- "NO AI SLOP" 명시는 인간 작성 콘텐츠에 대한 커뮤니티의 명시적 선호를 공개적으로 드러낸 것이다

**What's next:** AI 생성 기술 문서가 넘쳐날수록 검증된 인간 작성 콘텐츠를 큐레이션하는 채널의 가치가 올라갈 것이다. 품질 신호로서 "출처 명시"의 중요성이 커진다.

**Source:** [Free 750-page guide to self-hosting production apps - NO AI SLOP](https://i.redd.it/unvl3nq1okrg1.jpeg)

---

## Comments