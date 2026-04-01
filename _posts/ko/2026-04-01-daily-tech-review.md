---
layout: post
title: "OpenAI $852B 밸류에이션 / Axios NPM 공급망 공격 / Claude Code 소스 유출"
date: 2026-04-01
lang: ko
permalink: /ko/2026/04/01/daily-tech-review/
pair: 2026-04-01-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line
OpenAI가 사상 최대 $1,220억 펀딩으로 $852B 밸류에이션을 확정하는 날, npm 생태계를 뒤흔든 공급망 공격과 Anthropic의 소스 코드 유출이 동시에 터졌다.

---

## 1. OpenAI, $852B 밸류에이션으로 사상 최대 펀딩 라운드 클로즈

OpenAI가 3월 31일 $1,220억 규모의 펀딩 라운드 클로즈를 공식 발표했다. 기존 공개된 $1,100억에서 증액됐으며, 포스트머니 밸류에이션은 $8,520억으로 확정됐다. SoftBank가 공동 리드를 맡았고 Andreessen Horowitz, D.E. Shaw Ventures 등이 참여했으며, 개인 투자자 대상 은행 채널을 처음 열어 $30억을 추가로 확보했다.

**Why it matters:** AI API를 자동화 파이프라인의 핵심으로 쓰는 개발자 입장에서, $852B 밸류에이션을 뒷받침하는 월 $20억 매출 수치는 단순한 투자 뉴스가 아니다. OpenAI가 IPO 압박 속에서 비용 절감(Sora 앱 종료 등)과 수익화를 동시에 강화한다면, API 가격 정책 변화가 멀티AI 조율 워크플로우의 운영 비용에 직접 영향을 줄 수 있다.

- 라운드 총액 $1,220억, 개인 투자자로부터 $30억 포함 — 은행 채널 최초 활용
- ChatGPT 주간 활성 유저 9억 명 이상, 구독자 5,000만 명 이상
- 월 매출 $20억, 2025년 연간 매출 $131억

**What's next:** Sam Altman은 이 밸류에이션을 정당화해야 하는 압박을 받고 있다. Sora 단편 영상 앱 종료 등 비용 절감 기조를 유지하면서 IPO 준비를 이어갈 전망이다.

**Source:** [OpenAI closes funding round at an $852B valuation](https://www.cnbc.com/2026/03/31/openai-funding-round-ipo.html)

---

## 2. Axios NPM 공급망 공격 — RAT 드로퍼가 100M 다운로드 패키지를 노렸다

3월 30일, 주간 다운로드 1억 회 이상의 JavaScript HTTP 클라이언트 axios에서 두 개의 악성 버전(1.14.1, 0.30.4)이 npm에 배포됐다. 공격자는 유지관리자 계정을 탈취해 plain-crypto-js@4.2.1이라는 가짜 의존성을 주입했고, 이 패키지의 postinstall 스크립트가 macOS, Windows, Linux 세 플랫폼을 대상으로 RAT 드로퍼를 실행했다. 악성 코드는 실행 직후 자기 삭제하고 package.json을 깨끗한 버전으로 교체해 포렌식 탐지를 회피하도록 설계됐다.

**Why it matters:** 자동화 파이프라인이 npm 의존성을 기반으로 돌아간다면, 이번 공격은 추상적 위협이 아니다. axios 자체 코드에는 악성 코드가 한 줄도 없다는 점이 핵심이다 — 의존성 트리를 신뢰하는 순간 공격 벡터가 생긴다. CI/CD 환경에서 outbound 네트워크 모니터링 없이 npm install을 실행한다면 지금 당장 점검이 필요하다.

- 악성 의존성은 공격 18시간 전에 미리 스테이징됨 — 계획된 정밀 공격
- 두 브랜치(1.x, 0.x)가 39분 간격으로 동시 오염됨
- npm install 시작 2초 내에 C2 서버(sfrclak.com:8000)에 콜백 발생

**What's next:** axios@1.14.1 또는 0.30.4를 설치했다면 시스템이 침해됐다고 가정해야 한다. StepSecurity는 4월 1일 커뮤니티 타운홀을 개최해 전체 기술 분석을 공개할 예정이다.

**Source:** [Axios compromised on NPM – Malicious versions drop remote access trojan](https://www.stepsecurity.io/blog/axios-compromised-on-npm-malicious-versions-drop-remote-access-trojan)

---

## 3. Claude Code 소스 유출 — 가짜 툴, 감정 감지, 스텔스 모드

Anthropic이 Claude Code npm 패키지에 소스맵 파일을 실수로 포함시켜, 13만 2,000줄 규모의 TypeScript 소스 코드가 공개됐다. 패키지는 곧 삭제됐지만 이미 광범위하게 미러링됐다. 유출 소스에서 발견된 주요 내용은 다음과 같다: ANTI_DISTILLATION_CC 플래그로 API 요청에 가짜 툴 정의를 주입해 경쟁 모델 학습 데이터를 오염시키는 메커니즘, 사용자 좌절감을 정규식으로 감지하는 코드, AI 신원을 숨기는 undercover mode, 그리고 KAIROS라는 미공개 자율 에이전트 모드.

**Why it matters:** AI 도구를 조율 레이어로 쓰는 입장에서 이번 유출은 여러 레이어를 한꺼번에 드러냈다. 가짜 툴 주입(anti-distillation)은 Claude Code의 API 트래픽을 기록해 경쟁 모델을 학습시키려는 시도를 방어하기 위한 것이다. 다만 조건이 복잡해 — GrowthBook 피처 플래그, 1st-party API 제공자, CLI 진입점 등 4가지 조건 동시 충족 — CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS 환경변수 하나로 비활성화되는 등 실제 방어 효과는 제한적이라는 평가다. Connector-text summarization은 tool call 사이 추론 체인을 요약+암호 서명으로 대체해 외부 기록 시 원본 추론을 노출하지 않도록 설계됐다.

- 하루 약 250,000건의 불필요한 API 호출 패턴 발견
- Anthropic의 이번 주 두 번째 유출 사고 — 며칠 전 모델 spec 유출에 이어
- 미공개 KAIROS 자율 에이전트 모드 코드 존재 확인

**What's next:** KAIROS 자율 에이전트 모드의 실제 출시 여부가 주목된다. Anthropic은 아직 공식 입장을 밝히지 않았다.

**Source:** [The Claude Code Source Leak: fake tools, frustration regexes, undercover mode](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)

---

## Comments