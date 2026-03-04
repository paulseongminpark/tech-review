---
layout: post
title: "다중 에이전트 코딩 시대에 Git 병합 문제를 해결하는 Weave, Claude가 52년 오래된 수학 문제를 풀다, DeepSeek V4 출시 임박."
date: 2026-03-05
lang: ko
permalink: /ko/2026/03/05/daily-tech-review/
pair: 2026-03-05-daily-tech-review
tags: ["opensource", "developer-tools", "github", "frameworks"]
---

## Today in One Line
다중 에이전트 코딩 시대에 Git 병합 문제를 해결하는 Weave, Claude가 52년 오래된 수학 문제를 풀다, DeepSeek V4 출시 임박.

---

## 1. Weave: 에이전트-친화적 Git 병합 알고리즘 출시

Ataraxy Labs가 개발한 Weave는 Git의 라인 기반 병합의 한계를 극복하는 엔티티 수준 의미적 병합 드라이버다. Claude Code, Cursor, Codex가 동시에 코드를 작성할 때 여러 에이전트가 같은 파일에 서로 다른 함수를 추가해도 Git이 충돌로 표시하던 문제를 tree-sitter 파서로 코드 구조를 이해한 뒤 함수 단위로 병합한다.

**Why it matters:** 다중 에이전트 병렬 작업이 산업 표준이 되면서 Git의 라인 기반 병합은 심각한 병목이 되고 있다. Weave는 벤치마크에서 Git 15/31 대비 31/31 완벽한 병합을 달성했으며, MCP 서버로 제공돼 에이전트가 편집 전 엔티티를 점유할 수 있다.

- Weave는 Git 워크플로우를 변경하지 않고 병합 드라이버 레벨에서 동작하므로 기존 도구 체인과 즉시 호환 가능하다.
- 14개 도구를 탑재한 MCP 서버 형태로 에이전트가 충돌을 사전에 감지하고 조정할 수 있는 기반을 제공한다.
- Python 클래스 병합 같은 언어별 특수 케이스를 처리해 들여쓰기 실수로 인한 스코프 이탈을 방지한다.

**What's next:** Bash 등 기본 미지원 언어에 tree-sitter 그래머 추가로 범위 확장 예상.

**Source:** [Weave – A language aware merge algorithm based on entities](https://github.com/Ataraxy-Labs/weave)

---

## 2. Claude Opus 4.6이 52년 오래된 Knuth 수학 문제 해결

Stanford 컴퓨터 과학과 Donald Knuth 교수는 지난 몇 주간 고민하던 열린 문제가 Anthropic의 Claude Opus 4.6이 3주 전 출시된 후 짧은 시간 내에 해결됐다고 발표했다. 해밀턴 사이클 분해(Hamiltonian cycle decomposition) 문제로, Knuth가 31번의 탐색 시도를 거쳐 순수 수학적 프레이밍을 찾도록 Claude를 유도한 후 최종적으로 일반화된 구성을 도출했다.

**Why it matters:** 이는 대형 언어 모델이 추론 기반 문제 해결에서 인간 전문가를 질적으로 보조할 수 있음을 구체적으로 입증한 사례다. Knuth 같은 전설적 컴퓨터 과학자도 Claude의 체계적 탐색과 재프레이밍 능력으로부터 혜택을 받을 수 있음을 시사한다.

- Claude는 DFS 탐색, 결과 기록, 문제 재정의 등 31번의 반복 사이클에서 인간 지도자의 계획 검증 지시를 따르며 수렴했다.
- Knuth는 Claude의 일반화된 분해가 홀수 m > 1에 대해 유효하며, 760개의 고유한 "Claude식 분해"가 존재함을 증명했다.
- Stanford 논문([Claude's Cycles](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf))은 개발자 과제 제시 방식(명확한 진도 문서, 주기적 검증 요청)이 모델 성능 향상에 얼마나 중요한지 보여준다.

**What's next:** 이 협력 방식이 수학, 이론 물리학 등 전문 분야 문제 해결에 모범 사례로 확산될 전망.

**Source:** [Claude's Cycles [pdf]](https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf)

---

## 3. DeepSeek V4 3월 3일 출시 예정, 네이티브 멀티모달·코딩 최적화

Financial Times가 2월 28일 보도한 바에 따르면 DeepSeek V4는 1조 파라미터 규모로 3월 초 출시될 예정이며, 사진·영상·텍스트 생성을 네이티브로 지원하는 멀티모달 모델이다. 경신된 FlashMLA 라이브러리 코드에서 발견된 'Model1'로 추정되는 이 모델은 코딩과 장문맥 소프트웨어 엔지니어링 작업에 최적화돼 있다.

**Why it matters:** DeepSeek V3(2025년 1월)가 679억 파라미터로 10배 비용이 많은 모델들을 능가한 이후, 중국 오픈소스 진영이 서방 폐쇄 모델 기업들과의 경쟁을 급속도로 따라잡고 있다. V4의 코딩 벤치마크(83.7% on BenchVerified) 및 수학(99.4% on Frontier Math, GPT-5.2보다 11배 우수)는 업계 기준을 재설정할 수 있다.

- Huawei, Cambricon 등 중국 칩 제조사와의 협력으로 NVIDIA 의존도 감소, 멀티모달 지원으로 이미지·비디오 처리 기능 대폭 확대.
- 512차원 구조 변환, NVIDIA Blackwell(H200) GPU 최적화, 토큰 수준 스파스 MLA 구현으로 장문맥(1M+ 토큰) 시나리오 대응.
- 오픈웨이트 모델로 출시될 예상이므로 오픈소스 커뮤니티와 로컬 배포 생태계에 즉시 영향.

**What's next:** 3월 초 공식 출시 후 Ollama, vLLM 등 추론 프레임워크 통합, 로컬 배포 가이드 확산 예상.

**Source:** [DeepSeek's Next Move: What V4 Will Look Like](https://recodechinaai.substack.com/p/deepseeks-next-move-what-v4-will)

## Comments

