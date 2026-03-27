권한 이슈로 recall 없이 진행. startup hook 컨텍스트(03_pipeline-redesign_0327 — 3소스 현황 점검, free-sources v3)를 참고해 작성한다.

---

```markdown
---
layout: post
title: "GitHub, 모든 사용자 코드로 AI 훈련 자동 동의 / Tesla Model 3 컴퓨터, 폐차 부품으로 책상 위에 / 셀프호스터들의 HDD 소모 현황"
date: 2026-03-26
lang: ko
permalink: /ko/2026/03/26/daily-tech-review/
pair: 2026-03-26-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
source_type: free-sources
---

## Today in One Line
GitHub가 전 사용자 Copilot 데이터를 AI 훈련에 자동 사용하기로 바꿨고, 오픈소스 커뮤니티는 폐차 부품부터 HDD 수명까지 제조사 울타리 밖에서 직접 답을 찾고 있다.

---

## 1. GitHub, Copilot 상호작용 데이터를 모든 요금제에서 AI 훈련에 자동 사용

GitHub가 Copilot 상호작용 데이터 사용 정책을 업데이트했다. 유료 플랜뿐 아니라 무료 포함 모든 사용자 티어가 자동 동의(opt-in) 처리되어, 이제 Copilot 사용 중 발생하는 데이터가 모델 개선에 쓰인다. GitHub는 공식 블로그 포스트를 통해 이 변경을 발표했으며, r/programming에서 665점과 994점짜리 스레드 두 개가 동시에 상위권에 올라 커뮤니티 반응이 뜨겁다. 플랫폼은 이미 Copilot, GitHub Spark, GitHub Models, MCP Registry 등 AI 중심 제품군을 통해 코드 생성 전반에 걸쳐 데이터를 수집하는 구조로 재편되어 있다.

**Why it matters:** tech-review 파이프라인 03_pipeline-redesign에서 GitHub 연동 소스 확장을 검토 중인 시점에 중요한 정책 변수다. 공개 레포를 운영하거나 Copilot을 쓰는 개발자라면 opt-out 여부를 확인해야 하며, 오픈소스 기여 데이터가 상업 모델에 흡수되는 구조에 대한 커뮤니티 합의가 없다는 점이 핵심 쟁점이다.

- GitHub는 AI 코드 생성, 보안 취약점 탐지, 시크릿 보호 등 전 제품군에 걸쳐 데이터 수집 인프라를 구축해왔다
- 이번 정책은 유료 사용자에 한정되지 않고 무료 티어도 포함해 자동 동의로 처리된다
- 커뮤니티에서는 같은 뉴스가 두 개의 독립 스레드(665점, 994점)로 올라올 만큼 개발자 반응이 양분되어 있다

**What's next:** opt-out 옵션이 실제로 작동하는지, 기업용 GitHub AE나 GHES 환경에는 어떻게 적용되는지가 다음 논점이 될 것이다. 오픈소스 프로젝트 측에서 별도 대응 정책을 내놓을 가능성도 있다.

**Source:** [Updates to GitHub Copilot interaction data usage policy](https://github.blog/news-insights/company-news/updates-to-github-copilot-interaction-data-usage-policy/)

---

## 2. Tesla Model 3 컴퓨터, 폐차 부품으로 책상 위에서 구동

보안 연구자 xdavidhu가 사고 폐차에서 수거한 부품으로 Tesla Model 3의 온보드 컴퓨터를 책상 위에서 직접 구동하는 데 성공했다. 이 프로젝트는 HN에서 901점, 312개의 댓글을 기록하며 단숨에 상위권에 올랐다. Tesla는 자사 하드웨어에 대한 독립적 연구를 공식적으로 허용하지 않지만, 연구자는 폐차 시장에서 부품을 합법적으로 확보해 분해·실험하는 방식으로 이 한계를 우회했다.

**Why it matters:** 수리권(right to repair)과 오픈 하드웨어 생태계의 실질적 사례다. 제조사가 소프트웨어 잠금으로 제어하는 차량 컴퓨터를 외부 연구자가 독립 환경에서 재현할 수 있다는 것은, EV 플랫폼의 보안 구조와 오픈소스 호환성 모두에 영향을 미친다. HN 댓글 312개는 이 주제에 대한 기술 커뮤니티의 관심이 단순 호기심을 넘어섰음을 보여준다.

- 부품 출처는 사고 폐차 — 시중 중고 부품상에서 합법적으로 수급 가능하다
- 구동 환경은 실제 차량이 아닌 데스크탑 세팅으로, 차량 CAN 버스 없이 독립 실행
- 연구자 도메인(bugs.xdavidhu.me)은 Tesla 관련 보안 취약점을 지속 추적해온 이력이 있다

**What's next:** 이런 독립 연구가 쌓이면 Tesla 차량의 소프트웨어 구조에 대한 오픈소스 문서화가 가능해지고, 결국 수리권 법제화 논의에도 구체적 근거로 활용될 수 있다.

**Source:** [Running Tesla Model 3's computer on my desk using parts from crashed cars](https://bugs.xdavidhu.me/tesla/2026/03/23/running-tesla-model-3s-computer-on-my-desk-using-parts-from-crashed-cars/)

---

## 3. 셀프호스터들의 HDD 소모 실태, r/SelfHosted 최다 공감

r/SelfHosted에 올라온 HDD 교체 현황 이미지가 2496점이라는 이번 주 최고 점수를 기록했다. 98개의 댓글과 함께 오픈소스 인프라를 직접 운영하는 커뮤니티의 공통된 경험이 집약된 스레드다. 클라우드 서비스 대신 자체 서버를 운영하는 사람들이 직접 겪는 HDD 마모, 교체 주기, 비용 구조가 이 게시물 하나에 공명한 것이다.

**Why it matters:** tech-review 파이프라인이 free-sources v3에서 r/SelfHosted를 포함한 커뮤니티 소스를 추적하는 이유가 여기 있다. 이 커뮤니티는 제품 발표 없이도 실사용 데이터를 집단적으로 생성한다. 2496점은 같은 날 GitHub Copilot 정책 스레드(665점, 994점)를 합친 것보다 높으며, 셀프호스팅 하드웨어 피로도가 현재 이 커뮤니티의 핫이슈임을 수치로 보여준다.

- r/SelfHosted 기준 이번 주 최다 upvote 게시물로, 순수 커뮤니티 공감형 콘텐츠
- 댓글 98개는 단순 공감을 넘어 개인 경험 공유와 대안 논의가 이어졌음을 시사한다
- HDD 소모 문제는 ZFS, RAID, 스토리지 풀 관리 등 오픈소스 인프라 스택 전체와 연결된다

**What's next:** SSD 전환 비용이 낮아지면서 셀프호스팅 스택에서 HDD를 완전히 걷어내는 흐름이 가속될 것이다. 이 트렌드는 오픈소스 NAS 솔루션(TrueNAS, Unraid 등)의 스토리지 전략에도 영향을 미친다.

**Source:** [that HDD churn](https://i.redd.it/vjoxnk07serg1.png)

---

## Comments