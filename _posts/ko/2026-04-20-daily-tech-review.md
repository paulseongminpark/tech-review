---

```markdown
---
layout: post
title: "Claude Code 커맨드 인젝션 취약점 3건 / Claude Design, Figma에 도전 / VLM은 왜 감정을 못 읽나"
date: 2026-04-20
lang: ko
permalink: /ko/2026/04/20/daily-tech-review/
pair: 2026-04-20-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
source_type: free-sources
---

## Today in One Line

이번 주 첫날, Anthropic이 보안 사고와 제품 출시를 동시에 기록했다. Claude Code에서 CVSS 9.8짜리 커맨드 인젝션 취약점 3건이 드러난 바로 그날, 프롬프트로 UI 프로토타입을 만드는 Claude Design이 공개됐다. 그 사이 연구자들은 수많은 벤치마크를 통과한 시각-언어 모델이 왜 인간의 감정은 제대로 읽지 못하는지를 질문으로 꺼냈다.

---

## 1. Claude Code, CVSS 9.8 — 커맨드 인젝션 취약점 3건

Anthropic의 Claude Code AI 에이전트에서 커맨드 인젝션 취약점 3건이 드러났다. 모두 CVE-2026-35022로 묶여 CVSS 9.8이라는 최고 수준의 위험 점수를 받았다. 첫 번째 취약점(VULN-01)은 TERMINAL 환경 변수를 읽는 과정에서 발생한다. Node.js 런타임이 이 변수를 셸 명령 문자열에 직접 삽입하므로, .env 파일이나 CI/CD 설정에 메타문자만 심으면 사용자 권한 전체로 임의 코드가 실행된다. 사용자 상호작용 없이 자동으로 터지는 제로클릭 공격이다. 두 번째(VULN-02)는 편집기 호출부의 파일 경로 처리에서 생긴다. 더블 쿼트로 경로를 감싸도 POSIX 셸은 그 안의 명령 치환($() 또는 백틱)을 해석한다. 악의적 파일명이 담긴 저장소를 클론한 뒤 CLI로 열기만 해도 명령이 실행되는 구조다. 세 번째(VULN-03)가 가장 심각하다. 인증 헬퍼 서브시스템이 settings에서 읽은 명령을 전체 셸 해석으로 실행하고, 비대화형 모드에서는 신뢰 다이얼로그를 건너뛴다. 악의적 PR이 workspace settings를 수정하면 CI/CD 러너에서 AWS, GCP, Anthropic API 키가 통째로 빠져나간다. 인증 헬퍼는 에이전트 보안 샌드박스 이전에 실행되므로 내장 권한 체크를 전부 우회한다.

**Why it matters:** VULN-03은 Poisoned Pipeline Execution 패턴과 결합할 때 단 하나의 악의적 PR이 전체 소프트웨어 공급망을 무너뜨릴 수 있다. 이 취약점은 개별 개발자의 문제가 아니라 CI/CD 인프라를 공유하는 팀 전체의 위협이다. "AI 도구이니까 안전하겠지"라는 암묵적 신뢰가 얼마나 위험한 전제인지 정면으로 보여주는 사례다.

- 영향 버전: CLI 0.2.87, Claude Code 2.1.87 — 즉시 최신 버전으로 업데이트 필요
- 인증 헬퍼 사용 중단, ANTHROPIC_API_KEY 환경 변수 직접 설정으로 전환 권장
- .claude/settings.json 변경은 코드 리뷰와 동일한 수준의 PR 심사 필수, CI/CD에서 신뢰되지 않은 PR 대상 CLI 실행 금지

**What's next:** Anthropic은 셸 문자열 실행을 argv 기반 프로세스 스폰으로 교체하고 설정 소스 문자열에 메타문자 거부 정책을 강화할 것을 권고받았다. 이 패턴이 다른 AI 코딩 에이전트에도 잠재할 가능성이 높다.

**Source:** [Anthropic Claude Code Leak Reveals Critical Command Injection Vulnerabilities](https://beyondmachines.net/event_details/anthropic-claude-code-leak-reveals-critical-command-injection-vulnerabilities-e-6-c-1-k/gD2P6Ple2L)

---

보안 구멍이 드러난 같은 날, Anthropic은 정반대 방향의 뉴스도 내놓았다.

## 2. Claude Design: 프롬프트 한 줄로 프로토타입을 — Figma에 도전장

Anthropic이 Claude Design을 공개했다. 프롬프트를 입력하면 UI 프로토타입을 생성해 주는 도구다. VentureBeat는 이를 Figma에 대한 직접 도전으로 평가했다. 텍스트 설명에서 곧바로 인터페이스 프로토타입을 만든다는 개념 자체가 완전히 새롭지는 않다. v0(Vercel), Bolt, Lovable 같은 도구들이 이미 이 영역에서 먼저 자리를 잡았다. 그러나 Anthropic이 직접 뛰어들었다는 것은 신호가 다르다. 이 시장이 실험 단계를 넘어 본격적인 경쟁 영역이 됐다는 선언이다. Figma가 AI 기능을 내부로 흡수하는 방향으로 움직이는 동안, Anthropic은 AI에서 출발해 디자인 도구 쪽으로 접근하는 역방향 전략을 택했다.

**Why it matters:** 이 대결의 본질은 디자인 소프트웨어 시장 점유율이 아니다. 프로덕트를 만드는 과정에서 AI가 어디까지 결정권을 가져가는지에 대한 싸움이다. Claude Design이 설득력 있는 프로토타입을 만들어낼수록, 디자이너와 개발자 사이의 역할 경계는 더 빠르게 흐려진다. 어느 방향이 실제 워크플로를 포착하는가가 앞으로 1~2년의 핵심 경쟁이 될 것이다.

- 프롬프트 → UI 프로토타입 직접 생성
- 경쟁 구도: Figma AI, v0, Bolt, Lovable, Galileo AI

**What's next:** Claude Design이 기존 디자인 워크플로와 통합 가능한지, 아니면 독립 워크플로로 정착하는지에 따라 실제 채택률이 결정될 것이다.

**Source:** [Anthropic just launched Claude Design, an AI tool that turns prompts into prototypes and challenges Figma](https://venturebeat.com/technology/anthropic-just-launched-claude-design-an-ai-tool-that-turns-prompts-into-prototypes-and-challenges-figma)

---

도구 경쟁이 가속되는 사이, 연구자들은 이 도구들의 기반이 되는 모델에 더 근본적인 질문을 던졌다.

## 3. VLM은 왜 인간의 감정을 못 읽나

시각-언어 모델(VLM)은 최근 몇 년간 수많은 시각 태스크에서 인상적인 성과를 냈다. 그런데 지능형 시스템이 인간과 상호작용하는 데 가장 기본이 되는 능력인 감정 인식에서 VLM이 유독 취약하다는 연구가 arXiv에 게재됐다. 물체 분류, 장면 이해, 시각적 질의응답은 잘하면서 왜 감정만 안 되는가. 이 질문은 표면적인 성능 지표 너머를 들여다보게 만든다. 감정은 문맥 의존적이고 문화적 편차가 크다. 표정 하나에도 미묘한 강도 차이가 있고, 같은 표정이 상황에 따라 전혀 다른 감정을 의미할 수 있다. 이런 복합 신호를 텍스트-이미지 쌍 학습만으로 포착하는 데는 구조적 한계가 있을 수 있다는 것이 연구가 꺼낸 문제 의식이다.

**Why it matters:** AI 시스템이 의료 상담, 교육, 고객 응대처럼 감정이 중요한 영역으로 빠르게 확장되는 지금, 이 약점은 단순한 연구 과제로 머물지 않는다. "비전 능력이 된다"는 것과 "감정을 이해한다"는 것은 전혀 다른 문제다. 현재 VLM 훈련 패러다임이 이 간극을 메우지 못하고 있다면, 실제 운용 환경에서 예측 불가능한 오류가 생긴다.

- VLM은 다양한 시각 태스크에서 성과를 냈으나 감정 인식에서 구조적 약점 노출
- 원인 후보: 훈련 데이터 구성, 멀티모달 정렬 방식, 감정의 문맥 의존성과 문화적 편차

**What's next:** 감정 특화 벤치마크와 훈련 전략이 후속 연구의 중심이 될 것이다. 인간-AI 인터랙션의 품질을 실질적으로 높이려면 이 문제를 정면으로 다루는 접근이 필요하다.

**Source:** [Why Do Vision Language Models Struggle To Recognize Human Emotions?](http://arxiv.org/abs/2604.15280v1)

---

## Comments
```

---

저장 경로: _posts/ko/2026-04-20-daily-tech-review.md

선택된 3건: Claude Code 보안 취약점(CVE-2026-35022), Claude Design 출시, VLM 감정 인식 연구. 저장 권한 허용하면 즉시 파일 생성한다.