---
layout: post
title: "GitHub 내부 저장소 3,800개 유출, r/SelfHosted의 탈출 러시, 그리고 Jedi Academy 코드에 남겨진 크런치의 흔적"
date: 2026-05-21
lang: ko
permalink: /ko/2026/05/21/daily-tech-review/
pair: 2026-05-21-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
source_type: free-sources
---

## Today in One Line

GitHub가 흔들리고 있다. 악성 VSCode 확장 하나가 내부 저장소 수천 개를 털었고, r/SelfHosted 커뮤니티는 중앙화된 플랫폼을 떠나는 흐름을 본격화하고 있다. 그 혼란 속에서, 13년 전 Raven Software 개발자들이 Jedi Academy 코드에 남긴 크런치의 분노가 다시 화제가 됐다 — 오픈소스가 때로는 역사의 증언이 된다는 걸 상기시키면서.

---

## 1. GitHub 내부 저장소 3,800개, 악성 VSCode 확장 하나로 털렸다

GitHub가 5월 20일 공식 확인했다. 내부 직원이 악성 VSCode 확장을 설치했고, 그 결과 약 3,800개의 내부 저장소 데이터가 유출됐다. GitHub는 "고객 데이터에 영향이 없다"고 밝혔지만, 공격 그룹 TeamPCP(Google Threat Intelligence Group에서 UNC6780으로 추적 중)가 다크웹 포럼에 해당 데이터를 $50,000 이상에 판매하겠다는 글을 올리면서 사건이 수면 위로 드러났다. TeamPCP는 이번 공격 이전에도 Trivy 취약점 스캐너(CVE-2026-33634)를 통해 Cisco 포함 1,000개 이상 조직을 침해했고, Checkmarx와 LiteLLM을 겨냥해 CI/CD 파이프라인 자격증명을 탈취하는 캠페인을 벌여왔다. 패턴이 일정하다 — 개발자가 신뢰하는 도구를 벡터로 삼아 내부로 침투한다. GitHub는 해당 확장을 마켓플레이스에서 제거하고 기기를 격리했지만, 정확히 어떤 확장이었는지는 공개하지 않았다. 같은 확장을 설치한 다른 개발자들이 자신의 피해 여부를 확인할 방법이 없다는 뜻이다.

**Why it matters:** 이번 사건은 개발자 도구 공급망이 구조적으로 취약하다는 걸 다시 확인시켜준다. VSCode 확장은 업무 환경 깊숙이 통합되어 있고, Marketplace의 보안 검증은 느슨하다. GitHub, PyPI, NPM, Docker를 모두 공격 벡터로 활용한 TeamPCP의 이력을 보면 "개발 환경 자체가 공격 표면"이라는 인식은 이제 선택이 아니라 전제다. 개발자 개인의 주의로 막기엔 이미 구조적 문제가 됐다.

- TeamPCP는 "이것은 랜섬이 아니다, GitHub를 협박하는 데 관심 없다"고 명시했다 — 데이터 판매가 목적이며 구매자가 없으면 무료 공개하겠다고 밝혔다
- GitHub는 침해된 확장명을 끝내 공개하지 않았다 — 같은 확장을 설치한 외부 개발자들은 확인 수단이 없는 상태다

**What's next:** GitHub의 조사가 진행 중이며 고객 데이터 영향 여부에 대한 추가 발표가 예상된다. VSCode Marketplace 보안 강화 압력도 커질 것이다.

**Source:** [GitHub confirms breach of 3,800 repos via malicious VSCode extension](https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/)

---

GitHub 보안 사고는 단순히 한 기업의 실수로 끝나지 않는다 — 개발자들이 중앙화된 플랫폼에 얼마나 깊이 의존하고 있는지를 드러내고, 그 의존도를 다시 생각하게 만든다.

## 2. r/SelfHosted: "이제 GitHub 떠난다" — 프라이빗 저장소를 직접 운영하는 흐름

r/SelfHosted에 "Leaving GitHub for private repos"라는 글이 올라와 192 업보트, 121개 댓글을 받았다. 자기 서버에서 직접 소프트웨어를 운영하는 커뮤니티답게, 이 글은 단순한 불만이 아니라 실제로 대안을 찾고 있는 개발자들의 집단 움직임을 반영한다. Gitea, Forgejo 같은 자체호스팅 Git 솔루션들이 오픈소스로 활발히 개발되고 있고, 이미 많은 개발자들이 VPS나 홈서버 위에서 개인 저장소를 직접 운영하고 있다. GitHub가 Microsoft에 인수된 이후 꾸준히 제기되던 프라이버시·락인 우려가, 이번 보안 사고를 계기로 다시 수면 위로 올라오는 맥락이다. 자신의 코드를 오픈소스로 공개하면서 그것을 저장하는 인프라는 폐쇄 기업에 맡기는 아이러니 — 이 커뮤니티의 논의는 그 아이러니에 대한 응답이기도 하다.

**Why it matters:** 오픈소스 생태계의 인프라가 단일 민간 기업에 집중되어 있다는 점은 오래된 긴장이다. GitHub는 오픈소스 프로젝트의 사실상 표준 호스팅 플랫폼이지만 그 코드베이스 자체는 공개되어 있지 않다. 보안 사고는 그 긴장을 행동으로 바꾸는 계기가 된다. 자체호스팅이 모두에게 현실적인 선택지는 아니지만, 이 논의가 커질수록 GitHub도 무시할 수 없다.

- Forgejo는 Gitea의 커뮤니티 포크로, 기업 의존 없이 독립적으로 개발되고 있다
- 자체호스팅 선택 시 보안 관리 책임은 사용자에게 이전된다 — 탈중앙화는 공짜가 아니다

**What's next:** GitHub 보안 사고가 반복될수록 자체호스팅 솔루션에 대한 관심은 더 커질 것이다. 오픈소스 생태계 내 인프라 주권 논의는 계속될 전망이다.

**Source:** [Leaving GitHub for private repos](https://www.reddit.com/r/selfhosted/comments/1timhsb/leaving_github_for_private_repos/)

---

그런데 오픈소스의 가치는 인프라 독립성에만 있지 않다. 코드 자체가 역사의 문서가 될 때, 전혀 다른 종류의 진실이 드러나기도 한다.

## 3. Raven Software의 Jedi Academy 소스코드 — 2003년 개발자들의 분노가 아직 거기 있다

r/programming에 1,709 업보트를 받은 글이 올라왔다. Raven Software가 2013년에 오픈소스로 공개한 Star Wars Jedi Knight: Jedi Academy의 소스코드가 다시 화제가 된 이유는 게임 자체가 아니다 — 코드 곳곳에 남겨진 개발자 주석들 때문이다. 크런치에 대한 분노, 일정 압박에 대한 냉소, 기술 부채를 쌓아가며 느끼는 자괴감이 2003년 출시 당시 그대로 남아있다. 소스코드 공개는 기능 재사용이나 커뮤니티 포팅을 가능하게 하지만, 그 이상의 무언가를 한다 — 코드는 당시의 작업 환경과 팀 문화와 압박 구조를 기록하고, 오픈소스가 그것을 영구 보존한다. 이 저장소는 지금도 활성 상태로, id Tech 3 엔진 기반 위에서 커뮤니티 기여가 이어지고 있다.

**Why it matters:** 게임 업계 크런치 문제는 2026년에도 현재진행형이다. 2003년 게임 코드 속 주석이 20년이 지나 공감을 얻는다는 것은 구조가 거의 바뀌지 않았다는 신호다. 오픈소스는 코드 공유라는 실용적 목적 외에도, 개발자가 자신이 겪은 것을 남길 수 있는 드문 공간이다. 그 주석들이 지워지지 않고 공개된 채 남아있다는 것 자체가 하나의 증언이다.

- Jedi Academy는 2003년 출시, 2013년 Raven Software가 GitHub에 소스코드를 공개했다
- 저장소는 현재도 포크와 커뮤니티 수정이 이어지고 있다

**What's next:** 이 저장소는 역사적 코드베이스가 어떻게 살아남는지를 보여주는 사례로 남을 것이다. 그리고 아마 10년 후에도 누군가 그 주석을 다시 발견할 것이다.

**Source:** [Raven Software Jedi Academy Source Code](https://github.com/grayj/Jedi-Academy)

---

## Comments
