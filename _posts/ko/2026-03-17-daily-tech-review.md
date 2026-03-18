---
layout: post
title: "Mistral Small 4·Leanstral·Open-H-Embodiment 동시 공개 — 에이전트 스택 세 축이 구체화"
date: 2026-03-17
lang: ko
permalink: /ko/2026/03/17/daily-tech-review/
pair: 2026-03-17-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
---

## Today in One Line
오픈 웨이트 진영에서 256k 컨텍스트의 통합형 모델(Mistral Small 4), 정형증명 기반 '검증형' 코딩 에이전트(Leanstral), 의료 로봇 '행동' 데이터를 대규모로 개방한 Open-H-Embodiment(778시간) 및 수술 로봇용 VLA/WFM이 같은 날 연달아 공개됐다.

---

## 1. Mistral Small 4 공개 — Instruct·Reasoning·Coding·Vision을 한 모델로 통합

미스트랄은 2026년 3월 16일 Mistral Small 4를 공개하며, 추론(Reasoning)·멀티모달·에이전틱 코딩 역량을 단일 모델로 통합했다. 핵심 스펙으로 MoE 128 experts(토큰당 4개 활성화), 119B total parameters, 256k 컨텍스트, 그리고 요청별로 조절 가능한 `reasoning_effort`를 제시했다.

**Why it matters:** 멀티AI 오케스트레이션에서 모델별 역할 분리(Claude/Codex/Gemini)를 운영 중인데, 256k + Apache 2.0 통합 모델은 로컬 호스팅 가능한 에이전트 백본으로서 API 비용 없는 대안을 제시한다.

- 모델 식별자 `mistral-small-2603`, 119B total / 6B active parameters, 256k 컨텍스트, Apache 2.0 라이선스
- Small 3 대비 end-to-end completion time 40% 감소, 초당 처리량 3배 향상 (throughput-optimized)
- vLLM, llama.cpp, SGLang, Transformers 지원과 함께 공개. Mistral API·Hugging Face·NVIDIA NIM 경로 배포 가능

**What's next:** 오픈 웨이트 배포 후 256k 장문 컨텍스트 + reasoning 모드가 실제 워크로드(코딩·RAG·문서 분석)에서 비용/지연/정확도를 어떻게 재구성하는지 벤치마크가 빠르게 쌓일 전망이다.

**Source:** [Introducing Mistral Small 4](https://mistral.ai/news/mistral-small-4)

---

## 2. Leanstral 공개 — Lean 4 정형증명 '검증'에 최적화된 오픈소스 코드 에이전트

미스트랄은 같은 날 Lean 4 형식 검증(정형증명)용 오픈소스 코드 에이전트 Leanstral을 발표했다. "코드를 생성하는 에이전트"를 넘어, 검증(증명)이라는 '완전한 판정자(perfect verifier)'가 있는 영역에서 반복 실행(pass)로 성능을 끌어올리는 전략을 전면에 둔 것이 특징이다.

**Why it matters:** code-reviewer가 AI 판단에 의존하는 한계를 '기계적 증명'으로 구조적으로 우회한다. pass@2 기준 $36/26.3점(Sonnet $549/23.7점)이라는 비용-성능 비율은 에이전트 코딩의 경제학을 '검증 비용' 중심으로 재정의한다.

- Lean 4 전용 첫 오픈소스 코드 에이전트, Apache 2.0 라이선스, 무료/준무료 API endpoint (`labs-leanstral-2603`)
- MoE 128 experts/4 active, 119B total / 6.5B activated per token, 256k context
- FLTEval pass@16에서 31.9점 (Sonnet 대비 8점 높음), pass 횟수 증가에 따라 점수가 선형 상승하는 패턴

**What's next:** 훈련 접근(tech report) 및 FLTEval 확장이 실제로 공개되면, "vibe coding → verified coding" 전환이 Lean 생태계 밖의 Rust·안전중요 소프트웨어로 번질지 주목할 만하다.

**Source:** [Leanstral: Open-Source foundation for trustworthy vibe-coding](https://mistral.ai/news/leanstral)

---

## 3. NVIDIA·Hugging Face, 의료 로봇 Physical AI 공개 데이터셋·기초 모델 동시 발표

NVIDIA는 Hugging Face 블로그를 통해 2026년 3월 16일 의료 로봇 영역의 공개 데이터셋 Open-H-Embodiment와 수술 로봇용 기초 모델·시뮬레이터를 발표했다. 778시간 규모(CC-BY-4.0)의 로봇 학습 데이터를 포함하며, GR00T-H(수술 로봇 정책/VLA)와 Cosmos-H-Surgical-Simulator(행동 조건부 수술 영상 생성 WFM)를 함께 제시했다.

**Why it matters:** 데이터–정책–시뮬레이터 3층 구조가 mcp-memory의 관찰→패턴→원칙 성숙 경로와 동일한 패턴이다. 텍스트 도메인의 에이전트 자동화가 물리 세계로 확장되는 분기점을 보여준다.

- Open-H-Embodiment: 35개 조직 참여, 778시간 CC-BY-4.0 훈련 데이터 (수술 로봇 중심 + 초음파/대장내시경 자율 데이터)
- GR00T-H: 약 600시간 데이터로 학습된 첫 수술 로봇 정책 모델. VLM 백본으로 Cosmos Reason 2 2B 사용
- Cosmos-H-Surgical-Simulator: 64×A100 / 약 10,000 GPU-hours, 600 rollouts 기준 시뮬레이션 40분 vs 실물 벤치탑 2일

**What's next:** 버전 2의 목표를 '수술 로봇의 ChatGPT 순간'(설명·계획·적응 가능한 추론형 자율성)으로 설정하고, 의도·결과·실패 모드를 포함한 reasoning-ready 데이터 확장을 커뮤니티에 요청했다.

**Source:** [The First Healthcare Robotics Dataset and Foundational Physical AI Models for Healthcare Robotics](https://huggingface.co/blog/nvidia/physical-ai-for-healthcare-robotics)

## Comments
