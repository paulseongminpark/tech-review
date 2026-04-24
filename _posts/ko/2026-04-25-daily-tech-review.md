---
layout: post
title: "GPT-5.5 에이전트 코딩, 미 공군 자율 전투 드론, DeepSeek v4 출시"
date: 2026-04-25
lang: ko
permalink: /ko/2026/04/25/daily-tech-review/
pair: 2026-04-25-daily-tech-review
tags: ["ai-usecase", "enterprise", "adoption", "regulation"]
source_type: free-sources
---

## Today in One Line
이번 주 AI 뉴스의 수렴 방향은 하나다: 자율 시스템이 실제 작업을 가져가기 시작했다. 코드 에이전트는 지시 없이 멀티스텝 작업을 끝까지 수행하고, 전투 드론은 조종사 없이 이착륙하며, 그 인프라를 공급하는 API 시장에서는 기술적 교체 비용이 사라지고 있다.

---

## 1. GPT-5.5: "지저분한 멀티파트 작업을 주면 알아서 끝낸다"

GPT-5.5의 출시 메시지는 직접적이다. OpenAI는 이 모델이 멀티스텝 작업에서 계획, 도구 사용, 자기검증, 모호함 탐색을 독립적으로 처리하도록 설계됐다고 밝혔다. "messy, multi-part task"를 주면 끝까지 간다는 표현을 썼다. 에이전틱 코딩, 컴퓨터 사용, 지식 업무, 초기 과학 연구 — 네 영역을 주요 대상으로 지목했다.

수치는 그 주장을 뒷받침한다. Terminal-Bench 2.0에서 82.7%(GPT-5.4는 75.1%), OSWorld-Verified(컴퓨터 직접 사용)에서 78.7%, Expert-SWE(내부 소프트웨어 엔지니어링 벤치마크)에서 73.1%다. FrontierMath Tier 4(최고 난이도 수학)에서 35.4%로 GPT-5.4의 27.1%에서 크게 올랐다. 그러면서도 GPT-5.4와 동일한 토큰당 레이턴시를 유지하고, Codex 태스크에서는 더 적은 토큰을 소비한다고 밝혔다. 지금은 ChatGPT Plus, Pro, Business, Enterprise와 Codex에서 순차 롤아웃 중이며, API는 안전 요건 검토 후 곧 제공 예정이다.

**Why it matters:** Expert-SWE 73%는 추상적인 숫자가 아니다. 평균적인 소프트웨어 엔지니어링 작업의 상당 부분이 이 모델로 위임될 수 있다는 의미다. Computer Use 78.7%가 더 의미 있는 이유는 코드 작성을 넘어 GUI를 직접 조작하는 작업까지 에이전트에게 맡길 수 있다는 뜻이기 때문이다. 비용 구조까지 바뀌면, 사용 패턴이 따라온다.

- BrowseComp(웹 리서치) 84.4%, Claude Opus 4.7(79.3%), Gemini 3.1 Pro(85.9%)와 직접 경쟁
- GPT-5.5 Pro는 BrowseComp 90.1%, FrontierMath Tier 4 39.6%

**What's next:** API 공개 후 독립 벤치마크가 실제 서비스 환경에서 이 수치를 재현하는지가 관건이다. Codex CLI와의 통합이 구체화되면 에이전트 워크플로우 표준화 논의가 빨라질 것이다.

**Source:** [Introducing GPT-5.5](https://openai.com/index/introducing-gpt-5-5/)

---

소프트웨어가 자율적으로 작동하는 시대가 열리는 동안, 같은 변화가 하늘에서도 이미 진행 중이다.

## 2. 미 공군 YFQ-44A: 조종사의 조이스틱이 없다

Anduril의 YFQ-44A가 에드워즈 공군기지에서 여러 차례 소티(출격)를 수행했다. 조종사는 없다. Experimental Operations Unit(EOU) 에어맨들이 ruggedized 랩톱 한 대로 미션 계획을 업로드하고, 자율 택싱과 이륙을 개시했으며, 비행 중 임무를 재지시하고, 착륙 후 데이터를 회수했다. 무장 장착과 프리플라이트 체크도 소규모 팀이 직접 처리했다.

Anduril 엔지니어링 SVP Jason Levin의 표현이 핵심이다: "There is no operator with a stick and throttle flying the aircraft behind the scenes." 원격 조종이 아닌 진짜 자율 비행이다. 그 의미는 인프라에서 드러난다 — 대형 고정 기지 인프라가 필요 없고, 수일간의 훈련만으로 소규모 팀이 운용에 적응했다. 이 프로그램의 이름은 Collaborative Combat Aircraft(CCA) — 유인 전투기와 편대를 이루도록 설계된 무인 전투기다. 공군은 이번 시험을 통해 운용자, 엔지니어, 획득팀이 동일한 피드백 루프 안에서 작동하는 새로운 획득 모델을 검증했다.

**Why it matters:** 자율 전투기 논쟁은 언제나 "언제 가능해질 것인가"였다. 이번 시험은 그 질문을 닫는다 — 이미 가능하고, 지금은 확장 속도를 높이는 중이다. 랩톱 한 대로 전투기를 운용하는 소규모 팀의 등장은 군사력 투사의 진입 장벽이 구조적으로 낮아진다는 뜻이다. 획득 주기의 압축도 같은 방향을 향한다.

- 기존 드론은 원격 조종 의존 → YFQ-44A는 mission plan 업로드 후 자율 수행
- CCA는 유인 전투기와 편대 편성을 전제로 설계됐다

**What's next:** 다음 단계는 유인-무인 편대의 실전 통합 시나리오다. Warfighting Acquisition System 틀이 다른 무기 체계로 확장되면 군 전반의 획득 속도가 달라질 수 있다.

**Source:** [US Air Force tests Anduril semiautonomous combat jet drone](https://interestingengineering.com/military/usaf-jet-drone-semiautonomous-flight-test)

---

자율 시스템이 하늘과 소프트웨어 작업대를 점령하는 동안, 그 인프라를 공급하는 API 시장에서는 선택지가 조용히 늘었다.

## 3. DeepSeek v4: OpenAI·Anthropic 호환, 이제 교체 비용이 없다

DeepSeek가 v4 API를 공개했다. 두 모델이다 — deepseek-v4-flash(기존 deepseek-chat 대체)와 deepseek-v4-pro(기존 deepseek-reasoner 대체). 기존 모델명은 2026년 7월 24일에 deprecated된다. v4-flash는 비추론 모드가 기본이고, v4-pro는 thinking 파라미터와 reasoning_effort로 추론 깊이를 직접 제어한다.

기술적으로 가장 중요한 변화는 API 호환성이다. OpenAI SDK와 Anthropic SDK 둘 다를 직접 지원한다. base_url 한 줄만 바꾸면 된다. 기존 코드베이스에서 provider 전환의 마찰이 사실상 사라졌다. Context Caching, Tool Calls, JSON Output, FIM Completion, Coding Agents 통합도 공식 가이드에 포함됐다. flash로 bulk를 처리하고 reasoning_effort: high를 필요한 곳에만 쓰는 세분화된 비용 전략이 이제 코드 한 줄 수준의 결정이 됐다.

**Why it matters:** 모델 벤더 종속은 이제 기술적 문제가 아닌 순전히 경제적 선택의 문제가 됐다. OpenAI와 Anthropic 호환을 동시에 지원한다는 것은 기존 어떤 코드베이스에서도 A/B 테스트의 장벽이 없다는 의미다. 경쟁 구도가 성능 비교에서 가격-성능 비교로 이동하면, API 시장 전체의 무게중심이 달라진다.

- v4-pro의 실제 추론 품질 대비 GPT-5.5, Claude Opus 4.7 비교는 독립 벤치마크 부재
- FIM Completion(코드 자동완성)과 Chat Prefix Completion은 베타 제공

**What's next:** 커뮤니티 벤치마크가 v4-pro의 실제 추론 품질을 측정하는 시점이 전환 결정의 실질적인 기준점이 될 것이다.

**Source:** [DeepSeek v4 API Docs](https://api-docs.deepseek.com/)

---

## Comments

