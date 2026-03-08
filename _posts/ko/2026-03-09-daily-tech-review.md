---
layout: post
title: "Pentagon과 OpenAI 협약 체결, Anthropic 공급망 위험 지정으로 AI 업계 대분열 가시화하며 ChatGPT 앱 제거 295% 폭증."
date: 2026-03-09
lang: ko
permalink: /ko/2026/03/09/daily-tech-review/
pair: 2026-03-09-daily-tech-review
tags: ["ai-ml", "models", "research", "benchmarks"]
---

## Today in One Line
Pentagon과 OpenAI 협약 체결, Anthropic 공급망 위험 지정으로 AI 업계 대분열 가시화하며 ChatGPT 앱 제거 295% 폭증.

---

## 1. Pentagon의 Anthropic 공급망 위험 지정, OpenAI와 협약 체결

Anthropic이 자율무기와 대량 감시 금지를 요구하다가 Pentagon(국방부)으로부터 공급망 위험으로 지정되었고, OpenAI는 같은 날 Pentagon과 협약을 체결해 군사 AI 사용 시장을 선점했다. 이 결정으로 미국 국방부 계약업체들은 Anthropic의 Claude 기술 사용 금지를 받게 되었다.

**Why it matters:** AI 안전성 원칙과 국방부 실익 사이의 충돌이 구체적 규제로 구현되었으며, 이는 스타트업이 정부 계약 추구 여부를 근본적으로 재검토하게 만드는 업계 전환점이 될 수 있다. Pentagon의 공급망 위험 지정은 전례 없는 사으로, 국방 기술 계약의 정치화 심화를 의미한다.

- 2월 27일 Pete Hegseth 국방장관이 Anthropic 공급망 위험 선포 후 3월 4일 공식 지정; 3월 5일 OpenAI가 Pentagon과 협약 발표로 동일 시장 확보
- ChatGPT 모바일 앱 제거가 2월 28일 일일 기준 295% 폭증(평상시 9% vs 급증기 약 31%)하며 Claude 앱은 같은 기간 51% 설치 증가, Claude가 미국 App Store 1위 진입
- Anthropic CEO Dario Amodei가 3월 5일 법적 이의제기 예정 선언; OpenAI 하드웨어 책임자 Caitlin Kalinowski도 3월 7일 거버넌스 문제를 이유로 사직

**What's next:** Anthropic의 연방법원 소송과 동시에 Microsoft, Google, Amazon이 Anthropic Claude 비국방 고객 지원 유지 선언으로 기업용 AI 시장은 국방/비국방으로 이분화 진행 예상.

**Source:** [Pentagon Labels Anthropic "Supply-Chain Risk"](https://dailytechnewsshow.com/2026/03/06/pentagon-labels-anthropic-supply-chain-risk-anthropics-ceo-plans-to-challenge-in-court-dth/)

---

## 2. OpenAI $110B 펀딩 라운드 완료, AWS와 Stateful Runtime 협력

OpenAI가 역대 최대 규모 민간 펀딩인 $110B를 조달했으며, Amazon $50B, Nvidia $30B, SoftBank $30B이 참여했다. 동시에 AWS와 Stateful Runtime Environment 개발에 합의해 에이전트가 메모리와 컨스트를 다중 스텝 작업 간 유지하는 기술 구현 예정이다.

**Why it matters:** AI 인프라 경쟁이 단순 모델 능력에서 배포 아키텍처로 이동 중이며, AWS-OpenAI 협력은 기업용 에이전트 시장의 기술 표준화를 주도한다. $110B 규모는 AI가 연구 단계를 넘어 전사 인프라 투자 대상으로 전환됨을 명확히 한다.

- AWS 추가 $100B 장기 계약 체결로 OpenAI 총 계약 규모 $138B 도달; OpenAI는 AWS Trainium 최소 2GW 소비 약정
- Frontier 플랫폼 출시로 State Farm 등 초기 기업 클라이언트 확보, State Farm CEO Joe Park가 "수천 개 에이전트와 직원용 도구 가속화" 발표
- Meta도 2026년 capex $115-$135B 약정(2025년 $72B 대비 60% 증가), Google TPU 멀티년 임차 거래 체결로 인프라 공급처 다변화 추진 중

**What's next:** NVIDIA GTC 2026(3월 16-19일)에서 Jensen Huang이 주요 기조연설 예정이며, 추론 전용 칩과 Groq 기술 통합 공개 예상으로 GPU 패권 구조 변화 신호.

**Source:** [OpenAI raises $110B in one of the largest private funding rounds in history](https://techcrunch.com/2026/02/27/openai-raises-110b-in-one-of-the-largest-private-funding-rounds-in-history/)

---

## 3. Claude Opus 4.6, 2주간 Firefox 22개 보안 취약점 발견

Anthropic의 Claude Opus 4.6이 2월 1-14일 Mozilla와의 협력으로 Firefox에서 22개의 새로운 보안 취약점을 발견했으며, 이 중 14개는 고위험도 CVE로 분류되어 3월 초 Firefox 148에 대부분 수정됨.

**Why it matters:** AI 모델이 보안 취약점 발견 성능에서 인간 전문가 수준 도달을 시연했으며, 14개 고위험도 발견은 2025년 Firefox 전체 고위험도 패치의 약 20%에 해당해 AI 보안 도구의 실제 가치 증명. 이는 오픈소스 프로젝트의 보안 속도를 근본적으로 변화시킬 수 있는 선례 구축.

- Claude Opus 4.6이 20분 내 JavaScript 엔진의 Use-After-Free 버그 1건 식별 후 본격 분석으로 6,000개 C++ 파일 스캔, 총 112개 고유 보고서 제출; 개발 단계에서 $4,000 API 크레딧 소비로 exploits 2건만 성공(성공률 약 0.18%)
- Mozilla 보조 공개 발표에서 추가 90개 버그 발견 확인, 대부분 fuzzing으로 놓친 로직 오류 클래스 포함; Firefox 148 릴리즈로 주요 이슈 대다수 해결
- Anthropic이 3월 6일 Claude Code Security 제한 연구 프리뷰 출시, 자동 보안 검증을 위한 task verifier 시스템 도입으로 패치 신뢰도 향상

**What's next:** frontier 모델들의 취약점 발견/악용 능력 격차 축소 예상으로 방어 우선 전략의 긴급성 증가, 계 정보보안 팀들의 AI 보안 도구 도입 가속화 전망.

**Source:** [Anthropic's Claude found 22 vulnerabilities in Firefox over two weeks](https://techcrunch.com/2026/03/06/anthropics-claude-found-22-vulnerabilities-in-firefox-over-two-weeks/)

## Comments

