---
layout: post
title: "NASA Artemis II 내결함성 컴퓨터 / ChatGPT $100 Pro 신설 / Claude Code 비용 재배분"
date: 2026-04-10
lang: ko
permalink: /ko/2026/04/10/daily-tech-review/
pair: 2026-04-10-daily-tech-review
tags: ["hardware", "chips", "datacenter", "cloud", "infrastructure"]
source_type: free-sources
---

## Today in One Line

달을 향하는 컴퓨터는 고장이 허용되지 않는다. 지상에서는 OpenAI가 $100짜리 코딩 구독 티어를 신설하며 Anthropic에 정면으로 맞섰고, 이미 $100을 내고 있던 개발자들은 그 돈을 더 영리하게 쓰는 방법을 찾아 공유하기 시작했다. 신뢰성을 극한까지 밀어붙이는 쪽과 비용 효율을 극한까지 밀어붙이는 쪽이 같은 주에 나란히 뉴스를 만들었다.

---

## 1. 달까지 가는 컴퓨터는 어떻게 설계하는가

우주에서는 재부팅이 없다. NASA가 Artemis II 임무를 위해 내결함성 컴퓨터를 어떻게 구축했는지가 ACM Communications에 공개됐다. Artemis II는 달 궤도를 도는 첫 유인 임무다. 4명의 우주비행사가 탑승한 오리온 캡슐이 지구에서 수십만 킬로미터 떨어진 공간을 비행하는 동안, 하드웨어가 오류를 낸다고 지상에서 달려올 수는 없다. 내결함성 설계란 이 조건에서 출발한다. 단순히 잘 만든 컴퓨터가 아니라, 우주 방사선과 극한의 온도 변화 속에서 하드웨어 일부가 죽더라도 임무 전체가 멈추지 않도록 구조적으로 설계된 시스템이다. HN에서 이 이야기가 조용하지만 꾸준히 읽힌 건, NASA가 실제 유인 임무에 적용한 설계 결정이 이 분야에 드물게 공개된 실전 자료이기 때문이다.

**Why it matters:** 우주선용 내결함성 컴퓨팅은 의료 기기, 항공 제어, 금융 인프라처럼 오류 허용치가 0에 가까운 시스템 전체와 설계 원리를 공유한다. NASA가 유인 임무에 실제로 적용한 구조를 공개 논문으로 꺼내는 건, 이 분야 전반에서 참조점이 되는 드문 사건이다.

- Artemis II는 오리온 캡슐에 4명 탑승, 달 궤도 비행 임무
- 학술지 ACM이 다룰 만큼 엔지니어링 커뮤니티에서 주목받은 드문 공개 사례

**What's next:** Artemis II가 실제 비행에 들어가면 이 컴퓨터는 설계의 가장 큰 시험대를 통과하게 된다. 성공하면 내결함성 설계의 강력한 실증이 된다.

**Source:** [How NASA Built Artemis II's Fault-Tolerant Computer](https://cacm.acm.org/news/how-nasa-built-artemis-iis-fault-tolerant-computer/)

---

극한의 신뢰성을 설계하는 이야기에서, 이번엔 극한의 수요를 감당하기 위한 가격 경쟁으로 눈을 돌린다.

## 2. ChatGPT $100 Pro 신설: AI 코딩 구독 전쟁의 새 전선

OpenAI가 월 $100짜리 ChatGPT Pro 티어를 새로 출시했다. 이름에서 혼란이 시작된다. 이미 $200짜리 "Pro"가 존재하는데, 같은 이름의 티어가 하나 더 생겼다. OpenAI의 설명에 따르면 신규 $100 Pro는 코딩 에이전트 Codex 사용량을 Plus 대비 5배 제공하며 "장시간 고강도 Codex 세션에 최적"이다. $20 Plus에서 $200 Pro로의 간격이 너무 컸다는 판단인지, 그 사이에 계단을 하나 더 놓은 셈이다. 이 가격 포인트는 우연이 아니다. Anthropic의 Claude Max도 $100이다. OpenAI는 같은 가격대에 직접 경쟁자를 세웠고, 개발자 시장의 구독 전쟁이 $100을 전선으로 재편되고 있다.

**Why it matters:** 월 $100은 단순한 가격 책정이 아니라 AI 코딩 도구가 개인 개발자 예산에서 인프라 항목으로 올라섰다는 신호다. 두 회사가 동시에 같은 가격대에 자리를 잡은 순간, 비교는 피할 수 없어졌다.

- OpenAI 구독 구조는 무료·$8 Go·$20 Plus·$100 Pro·$200 Pro로 5단계
- 이름이 같은 Pro 티어가 두 개 공존하는 네이밍은 구조적 혼란을 낳고 있다

**What's next:** 가격이 같아졌으니 다음 경쟁은 에이전트 품질과 한도 운영 방식이다. Codex 대 Claude Code의 직접 비교가 더 본격화될 것이다.

**Source:** [ChatGPT has a new $100 per month Pro subscription](https://www.theverge.com/ai-artificial-intelligence/909599/chatgpt-pro-subscription-new)

---

가격이 정해지는 동안, 그 가격을 이미 내던 개발자들은 다른 선택지를 계산하고 있었다.

## 3. $100짜리 Claude 구독을 쓰지 않기로 한 이유

$100을 내고도 한도에 막힌다는 불만은 조용히 쌓이고 있었다. AMD의 AI 수석 디렉터를 포함해 여러 개발자들이 같은 경험을 공유했고, 한 개발자가 구체적인 대안을 제시했다. 전략은 단순하다. Claude Pro $100을 해지하고 Zed 에디터 $10/월에 OpenRouter $90/월을 예치한다. 총액은 같다. 구조가 다르다. 구독 모델은 월간 윈도우 안에 사용량을 채우지 못하면 소멸된다. OpenRouter는 API 방식으로 사용한 만큼 과금되고 잔액이 이월된다. 사용 패턴이 버스트형이라면, 집중 코딩 기간과 공백이 번갈아 오는 패턴이라면 이 구조가 훨씬 효율적이다. Zed는 Claude Code를 Agent Client Protocol(ACP)로 직접 통합하기 때문에 기존 워크플로우를 크게 바꾸지 않아도 된다. 부수 효과로, OpenRouter를 경유하면 Zed가 기본 통합에서 200K로 제한하던 Gemini의 컨텍스트 윈도우가 1M으로 풀린다.

**Why it matters:** 이것은 Claude를 떠나는 이야기가 아니다. 구독 한도 구조에 대한 저항이다. 동일한 $100이 더 유연하게 쓰일 수 있다면 사용자들은 그쪽으로 이동한다. AI 공급자들이 한도를 어떻게 설계하느냐가 단순 가격 경쟁보다 중요한 변수가 됐다.

- Claude Code는 Zed에서 ACP로 통합되어 에디터 교체 없이 그대로 사용 가능
- OpenRouter 경유 시 Gemini 컨텍스트가 Zed 기본 통합의 200K에서 1M으로 확장된다

**What's next:** 멀티 모델 라우팅 전략이 확산되면 단일 AI 공급자에 대한 lock-in이 약해진다. 에이전트 도구보다 모델 라우터가 핵심 인프라로 부상할 수 있다.

**Source:** [Reallocating $100/Month Claude Code Spend to Zed and OpenRouter](https://braw.dev/blog/2026-04-06-reallocating-100-month-claude-spend/)

---

## Comments