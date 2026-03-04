---
layout: post
title: "Diffusion 기반 추론 LLM이 1,000+ 토큰/초 달성하며 AI 생성 방식의 패러다임을 바꾸고, 오픈웨이트 코딩 모델들이 클라우드 API 의존도를 크게 낮추면서 로컬 AI 개발 생태계가 급속 확대 중이다."
date: 2026-02-26
lang: ko
permalink: /ko/2026/02/26/daily-tech-review/
pair: 2026-02-26-daily-tech-review
tags: ["developer", "developer-tools", "opensource"]
---


## Today in One Line

Diffusion 기반 추론 LLM이 1,000+ 토큰/초 달성하며 AI 생성 방식의 패러다임을 바꾸고, 오픈웨이트 코딩 모델들이 클라우드 API 의존도를 크게 낮추면서 로컬 AI 개발 생태계가 급속 확대 중이다.

---

## 1. Inception Labs, Mercury 2로 1,000 토큰/초 달성 — Diffusion 기반 추론 LLM 본격 출시

Inception Labs가 2월 25일 발표한 Mercury 2는 기존의 자동회귀 토큰 생성 방식을 완전히 버리고 Diffusion 기반의 병렬 정제 생성을 통해 1,009 토큰/초를 NVIDIA Blackwell GPU에서 달성했다. 이는 Claude Haiku의 약 11배, GPT-5 Mini의 약 14배 빠른 속도로, 추론 LLM 성능 기준(AIME 2025: 91.1%, GPQA, LiveCodeBench)에서는 속도 최적화 모델들과 동등한 품질 유지한다.

**Why it matters:** 프로덕션 AI 시스템에서 지연 시간이 누적되는 에이전트 루프, 음성 인터페이스, 실시간 코딩 자동완성 같은 분야에서 기존의 "속도 vs. 품질" 트레이드오프를 근본적으로 깨뜨렸다. 특히 도구 호출이 빈번한 워크플로우에서 각 단계의 지연이 복합되던 문제를 해결해 AI 에이전트의 실용성을 급격히 높였다.

- **아키텍처:** 노이즈에서 출발해 여러 토큰을 병렬로 정제하는 Diffusion 방식으로, Sora·Stable Diffusion·Flux 개발진이 구축한 검증된 기술 토대 위에 추론 최적화 적용
- **가격:** $0.25/1M 입력 토큰, $0.75/1M 출력 토큰 — OpenAI API 대비 약 60% 저가, 128K 컨텍스트 네이티브 지원으로 RAG·도구 사용 비용 대폭 절감
- **호환성:** OpenAI API 완전 호환, Vercel AI SDK 즉시 지원, GitHub에서 오픈소스 데모 공개 예정으로 기존 LLM 통합 자산 재사용 가능

**What's next:** Diffusion 기반 추론이 다른 모델 제공자들의 표준화 추진으로 이어질 것 예상되며, 특히 음성 AI와 실시간 편집 도구에서 이 기술의 채택이 가속화될 전망이다.

**Source:** [Introducing Mercury 2](https://www.inceptionlabs.ai/blog/introducing-mercury-2), [Mercury 2 Overview — YouTube](https://www.youtube.com/watch?v=quOe8V2n9rU), Hacker News #6 — Feb 25

---

## 2. Alibaba Qwen, 코딩 에이전트용 Qwen3-Coder-Next 오픈소스 공개 — 3B 활성 파라미터로 Claude Sonnet 급 성능

Alibaba의 Qwen 팀이 2월 초 공개한 Qwen3-Coder-Next는 80B 총 파라미터 중 3B만 활성화되는 Mixture-of-Experts 구조로, 기존 DeepSeek V3.2(37B 활성)·Kimi K2.5·GLM-4.7(각 32B 활성)을 코딩 벤치마크에서 추월했다. 256K 네이티브 컨텍스트 길이를 지원하며 로컬 하드웨어(64GB MacBook, RTX 5090, AMD Radeon 7900 XTX)에서 20~40 토큰/초 처리 속도로 운영 가능해 오픈웨이트 모델의 새로운 표준을 제시한다.

**Why it matters:** API 종속성을 제거하고 데이터 프라이버시를 보장하는 동시에, Claude나 OpenAI의 API 비용 제약 없이 복잡한 코딩 에이전트를 구동할 수 있게 됐다. 특히 Anthropic의 Claude Code 제약과 OpenAI의 가격 인상 속에서 개발자들이 신뢰할 수 있는 오픈소스 대안이 확보되면서, 엔터프라이즈급 로컬 AI 개발 환경 구축이 실질화하기 시작했다.

- **아키텍처:** Gated DeltaNet + Gated Attention 하이브리드로 기존 Qwen3(235B)보다 3배 작으면서 전문가 수는 4배 증가, 유 전문가 추가로 코딩 특화 성능 극대화
- **성능:** 코딩 벤치마크에서 Sonnet 4.5 수준, AIME 2025·GPQA에서 소형 모델 중 최고 평가 달성, 로컬 실행에서도 신뢰할 수 있는 함수 호출 및 JSON 스키마 생성
- **배포:** Ollama·Hugging Face·Kaggle을 통해 즉시 다운로드 가능, 양자화 옵션(Q4, Q5, FP8)으로 다양한 하드웨어 환경 지원, MIT/Apache 2.0 상용 라이선스로 제한 없음

**What's next:** Qwen3-Coder-Next 채택 확산에 따라 로컬 개발 에이전트 플랫폼(Emdash, OpenClaw 등)의 기본 모델 표준이 될 가능성이 높으며, 엔터프라이즈가 자체 서버에서 폐쇄 루프 코딩 시스템을 구축하는 기술적 기반이 마련될 전망이다.

**Source:** Qwen3-Coder-Next Blog, [The Complete 2026 Guide to Running Qwen3](https://dev.to/sienna/qwen3-coder-next-the-complete-2026-guide-to-running-powerful-ai-coding-agents-locally-1k95), [A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)

---

## 3. GitHub Agentic Workflows, 기술 프리뷰 시작 — CI/CD 외 저수준 리포지토리 자동화 활성화

GitHub가 2월 13일 발표한 Agentic Workflows는 GitHub Actions 내에서 AI 에이전트(GitHub Copilot CLI, Claude Code, OpenAI Codex)를 직접 실행하는 기능으로, 마크다운 파일로 자동화 의도를 기술하면 컴파일러가 이를 YAML로 변환해 이슈 트리아지·PR 리뷰·CI 실패 분석·문서 갱신·테스트 커버리지 모니터링을 에이전트가 자동 수행한다. 리드전용 기본 실행 권한에 Safe Outputs 샌드박싱으로 보안 갭을 최소화했으며, GitHub MCP 서버를 통해 리포지토리·이슈·액션·보안 정보에 원시 접근 가능하다.

**Why it matters:** 기존 CI/CD는 결정론적 빌드·배포에만 적합했으나, Agentic Workflows는 인간이 정하기 어려운 휴리스틱 결정(어떤 이슈에 어떤 라벨 붙일지, PR 코멘트 맥락에서 무엇을 수정할지)을 에이전트가 자율적으로 처리하도록 해, 개발자들의 반복적인 트리아지·검토 부담을 극적으로 감소시킨다. 특히 오픈소스 메인테이너들이 수천 개 PR 처리 시간을 시간 단위로 단축할 수 있는 게임 체인저가 될 전망이다.

- **보안 설계:** 컨테이너 격리 실행, 읽기전용 기본 권한, 방화벽 기반 인터넷 접근 제한, 사용자 입력 살균, Safe Outputs로 쓰기 작업 권한 제어 — 일반 CLI 에이전트보다 3배 이상 강한 샌드박싱
- **개발 경험:** `.github/workflows/` 렉터리에 마크다운 파일 추가만으로 자동화 정의, `gh aw` CLI로 컴파일 및 커밋, 모든 코딩 에이전트 호환(GitHub Copilot·Claude Code·OpenAI Codex 상호 교환 가능)
- **트리거:** 이슈·PR·주석 이벤트, 스케줄 실행, 수동 디스패치, 코멘트 명령어로 유연한 자동화 트리거, GitHub Next·Microsoft Research·Azure Core Upstream 협업으로 MIT 오픈소스 공개

**What's next:** 50개 이상의 공식 에이전트 워크플로우 템플릿(Peli's Agent Factory)이 빠르게 생태계에 확산되면서, 엔터프라이즈 리포지토리에서의 에이전트 자동화 도입 비용이 급락할 것으로 예상되며, 이에 따라 개발팀의 메인테이넌스 생산성이 30~50% 향상될 가능성이 높다.

**Source:** [GitHub Agentic Workflows Technical Preview](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/), GitHub previews Agentic Workflows, [GitHub Blog — Agentic Workflows](https://github.blog)

## Comments

