---
layout: post
title: "DeepClaude: Claude Code 17배 저렴하게, Alibaba Metis: 도구 호출 중복 98%→2%, 코딩 에이전트는 과학 논문을 재현할 수 있는가"
date: 2026-05-04
lang: ko
permalink: /ko/2026/05/04/daily-tech-review/
pair: 2026-05-04-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
source_type: free-sources
---

## Today in One Line
이번 주 AI 에이전트 생태계에서 세 방향의 신호가 동시에 들어왔다. 비용을 17분의 1로 낮추는 방법, 중복 도구 호출을 98%에서 2%로 줄이면서 정확도까지 높이는 방법, 그리고 벤치마크를 넘어 실제 과학 재현 가능성의 영역까지 에이전트를 밀어붙이는 질문. 세 흐름은 결국 하나의 물음으로 수렴한다 — 에이전트는 실제로 쓸 만한가, 그리고 얼마나 넓은 범위에서.

---

## 1. DeepClaude: 몸통은 Claude Code, 두뇌는 DeepSeek

Claude Code는 현재 가장 강력한 자율 코딩 에이전트 환경 중 하나지만, 월 $200에 사용량 상한까지 걸려 있다는 점은 개인 개발자나 스타트업에겐 현실적 장벽이다. DeepClaude는 이 구조를 분해했다. Claude Code CLI의 파일 편집, bash 실행, 서브에이전트 생성 같은 "몸통" 기능은 그대로 두고, Anthropic API로 나가는 추론 호출만 DeepSeek V4 Pro로 교체하는 프록시 레이어를 끼워 넣었다. DeepSeek V4 Pro는 LiveCodeBench에서 96.4%를 기록했고 출력 토큰 비용은 $0.87/M — Anthropic의 $15/M과 비교하면 약 17분의 1이다. 에이전트 루프 자체, 즉 파일을 읽고 편집하고 git을 다루고 멀티스텝 태스크를 수행하는 모든 능력은 변하지 않는다. 달라지는 건 어떤 모델이 생각하느냐뿐이다. 설정은 2분이면 끝난다.

**Why it matters:** 이 프로젝트가 증명하는 건 Claude Code의 실질적 가치가 모델 자체보다 도구 루프 설계에 있다는 사실이다. 추론 레이어가 교체 가능한 컴포넌트라면, "어떤 모델을 쓸 것인가"보다 "어떤 오케스트레이션을 쓸 것인가"가 점점 더 중요해진다. 비용 장벽이 낮아지면 에이전트 실험의 속도가 달라지고, 그건 커뮤니티 전체의 반복 속도에 영향을 준다.

- DeepSeek V4 Pro: LiveCodeBench 96.4%, $0.87/M output tokens vs Anthropic $15/M
- 교체 범위는 추론 API 호출뿐. 파일 편집·bash·git·서브에이전트는 변경 없음

**What's next:** OpenRouter 지원이 포함돼 있어 백엔드를 더 다양하게 실험할 수 있다. 고성능 저비용 오픈 모델이 늘어날수록 이 접근의 선택지도 함께 넓어진다.

**Source:** [DeepClaude – Claude Code agent loop with DeepSeek V4 Pro, 17x cheaper](https://github.com/aattaran/deepclaude)

---

비용이 낮아지면 다음 문제가 수면 위로 올라온다. 더 많이 실행할수록 불필요한 호출도 함께 늘어난다는 것.

## 2. Alibaba Metis: 중복 도구 호출 98%에서 2%로

Alibaba의 Metis 에이전트는 AI 에이전트 시스템의 잘 알려지지 않은 비효율을 정면으로 다뤘다. 기존 에이전트 환경에서 동일하거나 불필요한 도구 호출이 전체의 98%에 달한다는 진단에서 시작해, 이를 2%까지 떨어뜨리는 방법을 찾았다. 더 흥미로운 건 중복 호출을 줄이는 동시에 정확도도 높아졌다는 점이다. 덜 호출하면서 더 정확해졌다.

**Why it matters:** 에이전트가 같은 도구를 반복 호출하는 건 낭비이기 전에 판단력 결함의 신호다. 현재 상태를 추적하지 못하거나 자신이 이미 한 일을 기억하지 못한다는 뜻이다. 호출 횟수를 줄이면서 정확도가 올라갔다는 건 에이전트의 "어떻게 생각하는가"를 고치면 "무엇을 하는가"의 질이 달라진다는 것을 보여준다. 멀티스텝 태스크에서 에이전트 비용과 신뢰성을 함께 잡으려는 팀이라면 이 접근법이 중요한 참고점이 된다.

- 중복 도구 호출: 98%→2%
- 호출 감소와 정확도 향상이 트레이드오프 없이 동시에 발생

**What's next:** Alibaba가 이 접근을 Qwen 계열 에이전트에 통합할 경우 응답 속도와 운영 비용 모두 실질적으로 개선될 여지가 있다. 오케스트레이션 레이어에서의 상태 추적 설계가 다음 경쟁 지점이 될 것이다.

**Source:** [Alibaba's Metis agent cuts redundant AI tool calls from 98% to 2% — and gets more accurate doing it](https://venturebeat.com/orchestration/alibabas-metis-agent-cuts-redundant-ai-tool-calls-from-98-to-2-and-gets-more-accurate-doing-it)

---

효율이 개선돼도 에이전트의 한계가 사라지는 건 아니다. 더 근본적인 질문이 남는다 — 소프트웨어 엔지니어링 벤치마크 밖에서도 에이전트를 믿을 수 있는가.

## 3. 코딩 에이전트는 과학 논문 결과를 재현할 수 있는가

LLM 기반 코딩 에이전트가 SWE-bench 같은 소프트웨어 엔지니어링 벤치마크에서 인상적인 성과를 내고 있다는 건 잘 알려진 사실이다. 이 arXiv 논문은 그 성과가 다른 영역으로도 전이되는지 직접 시험한다. 대상은 계산 재료과학 분야의 실제 연구 결과 재현이다. 이 분야의 워크플로우는 단순한 코딩 능력 이상을 요구한다 — 물리적 직관, 도메인 지식, 수치 결과에 대한 검증 능력. 일반 벤치마크가 측정하지 않는 것들이다. 에이전트가 코드를 작성할 수 있다는 것과, 특정 물리 현상에 대한 기존 연구 결과를 코드로 정확히 재현할 수 있다는 건 다른 문제다.

**Why it matters:** 에이전트의 강점이 실제로는 매우 좁은 영역에 집중돼 있을 가능성을 이 연구가 직접 시험한다. 과학적 재현 가능성은 코드 생성보다 훨씬 엄격한 기준이고, 에이전트가 여기서 어디까지 할 수 있는지 아는 것은 연구 자동화를 진지하게 검토하는 팀에게 중요한 기준점이 된다. 긍정적 결과든 부정적 결과든, 현장 기준이 생긴다는 것 자체가 의미 있다.

- 대상: 계산 재료과학 분야 실제 연구 결과의 코딩 에이전트 재현 가능성
- 핵심 질문: SW 벤치마크 성과가 도메인 지식 의존적 과학 워크플로우로 전이되는가

**What's next:** 결과에 따라 "에이전트로 과학 연구 가속" 담론에 실질적인 보정이 들어갈 수 있다. 재현에 실패한다면 그 실패 지점이 다음 연구 방향을 정의할 것이다.

**Source:** [Can Coding Agents Reproduce Findings in Computational Materials Science?](http://arxiv.org/abs/2605.00803v1)

---

## Comments

