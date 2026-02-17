# Daily Digest Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Perplexity 리서치를 Daily Digest 형식으로 변환하여 Jekyll 블로그에 게시

**Architecture:** Perplexity 리서치 3개를 파싱하여 10-15개 핵심 뉴스를 선별하고, 3-섹션 구조(주요 발표, 기업 전략, 트렌드)로 정리한 Daily Digest 포스트를 생성. Comments는 Claude API로 자동 생성.

**Tech Stack:** Jekyll/Markdown, Claude API (Haiku), Python, Git

---

## Task 1: 샘플 Daily Digest 작성 (KO) - 콘텐츠 선별 및 구조화

**Files:**
- Create: `_posts/ko/2026-02-17-daily-digest.md`

**Step 1: Perplexity 리서치 3개 분석**

제공받은 리서치:
1. 2026년 2월 둘째~셋째 주 글로벌 기술 개발·전략 동향
2. 2026년 2월 2주차 AI·테크 핵심 동향
3. 2026년 2월 둘째 주 글로벌 기술·AI 동향 브리핑

각 리서치에서:
- 핵심 뉴스 10-20개 식별
- 중복 제거
- 우선순위 정렬 (실제 출시물 > 파트너십 > 트렌드)

**Step 2: 10-15개 핵심 뉴스 선별**

우선순위 기준:
```
높음  ✓ Anthropic Claude Opus 4.6
      ✓ OpenAI Frontier
      ✓ MiniMax M2.5
      ✓ Snowflake-OpenAI 파트너십
      ✓ Mistral Voxtral Transcribe 2
      ✓ ByteDance Seedance 2.0

중간  ○ Anthropic 무광고 전략
      ○ Amazon AI 콘텐츠 마켓플레이스
      ○ 에이전트 오케스트레이션 트렌드
      ○ Edge AI 분산 인프라

선택  △ 뉴로모픽 컴퓨팅
      △ 중국 저가 모델 러시
      △ Sovereign AI (캐나다-독일)
```

**Step 3: 3-섹션으로 분류**

```
주요 발표 & 제품 (5-6개):
- Claude Opus 4.6
- OpenAI Frontier
- MiniMax M2.5
- Mistral Voxtral Transcribe 2
- ByteDance Seedance 2.0
- Snowflake Cortex Code

기업 전략 & 파트너십 (3-4개):
- Snowflake-OpenAI 2억달러
- Anthropic 무광고 전략
- Amazon AI 콘텐츠 마켓플레이스

트렌드 & 인사이트 (3-4개):
- 에이전트 오케스트레이션
- 중국 저가 모델 러시
- Edge AI 분산 인프라
- Sovereign/Confidential AI
```

**Step 4: Front Matter 작성**

Create: `_posts/ko/2026-02-17-daily-digest.md`

```yaml
---
layout: post
title: "데일리 테크 다이제스트 - 2월 17일"
date: 2026-02-17
lang: ko
pair: 2026-02-17-daily-digest
tags: [ai, tech, digest]
---
```

**Step 5: "오늘의 핵심 요약" 작성**

전체 흐름을 3-5줄로 요약:

```markdown
## 오늘의 핵심 요약

이번 주 기술 동향의 핵심은 세 가지 축으로 요약된다.
첫째, Anthropic Claude Opus 4.6과 OpenAI Frontier로 대표되는 **멀티에이전트·오케스트레이션** 시대의 본격화.
둘째, MiniMax M2.5 등 중국발 **초저가 프런티어 모델**의 등장으로 글로벌 가격 구조 재편.
셋째, Edge AI·Sovereign AI·Confidential AI로 확장되는 **인프라·거버넌스** 경쟁 가속.
```

**Step 6: "주요 발표 & 제품" 섹션 작성**

각 뉴스당 3-5줄:

```markdown
## 주요 발표 & 제품

### Anthropic Claude Opus 4.6
멀티에이전트 "agent teams" 기능과 100만 토큰 컨텍스트를 제공하는 신규 모델 출시.
코드 플래닝, 리팩터링, 디버깅 성능이 향상되었으며, 대형 코드베이스와 재무 모델 작업에 특화.
단일 에이전트가 아닌 역할 분담된 복수 에이전트가 병렬로 처리하는 구조를 지원하며,
"챗봇 → 업무용 에이전트 팀" 전환을 가속하는 신호로 평가됨.

### OpenAI Frontier
엔터프라이즈 에이전트 플랫폼으로, 기업 내부 시스템과 데이터 웨어하우스를 연결해
여러 AI 에이전트를 "디지털 직원"처럼 운영하는 인프라 제공.
Business Context와 Agent Execution 계층을 통해 사내 시스템을 하나의 의미론적 레이어로 통합.
Intuit, State Farm, Uber 등이 초기 고객으로 참여 중.

### MiniMax M2.5 Lightning
중국 스타트업이 출시한 초저가 프런티어 모델로, GPT-5.2 대비 1/10~1/20 수준의 토큰 단가 제공.
주요 벤치마크에서 Google·Anthropic 모델에 근접한 성능을 보이며, 수정 MIT 라이선스로 오픈 배포.
MiniMax 내부에서 업무의 30%와 신규 코드의 80%를 M2.5가 생성한다고 밝히며,
에이전트 대량 운영의 경제성을 근본적으로 변화시키는 신호로 평가됨.

### Mistral Voxtral Transcribe 2
초저지연(200ms 이하) 실시간 음성 인식 모델로, Apache 2.0 라이선스 오픈소스 제공.
다국어 지원, 분당 약 0.003달러 수준의 가격으로 클라우드 호출 없이 현장 장비에서 실행 가능.
콜센터, 회의록, 실시간 번역 등 엣지/온디바이스 음성 AI 활용 가능성을 대폭 확대.

### ByteDance Seedance 2.0
텍스트·이미지·오디오·비디오를 한 번에 입력받는 쿼드모달 비디오 생성 모델.
하나의 시퀀스를 여러 샷으로 나누어 카메라·구도·전환까지 자동 연출하는 멀티샷 스토리보딩 지원.
상용 수준의 광고·쇼츠에 가까운 상세 카메라 워크와 물리 일관성을 보여주며,
중국 플랫폼(틱톡/두인)의 모델-플랫폼 수직 통합 전략을 명확히 함.

### Snowflake Cortex Code
Snowflake 네이티브 AI 코딩 에이전트로, 엔터프라이즈 데이터 문맥을 이해하는 에이전트가
데이터 파이프라인·애플리케이션 개발까지 자동화하도록 설계.
데이터 클라우드 사업자들이 "데이터+에이전트 런타임"을 하나의 패키지로 판매하는 구조로 이동 중.
```

**Step 7: "기업 전략 & 파트너십" 섹션 작성**

```markdown
## 기업 전략 & 파트너십

### Snowflake-OpenAI 2억달러 파트너십
다년간 2억 달러 규모의 파트너십을 체결, GPT-5.2 등 OpenAI 모델을 Snowflake Cortex AI 전역에서
네이티브로 호출 가능하도록 통합.
거버넌스된 데이터 위에서 컨텍스트 어웨어 에이전트를 빌드할 수 있는 구조를 제공하며,
"에이전트+엔터프라이즈 데이터" 인프라 레이어 구축의 핵심 사례로 평가됨.

### Anthropic 무광고 전략
Claude에 광고를 넣지 않겠다고 공식 선언하며, Super Bowl 광고까지 동원해
"무광고·신뢰성" 프레임 강화.
동시에 무료 플랜에 파일 생성, 커넥터, Skills, 대화 길이 확대 등 유료 기능 상당수를 개방.
OpenAI의 ChatGPT 광고 도입과 대조되며, "광고 vs 무광고" 수익모델 분기점이 명확해짐.

### Amazon AI 콘텐츠 마켓플레이스
퍼블리셔가 자사 콘텐츠를 AI 기업에 라이선스하고, AWS Bedrock 등과 연계하는
"AI 콘텐츠 증권거래소" 형태의 마켓플레이스 준비 중.
훈련·추론용 데이터 라이선스를 정식 거래소 형태로 만들고,
퍼블리셔에게 사용량 기반 보상을 제공하는 구조로 설계.
```

**Step 8: "트렌드 & 인사이트" 섹션 작성**

```markdown
## 트렌드 & 인사이트

### 에이전트 오케스트레이션 필수화
단일 에이전트는 복잡한 엔터프라이즈 워크플로를 감당하지 못하며,
역할 분리된 다수 에이전트와 상위 코디네이터를 갖춘 멀티에이전트 아키텍처가 필수로 전환.
Microsoft는 Agent2Agent(A2A) 프로토콜을 밀고, OpenAI는 Frontier로 에이전트 제어면을 노리는 중.
거버넌스 체계를 먼저 구축한 기업이 더 가치 높은 워크플로에 에이전트를 투입할 수 있어 경쟁우위 확보.

### 중국 저가 모델 러시
DeepSeek Shock 1년 후, DeepSeek V4·Alibaba Qwen 3.5·ByteDance 등
중국 업체들이 저가·고성능 모델을 잇달아 발표하며, 미국 빅테크의 고단가 전략을 흔들고 있음.
중국 모델은 통상 미국 동급 모델 대비 1/6~1/4 비용으로 운영되며,
글로벌 토큰 단가를 10-20배 낮추는 방향으로 가격 경쟁 심화.

### Edge AI 분산 인프라
EPRI·NVIDIA·Prologis는 변전소 인근 5-20MW급 소형 데이터센터를 여러 지역에 구축해,
대규모 중앙 데이터센터가 아닌 분산형 AI 추론 인프라를 실험 중.
2026년 AI의 핵심 전장은 "클라우드 학습"이 아니라 "엣지 추론"으로 이동하며,
공장·리테일·원격 사이트 등에서 실시간 의사결정이 필요해짐.

### Sovereign/Confidential AI
캐나다-독일 Sovereign Technology Alliance, 칠레 Latam-GPT, OPAQUE Confidential AI 등
"누가 어느 데이터로 어떤 모델을 어떤 행위에 사용했는가"를 추적·제어·검증하는 기능이 부상.
중장기적으로 엔터프라이즈 AI는 "성능/가격"뿐 아니라
"설명 가능한 계보, 규제 준수, 정책 검증 가능성"이 핵심 구매 기준이 될 가능성.
```

**Step 9: Source 섹션 작성**

Perplexity 리서치에서 인용한 모든 URL 나열:

```markdown
## Source

### AI/ML 혁신
- [Anthropic Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)
- [OpenAI Frontier](https://openai.com/business/frontier/)
- [MiniMax M2.5](https://www.minimax.io/news/minimax-m25)
- [Mistral Voxtral Transcribe 2](https://mistral.ai/news/voxtral-transcribe-2)
- [ByteDance Seedance 2.0](https://www.forbes.com/sites/ronschmelzer/2026/02/12/bytedances-seedance-20-nails-real-world-physics-and-hyper-real-outputs/)
- [Snowflake Cortex Code](https://www.linkedin.com/pulse/enterprise-technology-news-week-february-6th-2026-ri3te)

### 기업 전략
- [Snowflake-OpenAI Partnership](https://www.marketingprofs.com/opinions/2026/54257/ai-update-february-6-2026-ai-news-and-views-from-the-past-week)
- [Anthropic No Ads](https://www.cnbc.com/2026/02/04/anthropic-no-ads-claude-chatbot-openai-chatgpt.html)
- [Amazon AI Content Marketplace](https://finance.yahoo.com/news/amazon-plans-ai-content-marketplace-114027537.html)

### 트렌드
- [Agentic AI 2026](https://www.nexgenarchitects.com/blog-posts/agentic-ai-predictions-2026)
- [DeepSeek China AI Rush](https://finance.yahoo.com/news/deepseek-shock-set-flurry-low-062633968.html)
- [Edge AI Infrastructure](https://www.edgeir.com/ai-inference-moves-closer-to-the-grid-as-smaller-data-centers-take-shape-20260216)
- [Canada-Germany Sovereign AI](https://www.canada.ca/en/innovation-science-economic-development/news/2026/02/canada-and-germany-sign-ai-joint-declaration-and-launch-sovereign-technology-alliance.html)

### 전체 주간 요약
- [AI Update Feb 13, 2026](https://www.marketingprofs.com/opinions/2026/54304/ai-update-february-13-2026-ai-news-and-views-from-the-past-week)
- [AI Update Feb 6, 2026](https://www.marketingprofs.com/opinions/2026/54257/ai-update-february-6-2026-ai-news-and-views-from-the-past-week)
```

**Step 10: Comments 섹션 플레이스홀더**

```markdown
## Comments
<!-- Claude API로 자동 생성 예정 -->
```

**Step 11: 검토 및 조정**

- 총 뉴스 개수: 13개 (주요 발표 6 + 기업 전략 3 + 트렌드 4) ✓
- 각 뉴스 길이: 3-5줄 ✓
- 섹션 구조: 오늘의 핵심 요약 + 3-섹션 + Source + Comments ✓
- Front matter: 완성 ✓

**Step 12: 파일 저장**

Save: `_posts/ko/2026-02-17-daily-digest.md`

---

## Task 2: 샘플 Daily Digest 작성 (EN) - 영문 버전 생성

**Files:**
- Create: `_posts/en/2026-02-17-daily-digest.md`

**Step 1: Front Matter 작성**

```yaml
---
layout: post
title: "Daily Tech Digest - Feb 17, 2026"
date: 2026-02-17
lang: en
pair: 2026-02-17-daily-digest
tags: [ai, tech, digest]
---
```

**Step 2: 한국어 버전 기반으로 영문 작성**

Note: Perplexity 리서치가 한국어로 제공되었으므로, 영문은 한국어 버전을 번역/각색.

**핵심 원칙**:
- 단순 번역이 아닌, 영어 독자에 맞춘 표현
- 기술 용어는 원어 유지
- URL은 동일

**Step 3: "Today's Key Summary" 작성**

```markdown
## Today's Key Summary

This week's tech landscape centers on three key axes.
First, the **multi-agent orchestration** era arrives in earnest with Anthropic Claude Opus 4.6 and OpenAI Frontier.
Second, **ultra-low-cost frontier models** from China (MiniMax M2.5) reshape global pricing structures.
Third, competition accelerates around **infrastructure and governance** with Edge AI, Sovereign AI, and Confidential AI.
```

**Step 4: "Major Releases & Products" 섹션 작성**

```markdown
## Major Releases & Products

### Anthropic Claude Opus 4.6
Ships multi-agent "agent teams" capability and 1M token context window.
Enhanced code planning, refactoring, and debugging performance optimized for large codebases and financial models.
Supports role-separated agent teams working in parallel instead of single-agent sequential processing,
signaling the shift from "chatbot → work-ready agent teams."

### OpenAI Frontier
Enterprise agent platform connecting internal systems and data warehouses to operate
multiple AI agents as "digital employees."
Provides Business Context and Agent Execution layers to unify internal systems into a semantic layer.
Early customers include Intuit, State Farm, and Uber.

### MiniMax M2.5 Lightning
Ultra-low-cost frontier model from Chinese startup offering 1/10~1/20 of GPT-5.2's token price.
Performance near Google and Anthropic models on major benchmarks, released as open-weight with modified MIT license.
MiniMax reports 30% of work and 80% of new code generated by M2.5,
fundamentally changing the economics of mass agent deployment.

### Mistral Voxtral Transcribe 2
Real-time speech recognition model with ultra-low latency (<200ms), provided as Apache 2.0 open source.
Multilingual support, ~$0.003 per minute pricing, runs on-device without cloud calls.
Dramatically expands edge/on-device voice AI use cases in call centers, meeting transcription, and real-time translation.

### ByteDance Seedance 2.0
Quad-modal video generation model ingesting text, image, audio, and video simultaneously.
Supports multi-shot storyboarding with automatic camera work, composition, and transitions.
Shows commercial-grade detail and physics consistency for ads and shorts,
clarifying Chinese platforms' (TikTok/Douyin) model-platform vertical integration strategy.

### Snowflake Cortex Code
Snowflake-native AI coding agent designed to automate data pipeline and application development
with enterprise data context understanding.
Data cloud vendors moving toward "data + agent runtime" as bundled offering.
```

**Step 5: "Corporate Strategy & Partnerships" 섹션 작성**

```markdown
## Corporate Strategy & Partnerships

### Snowflake-OpenAI $200M Partnership
Multi-year $200M partnership integrating GPT-5.2 and other OpenAI models natively across Snowflake Cortex AI.
Enables building context-aware agents on governed data,
serving as key case of "agent + enterprise data" infrastructure layer construction.

### Anthropic's No-Ads Strategy
Officially declares no ads in Claude, reinforcing "ad-free and trustworthy" framing with Super Bowl campaign.
Simultaneously opens many premium features (file creation, connectors, Skills, conversation length) to free tier.
Contrasts sharply with OpenAI's ChatGPT ad rollout, clarifying "ad-based vs ad-free" revenue model bifurcation.

### Amazon AI Content Marketplace
Preparing "AI content securities exchange" where publishers license content to AI firms,
integrated with AWS Bedrock ecosystem.
Designed to formalize training/inference data licensing with usage-based publisher compensation.
```

**Step 6: "Trends & Insights" 섹션 작성**

```markdown
## Trends & Insights

### Agent Orchestration Becomes Essential
Single agents can't handle complex enterprise workflows;
multi-agent architectures with role separation and coordinator layers becoming mandatory.
Microsoft pushes Agent2Agent (A2A) protocol, OpenAI targets agent control plane with Frontier.
Organizations establishing governance frameworks first gain competitive advantage in deploying agents to high-value workflows.

### China's Low-Cost Model Rush
One year after DeepSeek Shock, Chinese firms (DeepSeek V4, Alibaba Qwen 3.5, ByteDance)
release low-cost, high-performance models challenging US big tech's premium pricing.
Chinese models typically operate at 1/6~1/4 cost of US equivalents,
intensifying price competition that lowers global token pricing 10-20x.

### Edge AI Distributed Infrastructure
EPRI, NVIDIA, Prologis building 5-20MW small data centers near substations across regions,
experimenting with distributed AI inference infrastructure over massive centralized data centers.
2026's key AI battleground shifts from "cloud training" to "edge inference,"
requiring real-time decision-making at factories, retail, and remote sites.

### Sovereign/Confidential AI
Canada-Germany Sovereign Technology Alliance, Chile Latam-GPT, OPAQUE Confidential AI emerging
to track, control, and verify "who used what data/model for what actions."
Long-term enterprise AI purchasing criteria likely expanding beyond "performance/price"
to include "explainable lineage, regulatory compliance, policy verifiability."
```

**Step 7: Source 및 Comments 섹션**

```markdown
## Source

[... 동일한 URL 리스트 ...]

## Comments
<!-- To be auto-generated by Claude API -->
```

**Step 8: 파일 저장**

Save: `_posts/en/2026-02-17-daily-digest.md`

---

## Task 3: Claude API 연동 스크립트 작성

**Files:**
- Create: `scripts/generate_comments.py`
- Create: `.env` (git ignore)
- Modify: `.gitignore`

**Step 1: .gitignore 업데이트**

Modify: `.gitignore`

```bash
# Add to .gitignore
.env
scripts/__pycache__/
```

**Step 2: Python 스크립트 작성**

Create: `scripts/generate_comments.py`

```python
#!/usr/bin/env python3
"""
Generate Comments section for Daily Digest using Claude API.

Usage:
    python scripts/generate_comments.py _posts/ko/2026-02-17-daily-digest.md
"""

import os
import sys
import re
from anthropic import Anthropic

def read_post(file_path):
    """Read the Daily Digest post."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_summary(content):
    """Extract '오늘의 핵심 요약' section."""
    match = re.search(r'## 오늘의 핵심 요약\n\n(.*?)\n\n##', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Try English version
    match = re.search(r'## Today\'s Key Summary\n\n(.*?)\n\n##', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

def generate_comments(summary, lang='ko'):
    """Generate Comments using Claude API."""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    if lang == 'ko':
        prompt = f"""다음은 오늘의 테크 뉴스 요약입니다:

{summary}

이 요약을 바탕으로 다음 3가지 관점에서 1-2문장씩 코멘트를 작성해주세요:

1. **산업 연관성**: 이 동향이 산업 전반에 어떤 영향을 미칠지
2. **직무 연관성**: 개발자/엔지니어 관점에서 어떤 역량이 중요해지는지
3. **자소서·면접**: 면접에서 어떤 질문이 나올 수 있고 어떻게 대비할지

형식:
- **산업 연관성**: [1-2문장]
- **직무 연관성**: [1-2문장]
- **자소서·면접**: [1-2문장]"""
    else:  # en
        prompt = f"""Here's today's tech news summary:

{summary}

Based on this summary, write 1-2 sentence comments for each of these 3 perspectives:

1. **Industry Relevance**: How this trend will impact the industry overall
2. **Role Relevance**: What capabilities become important from developer/engineer perspective
3. **Interview Prep**: What interview questions might come up and how to prepare

Format:
- **Industry Relevance**: [1-2 sentences]
- **Role Relevance**: [1-2 sentences]
- **Interview Prep**: [1-2 sentences]"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

def update_post(file_path, comments):
    """Update the post with generated comments."""
    content = read_post(file_path)

    # Replace Comments placeholder
    updated = re.sub(
        r'## Comments\n<!-- .* -->',
        f'## Comments\n{comments}',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated)

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/generate_comments.py <post_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Detect language
    lang = 'ko' if '/ko/' in file_path else 'en'

    print(f"Reading post: {file_path}")
    content = read_post(file_path)

    print("Extracting summary...")
    summary = extract_summary(content)
    if not summary:
        print("Error: Could not extract summary section")
        sys.exit(1)

    print(f"Generating comments ({lang})...")
    comments = generate_comments(summary, lang)

    print("Updating post...")
    update_post(file_path, comments)

    print(f"✓ Comments generated and updated in {file_path}")

if __name__ == "__main__":
    main()
```

**Step 3: requirements.txt 작성**

Create: `scripts/requirements.txt`

```
anthropic>=0.40.0
```

**Step 4: .env 템플릿 작성**

Create: `.env.example`

```bash
# Anthropic API Key
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_api_key_here
```

**Step 5: 테스트 준비**

실제 API 키는 사용자가 수동으로 `.env`에 추가:

```bash
# Create .env file (not in git)
cp .env.example .env
# Edit .env and add your actual API key
```

---

## Task 4: Comments 자동 생성 테스트

**Files:**
- Modify: `_posts/ko/2026-02-17-daily-digest.md`
- Modify: `_posts/en/2026-02-17-daily-digest.md`

**Step 1: Python 환경 설정**

```bash
cd scripts
pip install -r requirements.txt
```

Expected: Successfully installed anthropic

**Step 2: API 키 확인**

```bash
# Check .env file exists and has API key
cat ../.env | grep ANTHROPIC_API_KEY
```

Expected: ANTHROPIC_API_KEY=sk-ant-...

**Step 3: 한국어 포스트 Comments 생성**

```bash
cd ..  # tech-review root
python scripts/generate_comments.py _posts/ko/2026-02-17-daily-digest.md
```

Expected output:
```
Reading post: _posts/ko/2026-02-17-daily-digest.md
Extracting summary...
Generating comments (ko)...
Updating post...
✓ Comments generated and updated in _posts/ko/2026-02-17-daily-digest.md
```

**Step 4: 영문 포스트 Comments 생성**

```bash
python scripts/generate_comments.py _posts/en/2026-02-17-daily-digest.md
```

Expected: Similar success message

**Step 5: 결과 확인**

```bash
# Check Comments section was updated
tail -20 _posts/ko/2026-02-17-daily-digest.md
tail -20 _posts/en/2026-02-17-daily-digest.md
```

Expected: Comments section filled with generated content

**Step 6: 비용 확인**

Check Anthropic Console usage:
- Input tokens: ~2,000
- Output tokens: ~200
- Cost per post: ~$0.001
- Total for 2 posts: ~$0.002

---

## Task 5: Git Commit - 샘플 Daily Digest 완료

**Files:**
- `_posts/ko/2026-02-17-daily-digest.md`
- `_posts/en/2026-02-17-daily-digest.md`
- `scripts/generate_comments.py`
- `scripts/requirements.txt`
- `.env.example`
- `.gitignore`

**Step 1: Git status 확인**

```bash
git status
```

Expected: Shows new and modified files

**Step 2: Stage files**

```bash
git add _posts/ko/2026-02-17-daily-digest.md
git add _posts/en/2026-02-17-daily-digest.md
git add scripts/generate_comments.py
git add scripts/requirements.txt
git add .env.example
git add .gitignore
```

**Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
[tech-review] 샘플 Daily Digest 완료 (Phase 1)

- Daily Digest 포스트 작성 (KO/EN)
- 10-15개 핵심 뉴스, 3-섹션 구조
- Comments Claude API 자동 생성 스크립트
- 비용: ~$0.001 per post

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**Step 4: Push (optional)**

```bash
# If ready to deploy
git push origin master
```

Note: Jekyll will auto-rebuild on GitHub Pages

---

## Task 6: Perplexity 프롬프트 업데이트 (향후 작업)

**Files:**
- Update: Perplexity task settings

**Step 1: 현재 Perplexity 프롬프트 확인**

기존 프롬프트 (추정):
```
"이번 주의 가장 중요한 기술 개발 분석..."
```

**Step 2: 업데이트된 프롬프트**

```
이번 주(2026년 2월 둘째 주)의 가장 중요한 글로벌 기술 개발·전략 동향을 분석해주세요.

**선별 기준**:
- 실제 출시물 (모델, 제품, 플랫폼) 우선
- 주요 파트너십/투자 (금액, 전략적 의미)
- 판도 변화 (가격 혁신, 새로운 패러다임)

**출력 형식**:
1. 결론/요약 (핵심 축 3가지)
2. AI/ML 혁신 (5-10개 주제, 각 3-5문장)
3. 기업 전략 (3-5개 주제, 각 3-5문장)
4. 트렌드 (3-5개 주제, 각 3-5문장)
5. 소스 URL (각 주제별 출처)

**언어**:
- 첫 번째 응답: 한국어 (원어 작성, 번역 아님)
- 두 번째 응답: 영어 (원어 작성, 번역 아님)

**톤**:
- 업계 내부자 시선
- 보도자료 톤 금지
- 구체적 수치/이름 포함
```

**Step 3: Perplexity Task 설정**

1. Perplexity 스케줄 확인 (매일 8AM)
2. 프롬프트 업데이트
3. 언어 설정: KO + EN 각각 실행
4. 결과 확인 (이메일 또는 Perplexity Space)

---

## Next Steps (Phase 2 - 자동화)

**Not in this plan, but documented for reference:**

### 1. Google Apps Script (이메일 파싱)
- Gmail에서 Perplexity 이메일 읽기
- Markdown 추출
- GitHub repository_dispatch 트리거

### 2. GitHub Actions (자동 생성)
- repository_dispatch 이벤트 수신
- Perplexity 리서치 파싱
- Daily Digest 생성 (Claude API)
- Comments 생성 (Claude API)
- Git commit + push

### 3. E2E 테스트
- 전체 파이프라인 검증
- 오류 처리
- 모니터링

---

## Summary

**Phase 1 (This Plan):**
- ✓ 샘플 Daily Digest 작성 (KO/EN)
- ✓ Comments 자동 생성 스크립트
- ✓ Claude API 연동 테스트
- ✓ Git commit

**Phase 2 (Future):**
- ⏱ Google Apps Script (이메일 파싱)
- ⏱ GitHub Actions (자동 생성)
- ⏱ E2E 테스트

**Phase 3 (Future):**
- ⏱ 완전 자동화
- ⏱ 오류 감지 및 알림
- ⏱ 수동 개입 최소화
