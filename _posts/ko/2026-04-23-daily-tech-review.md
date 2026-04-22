---
layout: post
title: "GitHub CLI가 당신을 관찰하기 시작했다, Dropbox가 87GB짜리 모노레포를 20GB로 줄인 방법, Gleam 모노레포를 GitHub Actions로 돌리는 법"
date: 2026-04-23
lang: ko
permalink: /ko/2026/04/23/daily-tech-review/
pair: 2026-04-23-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
source_type: free-sources
---

## Today in One Line

오늘 오픈소스 생태계에서 눈에 띄는 신호가 세 갈래로 들어왔다. 신뢰받던 CLI 도구가 조용히 사용자 추적을 시작했고, 수십 GB로 불어난 모노레포를 플랫폼 레이어에서 해결하는 사례가 나왔으며, 다중 런타임을 타깃하는 소형 오픈소스 프로젝트가 CI 복잡성과 씨름하는 방법이 공유됐다. 공통된 질문은 하나다: 오픈소스 도구는 규모와 신뢰 사이에서 어디에 서야 하는가.

---

## 1. GitHub CLI가 당신을 관찰하기 시작했다

GitHub CLI는 터미널에서 PR을 열고 이슈를 닫는 데 쓰는 오픈소스 도구다. 소스가 공개되어 있고, 동작을 예측할 수 있고, 별다른 설명 없이도 믿고 쓸 수 있다는 것이 이 도구의 암묵적 가치였다. 그런데 GitHub는 최근 이 CLI에 수도익명(pseudoanonymous) 텔레메트리를 도입했다. 이유는 공식 문서에 명시되어 있다: "에이전틱 채택이 늘어나면서 기능이 실제로 어떻게 쓰이는지 파악해야 한다. 새 서브커맨드를 출시했을 때 아무도 쓰지 않는다면, 우리는 그 기능을 다시 검토해야 한다는 걸 알아야 한다." 논리는 타당하다. 그러나 오픈소스 도구에 텔레메트리가 들어간다는 사실 자체가 불편한 선례를 만든다. "수도익명"이 정확히 어떤 수준의 익명인지, 데이터가 어디까지 흘러가는지는 아직 명확하지 않다.

**Why it matters:** 오픈소스의 신뢰는 소스가 열려 있다는 사실에서 온다. 거기에 텔레메트리가 더해지는 순간, 그 신뢰는 "도구가 내 행동을 수집한다"는 동의 없는 계약으로 바뀐다. 기능 개선이 목적이라는 명분은 정당하지만, 이미 수많은 도구들이 같은 이유로 추적을 시작했고 그 축적이 문제가 됐던 역사가 있다. 오픈소스 CLI에서 이 결정이 내려진다는 건, 에코시스템 전반에 신호를 보내는 일이다.

- 텔레메트리는 기본 활성화 상태이며 opt-out 방식으로 운영된다
- 수집 목적은 기능 우선순위 결정과 실제 채택률 평가

**What's next:** opt-out 메커니즘의 구체적인 구현과 데이터 보존 정책이 공개되지 않으면 커뮤니티 반발이 이어질 가능성이 있다. 다른 오픈소스 CLI 도구들에 선례가 될 것이다.

**Source:** [GitHub CLI Telemetry](https://cli.github.com/telemetry)

---

텔레메트리가 도구가 사용자를 관찰하는 문제라면, 다음은 도구 자체가 규모를 감당하지 못하게 된 문제다.

## 2. Dropbox가 87GB짜리 Git 모노레포를 20GB로 줄인 방법

Git은 본래 소규모 프로젝트를 위해 설계됐다. 수년간 코드가 쌓이고 바이너리가 들어오고 히스토리가 누적되면, 어느 순간 클론 한 번에 몇 분이 걸리고 CI 시간이 폭발한다. Dropbox는 그 임계점을 넘었다. 모노레포가 87GB까지 불어난 것이다. Dropbox는 이 문제를 GitHub 엔지니어링 팀과 직접 협업해 해결했고, 결과는 20GB였다. 약 77%를 줄인 셈이다. 세부 기술은 공개된 기사에서 모두 다루지 않지만, 이 숫자가 전달하는 메시지는 분명하다: 모노레포 스케일 문제는 이제 개별 팀이 혼자 해결할 수 없는 영역에 들어서고 있고, 플랫폼 제공자와의 협업이 실질적인 해결 경로가 되고 있다.

**Why it matters:** 모노레포 논쟁은 수년째 계속됐지만, 87GB라는 숫자는 논쟁이 아니라 공학적 현실이다. Git sparse checkout, partial clone, object storage 연동 같은 기술이 존재하지만, 이를 실제로 대규모 레포에 적용해 검증된 사례는 드물다. Dropbox와 GitHub의 협업이 공개 레퍼런스로 자리잡으면, 같은 문제를 겪는 조직에 실질적인 참조점이 된다.

- 협업 대상은 GitHub 엔지니어링 팀 직접
- 87GB에서 20GB로, 약 77% 용량 감소

**What's next:** Git 모노레포 스케일 솔루션이 플랫폼 레이어로 이동하는 흐름이 가속될 것이다. 이 사례의 기술 상세가 공개될 경우 업계 표준 참조 사례가 될 가능성이 있다.

**Source:** [Dropbox Collaborates with GitHub to Reduce Monorepo Size from 87GB to 20GB](https://www.infoq.com/news/2026/04/dropbox-reduces-git-optimization/)

---

대형 조직이 플랫폼 레이어에서 모노레포 문제를 해결하는 동안, 작은 오픈소스 프로젝트는 다중 런타임이라는 다른 차원의 복잡성과 씨름한다.

## 3. Gleam 모노레포를 GitHub Actions로 돌리는 법

Gleam은 Erlang BEAM 위에서 돌아가는 정적 타입 함수형 언어다. 이 언어로 만든 EYG라는 스크립팅 언어 프로젝트는 "더 나은 bash"를 목표로 하며, 12개 이상의 패키지로 구성된 모노레포로 운영된다. 패키지마다 타깃 런타임이 다르다. 일부는 BEAM, 일부는 Bun(JavaScript), 일부는 양쪽 모두를 지원한다. 이 복잡성을 하나의 GitHub Actions 워크플로우로 처리하는 방식이 공개됐다. 핵심은 런타임별 job 분리와 matrix 전략이다. test-beam과 test-bun으로 job을 나누고, 각 job에 Gleam 버전과 패키지 목록을 matrix로 주입한다. 여기서 fail-fast: false 설정이 결정적이다. 이걸 켜두지 않으면 한 패키지가 실패했을 때 나머지 실행이 모두 취소되어 어떤 다른 패키지가 깨졌는지 볼 수 없게 된다. 검사 기준도 엄격하다. warnings-as-errors로 컴파일러 경고를 CI 실패 조건으로 처리하고, format --check로 포맷 불일치도 push 단계에서 잡는다.

**Why it matters:** 다중 런타임을 타깃하는 오픈소스 프로젝트의 CI는 설계를 잘못하면 실패 지점이 뒤엉킨다. 이 사례는 matrix를 통해 각 패키지-런타임 조합을 독립 라인으로 만들어 visibility를 확보하는 방법을 보여준다. Gleam 1.16.0 릴리즈 후보를 matrix에 추가해 미리 호환성을 검사하는 방식은, 소형 오픈소스 프로젝트가 릴리즈 품질을 유지하는 실용적인 전략이다.

- fail-fast: false로 부분 실패 시에도 전체 CI 결과 가시성 확보
- warnings-as-errors: 로컬 개발에선 경고를 허용하되 push 이후엔 0개 강제

**What's next:** Gleam 1.16.0 릴리즈 후보 주기가 진행 중이다. sans-io 패턴으로 런타임 독립성을 확보하는 접근에 대한 후속 글이 예고되어 있다.

**Source:** [GitHub Actions for a Gleam monorepo](https://crowdhailer.me/2026-04-21/github-actions-for-a-gleam-monorepo/)

---

## Comments

