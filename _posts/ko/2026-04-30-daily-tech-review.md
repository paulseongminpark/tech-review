---
layout: post
title: "Ghostty, GitHub을 떠나다 / GitHub 가용성 공식 입장 / Before GitHub"
date: 2026-04-30
lang: ko
permalink: /ko/2026/04/30/daily-tech-review/
pair: 2026-04-30-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
source_type: free-sources
---

## Today in One Line

오늘 오픈소스 커뮤니티를 관통한 이야기들은 모두 하나의 지점으로 수렴한다. GitHub이라는 플랫폼의 신뢰 위기다. 18년 동안 매일 GitHub을 열었던 사람이 마침내 떠나겠다고 선언했고, GitHub은 공식 블로그로 반응했으며, 한 베테랑 개발자는 더 긴 시간축으로 고개를 들어 "GitHub 이전"을 회상했다. 오픈소스 생태계의 중심 좌표가 흔들리고 있다.

---

## 1. Ghostty, GitHub을 떠나다

Mitchell Hashimoto는 GitHub 유저 번호 1299번이다. 2008년 2월에 가입했고, 그 이후 18년 동안 — 인생의 절반이 넘는 시간 동안 — 하루도 빠짐없이 GitHub을 열었다. 새벽 4시 기숙사에서 커밋을 올리고, 신혼여행 중 아내가 잠든 틈에 GitHub 이슈를 들여다봤다. 첫 오픈소스 프로젝트 Vagrant를 시작한 동기도 결국 GitHub에 입사하고 싶어서였다고 그는 말한다. 스무 살의 첫 발표에서 "이게 잘 되면 GitHub이 날 채용할지도!"라고 농담했을 정도였다. GitHub은 그에게 일도 취미도 열정도 전부였다.

그런 그가 터미널 에뮬레이터 프로젝트 Ghostty를 GitHub에서 이전하겠다고 선언했다. 계기는 분노가 아니라 기록이었다. 지난 한 달간 그는 GitHub 장애로 작업이 막힌 날마다 일지에 X를 표시했다. 거의 모든 날에 X가 찍혔다. 이 글을 쓰던 바로 그날도 GitHub Actions 장애로 약 2시간째 PR 리뷰를 못 하고 있었다. "진지한 작업을 하기에 더 이상 적합한 곳이 아니다." 상업적 대안과 FOSS 플랫폼 모두와 협의 중이며, 현재 URL은 읽기 전용 미러로 유지할 계획이라고 밝혔다.

**Why it matters:** 이건 한 개발자의 이탈 선언이 아니다. HashiCorp를 세우고 Terraform과 Vagrant를 만든 사람이, 18년간 GitHub의 열렬한 지지자였던 사람이 공개적으로 포기를 선언한 것이다. 제품의 실패는 수정할 수 있지만, 이런 서사가 커뮤니티에 퍼지면 플랫폼 신뢰는 다르게 작동한다. 장애 빈도가 아니라 떠나는 사람의 무게가 분기점을 만든다.

- 지난 한 달간 거의 매일 GitHub 장애로 업무 중단 기록
- 개인 프로젝트는 GitHub에 잔류, Ghostty만 단계적 이전 예정

**What's next:** 어느 플랫폼으로 이전할지는 아직 확정되지 않았다. Hashimoto는 여러 제공자와 논의 중이라고만 밝혔다. 그의 선택이 어디로 향하느냐에 따라 다른 대형 OSS 프로젝트들의 논의 방향도 달라질 가능성이 높다.

**Source:** [Ghostty Is Leaving GitHub](https://mitchellh.com/writing/ghostty-leaving-github)

---

이 파장이 커지자 GitHub은 침묵을 유지할 수 없었다.

## 2. GitHub의 공식 입장: 가용성 업데이트

Ghostty 이전 선언이 업계 전반의 주목을 받자, GitHub은 공식 블로그를 통해 가용성에 관한 공개 입장을 발표했다. 타이밍 자체가 모든 것을 말해준다. 평소라면 운영 공지 수준으로 조용히 처리됐을 장애 이슈가, Hashimoto의 글과 맞물리면서 커뮤니티 전체의 압력을 만들어냈다. GitHub Actions, PR 리뷰, 저장소 접근 — 현대 개발자의 일상 워크플로우가 단 하나의 플랫폼에 묶여 있을 때, 가용성 문제는 단순한 불편이 아니라 생산성 전체의 마비다.

플랫폼이 개발자에게 공개 사과에 가까운 입장을 내놓는 장면은 드물다. 수십 년간 "세계 모든 개발자의 집"을 내세워온 GitHub이 스스로 가용성 실패를 공식 인정했다는 사실은, 그 자체로 이미 무언가가 달라졌음을 보여준다. 해명이 있다고 해서 18년 사용자가 떠나기로 한 결정이 번복되지는 않는다.

**Why it matters:** 공식 입장 발표는 커뮤니티 이탈 압력이 임계치를 넘었다는 신호다. GitHub 같은 독점적 중앙화 플랫폼이 인프라 신뢰를 잃으면, OSS 생태계는 대안을 진지하게 탐색하기 시작한다. 그 탐색이 이미 시작된 것이다.

- GitHub Actions 등 핵심 기능의 반복 장애가 유지보수 신뢰도 하락으로 이어짐
- 공식 입장 발표는 커뮤니티 이탈 선언에 대한 직접적 반응으로 읽힌다

**What's next:** 블로그 포스트가 아닌 실제 인프라 안정화가 뒤따르지 않으면, 이 발표는 또 하나의 약속 문서로 끝날 것이다. 다음 대형 장애가 언제 오느냐가 신뢰 회복의 실질적 시험대다.

**Source:** [An update on GitHub availability](https://github.blog/news-insights/company-news/an-update-on-github-availability/)

---

이 소동 속에서 베테랑 개발자 한 명은 더 먼 과거로 시선을 돌렸다.

## 3. Before GitHub — 오픈소스는 GitHub 이전에도 살아있었다

Flask와 Jinja2를 만든 Armin Ronacher는 "GitHub 이전"을 회상하는 글을 썼다. SourceForge, 직접 운영하던 Trac 설치본, Subversion 저장소, 그리고 Bitbucket. GitHub이 등장하기 전 OSS 인프라는 분산되어 있었고, 대부분 개발자가 직접 통제하는 서버 위에 있었다. GitHub이 그 모든 것을 흡수하면서 네트워크 효과가 폭발했다. 코드를 올리는 것도, 가져다 쓰는 것도 거의 마찰 없이 가능해졌다. npm과의 결합은 마이크로 의존성 문화를 낳았고, 세계의 프로젝트 수는 폭발적으로 늘었다.

Ronacher는 이 변화가 긍정적이었음을 인정하면서도 양면을 놓치지 않는다. GitHub이 커뮤니티의 소셜 인프라가 됐다는 것, 전문적 관계와 우정이 이슈 스레드와 PR에서 시작됐다는 것. 그리고 지금 그 인프라가 흔들리고 있다는 것. 그는 GitHub의 쇠퇴를 Microsoft의 제품 결정으로 단순화하지 않는다. 한 시대의 소셜 인프라가 무너지는 과정으로 읽는다.

**Why it matters:** Ghostty 이전 선언이 개인의 결단이라면, Ronacher의 글은 그 결단이 놓인 역사적 맥락이다. OSS 생태계는 SourceForge에서 GitHub으로, 중심 플랫폼을 이동한 전례가 있다. 그 이동이 다시 일어날 조건이 갖춰지고 있는지, 이 글은 조용히 질문한다. 그리고 코드 배포의 마찰을 없애는 것이 꼭 좋은 일만은 아니었을 수 있다는 사실도.

- GitHub 이전 OSS 인프라: SourceForge → Trac/SVN → Bitbucket → GitHub 순으로 이동
- GitHub과 npm의 결합이 마이크로 의존성 문화를 구조적으로 형성

**What's next:** OSS 커뮤니티의 다음 중심지가 어디가 될지는 아직 아무도 모른다. 중요한 것은 그 질문이 이미 진지하게 제기되고 있다는 사실이다. 분산형 대안들의 시대가 오는 건지, 아니면 GitHub이 자정 능력을 보여줄 건지 — 2026년이 그 분기점이 될 수 있다.

**Source:** [Before GitHub](https://lucumr.pocoo.org/2026/4/28/before-github/)

---

## Comments

