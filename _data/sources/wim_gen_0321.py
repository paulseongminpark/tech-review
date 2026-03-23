import json, re

def clean_transcript(t):
    t = re.sub(r'<\d+:\d+:\d+\.\d+>', ' ', t)
    t = re.sub(r'</?c>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

base = 'C:/dev/01_projects/03_tech-review/blog/_data/sources'
path = f'{base}/youtube-2026-03-21.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

summaries = {}

summaries["How to Auto-Generate System Architecture Diagrams from Code (Miro MCP + Claude Code)"] = {
  "sections": [
    {
      "heading": "Miro MCP + Claude Code: 코드에서 아키텍처 다이어그램 자동 생성",
      "body": "Miro의 MCP 서버를 Claude와 연결하면 로컬 코드베이스를 직접 분석하여 Miro 보드에 시스템 아키텍처 다이어그램을 자동으로 생성할 수 있다. Claude Code에서 /mcp 명령어로 'code explain on board' 프롬프트를 실행하면, Miro 보드 URL과 코드 경로만 지정해도 다이어그램이 자동으로 만들어진다. 결과물로 시스템 아키텍처 다이어그램, 요청 흐름 시퀀스 다이어그램, 미들웨어 및 인증 플로우차트, MCP 도구 마인드맵 등 4가지 시각화가 생성된다.",
      "highlights": ["Miro의 MCP 서버를 Claude와 연결하면 로컬 코드베이스를 직접 분석하여 Miro 보드에 시스템 아키텍처 다이어그램을 자동으로 생성할 수 있다.", "Miro 보드 URL과 코드 경로만 지정해도 다이어그램이 자동으로 만들어진다."],
      "quote": "I just ran Miro's MCP server with Claude to generate a diagram explaining our internal MCP, and this is the result."
    },
    {
      "heading": "생성된 다이어그램 4종: 실제 출력물 검토",
      "body": "시스템 아키텍처 다이어그램은 AI 어시스턴트, 클라이언트, 서버, 데이터 스토어(Redis), 플랫폼 API 간의 연결 관계를 범례와 함께 시각화한다. 요청 흐름 시퀀스 다이어그램은 각 컴포넌트 간 메시지 흐름을 시간 순서로 표현하며, 미들웨어 및 인증 플로우차트는 요청 처리 경로를 보여준다. MCP 도구 마인드맵은 사용 가능한 도구들의 계층 구조를 한눈에 파악하게 해준다.",
      "highlights": ["시스템 아키텍처 다이어그램은 AI 어시스턴트, 클라이언트, 서버, 데이터 스토어(Redis), 플랫폼 API 간의 연결 관계를 범례와 함께 시각화한다.", "MCP 도구 마인드맵은 사용 가능한 도구들의 계층 구조를 한눈에 파악하게 해준다."],
      "quote": None
    },
    {
      "heading": "실용적 활용: 코드 문서화 자동화의 가능성",
      "body": "코드를 읽고 수동으로 다이어그램을 그리는 작업은 시간 소모가 크고 코드 변경 시 빠르게 구식이 된다. Miro MCP를 통한 자동 생성은 코드가 변경될 때마다 최신 상태의 아키텍처 문서를 유지하는 지속적 문서화 파이프라인의 기초가 된다. 신규 팀원 온보딩이나 코드 리뷰 시 시각적 컨텍스트를 즉시 제공할 수 있어 협업 효율이 크게 향상된다.",
      "highlights": ["Miro MCP를 통한 자동 생성은 코드가 변경될 때마다 최신 상태의 아키텍처 문서를 유지하는 지속적 문서화 파이프라인의 기초가 된다.", "신규 팀원 온보딩이나 코드 리뷰 시 시각적 컨텍스트를 즉시 제공할 수 있어 협업 효율이 크게 향상된다."],
      "quote": None
    },
    {
      "heading": "설정 방법: Claude Code + Miro MCP 연동",
      "body": "Claude Code에 Miro MCP 서버를 추가하는 것이 전제 조건이다. /mcp 명령어 실행 후 code explain on board 프롬프트를 선택하고, Miro 보드 URL과 분석할 코드 경로를 입력하면 Claude가 자동으로 코드를 분석하고 다이어그램을 생성한다. 빠른 처리를 위해 Claude가 작업하는 동안 대기하면 되며, 결과는 지정한 Miro 보드에 직접 나타난다.",
      "highlights": ["code explain on board 프롬프트를 선택하고, Miro 보드 URL과 분석할 코드 경로를 입력하면 Claude가 자동으로 코드를 분석하고 다이어그램을 생성한다.", "결과는 지정한 Miro 보드에 직접 나타난다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Miro MCP + Claude Code 조합으로 코드베이스에서 시스템 아키텍처 다이어그램 자동 생성 가능",
    "/mcp code explain on board 명령으로 4종 다이어그램(아키텍처, 시퀀스, 플로우차트, 마인드맵) 자동 생성",
    "코드 변경 시마다 최신 다이어그램 유지하는 지속적 문서화 파이프라인으로 활용 가능"
  ],
  "tech_stack": ["Miro", "Miro MCP", "Claude Code", "Redis"],
  "apply_points": [
    {"text": "mcp-memory 코드베이스를 Miro MCP로 자동 시각화하면 온톨로지 구조와 MCP 도구 관계를 시각적으로 파악할 수 있음", "key": True},
    {"text": "orchestration 파이프라인 구조를 Miro 보드에 자동 생성하여 문서화 자동화 파이프라인 구축 가능", "key": True},
    {"text": "index-system의 에코시스템 그래프 시각화 대안으로 Miro MCP 기반 자동 다이어그램 활용 검토", "key": False}
  ],
  "smart_brevity": {
    "why": "코드는 계속 바뀌는데 문서는 항상 뒤처진다. MCP가 이 시차를 없앤다 — 코드에서 다이어그램으로의 직접 연결이 문서 부채 문제의 구조적 해결책이다.",
    "what": "Miro MCP 서버와 Claude Code를 연동해 코드베이스에서 시스템 아키텍처 다이어그램을 자동 생성하는 방법 시연.",
    "axioms": [
      {"label": "Be smart", "content": "다이어그램을 손으로 그리는 것은 AI 시대에 시간 낭비다 — 코드가 다이어그램의 단일 진실 공급원이어야 한다."}
    ]
  }
}

summaries["How to make Claude Code less dumb"] = {
  "sections": [
    {
      "heading": "Claude Code가 멍청하게 느껴지는 진짜 이유",
      "body": "20년 경력의 테크 빌더이자 VC인 저자는 Claude Code가 처음에 기대에 미치지 못한다고 느끼는 사람들이 실제로 Claude Code 자체의 문제가 아니라 잘못된 사용 방식 때문에 좌절한다고 주장한다. Claude Code는 단순히 코드를 생성하는 도구가 아니라 컨텍스트 엔지니어링이 필요한 시스템이다. 충분한 컨텍스트, 명확한 지시, 올바른 CLAUDE.md 설정이 없으면 Claude Code는 반복적인 실수를 저지르고 비효율적으로 작동한다.",
      "highlights": ["Claude Code는 컨텍스트 엔지니어링이 필요한 시스템이다.", "충분한 컨텍스트, 명확한 지시, 올바른 CLAUDE.md 설정이 없으면 Claude Code는 반복적인 실수를 저지른다."],
      "quote": "Claude Code. Oh my goodness. I've been building in tech for 20 years, both as a founder and as a VC, but nothing has found me so much unlocked potential."
    },
    {
      "heading": "CLAUDE.md: Claude Code를 개인화하는 핵심 파일",
      "body": "CLAUDE.md는 Claude Code에게 프로젝트 맥락, 코딩 스타일, 금지 행동, 선호하는 패턴을 알려주는 설정 파일이다. 이 파일이 없거나 부실하면 Claude Code는 매번 처음부터 추론해야 하므로 일관성이 없고 비효율적이다. 프로젝트별 CLAUDE.md에 기술 스택, 아키텍처 결정, 금지된 접근법, 선호하는 라이브러리 등을 명시하면 Claude Code의 출력 품질이 극적으로 향상된다.",
      "highlights": ["이 파일이 없거나 부실하면 Claude Code는 매번 처음부터 추론해야 하므로 일관성이 없고 비효율적이다.", "프로젝트별 CLAUDE.md에 기술 스택, 아키텍처 결정, 금지된 접근법, 선호하는 라이브러리 등을 명시하면 Claude Code의 출력 품질이 극적으로 향상된다."],
      "quote": None
    },
    {
      "heading": "Sub-agent 패턴: 복잡한 작업을 분해하는 법",
      "body": "복잡한 작업을 하나의 대화에서 처리하려 하면 Claude Code가 혼란스러워지고 품질이 저하된다. 대신 작업을 작은 단위로 분해하고, 각 단계를 별도의 서브에이전트 또는 새 대화로 처리하는 방식이 훨씬 효과적이다. 이는 컨텍스트 윈도우 오염을 방지하고, 각 단계에서 Claude Code가 명확한 목표에 집중할 수 있게 한다.",
      "highlights": ["복잡한 작업을 하나의 대화에서 처리하려 하면 Claude Code가 혼란스러워지고 품질이 저하된다.", "작업을 작은 단위로 분해하고 각 단계를 별도의 서브에이전트 또는 새 대화로 처리하는 방식이 훨씬 효과적이다."],
      "quote": None
    },
    {
      "heading": "명령어 체인: Claude Code를 일관되게 유지하는 법",
      "body": "Claude Code 세션 시작 시 항상 같은 컨텍스트 주입 명령어를 실행하는 루틴을 만들면 일관성이 크게 향상된다. /init 명령어나 커스텀 슬래시 명령어를 통해 프로젝트 상태, 최근 변경사항, 현재 목표를 자동으로 Claude Code에 제공할 수 있다. 이 습관화된 컨텍스트 주입이 Claude Code를 멍청하게 느끼게 만드는 가장 큰 원인인 컨텍스트 손실 문제를 해결한다.",
      "highlights": ["Claude Code 세션 시작 시 항상 같은 컨텍스트 주입 명령어를 실행하는 루틴을 만들면 일관성이 크게 향상된다.", "이 습관화된 컨텍스트 주입이 컨텍스트 손실 문제를 해결한다."],
      "quote": None
    },
    {
      "heading": "Plan 모드와 Act 모드 분리",
      "body": "Claude Code를 곧바로 코드 작성에 투입하는 것보다 먼저 plan 모드에서 접근 방법을 검토하는 것이 더 나은 결과를 낳는다. 계획 단계에서 Claude Code가 제안하는 접근 방법에 동의하거나 수정하면 실제 구현 품질이 크게 향상된다. 특히 복잡하거나 위험한 작업에서 plan 모드는 오류와 되돌리기 어려운 변경을 방지하는 핵심 안전장치다.",
      "highlights": ["먼저 plan 모드에서 접근 방법을 검토하는 것이 더 나은 결과를 낳는다.", "특히 복잡하거나 위험한 작업에서 plan 모드는 오류와 되돌리기 어려운 변경을 방지하는 핵심 안전장치다."],
      "quote": None
    },
    {
      "heading": "반복 실수 방지: 교훈을 CLAUDE.md에 기록하는 루프",
      "body": "Claude Code가 실수를 반복하는 원인은 각 세션이 기억이 없이 시작되기 때문이다. 세션 중 발견한 나쁜 패턴이나 금지 사항을 즉시 CLAUDE.md에 추가하면 다음 세션부터 같은 실수가 반복되지 않는다. 이 피드백 루프를 통해 CLAUDE.md는 점점 더 정교해지고, Claude Code의 출력 품질은 사용할수록 향상된다.",
      "highlights": ["세션 중 발견한 나쁜 패턴이나 금지 사항을 즉시 CLAUDE.md에 추가하면 다음 세션부터 같은 실수가 반복되지 않는다.", "이 피드백 루프를 통해 CLAUDE.md는 점점 더 정교해지고, Claude Code의 출력 품질은 사용할수록 향상된다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Claude Code가 멍청하게 느껴지는 원인은 도구가 아니라 컨텍스트 엔지니어링 부재",
    "CLAUDE.md에 기술 스택, 금지 패턴, 선호 접근법을 명시하면 출력 품질이 극적으로 향상됨",
    "세션 중 발견한 나쁜 패턴을 즉시 CLAUDE.md에 추가하는 피드백 루프가 품질 개선의 핵심"
  ],
  "tech_stack": ["Claude Code"],
  "apply_points": [
    {"text": "orchestration의 CLAUDE.md 구조를 프로젝트별 금지 패턴과 선호 접근법으로 더 정교하게 구성하는 것 검토 — 현재 rules가 이 역할을 하고 있으나 세션별 학습 루프 강화 가능", "key": True},
    {"text": "각 프로젝트 루트에 프로젝트별 CLAUDE.md를 두고 기술 스택과 아키텍처 결정을 명시하는 패턴 강화", "key": True},
    {"text": "plan 모드 우선 실행을 workflow.md rules에 명시적으로 추가하여 위험한 작업 시 안전장치 강화", "key": False}
  ],
  "smart_brevity": {
    "why": "Claude Code의 품질은 도구의 한계가 아니라 컨텍스트 설계의 함수다. CLAUDE.md는 AI와 인간 간의 지식 외부화 인터페이스다.",
    "what": "CLAUDE.md 최적화, sub-agent 분해, plan 모드 활용으로 Claude Code 품질을 높이는 실전 가이드.",
    "axioms": [
      {"label": "Be smart", "content": "Claude Code가 반복적으로 실수한다면 그것은 신호다 — CLAUDE.md에 그 교훈을 즉시 기록해야 한다."}
    ]
  }
}

summaries["Build Self-Improving Claude Code Skills. The Results Are Crazy."] = {
  "sections": [
    {
      "heading": "Claude Code 스킬의 자기 개선 가능성",
      "body": "Claude Code의 스킬(slash command)은 AI가 실행하는 재사용 가능한 프롬프트 모듈이다. 스킬이 강력한 이유는 한 번 잘 만들어두면 반복 작업을 자동화할 수 있기 때문인데, 여기서 한 단계 더 나아가 스킬 자체가 실행 결과를 바탕으로 스스로를 개선하는 자기 개선 루프를 구축할 수 있다. 이 접근법은 AI 시스템이 사용할수록 더 나아지는 적응형 도구로 진화하는 핵심 메커니즘이다.",
      "highlights": ["스킬 자체가 실행 결과를 바탕으로 스스로를 개선하는 자기 개선 루프를 구축할 수 있다.", "이 접근법은 AI 시스템이 사용할수록 더 나아지는 적응형 도구로 진화하는 핵심 메커니즘이다."],
      "quote": "Skills are one of the most powerful things you can build inside Claude Code for your business."
    },
    {
      "heading": "자기 개선 스킬의 구조: 실행-평가-갱신 루프",
      "body": "자기 개선 스킬의 핵심 구조는 실행, 결과 평가, 스킬 파일 갱신의 3단계 루프다. 스킬 실행 후 Claude Code가 결과의 품질을 자체 평가하고, 개선이 필요한 부분을 스킬 파일에 직접 반영하도록 프롬프트를 설계한다. 이때 스킬 파일에는 이전 실행에서 배운 교훈, 효과적인 패턴, 피해야 할 접근법을 누적으로 기록한다.",
      "highlights": ["스킬 실행 후 Claude Code가 결과의 품질을 자체 평가하고, 개선이 필요한 부분을 스킬 파일에 직접 반영하도록 프롬프트를 설계한다.", "스킬 파일에는 이전 실행에서 배운 교훈, 효과적인 패턴, 피해야 할 접근법을 누적으로 기록한다."],
      "quote": None
    },
    {
      "heading": "비즈니스 유스케이스: 마케팅, 코드 리뷰, 문서화",
      "body": "마케팅 카피 생성 스킬은 여러 번 실행하면서 어떤 스타일이 더 나은 결과를 낳는지 학습하여 다음 실행 시 더 좋은 카피를 생성한다. 코드 리뷰 스킬은 반복적으로 놓치는 패턴을 추적하여 체크리스트를 자동으로 강화한다. 문서화 스킬은 사용자 피드백을 반영하여 출력 형식을 지속적으로 개선하는 방식으로 진화한다.",
      "highlights": ["마케팅 카피 생성 스킬은 여러 번 실행하면서 어떤 스타일이 더 나은 결과를 낳는지 학습하여 다음 실행 시 더 좋은 카피를 생성한다.", "코드 리뷰 스킬은 반복적으로 놓치는 패턴을 추적하여 체크리스트를 자동으로 강화한다."],
      "quote": None
    },
    {
      "heading": "구현 방법: 자기 평가 프롬프트 설계",
      "body": "자기 개선 루프를 만들기 위한 핵심은 스킬 마지막에 자기 평가 섹션을 추가하는 것이다. 이 섹션에서 Claude Code에게 방금 수행한 작업의 약점, 더 나은 접근 방법, 다음 실행을 위한 구체적 개선 사항을 분석하도록 지시한다. 그리고 이 분석 결과를 스킬 파일의 notes 또는 lessons learned 섹션에 자동으로 추가하도록 설계한다.",
      "highlights": ["스킬 마지막에 자기 평가 섹션을 추가하는 것이 자기 개선 루프의 핵심이다.", "이 분석 결과를 스킬 파일의 notes 또는 lessons learned 섹션에 자동으로 추가하도록 설계한다."],
      "quote": None
    },
    {
      "heading": "결과와 한계: 실험 데이터",
      "body": "실제 적용 결과 자기 개선 스킬은 반복 실행을 거칠수록 출력 품질이 눈에 띄게 향상되었다. 단, 이 접근법의 한계는 Claude Code가 자신의 출력을 평가하는 기준이 여전히 AI의 주관적 판단에 의존한다는 점이다. 가장 효과적인 운용 방식은 AI의 자기 평가와 사용자의 명시적 피드백을 병행하여 스킬을 개선하는 하이브리드 루프다.",
      "highlights": ["자기 개선 스킬은 반복 실행을 거칠수록 출력 품질이 눈에 띄게 향상되었다.", "가장 효과적인 운용 방식은 AI의 자기 평가와 사용자의 명시적 피드백을 병행하여 스킬을 개선하는 하이브리드 루프다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Claude Code 스킬에 자기 평가 섹션을 추가하면 실행할수록 자동으로 개선되는 적응형 도구가 됨",
    "실행-평가-갱신 3단계 루프가 자기 개선 스킬의 핵심 구조",
    "AI 자기 평가 + 사용자 명시적 피드백의 하이브리드 루프가 가장 효과적"
  ],
  "tech_stack": ["Claude Code"],
  "apply_points": [
    {"text": "orchestration의 스킬 파일들(commit-writer, code-reviewer 등)에 lessons learned 섹션을 추가하고 실행 후 자기 평가 결과를 누적하는 자기 개선 루프 도입 검토", "key": True},
    {"text": "mcp-memory의 auto_remember 메커니즘과 결합하여 스킬 실행 결과를 그래프에 자동 저장하는 학습 루프 설계 가능", "key": True},
    {"text": "tech-review 블로그의 WIM 생성 스킬에 품질 자기 평가 섹션을 추가하여 WIM 품질 지속 개선", "key": False}
  ],
  "smart_brevity": {
    "why": "도구가 사용할수록 나빠지는 게 아니라 나아진다는 것은 시스템 설계의 근본 목표다. Claude Code 스킬의 자기 개선은 그 목표를 현실로 만드는 첫 번째 실용적 구현이다.",
    "what": "Claude Code 스킬에 자기 평가 루프를 추가하여 실행할수록 자동으로 개선되는 스킬을 만드는 방법 시연.",
    "axioms": [
      {"label": "What's next", "content": "자기 개선 스킬의 다음 단계는 여러 스킬 간 교훈 공유 — 하나의 스킬에서 배운 것이 전체 스킬 생태계를 개선하는 메타 학습 루프다."}
    ]
  }
}

summaries["Claude Cowork Just Changed How You Do Marketing"] = {
  "sections": [
    {
      "heading": "Claude.ai Cowork: 마케팅 자동화의 새 패러다임",
      "body": "Claude.ai의 새 기능인 Cowork(코워크)는 마케팅 워크플로우 전반을 자동화하는 방식을 근본적으로 바꾸었다. 카피라이팅, 비주얼, 소셜 미디어 전략 등 마케팅의 거의 모든 부분을 Cowork 기반으로 자동화할 수 있게 되었다. Cowork는 Claude Chat, Claude Code와 함께 Claude 생태계의 세 번째 주요 인터페이스로, 특히 반복적이고 구조화된 작업에서 강점을 발휘한다.",
      "highlights": ["카피라이팅, 비주얼, 소셜 미디어 전략 등 마케팅의 거의 모든 부분을 Cowork 기반으로 자동화할 수 있게 되었다.", "Cowork는 Claude Chat, Claude Code와 함께 Claude 생태계의 세 번째 주요 인터페이스로, 특히 반복적이고 구조화된 작업에서 강점을 발휘한다."],
      "quote": "Claude Co has completely changed the way I do marketing."
    },
    {
      "heading": "Cowork 기반 마케팅 스킬 구축 방법",
      "body": "GitHub에서 Claude Cowork를 다운로드한 후, 원하는 마케팅 워크플로우를 스킬로 정의하여 Cowork에 연결한다. Visualization, PPT 생성, 데이터 분석 등의 스킬을 추가하면 단 하나의 명령어로 복잡한 마케팅 산출물을 자동으로 생성할 수 있다. 스킬 하나가 여러 명령을 조율하는 방식으로 동작하므로, 반복 작업이 많은 마케팅 업무에서 시간 절약 효과가 극적이다.",
      "highlights": ["Visualization, PPT 생성, 데이터 분석 등의 스킬을 추가하면 단 하나의 명령어로 복잡한 마케팅 산출물을 자동으로 생성할 수 있다.", "스킬 하나가 여러 명령을 조율하는 방식으로 동작하므로, 반복 작업이 많은 마케팅 업무에서 시간 절약 효과가 극적이다."],
      "quote": None
    },
    {
      "heading": "실전 데모: PPT 슬라이드 자동 생성",
      "body": "분석 자료, 데이터, 시장 조사 결과를 Cowork에 입력하고 PPT 스킬을 실행하면 Claude가 자동으로 구조화된 슬라이드 덱을 생성한다. 단순한 템플릿 채우기가 아니라 내용을 분석하고 논리적 흐름에 맞게 섹션을 구성하는 수준이다. 생성된 슬라이드는 즉시 프레젠테이션에 사용할 수 있는 수준이며, 필요 시 개별 슬라이드를 수정하는 방식으로 효율적으로 최종본을 만들 수 있다.",
      "highlights": ["단순한 템플릿 채우기가 아니라 내용을 분석하고 논리적 흐름에 맞게 섹션을 구성하는 수준이다.", "생성된 슬라이드는 즉시 프레젠테이션에 사용할 수 있는 수준이다."],
      "quote": None
    },
    {
      "heading": "마케터를 위한 진입 장벽 낮추기: Claude Code 없이도 가능",
      "body": "기존에는 Claude Code 숙련도가 있어야 고급 AI 자동화가 가능했지만, Cowork는 코딩 경험이 없는 마케터도 스킬을 활용할 수 있게 했다. Cowork 플랫폼을 통해 스킬을 추가하고 실행하는 과정이 직관적으로 설계되어 있다. 이 변화는 AI 자동화의 수혜 대상이 개발자에서 비기술 직군으로 확장되는 중요한 전환점이다.",
      "highlights": ["Cowork는 코딩 경험이 없는 마케터도 스킬을 활용할 수 있게 했다.", "이 변화는 AI 자동화의 수혜 대상이 개발자에서 비기술 직군으로 확장되는 중요한 전환점이다."],
      "quote": None
    },
    {
      "heading": "Claude 생태계 활용 전략: Chat vs Code vs Cowork",
      "body": "Claude Chat은 대화형 탐색과 일회성 작업에 적합하고, Claude Code는 복잡한 개발 프로젝트와 코드베이스 조작에 특화되어 있다. Cowork는 그 사이의 영역 — 반복적이고 구조화된 비개발 작업을 자동화하는 데 최적화되어 있다. 세 인터페이스를 작업 성격에 맞게 조합하여 사용하는 것이 Claude 생태계를 최대한 활용하는 전략이다.",
      "highlights": ["Claude Chat은 대화형 탐색과 일회성 작업, Claude Code는 복잡한 개발 프로젝트, Cowork는 반복적이고 구조화된 비개발 작업 자동화에 최적화되어 있다.", "세 인터페이스를 작업 성격에 맞게 조합하여 사용하는 것이 Claude 생태계를 최대한 활용하는 전략이다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Claude Cowork는 비개발 직군도 스킬 기반 AI 자동화를 사용할 수 있게 하는 Claude의 세 번째 인터페이스",
    "마케팅 카피, PPT 생성, 시각화 등 반복 구조화 작업에서 단일 명령으로 복잡한 산출물 자동 생성 가능",
    "Claude Chat(탐색), Claude Code(개발), Cowork(반복 자동화)의 역할 분리가 효율적 활용의 핵심"
  ],
  "tech_stack": ["Claude", "Claude Cowork", "Claude Code"],
  "apply_points": [
    {"text": "tech-review 블로그의 WIM 생성, 카테고리 분류, 태그 정리 등 반복 작업을 Cowork 스킬로 자동화하는 방안 검토", "key": False},
    {"text": "orchestration 스킬과 Cowork 스킬의 역할 경계 명확화 — 코드 관련 작업은 Claude Code, 문서/마케팅 자동화는 Cowork로 분리", "key": True},
    {"text": "portfolio 콘텐츠 업데이트나 essay 초안 작성 등 반복적 문서 생성 작업에 Cowork 스킬 패턴 적용 가능", "key": False}
  ],
  "smart_brevity": {
    "why": "AI 자동화가 개발자 전유물에서 벗어나는 순간이다. Cowork는 그 경계를 허문다 — 스킬을 만드는 사람과 사용하는 사람이 달라도 된다는 것.",
    "what": "Claude Cowork를 이용해 마케팅 카피, PPT 생성, 시각화 등의 반복 작업을 스킬 기반으로 자동화하는 방법 시연.",
    "axioms": [
      {"label": "The big picture", "content": "Claude 생태계는 Chat, Code, Cowork 세 레이어로 구조화되고 있다 — 어떤 레이어에서 작업하느냐가 생산성의 핵심 변수다."}
    ]
  }
}

summaries["800+ hours of Learning Claude Code in 8 minutes (2026 tutorial / unknown tricks / newest model)"] = {
  "sections": [
    {
      "heading": "800시간 실전 경험에서 나온 비직관적 교훈들",
      "body": "800시간 이상 Claude Code를 사용한 저자가 발견한 가장 중요한 교훈은 더 복잡하게 사용할수록 더 나쁜 결과를 낳는다는 것이다. 대부분의 사용자가 하는 실수는 Claude Code에게 너무 많은 것을 한꺼번에 요청하거나, 충분한 컨텍스트 없이 작업을 시작하거나, Claude Code의 실수를 수정하면서 컨텍스트를 오염시키는 것이다. 이 영상은 공식 문서나 입문 튜토리얼에서 찾기 어려운 실전 노하우를 압축적으로 전달한다.",
      "highlights": ["더 복잡하게 사용할수록 더 나쁜 결과를 낳는다는 것이 핵심 교훈이다.", "대부분의 사용자가 하는 실수는 Claude Code에게 너무 많은 것을 한꺼번에 요청하거나 충분한 컨텍스트 없이 작업을 시작하는 것이다."],
      "quote": "After spending over 800 hours in Claude Code, I've discovered ways to actually make this thing work for me, not against me."
    },
    {
      "heading": "새 프로젝트 vs 기존 프로젝트: 접근법이 달라야 한다",
      "body": "새 프로젝트를 시작할 때는 Claude Code에게 아키텍처 결정 권한을 더 많이 주고 탐색적으로 진행하는 것이 효과적이다. 반면 기존 프로젝트에서는 먼저 코드베이스 구조를 충분히 설명하고, 기존 패턴과 일관된 방식으로 작업을 요청해야 한다. 기존 코드베이스에서 Claude Code가 일관성을 유지하지 못하는 가장 큰 원인은 컨텍스트 부족이지, Claude Code 능력의 한계가 아니다.",
      "highlights": ["새 프로젝트에서는 Claude Code에게 아키텍처 결정 권한을 더 많이 주고 탐색적으로 진행하는 것이 효과적이다.", "기존 코드베이스에서 Claude Code가 일관성을 유지하지 못하는 가장 큰 원인은 컨텍스트 부족이다."],
      "quote": None
    },
    {
      "heading": "가장 효과적인 프롬프트 패턴 5가지",
      "body": "첫째, 결과물이 아닌 의도를 설명한다. 둘째, 금지 사항을 명시한다(하지 말아야 할 것). 셋째, 예시를 제공한다. 넷째, 단계적으로 검증 요청을 포함한다. 다섯째, 불확실한 부분은 질문하도록 명시적으로 허용한다. 이 5가지 패턴을 일관되게 적용하면 Claude Code의 결과물 품질이 크게 향상된다.",
      "highlights": ["결과물이 아닌 의도를 설명하는 것이 가장 중요한 프롬프트 원칙이다.", "금지 사항을 명시하는 것이 긍정적 지시만큼 중요하다."],
      "quote": None
    },
    {
      "heading": "컨텍스트 관리: 실패를 막는 핵심 습관",
      "body": "컨텍스트 윈도우가 가득 차면 Claude Code의 품질이 급격히 저하된다. 장기 작업에서는 중간에 새 대화를 시작하고 현재 상태와 다음 목표를 명시적으로 리셋하는 것이 필수다. 또한 오류 수정 시 같은 대화에서 계속 시도하는 것보다 새 대화에서 더 명확한 지시로 재시작하는 것이 훨씬 효과적인 경우가 많다.",
      "highlights": ["컨텍스트 윈도우가 가득 차면 Claude Code의 품질이 급격히 저하된다.", "오류 수정 시 같은 대화에서 계속 시도하는 것보다 새 대화에서 더 명확한 지시로 재시작하는 것이 훨씬 효과적인 경우가 많다."],
      "quote": None
    },
    {
      "heading": "최신 모델 활용: Claude 3.7 Sonnet의 달라진 점",
      "body": "Claude 3.7 Sonnet(2026)은 이전 모델 대비 코드 복잡도 처리 능력이 크게 향상되었다. 특히 긴 파일을 수정할 때 전체 파일을 재작성하는 경향이 줄어들고, 더 정밀한 부분 수정이 가능해졌다. 새 모델을 최대한 활용하려면 이전에 개발했던 CLAUDE.md 설정을 최신 모델 특성에 맞게 재검토하는 것이 필요하다.",
      "highlights": ["Claude 3.7 Sonnet은 이전 모델 대비 코드 복잡도 처리 능력이 크게 향상되었다.", "새 모델을 최대한 활용하려면 CLAUDE.md 설정을 최신 모델 특성에 맞게 재검토하는 것이 필요하다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "복잡하게 사용할수록 나쁜 결과 — 단순하고 명확한 지시 + 충분한 컨텍스트가 핵심",
    "의도 설명, 금지 명시, 예시 제공, 단계적 검증, 질문 허용의 5가지 프롬프트 패턴",
    "컨텍스트 윈도우 한계 도달 시 새 대화 재시작이 같은 대화에서 수정 반복보다 효과적"
  ],
  "tech_stack": ["Claude Code", "Claude 3.7 Sonnet"],
  "apply_points": [
    {"text": "orchestration의 pre-flight recall 규칙과 컨텍스트 cascade 전략은 이 영상의 컨텍스트 관리 원칙과 완전히 부합 — 현재 접근법이 올바름을 확인", "key": False},
    {"text": "프로젝트별 CLAUDE.md에 금지 사항 섹션을 더 명시적으로 구성하여 반복 실수 패턴 차단 강화", "key": True},
    {"text": "Claude 3.7 Sonnet 모델 특성 변화에 맞춰 각 프로젝트 CLAUDE.md 설정 재검토 필요", "key": True}
  ],
  "smart_brevity": {
    "why": "800시간이 증명하는 것은 Claude Code가 강력하다는 게 아니라, 컨텍스트 엔지니어링이 모든 것을 결정한다는 것이다.",
    "what": "800시간 이상의 Claude Code 실전 사용에서 추출한 비직관적 교훈, 프롬프트 패턴, 컨텍스트 관리 전략 압축 정리.",
    "axioms": [
      {"label": "The bottom line", "content": "Claude Code 품질 향상의 한계는 도구가 아니라 사용자의 컨텍스트 설계 능력에 있다."}
    ]
  }
}

summaries["Claude Code + Nano Banana 2 + Kling =  $15K Animated Sites"] = {
  "sections": [
    {
      "heading": "15분에 $15,000 수준의 애니메이션 웹사이트 제작",
      "body": "Nano Banana 2(이미지 생성), Kling(비디오 변환), Claude Code(코딩)를 조합하면 과거에는 5,000~10,000달러가 들었던 3D 스크롤 애니메이션 웹사이트를 15분, 2~3달러의 비용으로 제작할 수 있다. 헤드폰, 환경 보호 지구본, 인테리어 디자인, 우주 정거장 등 다양한 테마의 웹사이트 4개를 시연하며 이 도구 조합의 실용성을 증명한다. 핵심은 각 도구의 역할 분리 — Nano Banana 2로 시작 이미지 생성, Kling으로 영상 변환, Claude Code로 웹사이트 조립이다.",
      "highlights": ["과거에는 5,000~10,000달러가 들었던 3D 스크롤 애니메이션 웹사이트를 15분, 2~3달러의 비용으로 제작할 수 있다.", "핵심은 각 도구의 역할 분리 — Nano Banana 2로 시작 이미지 생성, Kling으로 영상 변환, Claude Code로 웹사이트 조립이다."],
      "quote": "A few years back, this would probably be $5 to $10,000 a pop. Now you can literally do it in less than 10 minutes for somewhere around $2 to $3 in tokens."
    },
    {
      "heading": "워크플로우 1단계: Nano Banana 2로 배경 이미지 생성",
      "body": "Nano Banana 2 Pro에서 웹사이트의 히어로 섹션용 배경 이미지를 생성한다. 이 이미지는 이후 비디오 변환의 시작 프레임이 되며, 모바일 반응형 레이아웃 설계 참고 자료로도 활용된다. 이미지 생성 시 웹사이트의 색상 팔레트, 분위기, 시각적 스타일을 명확히 프롬프트에 반영해야 이후 단계에서 일관된 비주얼이 만들어진다.",
      "highlights": ["이미지는 이후 비디오 변환의 시작 프레임이 되며, 모바일 반응형 레이아웃 설계 참고 자료로도 활용된다.", "이미지 생성 시 웹사이트의 색상 팔레트, 분위기, 시각적 스타일을 명확히 프롬프트에 반영해야 한다."],
      "quote": None
    },
    {
      "heading": "워크플로우 2단계: Kling으로 이미지를 비디오로 변환",
      "body": "Nano Banana 2에서 생성한 이미지를 Kling에 업로드하여 3D 움직임이 있는 배경 비디오로 변환한다. Kling은 정적 이미지에 카메라 무빙, 깊이감, 3D 효과를 자동으로 추가하여 웹사이트 배경으로 사용하기에 최적화된 루프 비디오를 생성한다. 이 단계에서 나온 비디오가 웹사이트의 wow factor를 결정하는 핵심 자산이다.",
      "highlights": ["Kling은 정적 이미지에 카메라 무빙, 깊이감, 3D 효과를 자동으로 추가하여 웹사이트 배경으로 사용하기에 최적화된 루프 비디오를 생성한다.", "이 단계에서 나온 비디오가 웹사이트의 wow factor를 결정하는 핵심 자산이다."],
      "quote": None
    },
    {
      "heading": "워크플로우 3단계: Claude Code로 웹사이트 조립",
      "body": "생성된 이미지와 비디오를 Claude Code에 제공하고 웹사이트 구축을 지시하면, Claude Code가 HTML/CSS/JavaScript로 완성된 애니메이션 웹사이트를 자동으로 생성한다. 프롬프트에 시각적 레퍼런스와 원하는 인터랙션 패턴을 구체적으로 명시할수록 결과물 품질이 높아진다. 생성된 코드는 Vercel 같은 플랫폼에 바로 배포 가능한 수준이다.",
      "highlights": ["생성된 이미지와 비디오를 Claude Code에 제공하고 웹사이트 구축을 지시하면, Claude Code가 HTML/CSS/JavaScript로 완성된 애니메이션 웹사이트를 자동으로 생성한다.", "생성된 코드는 Vercel 같은 플랫폼에 바로 배포 가능한 수준이다."],
      "quote": None
    },
    {
      "heading": "비즈니스 임팩트: 웹 에이전시 시장의 재편",
      "body": "이 3단계 워크플로우가 상용화되면 전통적인 웹 에이전시의 고가 서비스 모델이 근본적으로 위협받는다. 단순 랜딩 페이지 제작 서비스는 AI 도구로 대체될 수 있으며, 에이전시는 전략, 브랜딩, 더 복잡한 시스템 구축으로 포지셔닝을 전환해야 한다. 반면 이 도구를 마스터한 프리랜서는 기존 에이전시 대비 극적으로 낮은 비용으로 높은 품질의 작업물을 제공할 수 있다.",
      "highlights": ["전통적인 웹 에이전시의 고가 서비스 모델이 근본적으로 위협받는다.", "이 도구를 마스터한 프리랜서는 기존 에이전시 대비 극적으로 낮은 비용으로 높은 품질의 작업물을 제공할 수 있다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Nano Banana 2 + Kling + Claude Code 3단계 워크플로우로 $15K 수준의 애니메이션 웹사이트를 2~3달러, 15분에 제작 가능",
    "각 도구의 역할 분리가 핵심 — 이미지 생성(Nano Banana 2), 비디오 변환(Kling), 코딩(Claude Code)",
    "전통적 웹 에이전시 시장 재편 신호 — 단순 제작 서비스는 AI로 대체, 에이전시는 전략/브랜딩으로 포지셔닝 전환 필요"
  ],
  "tech_stack": ["Claude Code", "Nano Banana 2", "Kling", "HTML", "CSS", "JavaScript", "Vercel"],
  "apply_points": [
    {"text": "portfolio 웹사이트의 히어로 섹션에 Nano Banana 2 + Kling 기반 배경 비디오를 적용하여 시각적 차별화 가능", "key": True},
    {"text": "tech-review 블로그 리뷰 포스트에 이 워크플로우 튜토리얼을 정리하면 실용적 콘텐츠로 트래픽 유입 가능", "key": False},
    {"text": "AI 도구 조합의 역할 분리 패턴(이미지 생성, 변환, 코딩 도구 각각 전문화)은 orchestration의 Worker 역할 분리 철학과 일치", "key": False}
  ],
  "smart_brevity": {
    "why": "웹 에이전시의 가격 정당성이 무너지는 순간이다. 제작 비용이 2달러인 시대에 1만 달러를 받을 수 있는 것은 도구 사용 능력이 아니라 전략적 판단력뿐이다.",
    "what": "Nano Banana 2로 이미지 생성, Kling으로 비디오 변환, Claude Code로 웹사이트 조립하는 3단계 워크플로우 시연.",
    "axioms": [
      {"label": "By the numbers", "content": "제작비 2~3달러 vs 기존 에이전시 5,000~10,000달러 — 이 차이가 웹 디자인 산업 구조를 바꾸고 있다."}
    ]
  }
}

summaries["Use Claude Code DESIGNER Skill to 10x UI Designs"] = {
  "sections": [
    {
      "heading": "30일 UI 디자인 챌린지: Claude Code + DESIGNER 스킬",
      "body": "designcourse.com에서 진행 중인 30일 UI 디자인 챌린지에 Claude Code의 DESIGNER 스킬을 활용하는 실험이다. 200명 이상이 이미 참여한 이 챌린지는 동일한 가상 비즈니스 아이디어를 주고 각자가 어떤 수준의 UI를 만들 수 있는지 겨루는 방식이다. 목표는 프롬프트 능력이 AI 디자인 결과물 품질을 얼마나 크게 좌우하는지 집단적으로 검증하는 것이다.",
      "highlights": ["동일한 가상 비즈니스 아이디어를 주고 각자가 어떤 수준의 UI를 만들 수 있는지 겨루는 방식이다.", "목표는 프롬프트 능력이 AI 디자인 결과물 품질을 얼마나 크게 좌우하는지 집단적으로 검증하는 것이다."],
      "quote": "I'm going to give you along with hundreds of other designers a really cool experiment."
    },
    {
      "heading": "DESIGNER 스킬 설정: Claude Code에 디자인 역량 주입",
      "body": "Claude Code에 DESIGNER 스킬을 추가하면 일반 코딩 어시스턴트가 UI 디자인 전문가 수준으로 업그레이드된다. 이 스킬은 Claude Code가 디자인 원칙, 시각적 계층 구조, 타이포그래피, 색상 이론을 이해하고 적용하도록 시스템 프롬프트를 강화한다. Claude Code에 /디자이너 스킬 파일을 추가하고 헤더에 스킬을 활성화하면 즉시 사용 가능하다.",
      "highlights": ["이 스킬은 Claude Code가 디자인 원칙, 시각적 계층 구조, 타이포그래피, 색상 이론을 이해하고 적용하도록 시스템 프롬프트를 강화한다.", "Claude Code에 DESIGNER 스킬 파일을 추가하고 활성화하면 즉시 사용 가능하다."],
      "quote": None
    },
    {
      "heading": "히어로 섹션 제작 실전: 프롬프트 전략",
      "body": "단순히 히어로 섹션을 만들어달라고 요청하는 것과 디자인 의도, 타겟 사용자, 원하는 분위기, 시각적 레퍼런스를 함께 제공하는 것은 결과물 품질에 큰 차이를 만든다. DESIGNER 스킬이 활성화된 Claude Code는 폰트 선택, 여백 설계, 컬러 팔레트, 시각적 계층 구조에서 더 섬세한 결정을 내린다. 챌린지 참여자들의 결과물을 통해 같은 비즈니스 아이디어도 프롬프트 방식에 따라 완전히 다른 UI가 나온다는 것이 검증된다.",
      "highlights": ["디자인 의도, 타겟 사용자, 원하는 분위기, 시각적 레퍼런스를 함께 제공하는 것은 결과물 품질에 큰 차이를 만든다.", "DESIGNER 스킬이 활성화된 Claude Code는 폰트 선택, 여백 설계, 컬러 팔레트, 시각적 계층 구조에서 더 섬세한 결정을 내린다."],
      "quote": None
    },
    {
      "heading": "디자이너 스킬의 작동 원리: 스킬 파일 구조 분석",
      "body": "DESIGNER 스킬 파일은 Claude Code가 UI를 생성할 때 따라야 하는 디자인 원칙, 검토 체크리스트, 피해야 할 반패턴을 정의한다. 스킬 파일에 특정 디자인 스타일 가이드나 브랜드 토큰을 추가하면 일관된 브랜드 아이덴티티를 유지하는 UI 생성이 가능해진다. 이 구조는 팀 전체가 동일한 디자인 기준으로 AI를 활용할 수 있게 하는 표준화 메커니즘이기도 하다.",
      "highlights": ["스킬 파일에 특정 디자인 스타일 가이드나 브랜드 토큰을 추가하면 일관된 브랜드 아이덴티티를 유지하는 UI 생성이 가능해진다.", "이 구조는 팀 전체가 동일한 디자인 기준으로 AI를 활용할 수 있게 하는 표준화 메커니즘이기도 하다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Claude Code에 DESIGNER 스킬을 추가하면 디자인 원칙을 이해하는 AI 디자이너로 업그레이드 가능",
    "프롬프트에 디자인 의도, 타겟 사용자, 분위기, 레퍼런스를 포함하는 것이 결과물 품질의 핵심 변수",
    "스킬 파일에 브랜드 스타일 가이드를 추가하면 팀 전체의 AI 디자인 출력물이 일관된 기준을 유지"
  ],
  "tech_stack": ["Claude Code"],
  "apply_points": [
    {"text": "portfolio 웹사이트 UI 개선 시 DESIGNER 스킬 파일에 portfolio 브랜드 토큰과 디자인 원칙을 추가하여 일관된 UI 생성 파이프라인 구축", "key": True},
    {"text": "orchestration 스킬 파일 구조에 도메인별 전문 지식을 주입하는 패턴(DESIGNER 스킬처럼)을 code-reviewer나 commit-writer에 적용 검토", "key": True},
    {"text": "tech-review 블로그 포스트 헤더 이미지나 썸네일 생성에 DESIGNER 스킬 패턴 활용 가능", "key": False}
  ],
  "smart_brevity": {
    "why": "스킬은 단순한 프롬프트 템플릿이 아니다 — 특정 도메인 전문성을 AI에 주입하는 인터페이스다. DESIGNER 스킬은 그 가능성의 시연이다.",
    "what": "Claude Code에 DESIGNER 스킬을 추가하여 UI 디자인 품질을 10배 향상시키는 방법 및 챌린지 실험 결과 소개.",
    "axioms": [
      {"label": "Be smart", "content": "같은 Claude Code라도 어떤 스킬을 주입하느냐에 따라 전혀 다른 전문가가 된다 — 스킬 파일은 AI 역량의 확장 모듈이다."}
    ]
  }
}

summaries["Claude Code + Nano Banana = Beautiful Animated Websites"] = {
  "sections": [
    {
      "heading": "AI 슬롯 몬스터 탈출: 애니메이션으로 차별화",
      "body": "AI로 만든 웹사이트의 가장 큰 문제는 어디서나 볼 수 있는 제너릭한 디자인, 즉 AI 슬롯 몬스터 현상이다. 이를 극복하는 가장 강력하고 간단한 방법이 애니메이션 추가인데, 99%의 AI 생성 웹사이트에 없는 요소이므로 즉각적인 차별화가 가능하다. Nano Banana Pro + Kling + Claude Code 조합으로 이 차별화를 구현하면 높은 레버리지(단순하지만 임팩트 큰) 솔루션이 된다.",
      "highlights": ["AI로 만든 웹사이트의 가장 큰 문제는 어디서나 볼 수 있는 제너릭한 디자인, 즉 AI 슬롯 몬스터 현상이다.", "애니메이션 추가는 99%의 AI 생성 웹사이트에 없는 요소이므로 즉각적인 차별화가 가능하다."],
      "quote": "Your number one goal when creating websites with AI has to be to defeat the AI slot monster."
    },
    {
      "heading": "워크플로우: 시작 이미지 생성 (Nano Banana Pro)",
      "body": "Nano Banana Pro에서 웹사이트의 비주얼 방향을 결정하는 시작 이미지를 생성한다. 이 이미지는 이후 비디오로 변환될 첫 번째 프레임이 되므로, 움직임이 자연스럽게 보일 수 있는 배경이나 환경을 포함하는 구도가 좋다. 시작 이미지의 색상과 분위기가 최종 웹사이트의 시각적 정체성을 결정하므로 충분한 시간을 투자하는 것이 중요하다.",
      "highlights": ["이미지는 이후 비디오로 변환될 첫 번째 프레임이 되므로, 움직임이 자연스럽게 보일 수 있는 배경이나 환경을 포함하는 구도가 좋다.", "시작 이미지의 색상과 분위기가 최종 웹사이트의 시각적 정체성을 결정한다."],
      "quote": None
    },
    {
      "heading": "워크플로우: Kling으로 비디오 변환",
      "body": "Nano Banana Pro에서 생성한 이미지를 Kling에 업로드하여 루프 가능한 배경 비디오로 변환한다. Kling은 이미지의 시각적 요소에 카메라 패닝, 패럴랙스 효과, 환경 움직임을 추가하여 생동감 있는 배경을 만들어낸다. 비디오 길이와 루프 설정을 웹사이트 배경에 적합하게 조정하는 것이 마지막 단계다.",
      "highlights": ["Kling은 이미지의 시각적 요소에 카메라 패닝, 패럴랙스 효과, 환경 움직임을 추가하여 생동감 있는 배경을 만들어낸다.", "비디오 길이와 루프 설정을 웹사이트 배경에 적합하게 조정하는 것이 중요하다."],
      "quote": None
    },
    {
      "heading": "워크플로우: Claude Code로 웹사이트 완성",
      "body": "생성된 이미지와 비디오를 Claude Code에 제공하고 웹사이트 구조, 색상 팔레트, 모바일 반응형 요구사항을 프롬프트에 명시한다. Claude Code는 비디오 배경 위에 오버레이되는 텍스트, 버튼, 섹션을 생성하며, 비디오와 텍스트 간의 가독성을 위한 오버레이 처리도 자동으로 처리한다. 완성된 코드는 어떤 호스팅 플랫폼에도 즉시 배포 가능하다.",
      "highlights": ["Claude Code는 비디오 배경 위에 오버레이되는 텍스트, 버튼, 섹션을 생성하며, 비디오와 텍스트 간의 가독성을 위한 오버레이 처리도 자동으로 처리한다.", "완성된 코드는 어떤 호스팅 플랫폼에도 즉시 배포 가능하다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Nano Banana Pro + Kling + Claude Code 3단계로 제너릭한 AI 웹사이트 탈출 — 애니메이션이 핵심 차별화 요소",
    "Kling의 이미지→비디오 변환이 정적 웹사이트에 생동감을 부여하는 가장 쉽고 효과적인 방법",
    "같은 도구를 써도 시작 이미지 품질이 최종 웹사이트의 시각적 수준을 결정"
  ],
  "tech_stack": ["Claude Code", "Nano Banana Pro", "Kling", "HTML", "CSS", "JavaScript"],
  "apply_points": [
    {"text": "portfolio 사이트 히어로 섹션의 시각적 임팩트를 Nano Banana 2 + Kling으로 즉시 업그레이드 가능", "key": True},
    {"text": "AI 생성 웹사이트의 제너릭함을 탈출하는 애니메이션 전략은 tech-review 블로그의 포스트 헤더나 featured 섹션에도 응용 가능", "key": False},
    {"text": "이 워크플로우의 이미지→비디오→코드 변환 파이프라인은 AI 도구 간 역할 분리와 순차 처리의 좋은 예시로 orchestration 설계에 참고", "key": False}
  ],
  "smart_brevity": {
    "why": "제너릭한 AI 출력물의 홍수 속에서 차별화는 더 좋은 AI가 아니라 더 좋은 파이프라인에서 나온다. 애니메이션은 그 파이프라인의 마지막 한 단계다.",
    "what": "Nano Banana Pro로 이미지 생성, Kling으로 비디오 변환, Claude Code로 웹사이트 구축하는 3단계 애니메이션 웹사이트 제작 워크플로우.",
    "axioms": [
      {"label": "Be smart", "content": "애니메이션 하나가 99%의 AI 생성 웹사이트와 구분되는 차이를 만든다 — 단순하지만 높은 레버리지 전략이다."}
    ]
  }
}

summaries["Google Stitch + Claude Code = Insane App Design"] = {
  "sections": [
    {
      "heading": "Google Stitch: AI 디자인 세계의 패러다임 전환",
      "body": "Google Stitch의 최신 버전은 단순한 새 디자인 도구가 아니라 코드 내에서 디자인 스타일을 관리하는 새로운 패러다임을 제시한다. Stitch는 design.md라는 마크다운 파일에 디자인 시스템 전체를 코드로 정의하고, 이를 Claude Code와 연동하여 앱 UI를 일관되게 업데이트하는 워크플로우를 가능하게 한다. 15년간 앱 디자인을 해온 저자는 이 변화가 디자이너가 AI와 협업하는 방식을 근본적으로 바꾼다고 평가한다.",
      "highlights": ["Stitch는 design.md라는 마크다운 파일에 디자인 시스템 전체를 코드로 정의하고, 이를 Claude Code와 연동하여 앱 UI를 일관되게 업데이트하는 워크플로우를 가능하게 한다.", "이 변화가 디자이너가 AI와 협업하는 방식을 근본적으로 바꾼다."],
      "quote": "Google just dropped one of the biggest changes in the AI design world with this latest release."
    },
    {
      "heading": "Google Stitch에서 디자인 시스템 생성: design.md",
      "body": "Stitch에서 원하는 디자인 스타일을 입력하고 디자인 시스템을 생성하면, 색상 팔레트, 타이포그래피, 컴포넌트 스펙이 자동으로 design.md 파일로 내보내진다. 이 파일은 단순한 문서가 아니라 Claude Code가 해석하고 실행할 수 있는 구조화된 디자인 명세서다. 기존 앱의 디자인 언어를 Stitch에 업로드하면 역방향으로 design.md를 추출할 수도 있다.",
      "highlights": ["Stitch에서 디자인 시스템을 생성하면 색상 팔레트, 타이포그래피, 컴포넌트 스펙이 자동으로 design.md 파일로 내보내진다.", "이 파일은 단순한 문서가 아니라 Claude Code가 해석하고 실행할 수 있는 구조화된 디자인 명세서다."],
      "quote": None
    },
    {
      "heading": "design.md + Claude Code: 앱 UI 자동 업데이트 워크플로우",
      "body": "Stitch에서 내보낸 design.md를 프로젝트에 추가하고, Claude Code에게 이 파일을 참조하여 UI를 업데이트하도록 지시하면 전체 앱의 디자인이 일관되게 변경된다. 단순히 스타일을 바꾸는 것이 아니라, design.md가 변경되면 Claude Code가 앱 전체에서 해당 스타일이 적용된 모든 컴포넌트를 찾아 일관되게 업데이트한다. 이는 디자인 변경사항이 즉시 코드에 반영되는 진정한 디자인-코드 동기화를 실현한다.",
      "highlights": ["design.md가 변경되면 Claude Code가 앱 전체에서 해당 스타일이 적용된 모든 컴포넌트를 찾아 일관되게 업데이트한다.", "이는 디자인 변경사항이 즉시 코드에 반영되는 진정한 디자인-코드 동기화를 실현한다."],
      "quote": None
    },
    {
      "heading": "실전 데모: 기존 앱의 디자인 완전 리뉴얼",
      "body": "기존 AI 슬롯 외형의 앱을 Stitch로 새 디자인 시스템을 생성하고, design.md로 내보내 Claude Code와 연동하면 앱 전체가 새 디자인으로 업데이트되는 과정을 시연한다. 색상, 폰트, 버튼 스타일, 카드 레이아웃 등 모든 시각적 요소가 design.md에 정의된 스타일로 일관되게 교체된다. 이 프로세스는 디자이너가 Figma에서 직접 코딩하는 것에 가까운 수준의 제어력을 Claude Code를 통해 간접적으로 실현한다.",
      "highlights": ["색상, 폰트, 버튼 스타일, 카드 레이아웃 등 모든 시각적 요소가 design.md에 정의된 스타일로 일관되게 교체된다.", "이 프로세스는 디자이너가 Figma에서 직접 코딩하는 것에 가까운 수준의 제어력을 Claude Code를 통해 간접적으로 실현한다."],
      "quote": None
    },
    {
      "heading": "AI 슬롯 탈출 전략: Stitch의 차별화 포인트",
      "body": "Google Stitch가 다른 AI 디자인 도구와 다른 점은 시각적 프리셋이 아니라 구조화된 디자인 시스템을 코드 형태로 정의한다는 것이다. 이 접근법은 AI가 만드는 모든 UI가 동일한 디자인 기준을 따르도록 강제하여, 반복 사용할수록 브랜드 일관성이 강화된다. 디자인 의도가 코드 레벨에서 명시적으로 관리되므로 AI가 임의로 디자인 결정을 내리는 것을 구조적으로 방지한다.",
      "highlights": ["Google Stitch는 시각적 프리셋이 아니라 구조화된 디자인 시스템을 코드 형태로 정의한다.", "디자인 의도가 코드 레벨에서 명시적으로 관리되므로 AI가 임의로 디자인 결정을 내리는 것을 구조적으로 방지한다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Google Stitch의 design.md는 Figma MCP와 유사하지만 더 단순한 방식으로 디자인-코드 동기화를 실현",
    "design.md + Claude Code 연동으로 앱 전체의 디자인을 일관되게 일괄 업데이트 가능",
    "디자인 의도를 코드 레벨에서 명시적으로 관리하는 것이 AI 슬롯 현상을 구조적으로 방지하는 핵심"
  ],
  "tech_stack": ["Google Stitch", "Claude Code", "design.md"],
  "apply_points": [
    {"text": "portfolio 프로젝트에 Google Stitch로 design.md를 생성하고 Claude Code와 연동하면 디자인 일관성을 구조적으로 유지 가능 — Figma MCP 대안으로 더 간단한 진입점", "key": True},
    {"text": "tech-review 블로그의 CSS 스타일 관리를 design.md 방식으로 리팩토링하여 AI 기반 테마 변경 파이프라인 구축 검토", "key": False},
    {"text": "orchestration의 CLAUDE.md 구조가 코드 컨텍스트를 관리하듯, design.md는 디자인 컨텍스트를 관리한다 — 이 두 파일의 조합이 프로젝트 전체 일관성의 기반이 됨", "key": True}
  ],
  "smart_brevity": {
    "why": "디자인 시스템을 마크다운 파일로 외부화하는 발상이 핵심이다 — AI가 디자인을 해석하는 언어를 코드로 만든 것. 이것은 단순 도구가 아니라 인간-AI 협업의 새로운 인터페이스다.",
    "what": "Google Stitch로 design.md를 생성하고 Claude Code와 연동하여 앱 UI 디자인을 일관되게 자동 업데이트하는 워크플로우 시연.",
    "axioms": [
      {"label": "What's next", "content": "design.md가 코드베이스의 표준 파일이 되면, AI는 항상 디자이너의 의도를 먼저 읽고 UI를 결정하게 된다 — 프롬프트 중심에서 의도 중심으로."}
    ]
  }
}

summaries["Nano Banana 2: The JSON Control Hack"] = {
  "sections": [
    {
      "heading": "AI 이미지 편집의 핵심 문제: 부분 수정 시 전체 변형",
      "body": "AI 이미지 생성 도구의 가장 큰 좌절은 거의 완벽한 이미지에서 작은 디테일 하나를 바꾸려 할 때 발생한다. 프롬프트를 조금만 수정해도 AI가 가구 배치를 바꾸거나 원근감을 망치거나 이미지 전체를 재구성해버린다. Nano Banana 2 모델과 JSON 코드 형식을 결합하면 이 문제를 구조적으로 해결할 수 있다.",
      "highlights": ["프롬프트를 조금만 수정해도 AI가 가구 배치를 바꾸거나 원근감을 망치거나 이미지 전체를 재구성해버린다.", "Nano Banana 2 모델과 JSON 코드 형식을 결합하면 이 문제를 구조적으로 해결할 수 있다."],
      "quote": "You generate an almost perfect AI image and you just want to change one tiny detail. But the moment you adjust the prompt, the AI ruins the entire image."
    },
    {
      "heading": "핵심 기법: Gemini 앱에서 JSON 포맷으로 이미지 편집 지시",
      "body": "Gemini 앱(gemini.google.com)에서 Gemini 3.1 Pro 모델로 전환하고, 이미지 편집 지시를 JSON 형식으로 구조화하여 입력하면 AI의 환각(hallucination)을 효과적으로 억제할 수 있다. JSON 포맷은 변경할 요소, 유지할 요소, 변경 강도를 명시적으로 분리하여 AI가 범위를 벗어난 수정을 하지 않도록 구조적으로 제약한다. Gemini 3.1 Fast보다 Pro가 JSON 기반 편집에서 훨씬 우수한 결과를 보여주었다.",
      "highlights": ["JSON 포맷은 변경할 요소, 유지할 요소, 변경 강도를 명시적으로 분리하여 AI가 범위를 벗어난 수정을 하지 않도록 구조적으로 제약한다.", "Gemini 3.1 Fast보다 Pro가 JSON 기반 편집에서 훨씬 우수한 결과를 보여주었다."],
      "quote": "The secret to stopping hallucinations is the JSON format."
    },
    {
      "heading": "단계별 실전: 색상 변경에서 복잡한 원근 변환까지",
      "body": "간단한 색상 변경부터 시작하여 복잡한 원근감 조정, 오브젝트 교체까지 JSON 포맷의 제어력이 어떻게 작동하는지 단계적으로 시연한다. 색상 변경 JSON은 target_object, change_color, preserve_elements를 명시하고, 오브젝트 교체는 replace_object, maintain_perspective, keep_unchanged_elements를 정의한다. 가장 어려운 유스케이스인 원근감을 유지하면서 오브젝트만 교체하는 작업에서 JSON 포맷이 가장 큰 차이를 만든다.",
      "highlights": ["가장 어려운 유스케이스인 원근감을 유지하면서 오브젝트만 교체하는 작업에서 JSON 포맷이 가장 큰 차이를 만든다.", "replace_object, maintain_perspective, keep_unchanged_elements를 JSON으로 정의한다."],
      "quote": None
    },
    {
      "heading": "Nano Banana 2와 JSON의 시너지: 왜 이 조합인가",
      "body": "Nano Banana 2는 인페인팅과 부분 수정에 최적화된 모델로, JSON 형식의 구조화된 지시를 다른 모델보다 정확하게 해석한다. 일반 텍스트 프롬프트는 AI가 해석의 자유를 가지지만, JSON은 계층적 구조와 명시적 제약으로 그 자유를 제한한다. 이 두 요소의 결합이 기존에는 불가능했던 수준의 정밀 편집을 가능하게 한다.",
      "highlights": ["Nano Banana 2는 인페인팅과 부분 수정에 최적화된 모델로, JSON 형식의 구조화된 지시를 다른 모델보다 정확하게 해석한다.", "일반 텍스트 프롬프트는 AI가 해석의 자유를 가지지만, JSON은 계층적 구조와 명시적 제약으로 그 자유를 제한한다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Gemini 앱에서 Nano Banana 2 + JSON 포맷 조합이 AI 이미지 부분 수정 시 환각을 효과적으로 억제",
    "JSON 포맷의 핵심: 변경할 요소, 유지할 요소, 변경 강도를 명시적으로 분리하여 AI 자유 해석 범위 제약",
    "색상 변경, 오브젝트 교체, 원근감 유지 수정 등 복잡도에 따라 JSON 구조를 단계적으로 세밀하게 설계"
  ],
  "tech_stack": ["Nano Banana 2", "Gemini", "Gemini 3.1 Pro"],
  "apply_points": [
    {"text": "portfolio나 tech-review 블로그의 이미지 에셋 제작 시 Nano Banana 2 + JSON 패턴으로 브랜드 일관성을 유지한 부분 수정 가능", "key": False},
    {"text": "JSON 포맷으로 AI 행동을 구조적으로 제약하는 원리는 Claude 프롬프트 설계에도 동일하게 적용 가능 — 명시적 허용/금지 분리", "key": True},
    {"text": "mcp-memory 온톨로지에서 엔티티 속성을 JSON으로 정의할 때 이 제약 철학(변경할 것/유지할 것 명시)을 스키마 설계에 반영 가능", "key": False}
  ],
  "smart_brevity": {
    "why": "AI 제어의 핵심은 자유를 주는 것이 아니라 범위를 명시하는 것이다. JSON 포맷은 그 명시성의 가장 실용적인 구현이다.",
    "what": "Nano Banana 2 + Gemini 앱에서 JSON 포맷으로 AI 이미지를 정밀하게 부분 수정하는 방법 시연.",
    "axioms": [
      {"label": "Be smart", "content": "구조화된 입력이 자유로운 입력보다 나은 출력을 낳는다 — JSON이 자연어보다 AI 이미지 편집에서 더 정밀한 이유다."}
    ]
  }
}

summaries["NotebookLM is becoming the Most Essential AI Tool (7 Use Cases to Try!)"] = {
  "sections": [
    {
      "heading": "NotebookLM이 필수 AI 도구가 된 이유",
      "body": "Google NotebookLM은 출처 기반 응답(grounded answers)으로 환각을 최소화하고, 50개 이상의 소스를 통합하여 핵심을 추출하는 능력이 특징이다. 최근 업데이트로 소스를 슬라이드 덱, 인포그래픽, 비디오, 데이터 테이블 등 다양한 형태의 콘텐츠로 자동 변환하는 기능이 추가되어 단순한 리서치 도구를 넘어 콘텐츠 생산 시스템으로 진화했다. 여러 포맷의 소스를 수분 내에 통합하고 연결고리를 찾아주는 능력이 높은 정보 밀도의 업무에서 가장 큰 가치를 발휘한다.",
      "highlights": ["NotebookLM은 출처 기반 응답으로 환각을 최소화하고, 50개 이상의 소스를 통합하여 핵심을 추출하는 능력이 특징이다.", "단순한 리서치 도구를 넘어 콘텐츠 생산 시스템으로 진화했다."],
      "quote": "NotebookLM has always been my favorite tool and it's becoming one of the most essential AI tools for so many people."
    },
    {
      "heading": "유스케이스 1: 전략 프레젠테이션 자동 준비",
      "body": "30개 이상의 산업 보고서를 읽을 시간이 없을 때 NotebookLM에 소스를 업로드하고, 목적에 맞는 전략 질문을 입력하면 수분 내에 프레젠테이션 자료가 준비된다. NotebookLM의 리서치 기능은 Forrester, Gartner 같은 권위 있는 출처를 우선시하도록 프롬프트를 통해 제어할 수 있다. 생성된 딥 리서치 보고서의 모든 소스 링크를 원클릭으로 노트북에 추가하면 즉시 후속 작업이 가능하다.",
      "highlights": ["NotebookLM의 리서치 기능은 Forrester, Gartner 같은 권위 있는 출처를 우선시하도록 프롬프트를 통해 제어할 수 있다.", "생성된 딥 리서치 보고서의 모든 소스 링크를 원클릭으로 노트북에 추가하면 즉시 후속 작업이 가능하다."],
      "quote": None
    },
    {
      "heading": "유스케이스 2-3: 팟캐스트와 인터랙티브 학습",
      "body": "업로드한 소스들을 바탕으로 대화형 팟캐스트를 자동 생성하는 Audio Overview 기능은 이동 중에도 복잡한 소스를 소화할 수 있게 한다. 팟캐스트 진행 중 실시간으로 궁금한 점을 인터럽트하여 질문하면 대화를 멈추고 답변을 제공하는 인터랙티브 모드도 지원한다. 이 기능은 긴 기술 문서나 연구 보고서를 효율적으로 처리하는 데 특히 유용하다.",
      "highlights": ["업로드한 소스들을 바탕으로 대화형 팟캐스트를 자동 생성하는 Audio Overview 기능은 이동 중에도 복잡한 소스를 소화할 수 있게 한다.", "팟캐스트 진행 중 실시간으로 질문하면 대화를 멈추고 답변을 제공하는 인터랙티브 모드도 지원한다."],
      "quote": None
    },
    {
      "heading": "유스케이스 4-5: 콘텐츠 변환과 소셜 미디어 최적화",
      "body": "긴 리서치 보고서나 문서를 인포그래픽, 뉴스레터, 소셜 미디어 포스트, 브리핑 문서 등 다양한 포맷으로 자동 변환하는 기능이 추가되었다. Studio 패널의 원클릭 변환으로 동일한 소스에서 복수의 콘텐츠 형태를 병렬로 생성할 수 있어 콘텐츠 마케팅 워크플로우가 크게 단순화된다. 변환된 콘텐츠는 NotebookLM의 소스 기반 특성 덕분에 환각 없이 원본 데이터에 기반한 정확한 정보를 포함한다.",
      "highlights": ["Studio 패널의 원클릭 변환으로 동일한 소스에서 복수의 콘텐츠 형태를 병렬로 생성할 수 있어 콘텐츠 마케팅 워크플로우가 크게 단순화된다.", "변환된 콘텐츠는 소스 기반 특성 덕분에 환각 없이 원본 데이터에 기반한 정확한 정보를 포함한다."],
      "quote": None
    },
    {
      "heading": "유스케이스 6-7: 교육 자료 생성과 팀 지식 공유",
      "body": "학습 자료를 NotebookLM에 업로드하고 플래시카드, 퀴즈, 학습 가이드를 자동 생성하면 교육 콘텐츠 제작 시간을 크게 단축할 수 있다. 팀 노트북을 공유하면 모든 팀원이 같은 소스를 기반으로 질문하고 답변을 얻을 수 있어 지식 분산 문제를 해결한다. 특히 기업 내부 문서, 프로젝트 히스토리, 정책 문서를 노트북에 통합하면 신규 팀원 온보딩 시간을 극적으로 단축할 수 있다.",
      "highlights": ["팀 노트북을 공유하면 모든 팀원이 같은 소스를 기반으로 질문하고 답변을 얻을 수 있어 지식 분산 문제를 해결한다.", "기업 내부 문서를 노트북에 통합하면 신규 팀원 온보딩 시간을 극적으로 단축할 수 있다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "NotebookLM은 리서치 도구를 넘어 소스 기반 콘텐츠 생산 시스템(슬라이드, 인포그래픽, 팟캐스트, 퀴즈)으로 진화",
    "출처 기반 응답으로 환각 최소화 + 50개 이상 소스 통합이 핵심 차별화 강점",
    "Studio 패널 원클릭 변환으로 동일 소스에서 복수 콘텐츠 포맷을 병렬 생성 가능"
  ],
  "tech_stack": ["NotebookLM", "Google", "Forrester", "Gartner"],
  "apply_points": [
    {"text": "tech-review 블로그의 WIM 생성 과정에서 NotebookLM으로 여러 유사 영상을 동시에 분석하고 트렌드를 추출하는 리서치 레이어로 활용 가능", "key": False},
    {"text": "mcp-memory의 세션 기록과 작업 로그를 NotebookLM에 업로드하여 프로젝트 패턴 분석 및 온보딩 자료 자동 생성에 활용 검토", "key": True},
    {"text": "orchestration 파이프라인 문서들을 NotebookLM에 통합하여 새 Claude 세션 시작 시 컨텍스트 복구용 인터랙티브 Q&A 도구로 활용 가능", "key": True}
  ],
  "smart_brevity": {
    "why": "정보 과잉 시대에서 진짜 문제는 수집이 아니라 통합이다. NotebookLM은 소스의 양을 이해의 깊이로 전환하는 드문 도구다.",
    "what": "Google NotebookLM의 7가지 실전 유스케이스 — 전략 리서치, 팟캐스트 생성, 콘텐츠 변환, 교육 자료, 팀 지식 공유.",
    "axioms": [
      {"label": "The big picture", "content": "AI 도구의 다음 경쟁은 생성 능력이 아니라 소스 충실도(grounding)에서 결정된다 — NotebookLM이 이 방향을 선도하고 있다."}
    ]
  }
}

# Korean title video — garbled encoding, process based on transcript content
# The transcript is about 자동화 (automation) with Korean content
k_title_1 = None
k_title_2 = None
for v in data:
    title = v.get('title', '')
    t = v.get('transcript', '') or ''
    if len(t) > 100 and not v.get('summary', {}).get('sections'):
        if 'Claude' not in title and 'How' not in title and 'Build' not in title and 'Google' not in title and 'Nano' not in title and 'NotebookLM' not in title and '800' not in title and 'Use' not in title:
            print(f"Korean title candidate: [{title}] len={len(t)}")
            if k_title_1 is None:
                k_title_1 = title
            else:
                k_title_2 = title

print(f"k1={k_title_1}, k2={k_title_2}")
