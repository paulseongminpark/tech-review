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
에이전트를 어떻게 격리하고, 어떻게 훈련시키고, 어떻게 디버깅할 것인가 — 오늘 세 가지 발표는 AI 개발 스택의 서로 다른 층을 한꺼번에 건드렸다. NVIDIA는 에이전트 실행 경계를 커널 레벨에서 그었고, Unsloth는 파인튜닝 진입 장벽을 노코드 GUI로 허물었으며, LangSmith는 멀티턴 에이전트 디버깅에 AI 어시스턴트를 직접 붙였다. 개발 파이프라인의 보안·훈련·관찰 가능성이 같은 날 동시에 강화된 것이다.

---

## 1. 엔비디아 OpenShell — 자율 AI 에이전트용 오픈소스 샌드박스로 사실상 보안 표준을 노린다

NVIDIA가 GTC 2026에서 자율 AI 에이전트 전용 런타임인 OpenShell을 Apache 2.0 오픈소스로 공개했다. 3월 16일 첫 공개 이후 불과 며칠 만에 v0.0.10까지 알파 버전을 연속 릴리스하고 있다는 점에서, 속도 자체가 메시지다. OpenShell은 에이전트와 인프라 사이에 위치해 파일·네트워크·모델 호출을 YAML 정책으로 통제하는 샌드박스 레이어다. 리눅스 Landlock LSM 기반의 커널 레벨 격리를 채택해, 파일·프로세스·소켓을 선언적 정책 파일 하나로 묶는다. 설치는 curl 한 줄이고, 리눅스 x86_64·ARM64·macOS ARM 바이너리를 모두 제공한다.

무엇보다 눈에 띄는 건 NemoClaw 스택을 통해 Claude Code·Codex·Cursor를 코드 수정 없이 감싸는 것을 목표로 한다는 점이다. 에이전트별로 서로 다른 권한 경계를 인프라 레벨에서 강제할 수 있다는 뜻이다. LangChain·TrendAI·EQTY Lab 등과의 통합도 동시에 발표됐다.

**Why it matters:** 에이전트가 서버 측 코드를 실행하는 구조에서, 권한 경계는 프롬프트로 설정하는 게 아니라 인프라 레이어가 강제해야 한다. 그 레이어가 오픈소스로, 커널 레벨로 등장한 것이 이번 발표의 핵심이다. 엔터프라이즈가 에이전트를 도입할 때 "얼마나 안전하게 격리할 수 있는가"를 물을 텐데, OpenShell은 그 질문에 처음으로 구체적인 인프라 답변을 내놓았다.

- 현재는 알파 단계 소규모 팀 중심이지만, 금융·보안 벤더와의 통합이 이미 발표된 만큼 엔터프라이즈 에이전트용 기본 런타임 위치를 노리는 움직임이 가속될 것으로 보인다.
- curl 한 줄 설치, v0.0.10까지 연속 릴리스, 리눅스 x86_64·ARM64·macOS ARM 바이너리를 제공한다.

**What's next:** 금융·보안 벤더와의 통합이 이미 발표된 만큼, 1년 내 엔터프라이즈 에이전트용 기본 런타임 위치를 노리는 움직임이 가속될 것으로 보인다.

**Source:** NVIDIA OpenShell Developer Guide (docs.nvidia.com)

---

로컬 추론 보안이 잡히면, 다음 질문은 자연스럽게 '그 에이전트를 어떻게 훈련시킬 것인가'로 이어진다.

## 2. Unsloth Studio — 로컬 LLM 파인튜닝을 위한 오픈소스 노코드 웹 UI로 2배 속도·VRAM 70% 절감을 내세운다

Unsloth AI가 3월 17일 'Unsloth Studio'(Beta)를 공개했다. Mac·Windows·Linux에서 100% 로컬로 LLM을 실행·파인튜닝·배포할 수 있는 오픈소스 노코드 웹 UI다. 기존에는 파이썬 스크립트와 복잡한 CUDA 세팅이 필요했던 파인튜닝 과정을, 브라우저 기반 GUI에서 데이터 준비부터 GGUF·vLLM·Ollama 내보내기까지 한 번에 처리하는 것이 목표다.

성능 수치가 이례적이다. Triton 기반 수작업 백워드 패스를 통해 학습 속도 2배, VRAM 70% 절감을 달성했으며, 이는 정확도 손실 없이 이뤄졌다. 지원 모델은 텍스트·비전·TTS·임베딩을 포함해 500개 이상이다. Data Recipes 기능은 노드 기반 그래프 UI로 PDF·CSV·DOCX 파일에서 ChatML·Alpaca 포맷 합성 데이터셋을 자동 생성하고, 훈련 후 GGUF·safetensors·vLLM 포맷으로 원클릭 내보내기가 가능하다.

**Why it matters:** 파인튜닝은 오랫동안 "아는 사람만 하는 영역"이었다. VRAM 70% 절감과 노코드 GUI의 조합은 그 진입 장벽을 허문다. 500개 이상의 모델을 동일한 인터페이스로 다룰 수 있다는 것은, 용도에 맞는 소형 모델을 빠르게 실험하고 배포하는 경로를 실질적으로 연다. 클라우드 API 없이 로컬에서 실행된다는 점도, 데이터 외부 유출 우려가 있는 도메인에서는 결정적 장점이다.

- 현재는 NVIDIA GPU 중심이지만, AMD·Intel GPU와 멀티 GPU, Apple MLX 훈련까지 로드맵에 올려둔 만큼 로컬 LLM 파이프라인의 기본 GUI로 자리 잡을 가능성이 크다.

**What's next:** AMD·Intel GPU와 멀티 GPU, Apple MLX 훈련까지 로드맵에 있어, 로컬 LLM 파이프라인의 기본 GUI로 자리 잡을 가능성이 크다.

**Source:** Unsloth Studio – Introducing Unsloth Studio (unsloth.ai)

---

에이전트를 격리하고 훈련시킨 다음 문제는 실전에서 무엇이 잘못됐는지 찾아내는 것이다.

## 3. LangSmith Polly — LangChain 전역 GA로 에이전트 디버깅·평가·프롬프트 수정을 한 화면에서 처리 가능해진다

LangChain이 3월 18일 LangSmith 내 에이전트 디버깅용 AI 어시스턴트 Polly를 플랫폼 전역에서 사용할 수 있도록 확장하고 GA 수준으로 올렸다. LangChain 오픈소스 프레임워크는 10억 회 이상 다운로드를 기록하며 에이전트 생태계 표준 중 하나로 자리잡았는데, 그 위에서 돌아가는 에이전트가 복잡해질수록 디버깅이 불가능해지는 문제가 쌓여왔다.

Polly는 수백 단계짜리 트레이스와 장시간 대화 스레드를 분석해 실패 지점을 찾아주고, 프롬프트·데이터셋·평가 코드를 직접 수정해 주는 "AI 에이전트 엔지니어"로 설계됐다. LangSmith 모든 페이지 우하단에 상주하며, 페이지 간 대화를 유지하는 persistent memory를 제공한다. Cmd+I / Ctrl+I로 어디서든 호출 가능하고, OpenAI·Anthropic 등 모델 API 키를 워크스페이스 시크릿으로 연결한다. 실패 런에서 데이터셋 생성, 실험 비교, 평가 코드 자동 작성까지 처리한다.

**Why it matters:** 멀티턴·멀티도구 에이전트 트레이스가 길어질수록 수작업 디버깅은 사실상 불가능해진다. 수백 단계 트레이스에서 어느 지점이 문제였는지를 AI가 자동으로 짚어주고, 프롬프트 수정까지 제안한다는 것은 디버깅 사이클 자체를 단축한다. 에이전트 파이프라인이 복잡해질수록 관찰 가능성(observability) 도구의 가치는 선형이 아닌 지수적으로 올라간다.

- LangChain 측은 Polly가 실험·A/B 테스트·평가 결과까지 자동 분석해 어떤 프롬프트·모델·아키텍처가 지표를 올리는지 추천하는 방향으로 진화할 것이라고 예고하고 있다.

**What's next:** LangChain 측은 Polly가 실험·A/B 테스트·평가 결과까지 자동 분석해 어떤 프롬프트·모델·아키텍처가 지표를 올리는지 추천하는 방향으로 진화할 것이라고 예고한다.

**Source:** LangSmith Polly Docs (docs.langchain.com)

---

## Comments
