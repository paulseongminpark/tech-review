---
layout: post
title: "Cal.com 코드 비공개화의 교훈, Xata 오픈소스 Postgres, GitHub Stacked PRs"
date: 2026-04-16
lang: ko
permalink: /ko/2026/04/16/daily-tech-review/
pair: 2026-04-16-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
source_type: free-sources
---

## Today in One Line
오픈소스에 관한 오래된 계약이 흔들리고 있다. Cal.com이 AI 위협을 이유로 코드를 비공개 전환하겠다고 발표한 같은 날, Xata는 오픈소스 Postgres 플랫폼을 공개하고 GitHub은 협업 방식 자체를 재설계하는 새 도구를 내놓았다. 오픈소스가 죽어가고 있다는 진단과, 오픈소스로만 가능한 것들이 동시에 뉴스를 채우는 하루다.

---

## 1. Cal.com이 코드를 닫는다, 그리고 그 오해에 대하여

Cal.com이 오픈소스 코드를 비공개로 전환하겠다고 밝혔다. 이유는 AI 위협이다. 자신들의 코드베이스가 경쟁 제품을 만드는 데 활용된다는 것이다. 이에 대해 Strix는 제목부터 단호하게 반박한다. "오픈소스는 죽지 않았다. Cal.com이 잘못된 교훈을 얻은 것이다." AI 시대에 오픈소스 기업이 직면하는 딜레마는 실재한다. 코드를 공개하면 기여와 신뢰를 얻지만, 동시에 자신의 코드베이스가 경쟁자의 학습 데이터가 된다. Cal.com의 선택은 이 긴장을 라이선스 전략이나 커뮤니티 육성이 아닌, 벽을 세우는 방식으로 해소하려 했다는 점에서 비판을 받는다. 오픈소스의 가치는 코드 자체가 아니라, 그 코드를 중심으로 형성된 신뢰와 가시성에 있기 때문이다.

**Why it matters:** AI가 오픈소스 코드를 학습 데이터로 사용하는 문제는 Cal.com만의 이야기가 아니다. 이 결정이 하나의 선례로 굳어지면, 오픈소스 생태계의 공유 지식이 단계적으로 벽 뒤로 숨는 흐름이 가속될 수 있다. 비공개 전환이 AI 위협에 대한 진짜 해법인지, 아니면 오픈소스가 가진 가장 큰 자산을 포기하는 것인지에 대한 판단을 커뮤니티 전체가 요구받고 있다.

- 비공개 전환은 단기 보호처럼 보이지만, 커뮤니티 이탈과 포크 발생으로 이어질 수 있다.
- AI 학습 데이터 문제를 다루는 현실적 대안으로 라이선스 변경이 더 주목받고 있다.

**What's next:** Cal.com의 결정이 유사한 포지션의 오픈소스 스타트업들에게 어떤 영향을 줄지, 그리고 커뮤니티가 어떻게 반응할지 지켜봐야 한다.

**Source:** [Open Source Isn't Dead. Cal.com Just Learned the Wrong Lesson](https://www.strix.ai/blog/cal-com-is-closing-its-code-due-to-ai-threats)

---

한쪽에서 오픈소스의 경계가 좁아지는 동안, 다른 한쪽에서는 새로운 오픈소스 인프라가 조용히 공개됐다.

## 2. Xata: 오픈소스 Postgres, 브랜칭을 스토리지 레벨로 끌어내리다

Xata가 오픈소스 클라우드 네이티브 Postgres 플랫폼을 공개했다. 핵심은 Copy-on-Write 방식의 브랜칭이다. 수 테라바이트의 데이터를 스토리지 레벨에서 복사하는 데 걸리는 시간이 몇 초에 불과하다. 기존 데이터베이스 브랜칭은 대부분 논리적 복사나 스냅샷 방식이라 대용량에서는 실용적이지 않았다. Xata는 이를 Kubernetes 위에서 자기 호스팅할 수 있는 형태로 만들었고, Scale-to-zero도 지원한다. 사용하지 않을 때 인스턴스가 0으로 축소된다. 데이터베이스 브랜칭은 그동안 소수의 상업 서비스들이 주도해온 영역이었다. Xata가 이를 Apache-2.0으로 공개한다는 것은, 이 기능이 특정 SaaS에 종속되지 않아도 된다는 신호다.

**Why it matters:** "데이터베이스를 코드 브랜치처럼 다룬다"는 개념이 오픈소스로 구현되기 시작했다는 것이 핵심이다. 자기 호스팅 가능한 CoW 브랜칭이 성숙하면, 개발 워크플로우에서 데이터베이스를 코드처럼 다루는 방식이 상업 서비스 없이도 일반화될 수 있다. 아직 초기지만, 방향이 가리키는 곳은 분명하다.

- Apache-2.0 라이선스, Kubernetes 기반 자기 호스팅 지원
- Copy-on-Write 브랜칭은 스토리지 레벨에서 작동해 TB 규모에서도 빠른 브랜치 생성이 가능하다.

**What's next:** 커뮤니티 기여가 어떤 속도로 붙을지, 그리고 기존 상업 서비스들과 어떤 경쟁 구도를 만들어낼지가 관건이다.

**Source:** [Xata: Open source Postgres platform with copy-on-write branching and scale-to-zero](https://github.com/xataio/xata)

---

데이터베이스 브랜칭이 코드 브랜칭을 닮아가는 동안, GitHub은 코드 협업 방식 자체를 바꾸는 실험을 시작했다.

## 3. GitHub Stacked PRs: 큰 변경을 쌓는 방법

GitHub이 Stacked PRs를 프라이빗 프리뷰로 공개했다. 아이디어는 간결하다. 큰 변경을 작은 PR들의 체인으로 분해하고, 각 PR이 독립적으로 리뷰되면서 스택 전체가 함께 머지된다. main을 베이스로 auth-layer, api-routes, frontend가 차례로 쌓이는 구조다. 기존에도 서드파티 도구들이 이 방식을 지원했지만, GitHub 네이티브 지원은 결이 다르다. PR UI에 스택 맵이 표시되고, 브랜치 보호 규칙은 최종 타겟 브랜치 기준으로 적용되며, CI도 각 PR을 최종 브랜치를 타겟하는 것처럼 실행한다. gh stack CLI를 통해 브랜치 생성, 리베이스, PR 생성을 터미널에서 한 번에 처리할 수 있다. AI 코딩 에이전트 통합도 포함됐다. npx skills add github/gh-stack 명령 하나로 에이전트에게 스택 작업 방식을 가르칠 수 있다.

**Why it matters:** 큰 PR은 리뷰어의 집중력을 분산시키고 피드백 품질을 떨어뜨린다. 오픈소스 커뮤니티에서 오래된 문제다. GitHub 네이티브 Stacked PRs가 일반화되면, 리뷰어가 전체 변경을 파악하지 않아도 레이어 하나씩 검토할 수 있게 된다. 서드파티 도구 없이 이 워크플로우를 쓸 수 있다는 것은 커뮤니티 채택에 실질적인 차이를 만든다.

- 현재 프라이빗 프리뷰 단계, 레포지토리 단위로 활성화해야 작동
- 머지 후 남은 PR들이 자동으로 리베이스되는 캐스케이딩 리베이스 지원

**What's next:** 프라이빗 프리뷰에서 일반 공개로 전환되는 시점, 그리고 AI 에이전트와의 통합이 오픈소스 기여 워크플로우에서 실제로 어떻게 쓰일지 주목된다.

**Source:** [GitHub Stacked PRs](https://github.github.com/gh-stack/)

---

## Comments