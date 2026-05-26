---
layout: post
title: "오픈소스로 반도체 회사 세우기, 네덜란드의 M&A 차단, SwiftUI Mac 앱 실전기"
date: 2026-05-27
lang: ko
permalink: /ko/2026/05/27/daily-tech-review/
pair: 2026-05-27-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line
오늘 스타트업 신호는 세 겹의 경계에서 왔다. 지적재산권의 벽을 허물려는 반도체 창업자, 국가가 디지털 주권을 내세워 M&A를 막는 현장, 그리고 플랫폼의 한계를 혼자 테스트하는 인디 개발자. 셋 다 제약을 마주하고 있다는 점에서 같다. 그 제약을 어떻게 다루느냐가 전략이 된다.

---

## 1. 공짜 IP로 반도체 회사를 세울 수 있을까

반도체 설계는 순수한 지적재산권 싸움이다. 세계 최고 두뇌들이 만든 아이디어가 수조 달러의 가치를 만들어내는 이 산업에서, IP를 소유하지 못하면 사업 자체가 없다는 것이 정설이다. 그런데 aesc silicon의 창업자 Daniel Schultz는 그 IP를 통째로 공개하면서 회사를 시작했다. 모델은 사실 새롭지 않다. Linux가 그랬고, Red Hat이 그 위에서 돈을 벌었다. 핵심 IP는 누구나 공짜로 쓸 수 있지만, 지원과 커스터마이징과 전문 서비스에서 수익이 나오는 구조다.

Daniel이 꼽는 킬러 앱은 검증 가능한 보안이다. 설계부터 제조까지 전체 공급망이 오픈소스여서, 누군가 백도어를 슬쩍 끼워 넣었는지 감사할 수 있다. 암호화 엔진은 신뢰받으려면 열려 있어야 한다는 논리다. 또 하나의 성장 동력은 맞춤 칩 수요가 늘어나는 흐름이다. 더 많은 회사들이 특화 칩을 원하게 되면서, 오픈소스 IP가 진입 비용을 낮추는 역할을 할 수 있다. 그가 만들고 있는 IP Forge는 NPM이나 pip 같은 오픈소스 IP 블록 패키지 매니저다. 칩 설계자가 블록을 검색하고 다운로드해 프로젝트에 바로 쓸 수 있게 하려는 것으로, 생태계 락인을 노린 핵심 도구다. 실험 비용도 내려갔다. Wafer.Space를 통한 테이프아웃 한 번에 4천~7천 달러면 된다. Raspberry Pi가 엔지니어 한 명의 힘으로 자체 마이크로컨트롤러를 만들어낸 것처럼, 칩 설계의 문턱을 그 수준까지 낮추는 것이 목표다.

**Why it matters:** 오픈소스 소프트웨어가 엔터프라이즈 시장을 재편한 방식이 반도체에서 재연될 수 있다는 첫 번째 진지한 시도다. Cadence나 Synopsys 없이 칩을 설계할 수 있는 환경이 만들어지면, 소규모 스타트업도 자체 실리콘을 가질 수 있게 된다. 그 상상이 현실이 되는 속도를 IP Forge가 결정할 것이다.

- 오픈 FPGA, RISC-V 프로세서 등이 이미 wafer.space에서 테이프아웃 중
- IP Forge는 생태계 락인 전략이자, 수익 모델의 핵심 입구

**What's next:** 오픈소스 실리콘이 소프트웨어처럼 생태계를 형성하려면 Tiny-Tapeout 규모를 넘어서는 채택이 필요하다. IP Forge가 그 허브가 될 수 있는지가 관건이다.

**Source:** [How do you build a semiconductor company on something that's free?](https://www.siliconimist.com/p/the-open-source-silicon-business)

---

지적재산권 대신 개방으로 승부를 거는 스타트업이 있다면, 반대 방향에서 국가가 기술 주권을 내세우며 장벽을 세우는 장면도 있다.

## 2. 디지털 주권이 M&A를 막다: 네덜란드의 결정

네덜란드 시민들이 병원 예약을 하고, 집을 사고, 정부 서비스를 이용할 때 쓰는 인증 플랫폼이 DigiD다. 이 앱의 핵심 인프라를 운영하는 회사가 Solvinity인데, 지난해 11월 IBM에서 분사한 미국계 IT 기업 Kyndryl이 인수를 발표하면서 네덜란드 정부의 레이더망에 걸렸다. 국가 온라인 신원 시스템이 외국 기업 손에 넘어간다는 것이 문제였다. 네덜란드 디지털경제 국무장관 Willemijn Aerdts는 의회에 보낸 서한에서 투자 심사 당국이 "공익에 가능한 위험을 초래한다"는 이유로 인수 차단을 권고했다고 밝혔고, 정부는 그 권고를 받아들였다.

Kyndryl은 "이 과정이 지나치게 정치화됐다"며 실망감을 드러냈다. 네덜란드 정부는 미국 기업들의 기여를 높이 평가하며 외국 투자에 똑같이 적용되는 독립적 심사 프레임워크라고 강조했지만, 결과는 명확하다. 공공 인프라에 연결된 회사는 국경을 넘는 순간 다른 규칙이 작동한다. 타이밍도 묘하다. 유럽 집행위원회가 다음 주 클라우드, 마이크로칩, AI 분야의 외국 기술 의존도를 줄이기 위한 기술 주권 패키지를 발표할 예정이다. 네덜란드의 결정은 그 흐름 위에 놓여 있다.

**Why it matters:** 디지털 인프라가 국가 주권의 영역으로 편입되면서, 유럽에서 공공 서비스와 연결된 회사를 인수하는 일은 구조적으로 더 복잡해지고 있다. 스타트업 관점에서는 잠재적 인수자의 국적이 Exit 경로의 변수가 되는 새로운 현실이다.

- "공익" 기준이 점점 넓게 해석되는 신호로 읽힌다
- EU 기술 주권 패키지 발표를 앞두고 유사한 심사 강화가 확산될 가능성이 있다

**What's next:** Kyndryl이 결정에 이의를 제기할 가능성이 있다. 더 중요한 것은, 유럽 전역에서 디지털 공공 인프라를 다루는 회사들이 M&A 시장에서 어떻게 가격이 매겨질지다.

**Source:** [Netherlands blocks US takeover of vital digital supplier](https://www.politico.eu/article/netherlands-blocks-us-takeover-vital-digital-supplier/)

---

국가 차원의 장벽이 M&A를 막는 동안, 개인 개발자 차원에서는 플랫폼의 기술적 경계와 씨름하는 현장이 있다.

## 3. SwiftUI로 혼자 Mac 앱을 만든다는 것

Paulo Andrade는 작년 말 iOS App Store에 Shopie를 출시했다. 관심 있는 제품을 위시리스트에 담아두고, 가격과 재고가 바뀌면 알림을 받는 앱이다. 최근 macOS 버전을 추가했는데, 다른 앱들과 달리 AppKit이나 UIKit 없이 100% SwiftUI로 만들었다. 이유는 단순하다. iOS, iPadOS, macOS에서 코드를 최대한 공유하려면 그 길밖에 없었다.

"Mac-assed app"이라는 표현이 있다. Collin Donnell이 만들고, Brent Simmons와 John Gruber가 퍼뜨린 이 개념은 단순히 네이티브를 넘어서, macOS의 컨트롤과 관례를 충실히 따르고 운영체제 기능과 완벽하게 통합된 앱을 뜻한다. Paulo가 SwiftUI로 만들려 한 것이 바로 그것이다. 결론은 솔직하다. "아직 거기까지 못 왔다." 포팅 과정에서 부딪힌 문제들을 레시피처럼 정리한 이 글은, 작은 앱 하나를 멀티플랫폼으로 가져가는 일이 2026년에도 여전히 험한 길임을 보여준다. 코드 재사용이라는 이상과 각 플랫폼의 관례를 충실히 따르는 것 사이의 긴장은 여전히 해소되지 않았다.

**Why it matters:** 인디 개발자 혼자서 멀티플랫폼 앱을 유지할 수 있느냐는 질문은 Apple 플랫폼 전략의 실효성과 직결된다. SwiftUI가 그 약속을 충분히 이행하지 못하면, 인디 생태계의 선택지는 다시 React Native나 Flutter 쪽으로 기울 수 있다. 프레임워크 선택이 곧 창업 방식의 선택이 되는 시대다.

- Shopie는 iOS에서 시작해 macOS로 확장한 1인 개발 제품으로, SwiftUI 코드 공유를 핵심 전략으로 삼았다
- "Mac-assed" 수준의 네이티브 경험을 SwiftUI 단독으로 달성하는 것은 2026년 현재도 미완이다

**What's next:** Apple이 WWDC에서 SwiftUI를 어느 수준으로 끌어올릴지가 이 질문의 다음 챕터다. 인디 개발자들이 기다리는 것도 결국 그 발표다.

**Source:** [Using SwiftUI to Build a Mac-assed App in 2026](https://pfandrade.me/blog/mac-assed-swiftui-app/)

---

## Comments
