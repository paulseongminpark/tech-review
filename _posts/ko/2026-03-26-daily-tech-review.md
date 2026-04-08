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
오늘은 기술 업계 거물이 아니라 개발자들의 목소리가 주인공이었다. 전직 CircleCI 초기 직원이 세계에서 가장 부유한 회사가 만든 CI 도구를 정면 비판했고, 마이크로커널 OS 연구자는 커널에서 유저스페이스로 권한을 이전하는 실험을 조용히 진전시켰으며, 750페이지짜리 인간 작성 기술 가이드가 커뮤니티를 뜨겁게 달궜다. 세 소식 모두 "편의성"이라는 이름 아래 누적된 기술 부채에 대한 반응이다.

---

## 1. GitHub Actions가 엔지니어링 팀을 서서히 죽이고 있다

전직 CircleCI 초기 직원 Ian Duncan이 쓴 GitHub Actions 직격 비판글이다. Jenkins, Travis, CircleCI, Semaphore, Drone, Concourse, TeamCity, Bamboo, GitLab CI, CodeBuild 등 실전에서 거의 모든 CI 시스템을 직접 사용한 경험을 바탕으로 "GitHub Actions는 좋지 않다. 그냥 평범하지도 않다. 인기의 유일한 이유는 레포지토리에 바로 붙어있다는 것"이라고 단언한다. 그 근거는 구체적이다. 로그 뷰어가 크롬을 반복적·안정적으로 크래시시키고, 대용량 로그에서는 스크롤바 자체가 작동하지 않아 raw 로그를 텍스트 에디터로 열어야 하는 상황이 일상적으로 발생한다. 뒤로가기 버튼은 PR로 돌아가지 않고 무작위 페이지로 이동하는 "룰렛 휠"이다. 그는 이 모든 것을 "2025년에 세계에서 가장 부유한 기업 중 하나가 만든 제품"이라며 꼬집는다. 대안으로는 Nix 환경에서 YAML 설정 없이 flake를 보고 빌드를 자동 판단하는 Garnix를 제시하고, 최종 추천은 Buildkite다.

**Why it matters:** 체크 요약에서 워크플로우 런, 잡, 스텝까지 4번을 클릭해야 실패 원인에 도달하는 구조는 단순한 UX 불편이 아니다. 지속적으로 돌아가는 자동화 시스템에서 빌드 실패를 추적하는 시간이 축적되면 운영 비용이 된다. GitHub Actions의 시장 지배력이 편의성에만 기반한다면, 그 편의성이 사라지는 순간 대안 생태계로의 이동 속도는 예상보다 빠를 수 있다.

- 로그 뷰어 크래시는 한 번이 아니라 반복적·안정적으로 발생한다는 점이 핵심이다
- Garnix는 Nix 환경에서 flake를 읽고 빌드 여부를 자동 판단한다 — YAML 설정이 필요 없다

**What's next:** 저자는 Buildkite를 "CI가 느껴져야 하는 것"으로 추천한다. GitHub Actions 점유율이 편의성에 기반한 것인 만큼, 대안 생태계로의 이동이 본격화될 가능성이 있다.

**Source:** [GitHub Actions Is Slowly Killing Your Engineering Team](https://www.iankduncan.com/engineering/2026-02-05-github-actions-killing-your-team)

---

GitHub Actions가 편의성의 함정을 드러낸다면, Redox OS는 그 반대편에서 불편하더라도 올바른 구조를 향해 한 발씩 나아가고 있다.

## 2. Redox OS, 캐퍼빌리티로 네임스페이스를 커널 밖으로 꺼냈다

Ibuki Omatsu가 NGI Zero Commons와 NLnet 지원으로 진행 중인 "Redox OS 캐퍼빌리티 기반 보안" 프로젝트 업데이트다. Redox OS는 파일시스템·프로세스 매니저 등 대부분 컴포넌트가 유저스페이스 별도 프로그램으로 실행되는 마이크로커널 OS로, 모든 리소스는 /scheme/{scheme-name}/{resource-name} 형식의 Scheme 경로로 접근한다. 이번 업데이트에서는 기존에 커널이 정수 ID로 바인딩해 관리하던 네임스페이스를 유저스페이스로 이전하고, 문자열 기반이던 CWD를 캐퍼빌리티로 재구현했다. 네임스페이스가 Scheme 가시성을 제어하는 구조여서, file과 uds 네임스페이스에 속하면 네트워크 스택에는 접근할 수 없다. relibc의 redox-rt가 POSIX 호환 레이어를 제공하며, Redox에서 스레드와 프로세스는 파일 디스크립터로 관리된다.

**Why it matters:** 권한의 경계를 커널이 아닌 유저스페이스에서 명시적으로 정의한다는 것은, 누가 어디에 접근할 수 있는지를 설계 단계에서 강제한다는 뜻이다. 이 접근은 모놀리식 커널에서 수십 년간 쌓인 묵시적 권한 구조를 뒤집는 시도다. 실용적 구현 사례가 드문 영역에서 Redox가 조금씩 경계를 확인해가고 있다는 점 자체가 주목할 만하다.

- Scheme은 유저스페이스 서비스로, 모든 리소스 접근이 scheme/{scheme-name}/{resource-name} 경로를 통해 이뤄진다
- file·uds 네임스페이스에 속하면 네트워크 스택 접근이 차단된다 — 가시성 제어가 네임스페이스 단위로 작동한다

**What's next:** 커널에서 유저스페이스로의 권한 이전이 완성되면 프로세스 격리가 강화될 전망이다. 마이크로커널 OS의 실용적 구현 사례로 학술적·산업적 주목도 모두 높다.

**Source:** [Capability-Based Security for Redox: Namespace and CWD as Capabilities](https://www.redox-os.org/news/nlnet-cap-nsmgr-cwd/)

---

구조적 올바름을 추구하는 OS 연구가 있는가 하면, 같은 날 커뮤니티에서는 훨씬 직접적인 신호가 터져 나왔다.

## 3. "AI 슬롭 없음" — 750페이지 프로덕션 셀프호스팅 가이드

r/SelfHosted에 등장한 750페이지짜리 프로덕션 셀프호스팅 가이드가 스코어 1498, 153개 댓글을 기록하며 폭발적 반응을 이끌어냈다. 분량보다 더 주목받은 것은 제목에 명시된 "NO AI SLOP"이다. AI 생성 콘텐츠가 기술 문서 시장을 빠르게 채우는 시기에, 인간이 직접 쓴 750페이지짜리 가이드가 커뮤니티에서 이 정도 반응을 이끌어냈다는 것은 수요가 어디 있는지를 보여준다. 가이드는 프로덕션 앱 셀프호스팅 전반을 다루는 종합 문서로, "NO AI SLOP" 태그가 커뮤니티 신호로 작동했다.

**Why it matters:** 콘텐츠의 품질이 아니라 생산 방식이 신뢰의 기준이 되기 시작했다. "NO AI SLOP"은 선언이자 필터다. 이 태그가 스코어 1498을 만들어냈다면, 출처 명시가 기술 문서의 신뢰도 지표로 자리잡는 속도는 예상보다 빠를 것이다.

- 750페이지 분량으로 프로덕션 앱 셀프호스팅 전반을 다룬다
- r/SelfHosted에서 스코어 1498, 153개 댓글로 높은 참여율을 기록했다

**What's next:** AI 생성 기술 문서가 넘쳐날수록 검증된 인간 작성 콘텐츠를 큐레이션하는 채널의 가치가 올라갈 것이다. 품질 신호로서 "출처 명시"의 중요성이 커진다.

**Source:** [Free 750-page guide to self-hosting production apps - NO AI SLOP](https://i.redd.it/unvl3nq1okrg1.jpeg)

---

## Comments
