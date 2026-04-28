---
layout: post
title: "1930년대 언어 모델 Talkie / GitHub Actions 공급망 위기 / GitHub 가용성 이슈"
date: 2026-04-29
lang: ko
permalink: /ko/2026/04/29/daily-tech-review/
pair: 2026-04-29-daily-tech-review
tags: ["ai-industry", "business-model", "enterprise-ai", "vertical-ai"]
source_type: free-sources
---

## Today in One Line
오늘의 공통 주제는 의존성의 취약성이다. GitHub Actions가 지난 18개월간 반복된 오픈소스 공급망 사고의 공통 진입점이었다는 분석이 나왔고, GitHub 자체도 가용성 이슈를 공식 공개했다. 그 사이, 1930년 이전 텍스트로만 훈련된 13B 언어 모델이 AI 연구에 조용한 질문을 던지고 있다.

---

## 1. 1930년에서 온 AI: Talkie, 과거를 훈련한 13B 모델

Nick Levine, David Duvenaud, Alec Radford — GPT-2 공동 저자로 알려진 Radford의 이름이 올라간 순간 주목을 끌 수밖에 없었다. 이들이 공개한 Talkie는 1931년 이전 텍스트로만 훈련된 13B 파라미터 언어 모델이다. 핵심 질문은 단순하다: 현대를 전혀 모르는 모델과 대화하면 무엇을 얻을 수 있는가. 팀은 뉴욕타임스 역사적 사건 설명 약 5,000개를 Talkie에 입력해 각 사건이 모델에게 얼마나 "놀라운" 것인지 bits per byte로 측정했다. 결과는 예측 가능하면서도 흥미롭다: 1930년 이후 사건일수록 높은 놀라움 수치를 기록했고, 모델 크기가 커질수록 사전 지식 범위 내 사건을 더 효율적으로 압축했다. 현재 talkie-lm.com에서는 Claude Sonnet 4.6이 Talkie를 24/7 프롬프팅하는 라이브 피드를 공개 중이다. vintage LM이 현대 모델과 실시간으로 대화하는 장면은 그 자체로 하나의 실험적 퍼포먼스다.

**Why it matters:** 더 크고, 더 많은 데이터, 더 빠른 모델로 달리는 AI 경쟁 속에서, 이 팀은 반대 방향의 실험으로 LLM이 어떻게 지식을 표현하고 압축하는지 근본적으로 파고든다. 특정 도메인 데이터만으로 훈련된 소형 모델이 범용 대형 모델을 능가할 수 있다는 가설을 실증적으로 검증하는 길을 열 수 있다는 점이 AI 스타트업 입장에서 실질적인 관심사다.

- Alec Radford, David Duvenaud 참여 — 모델 및 코드 HuggingFace와 GitHub에 오픈소스 공개
- 모델 크기별 지식 압축 효율 비교 분석(Figure 1c, 1d) 논문 초안 동시 공개

**What's next:** 팀이 예고한 모델 크기별 비교 분석이 이어질 전망이다. vintage LM의 지식 경계를 수치로 확정하면 도메인 특화 소형 모델 설계의 이론적 근거가 더 탄탄해진다.

**Source:** [Introducing talkie: a 13B vintage language model from 1930](https://talkie-lm.com/introducing-talkie)

---

AI 연구가 새로운 실험 방향을 탐색하는 사이, 스타트업 엔지니어들이 매일 쓰는 인프라에서는 더 급박한 경고음이 울리고 있었다.

## 2. GitHub Actions는 왜 공급망 사고의 공통 분모인가

Andrew Nesbitt의 분석은 서두부터 직설적이다: 지난 18개월간 주요 오픈소스 공급망 사고를 역추적하면 거의 예외 없이 .github/workflows YAML 파일로 이어진다. Ultralytics에 크립토 마이너가 심겼고, tj-actions/changed-files 사건으로 23,000개 레포지토리의 secrets가 퍼블릭 빌드 로그에 노출됐으며, elementary-data는 외부인의 GitHub 댓글이 달린 지 10분 만에 악성 wheel을 배포했다. 이 사건들의 공통점은 GitHub Actions 기능이 "문서대로 정확히" 동작했다는 것이다. pull_request_target 트리거는 포크된 코드를 원본 레포의 컨텍스트에서 full secret access와 write 토큰을 가지고 실행할 수 있도록 설계됐고, 2021년부터 GitHub 문서가 이 조합의 위험성을 경고해왔지만 기본값은 바뀌지 않았다. 더 구조적인 문제는 uses 한 줄이 외부 레포의 mutable git 태그를 참조한다는 점이다. 2024년 11월 spotbugs에서 탈취한 PAT 하나가 reviewdog 태그를 교체했고, 그 연쇄가 23,000개 레포에 전파됐다. CISA가 권고문을 발행했고, 최초 표적이 Coinbase였음이 사후에 확인됐다.

**Why it matters:** 이것은 보안 취약점이 아니라 설계 철학의 불일치다. GitHub Actions는 기업 내부 CI 도구로 시작했고, 그 기본값이 익명 포크와 드라이브바이 PR이 존재하는 오픈소스 환경에 맞게 재설계된 적이 없다. 스타트업들이 GitHub Actions를 표준 파이프라인으로 채택하는 한, 이 구조적 위험은 기본 설정 그대로 따라온다.

- pull_request_target + fork checkout 조합이 연쇄 침해의 공통 진입점
- 현재 가장 실용적인 완화책은 actions 버전을 content hash로 핀닝하는 것

**What's next:** Nesbitt은 action 로더 수준의 구조 변경 없이는 근본 해결이 어렵다고 본다. GitHub이 기본값을 변경하거나 mutable 태그 소비를 제한하는 방향으로 움직이지 않는 한 유사 사고는 반복될 것이다.

**Source:** [GitHub Actions is the weakest link](https://nesbitt.io/2026/04/28/github-actions-is-the-weakest-link.html)

---

파이프라인 보안이 구조적 문제라면, 플랫폼 자체의 신뢰성 문제는 또 다른 차원의 리스크다.

## 3. GitHub 가용성 업데이트, 플랫폼 집중화의 대가

GitHub이 가용성 관련 공식 업데이트를 블로그에 게재했다. 세부 내용은 제한적이지만, GitHub이 company news 채널을 통해 가용성 이슈를 직접 공개한다는 사실 자체가 플랫폼 의존도가 높은 생태계에서 하나의 신호다. 오늘날 스타트업 기술 스택에서 GitHub은 코드 호스팅, CI/CD, 이슈 트래킹, 코드 리뷰가 한데 모인 중심축이다. 업무 흐름의 대부분이 GitHub을 거쳐간다. 이 구조에서 플랫폼 다운타임은 단순한 불편이 아니다: 배포가 중단되고, 팀 협업이 멈추고, 고객 영향이 생긴다. Lobsters 커뮤니티에서 이 글이 빠르게 주목받은 것은, 개발자들이 이 의존성의 무게를 이미 체감하고 있기 때문이다.

**Why it matters:** 플랫폼 집중화는 생산성과 단일 장애점을 함께 가져온다. GitHub에 더 많은 워크플로우를 위임할수록 가용성 이슈의 파급력은 비례해 커진다. 빠르게 빌드하기 위해 선택한 의존성들이, 규모가 커지면 리스크 목록이 되는 것은 스타트업이 반복하는 아이러니다.

- GitHub Actions 보안 이슈와 가용성 이슈가 같은 날 동시에 주목받은 것은 우연이 아니다
- 플랫폼 분산 전략이나 self-hosted 옵션 검토가 현실적인 대응으로 부상 중

**What's next:** GitHub이 근본 원인 분석(RCA)과 재발 방지 계획을 후속 포스트로 공개할 것으로 보인다. 장기적으로 멀티 플랫폼 전략을 검토하는 팀이 늘어날 전망이다.

**Source:** [An update on GitHub availability](https://github.blog/news-insights/company-news/an-update-on-github-availability/)

---

## Comments
