---
layout: post
title: "빅테크의 AI 경쟁이 고조되는 가운데 IBM 주가 25년 만에 최악을 기록했고, VC 충성도가 붕괴되며, 중국 AI 랩의 모 추출 적발로 정책 논쟁이 심화했다."
date: 2026-02-24
lang: ko
permalink: /ko/2026/02/24/daily-tech-review/
pair: 2026-02-24-daily-tech-review
tags: ["apple", "google", "meta", "microsoft", "nvidia"]
---

## Today in One Line
빅테크의 AI 경쟁이 고조되는 가운데 IBM 주가 25년 만에 최악을 기록했고, VC 충성도가 붕괴되며, 중국 AI 랩의 모 추출 적발로 정책 논쟁이 심화했다.

---

## 1. IBM 주가 25년 만에 최악 하락 - Anthropic COBOL 도구 발표에 당황

Anthropic이 2월 23일 Claude 코드 도구로 COBOL 레거시 코드를 현대화할 수 있다고 발표하자 IBM 주가가 13.2% 급락해 $40억 시장가를 순간에 증발시켰다. 이는 2000년 10월 닷컴 붕괴 이후 최악의 단일 거래일 손실이며, IBM의 메인프레임 사업을 중심으로 구축된 장기 수익 모델에 대한 투자자들의 근본적 우려를 드러냈다.

**Why it matters:** Claude Code가 레거시 코드 마이그레이션을 자동화할 수 있다는 발표는, orchestration이 이미 구현한 에이전틱 코딩(implement -> code-reviewer -> commit-writer 체인)의 산업적 파급력을 보여준다. 에이전트가 코드를 이해하고 변환하는 능력은 기존 소프트웨어 비즈니스 모델 전체를 위협한다.

- Anthropic의 COBOL 발표에 따라 IBM이 전일 대비 13.2% 하락한 $223.35에 마감, 시가총액 약 $40억 감소
- 향후 12개월 누적 낙폭은 24% 이상으로 2월 단 한 달에만 사상 최악의 월간 낙폭 기록 (1968년 이후 기준)
- IBM은 지난달 20년 만에 최고 메인프레임 익을 달성했으나, AI 도구의 가능성으로 인한 근본적 위협 평가

**What's next:** IBM은 COBOL 현대화 전략을 자체 Watsonx Code Assistant로 2023년부터 추진해 왔으나, Anthropic의 더 광범위한 AI 에코시스템이 경쟁력을 빼앗을 가능성에 대한 장기 협상이 시장에서 재평가될 전망이다.

**Source:** IBM stock dives after Anthropic points out AI can rewrite COBOL fast / [IBM Stock Suffers Worst Single-Day Drop in 25 Years](https://www.trendingtopics.eu/ibm-stock-suffers-worst-single-day-crash-in-25-years-after-anthropic-ai-announcement/)

---

## 2. OpenAI 투자자 충성도 붕괴 - 최소 12개 VC가 Anthropic $300억 펀드라운드에 동시 투자

Anthropic이 2월 중순 $300억 규모의 거대 펀드라운드를 마감하면서 Founders Fund, Iconiq, Insight Partners, Sequoia Capital을 포함한 최소 12개의 OpenAI 직접 투자자들이 동시에 Anthropic에도 출자했으며, BlackRock의 계열사까지 포함되어 실리콘밸리의 구조적 투자 원칙에 균열이 생겼다. 특히 BlackRock의 Adebayo Ogunlesi는 OpenAI 이사로 재직하면서 BlackRock 계열 펀드가 Anthropic에 투자하는 모순적 상황이 발생했다.

**Why it matters:** VC가 OpenAI와 Anthropic 양쪽에 동시 투자한다는 것은, 어느 한 모델에 종속되지 않으려는 시장의 판단이다. orchestration이 Claude(설계)+Codex(추출)+Gemini(2nd opinion) 멀티AI 구조를 택한 것과 같은 논리가 투자 시장에서도 작동한다.

- Sequoia Capital, Founders Fund, Iconiq 등 실리콘밸리 최고 권위의 VC들이 OpenAI와 Anthropic 모두에 직접 투자
- OpenAI는 $1,000억 규모의 새 펀드라운드 최종 단계를 진행 중인 가운데, Anthropic의 $300억이 진행되자 투자자 분산 심화
- 이사 겸임 등으로 인한 이해관계 충돌 문제는 법적 검토 대상이 되고 있으나, 투자자들은 "이사직이 없으면 문제없다"며 규제 회피

**What's next:** 앞으로 AI 투자 계약서에 명시적 이해관계 충돌 조항이 추가될 것으로 예상되며, 투자자의 기밀정보 접근 권한 제한도 논의 대상이 될 전망이다.

**Source:** [With AI, investor loyalty is (almost) dead: At least a dozen OpenAI VCs now also back Anthropic](https://techcrunch.com/2026/02/23/with-ai-investor-loyalty-is-almost-dead-at-least-a-dozen-openai-vcs-now-also-back-anthropic/)

---

## 3. Anthropic이 중 AI 랩의 대규모 Claude 모델 추출 적발 - 1,600만 쿼리로 불법 증류

Anthropic이 2월 23일 DeepSeek, Moonshot AI, MiniMax 등 중국 AI 랩 3곳이 약 24,000개의 가짜 계정으로 Claude에 접근해 1,600만 건의 쿼리를 생성하며 불법적으로 모델 증류(distillation)를 시행했음을 적발하고 공개했다. 이들은 Claude의 추론 능력, 도구 사용, 코딩 등 가장 차별화된 기능을 표적으로 삼았으며, DeepSeek의 경우 정치적으로 민감한 쿼리에 대한 검열 회피 방안까지 추출했다.

**Why it matters:** Claude의 추론 능력과 도구 사용 패턴이 1,600만 쿼리로 추출당했다는 것은, orchestration이 의존하는 모델의 핵심 역량이 복제 위험에 노출됐다는 뜻이다. API 사용 패턴 자체가 방어 대상이 되는 시대다.

- DeepSeek: 15만 건 이상의 쿼리로 추론 능력과 검열 우회 방법 추출, 동기화된 트래픽으로 탐지 회피
- Moonshot AI: 340만 건 이상으로 에이전트 추론, 도구 사용, 컴퓨터 활용 에이전트 개발 표
- MiniMax: 1,300만 건 이상으로 에이전트 코딩 능력 추출, 신모델 출시 직후 24시간 내 트래픽 절반을 새 모델로 전환

**What's next:** Anthropic은 API 트래픽 탐지, 행동 지문 분석, 증류 공격 패턴 식별 강화를 진행 중이며, 미국 정부와 클라우드 제공업체들과 기술 지표를 공유해 업계 전반의 대응을 촉구할 계획이다.

**Source:** [Anthropic accuses Chinese AI labs of mining Claude as US debates AI chip exports](https://techcrunch.com/2026/02/23/anthropic-accuses-chinese-ai-labs-of-mining-claude-as-us-debates-ai-chip-exports/) / [Anthropic Says Chinese AI Firms Used 16 Million Claude Queries to Train Their Models](https://thehackernews.com/2026/02/anthropic-says-chinese-ai-firms-used-16.html)

## Comments

