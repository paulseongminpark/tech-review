---
layout: post
title: "엔비디아 OpenShell 에이전트 샌드박스, Unsloth Studio 로컬 파인튜닝 UI, LangSmith Polly GA"
date: 2026-03-19
lang: ko
permalink: /ko/2026/03/19/daily-tech-review-2/
pair: 2026-03-19-daily-tech-review-2
tags: ["opensource", "developer", "tools"]
source_type: perplexity
---

## Today in One Line
엔비디아 OpenShell, Unsloth Studio, LangSmith Polly GA가 동시에 나와 에이전트 보안·로컬 파인튜닝·에이전트 디버깅까지 AI 개발 스택 전체를 한 단계 끌어올리고 있다.

---

## 1. 엔비디아 OpenShell — 자율 AI 에이전트용 오픈소스 샌드박스로 사실상 보안 표준을 노린다

엔비디아가 GTC 2026에서 자율 AI 에이전트 전용 런타임인 OpenShell을 Apache 2.0 오픈소스로 공개했고, 3월 16일 첫 공개 이후 18일 기준 v0.0.10까지 알파 버전을 연속 릴리스하고 있다. OpenShell은 에이전트와 인프라 사이에 위치해 파일·네트워크·모델 호출을 모두 YAML 정책으로 통제하는 샌드박스 레이어로, Claude Code·Codex·OpenClaw 같은 에이전트를 코드 수정 없이 감싸는 것을 목표로 한다.

**Why it matters:** orchestration Workers 3개(code-reviewer, compressor, commit-writer)가 서버 측 코드를 실행하는 구조에서, OpenShell의 YAML 정책 기반 격리는 /delegate 멀티AI 위임 시 에이전트별 권한 경계를 인프라 레벨에서 강제하는 레이어로 직접 검토할 만하다.

- Apache 2.0 라이선스, 리눅스 Landlock LSM 기반 커널 레벨 격리로 파일·프로세스·소켓을 YAML 정책으로 통제한다
- curl 한 줄 설치, v0.0.10까지 연속 릴리스, 리눅스 x86_64·ARM64·macOS ARM 바이너리를 제공한다
- NemoClaw 스택으로 OpenClaw뿐 아니라 Claude Code·Codex·Cursor도 코드 수정 없이 감싸는 것을 목표로 한다
- LangChain·TrendAI·EQTY Lab 등과의 통합을 동시에 발표했다

**What's next:** 현재는 알파 단계 소규모 팀 중심이지만, 금융·보안 벤더와의 통합이 이미 발표된 만큼 1년 내 엔터프라이즈 에이전트용 기본 런타임 위치를 노리는 움직임이 가속될 것으로 보인다.

**Source:** NVIDIA OpenShell Developer Guide (docs.nvidia.com)

---

## 2. Unsloth Studio — 로컬 LLM 파인튜닝을 위한 오픈소스 노코드 웹 UI로 2배 속도·VRAM 70% 절감을 내세운다

Unsloth AI가 3월 17일 'Unsloth Studio'(Beta)를 공개해 Mac·Windows·Linux에서 100% 로컬로 LLM을 실행·파인튜닝·배포할 수 있는 오픈소스 노코드 웹 UI를 출시했다. 기존에는 파이썬 스크립트와 복잡한 CUDA 세팅이 필요했던 파인튜닝 과정을, 브라우저 기반 GUI에서 데이터 준비부터 GGUF·vLLM·Ollama 내보내기까지 한 번에 처리하는 것이 목표다.

**Why it matters:** Gate B/C에서 Codex·Gemini 외에 로컬 파인튜닝 모델을 대안 워커로 투입할 수 있는 진입 장벽이 대폭 낮아졌다. Data Recipes의 합성 데이터 생성은 mcp-memory 지식 그래프 데이터를 파인튜닝 학습셋으로 전환하는 경로를 열어준다.

- Triton 기반 수작업 백워드 패스로 학습 속도 2배, VRAM 70% 절감(정확도 손실 없음)을 달성했다
- 텍스트·비전·TTS·임베딩 포함 500개 이상 모델을 지원한다
- Data Recipes: 노드 기반 그래프 UI로 PDF·CSV·DOCX에서 ChatML·Alpaca 포맷 합성 데이터셋을 자동 생성한다
- 훈련 후 GGUF·safetensors·vLLM 포맷으로 원클릭 내보내기가 가능하다

**What's next:** 현재는 NVIDIA GPU 중심이지만, AMD·Intel GPU와 멀티 GPU, Apple MLX 훈련까지 로드맵에 올려둔 만큼 로컬 LLM 파이프라인의 기본 GUI로 자리 잡을 가능성이 크다.

**Source:** Unsloth Studio – Introducing Unsloth Studio (unsloth.ai)

---

## 3. LangSmith Polly — LangChain 전역 GA로 에이전트 디버깅·평가·프롬프트 수정을 한 화면에서 처리 가능해진다

LangChain이 LangSmith 내 에이전트 디버깅용 AI 어시스턴트 Polly를 3월 18일 기준 플랫폼 전역에서 사용할 수 있도록 확장하고 GA 수준으로 올렸다고 발표했다. Polly는 수백 단계짜리 트레이스와 장시간 대화 스레드를 분석해 실패 지점을 찾아주고, 프롬프트·데이터셋·평가 코드를 직접 수정해 주는 "AI 에이전트 엔지니어"로 설계되었다.

**Why it matters:** tech-review 3-Tier DR 파이프라인(Perplexity→Gemini→ChatGPT)처럼 멀티턴·멀티도구 에이전트 트레이스가 길어질수록 수작업 디버깅이 불가능해지는데, Polly의 자동 실패 지점 분석과 프롬프트 수정은 이 병목을 정확히 겨냥한다.

- LangSmith 모든 페이지 우하단에 상주하며, 페이지 간 대화를 유지하는 persistent memory를 제공한다
- 프롬프트 수정, 실패 런에서 데이터셋 생성, 실험 비교, 평가 코드 자동 작성까지 수행한다
- Cmd+I / Ctrl+I로 어디서든 호출 가능하며, OpenAI·Anthropic 등 모델 API 키를 워크스페이스 시크릿으로 연결한다
- LangChain 오픈소스 프레임워크는 10억 회 이상 다운로드를 기록하며 에이전트 생태계 표준 중 하나로 자리잡았다

**What's next:** LangChain 측은 Polly가 실험·A/B 테스트·평가 결과까지 자동 분석해 어떤 프롬프트·모델·아키텍처가 지표를 올리는지 추천하는 방향으로 진화할 것이라고 예고하고 있다.

**Source:** LangSmith Polly Docs (docs.langchain.com)

---

## Comments