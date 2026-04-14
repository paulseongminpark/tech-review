---
layout: post
title: "DaVinci, 사진 시장에 무료로 진입 · Backblaze, 아무 말 없이 백업 멈춰 · Google, 뒤로가기 버튼 조작에 스팸 규정"
date: 2026-04-15
lang: ko
permalink: /ko/2026/04/15/daily-tech-review/
pair: 2026-04-15-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line
오늘 세 뉴스가 공통으로 가리키는 건 신뢰다. Blackmagic Design은 무료 도구로 Adobe의 사진 시장에 직접 도전했고, Backblaze는 10년을 함께한 사용자들에게 아무 말 없이 백업을 멈췄으며, Google은 검색 생태계를 이용해 사용자를 묶어두던 관행 하나에 스팸 딱지를 붙였다. 신뢰는 스타트업이 가장 빠르게 얻고 가장 쉽게 잃는 자산이라는 걸, 세 사건이 각자의 방식으로 보여준다.

---

## 1. Blackmagic Design이 Adobe Lightroom에 선전포고했다

Blackmagic Design은 영상 편집 소프트웨어 DaVinci Resolve로 수년간 할리우드 컬러리스트들의 신뢰를 쌓아왔다. 그 신뢰를 이번에는 사진 시장으로 가져간다. DaVinci Resolve 21에 추가된 Photo 페이지는 무료 버전과 $295짜리 Studio 버전으로 제공되며, 사진 작가들에게 노드 기반 색보정 워크플로우를 처음으로 열어준다. Canon, Fujifilm, Nikon, Sony, iPhone ProRAW를 포함한 주요 RAW 포맷을 지원하고, 소스 해상도 그대로 32K(최대 400 메가픽셀)까지 처리한다. Lightroom이 레이어 방식의 한계 안에 사진 작가를 묶어두는 동안, DaVinci는 Power Windows, 커스텀 커브, Qualifier, 전문 스코프를 그대로 사진에 얹는다. 기존 컬러 페이지와 연결되어 전체 색보정 툴셋을 사용할 수 있으며, GPU 가속으로 대용량 RAW 이미지 내보내기 속도도 확보했다.

**Why it matters:** "프로급 도구를 무료로"라는 메시지는 Adobe 구독 모델에 지쳐 있는 사진 작가들에게 직접 꽂힌다. Blackmagic이 영상 편집 시장에서 그랬듯이, 이미 검증된 기술 자산을 인접 시장에 무료로 투하하는 전략은 스타트업이 쓰는 방식이다. 대기업이 이 방식을 쓰기 시작하면 시장 지도가 빠르게 바뀐다.

- 사진 편집에 필요한 기본 조정(화이트밸런스, 노출, 색, 채도)과 전문 도구가 동일 인터페이스 안에 공존한다
- AI 툴셋과 Resolve FX, Fusion FX를 사진에도 그대로 쓸 수 있다

**What's next:** 기능 격차보다 워크플로우 전환 비용이 더 높은 시장이다. 사진 작가 커뮤니티 안에서 학습 곡선이 채택 속도를 결정할 것이다.

**Source:** [DaVinci Resolve – Photo](https://www.blackmagicdesign.com/products/davinciresolve/photo)

---

도전자가 시장을 빠르게 파고드는 건 기존 서비스가 사용자와의 약속을 조용히 깨뜨릴 때 더 쉬워진다.

## 2. Backblaze는 백업을 멈췄고, 아무도 알려주지 않았다

Robert Reese는 10년 넘게 Backblaze를 써왔다. 2015년에 시작해, 하드드라이브 장애가 났을 때 실제로 복구에 성공했고, 지인들에게 적극 추천까지 했다. 신뢰는 충분히 쌓여 있었다. 균열이 시작된 건 2025년, GitHub 저장소의 git 히스토리를 실수로 날렸을 때였다. Backblaze가 언제부터인가 .git 폴더를 백업하지 않고 있었다. 설정 화면의 제외 목록 어디에도 이 사실은 적혀 있지 않았다. 그러다 Reddit 스레드에서 Dropbox 폴더도 통째로 누락된다는 걸 알게 됐고, 자신의 계정을 확인하니 OneDrive 폴더 역시 백업에서 사라져 있었다. Backblaze는 "모든 파일을 백업한다"고 홍보해왔다. 실제로는 그렇지 않았다.

**Why it matters:** OneDrive와 Dropbox는 동기화 서비스이지 백업이 아니다. 삭제된 파일을 1개월만 보관하는 반면, Backblaze는 1년치 버전 이력을 유지해 왔다. 이 차이가 중요한 순간은 반드시 온다. 아무 통보 없이 핵심 기능을 축소한 건 단순한 버그가 아니라 제품 방향의 결정이며, 그 결정이 사용자 모르게 이뤄졌다는 사실이 10년치 신뢰를 단번에 날려버렸다.

- OneDrive, Dropbox, .git 폴더 모두 Backblaze 설정 화면의 제외 목록에 명시되지 않았다
- Backblaze의 경쟁 우위는 무제한 저장 공간과 장기 보관 이력이었는데, 정작 백업 대상이 줄어들고 있었다

**What's next:** "진짜 모든 것을 백업한다"는 포지셔닝이 지금 당장 효과적인 메시지가 된다. 대안 서비스들이 반사이익을 노릴 기회가 열렸다.

**Source:** [Backblaze has stopped backing up OneDrive and Dropbox folders and maybe others](https://rareese.com/posts/backblaze/)

---

제품이 사용자 모르게 바뀌는 건 회사 내부의 결정이지만, 플랫폼이 규칙을 바꾸는 건 그 위에 올라탄 모든 서비스를 동시에 흔든다.

## 3. Google이 뒤로가기 버튼 조작을 스팸으로 규정했다

Google은 검색 중앙 블로그를 통해 "back button hijacking"에 대한 새 스팸 정책을 발표했다. 사용자가 브라우저의 뒤로가기 버튼을 누를 때, 검색 결과 대신 다른 페이지로 보내거나 현재 페이지에 묶어두는 방식이다. JavaScript로 브라우저 히스토리를 조작해 구현한다. SEO 관점에서는 체류 시간을 늘려 순위를 올리는 수법이었고, 광고 수익을 극대화하는 콘텐츠 팜에서 특히 자주 쓰였다. Google은 이 관행을 사용자 경험 침해이자 검색 결과 조작으로 동시에 규정했다. 정책 적용 범위와 판단 기준은 구체적으로 공개되지 않았다.

**Why it matters:** 이 정책이 직접 겨냥하는 건 검색 생태계를 착취해온 스팸 모델이지만, 문제는 경계선이 모호하다는 점이다. SPA나 커스텀 네비게이션 라이브러리를 사용하는 정상적인 웹 앱도 구분 없이 걸릴 수 있다. 검색 트래픽이 생명선인 초기 스타트업일수록, Google이 어디서 선을 그었는지 파악하기 전에 순위가 먼저 떨어지는 상황을 맞을 수 있다.

- 판단 기준이 공개되지 않아 자기 사이트가 해당되는지 즉각 파악이 어렵다
- 콘텐츠 팜이 주요 타겟이지만 SPA의 히스토리 관리 코드도 동일한 API를 사용한다

**What's next:** 이 기법을 써온 사이트들은 검색 순위 하락을 경험할 것이다. 어느 구현 방식까지가 허용선인지에 대한 논쟁이 SEO 커뮤니티에서 한동안 이어질 것이다.

**Source:** [A new spam policy for "back button hijacking"](https://developers.google.com/search/blog/2026/04/back-button-hijacking)

---

## Comments