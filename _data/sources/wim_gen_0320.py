import json, re

def clean_transcript(t):
    t = re.sub(r'<\d+:\d+:\d+\.\d+>', ' ', t)
    t = re.sub(r'</?c>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

base = 'C:/dev/01_projects/03_tech-review/blog/_data/sources'
path = f'{base}/youtube-2026-03-20.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

summaries = {}

summaries["I Built My Entire Design System in 4 Hours With AI. Full Tutorial (Claude + Cursor + Figma)"] = {
  "sections": [
    {
      "heading": "핵심 주장: AI로 디자인 시스템 구축 시간 단축",
      "body": "팀이 새 기능을 출시하는 데 2주가 걸리는 반면, AI 기반 디자인 시스템을 갖춘 팀은 2시간이면 충분하다. 개발자의 62%가 Figma와 코드 간 핸드오프 불일치로 인해 설계를 다시 만드는 데 시간을 낭비하고 있다. Claude, Cursor, Figma MCP를 조합하면 기존에는 복잡하고 시간 소모적이었던 디자인 시스템 코드화를 단 하루 오후에 완성할 수 있다.",
      "highlights": ["팀이 새 기능을 출시하는 데 2주가 걸리는 반면, AI 기반 디자인 시스템을 갖춘 팀은 2시간이면 충분하다.", "개발자의 62%가 Figma와 코드 간 핸드오프 불일치로 인해 설계를 다시 만드는 데 시간을 낭비하고 있다."],
      "quote": "My team takes two hours. The difference, we built our design system in code and it took us one afternoon."
    },
    {
      "heading": "Figma MCP로 스타일 토큰 자동 추출",
      "body": "Figma MCP 연결을 통해 Claude에게 style tokens.ts 파일 생성을 지시하면, 색상 변수, 타이포그래피, 간격, 테두리 등 모든 토큰이 Figma 컴포넌트 라이브러리에서 자동으로 추출된다. 이렇게 만들어진 스타일 가이드가 모든 컴포넌트와 토큰의 단일 진실 공급원(Single Source of Truth)이 된다. 모든 색상, 간격 스타일, 폰트가 Figma에서 직접 가져와 TypeScript로 코드화되므로 디자인-개발 간 불일치가 구조적으로 차단된다.",
      "highlights": ["이렇게 만들어진 스타일 가이드가 모든 컴포넌트와 토큰의 단일 진실 공급원(Single Source of Truth)이 된다.", "모든 색상, 간격 스타일, 폰트가 Figma에서 직접 가져와 TypeScript로 코드화되므로 디자인-개발 간 불일치가 구조적으로 차단된다."],
      "quote": "Now we have the single source of truth for all of our components and tokens from here on out."
    },
    {
      "heading": "컴포넌트 라이브러리 빌드: 상세 프롬프트 전략",
      "body": "컴포넌트 빌드 시 단순한 지시가 아닌 상호작용, 디자인 명세, 동작 방식을 포함한 상세 프롬프트가 핵심이다. Figma 파일에서 가져온 컴포넌트 정의에 사용 예시까지 포함하면 Claude가 개발자 기준에 맞는 정확한 컴포넌트를 생성한다. 각 새 기능이나 프로젝트 파트를 시작할 때마다 별도의 Claude 대화창을 열어야 해당 컨텍스트가 하나의 채팅에 집중되어 일관성이 유지된다.",
      "highlights": ["컴포넌트 빌드 시 단순한 지시가 아닌 상호작용, 디자인 명세, 동작 방식을 포함한 상세 프롬프트가 핵심이다.", "각 새 기능이나 프로젝트 파트를 시작할 때마다 별도의 Claude 대화창을 열어야 한다."],
      "quote": None
    },
    {
      "heading": "실전 워크플로우: KPI 카드 컴포넌트 구축",
      "body": "KPI 카드 컴포넌트 예시를 통해 상세 프롬프트 작성, Figma MCP에서 컴포넌트 정의 추출, TypeScript 컴포넌트 생성, 스타일 토큰 적용까지의 전체 흐름을 보여준다. 프롬프트에 Figma 컴포넌트 이름을 명시하면 Claude가 해당 스펙을 MCP를 통해 직접 읽어 구현하므로 수동 번역 오류가 없다. 컨텍스트 윈도우가 가득 차기 전에 대화를 저장하는 팁도 중요한데, 완성된 컴포넌트 라이브러리를 파일로 내보내 보존해야 한다.",
      "highlights": ["프롬프트에 Figma 컴포넌트 이름을 명시하면 Claude가 해당 스펙을 MCP를 통해 직접 읽어 구현하므로 수동 번역 오류가 없다.", "컨텍스트 윈도우가 가득 차기 전에 대화를 저장하는 팁도 중요하다."],
      "quote": None
    },
    {
      "heading": "Cursor 통합: 컴포넌트 라이브러리를 실제 코드에 적용",
      "body": "완성된 스타일 토큰과 컴포넌트 라이브러리를 Cursor에 연결하면 새 기능 구현 시 AI가 항상 동일한 디자인 시스템을 참조한다. Cursor의 rules 파일에 디자인 시스템 경로를 명시하여 모든 AI 지원 코딩이 일관된 디자인 토큰을 사용하게 된다. 이 구조 덕분에 디자이너-개발자 협업 시 Figma 변경사항이 코드에 자동으로 반영되는 파이프라인이 완성된다.",
      "highlights": ["완성된 스타일 토큰과 컴포넌트 라이브러리를 Cursor에 연결하면 새 기능 구현 시 AI가 항상 동일한 디자인 시스템을 참조한다.", "Cursor의 rules 파일에 디자인 시스템 경로를 명시하여 모든 AI 지원 코딩이 일관된 디자인 토큰을 사용하게 된다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "Figma MCP → Claude → style tokens.ts 파이프라인으로 디자인-코드 단일 진실 공급원 구축 가능",
    "새 기능마다 별도 Claude 대화창을 열어야 컨텍스트 오염 없이 일관성 유지됨",
    "상세 프롬프트(상호작용+디자인 명세+사용 예시)가 컴포넌트 품질을 결정하는 핵심 변수"
  ],
  "tech_stack": ["Claude", "Cursor", "Figma", "Figma MCP", "TypeScript"],
  "apply_points": [
    {"text": "portfolio 프로젝트에 Figma MCP + Claude 연동으로 스타일 토큰 자동 추출 파이프라인 구축 가능", "key": True},
    {"text": "tech-review 블로그 컴포넌트를 디자인 시스템화하여 포스트 레이아웃 일관성 확보 검토", "key": False},
    {"text": "orchestration의 CLAUDE.md rules처럼, Cursor rules에 디자인 시스템 경로를 명시하는 패턴은 컨텍스트 주입 방식으로 응용 가능", "key": True}
  ],
  "smart_brevity": {
    "why": "디자인-코드 핸드오프 문제는 도구 부족이 아니라 단일 진실 공급원 부재의 문제다. Figma MCP가 이 구조적 결함을 제거한다.",
    "what": "Claude + Figma MCP + Cursor를 연결해 4시간 안에 전체 디자인 시스템을 코드로 구축하는 풀 튜토리얼.",
    "axioms": [
      {"label": "The bottom line", "content": "AI 디자인 시스템의 핵심은 Figma에서 코드로의 자동 동기화다 — 수동 번역 단계를 구조적으로 제거하는 것."}
    ]
  }
}

summaries["GSD Is the Missing Piece For Claude Code"] = {
  "sections": [
    {
      "heading": "프레임워크 선택 실패의 진짜 원인",
      "body": "AI 코딩 프레임워크가 계속 증가하고 있지만, 프레임워크가 맞지 않을 때의 실패는 프레임워크 자체의 문제가 아니라 선택의 문제다. 각 프레임워크는 설계된 유스케이스에서는 잘 작동하며 모두를 위한 하나의 정답은 없다. GSD(Get Stuff Done)는 BMAD, Superpowers 같은 기존 프레임워크와 달리 사전 계획을 최소화하고 단계별 실험을 허용하는 방식으로 설계되었다.",
      "highlights": ["프레임워크가 맞지 않을 때의 실패는 프레임워크 자체의 문제가 아니라 선택의 문제다.", "각 프레임워크는 설계된 유스케이스에서는 잘 작동하며 모두를 위한 하나의 정답은 없다."],
      "quote": "That's not the framework's problem. That's a selection problem."
    },
    {
      "heading": "GSD란 무엇인가: 설계 철학",
      "body": "GSD는 Get Stuff Done의 약자로, 무엇을 만들지 완전히 확신하지 못하거나 요구사항이 계속 변할 가능성이 있는 프로젝트에 최적화된 프레임워크다. BMAD처럼 모든 단계를 사전에 상세하게 계획하지 않고, 초기 범위를 기반으로 각 구현 단계를 순차적으로 계획한다. MVP를 최대한 빠르게 구축하고 싶거나, 이전에 만들어진 적 없는 커스텀 솔루션을 실험적으로 개발할 때 특히 적합하다.",
      "highlights": ["GSD는 무엇을 만들지 완전히 확신하지 못하거나 요구사항이 계속 변할 가능성이 있는 프로젝트에 최적화된 프레임워크다.", "초기 범위를 기반으로 각 구현 단계를 순차적으로 계획한다."],
      "quote": "You use GSD where you aren't really sure what to build and you don't want to pre-plan everything because the requirements might change in the future."
    },
    {
      "heading": "GSD vs BMAD vs Superpowers: 선택 기준 매트릭스",
      "body": "BMAD는 GSD와 정반대 접근법으로, 모든 단계를 상세하게 사전 계획하므로 요구사항이 명확하고 안정적인 프로젝트에 적합하다. Superpowers는 특정 도메인에 최적화된 워크플로우를 제공하며 각 프레임워크마다 빛나는 유스케이스가 다르다. 선택 기준은 단순히 더 좋은 프레임워크가 아니라 프로젝트의 불확실성 수준, 실험 필요 여부, 팀 규모에 따라 결정되어야 한다.",
      "highlights": ["BMAD는 요구사항이 명확하고 안정적인 프로젝트에 적합하다.", "선택 기준은 프로젝트의 불확실성 수준, 실험 필요 여부, 팀 규모에 따라 결정되어야 한다."],
      "quote": None
    },
    {
      "heading": "GSD 실전: 단계별 구현 흐름과 적합한 유스케이스",
      "body": "GSD는 초기 범위 정의 후 각 단계를 하나씩 계획하고 실행하는 방식으로 작동하며, 각 단계에서 다음 단계가 결정된다. 후반부 단계는 미리 상세하게 잠기지 않으므로 실험 결과에 따라 방향을 유연하게 바꿀 수 있다. Cluey 같은 온스크린 인터뷰 어시스턴트처럼 화면 공유 탐지 회피나 UX 결정 같이 사전에 결정할 수 없는 요소가 많은 프로젝트가 GSD의 대표적 유스케이스다.",
      "highlights": ["후반부 단계는 미리 상세하게 잠기지 않으므로 실험 결과에 따라 방향을 유연하게 바꿀 수 있다.", "사전에 결정할 수 없는 요소가 많은 프로젝트가 GSD의 대표적 유스케이스다."],
      "quote": None
    },
    {
      "heading": "실용적 결론: 프레임워크 선택 가이드",
      "body": "GSD는 불확실성이 높고 빠른 MVP 구축이 필요한 경우, BMAD는 요구사항이 명확하고 대규모 프로젝트에 체계적 계획이 필요한 경우, Superpowers는 특정 도메인에 최적화된 워크플로우가 필요한 경우에 선택한다. 세 프레임워크를 프로젝트 성격에 따라 조합하여 전환하는 것도 가능하다. 핵심은 프레임워크의 우열을 따지는 것이 아니라 자신의 프로젝트 성격을 먼저 파악하는 것이다.",
      "highlights": ["핵심은 프레임워크의 우열을 따지는 것이 아니라 자신의 프로젝트 성격을 먼저 파악하는 것이다.", "세 프레임워크를 프로젝트 성격에 따라 조합하여 전환하는 것도 가능하다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "GSD(Get Stuff Done)는 요구사항 불확실성이 높은 프로젝트에서 BMAD보다 적합한 프레임워크",
    "프레임워크 실패의 원인은 대부분 프레임워크 자체가 아닌 잘못된 선택",
    "선택 기준: 불확실성 높음 GSD, 요구사항 명확 BMAD, 특정 도메인 Superpowers"
  ],
  "tech_stack": ["Claude Code", "GSD", "BMAD", "Superpowers"],
  "apply_points": [
    {"text": "orchestration 파이프라인(Diagnose-Architect-Build-Harden)은 BMAD 철학에 가깝다 — 불확실성 높은 신규 아이디에이션에 GSD 방식 경량 파이프라인 도입 검토 가능", "key": True},
    {"text": "mcp-memory 신기능 실험처럼 요구사항이 탐색적인 작업에는 GSD 방식(단계별 계획)이 현재 파이프라인보다 빠를 수 있음", "key": False},
    {"text": "Claude Code 사용 시 프로젝트 성격에 따라 프레임워크를 명시적으로 선택하는 의사결정 기준을 orchestration rules에 추가 가능", "key": False}
  ],
  "smart_brevity": {
    "why": "프레임워크 논쟁은 잘못된 질문이다. 진짜 질문은 이 프로젝트의 불확실성 수준이 얼마인가다. GSD는 그 질문에 구조적으로 답한다.",
    "what": "AI 코딩 프레임워크 GSD 소개 및 BMAD, Superpowers와의 선택 기준 비교.",
    "axioms": [
      {"label": "The big picture", "content": "AI 코딩 프레임워크의 진화는 더 좋은 계획 도구가 아니라 불확실성을 다루는 방식의 다양화로 이해해야 한다."},
      {"label": "The bottom line", "content": "프로젝트 착수 전 불확실성 수준을 명시적으로 평가하고 프레임워크를 선택하는 습관이 실패를 줄이는 핵심이다."}
    ]
  }
}

summaries["Jenny Wen: The design process is dead. Why Designers can no longer trust it."] = {
  "sections": [
    {
      "heading": "전통적 디자인 프로세스의 붕괴",
      "body": "Jenny Wen은 분기 시작마다 반복되는 사용자 리서치, 퍼소나 생성, 여정 지도, 브레인스토밍, 문제 정의, 솔루션 설계의 전통적 디자인 프로세스가 더 이상 신뢰할 수 없다고 주장한다. AI가 이 모든 단계를 순식간에 처리할 수 있게 되면서, 6주짜리 프로세스를 따른다는 것 자체가 경쟁 우위가 아니라 오히려 느린 실행의 증거가 되었다. 문제는 프로세스의 순서나 품질이 아니라, 프로세스를 따르는 것 자체가 더 이상 좋은 결과를 보장하지 않는다는 근본적 위기다.",
      "highlights": ["AI가 이 모든 단계를 순식간에 처리할 수 있게 되면서, 6주짜리 프로세스를 따른다는 것 자체가 경쟁 우위가 아니라 오히려 느린 실행의 증거가 되었다.", "프로세스를 따르는 것 자체가 더 이상 좋은 결과를 보장하지 않는다는 근본적 위기다."],
      "quote": "Imagine this. It is the start of a quarter. Your team has to figure out what to do."
    },
    {
      "heading": "OKR과 디자인 의사결정의 연결 실패",
      "body": "많은 팀에서 디자인 프로세스와 OKR이 연결되지 않는 구조적 문제가 존재한다. 사용자 여정 지도와 퍼소나를 완벽하게 만들어도 그것이 비즈니스 목표 달성에 기여하는지 검증하지 않으면 의미 없는 작업이 된다. 디자인 의사결정이 항상 측정 가능한 비즈니스 지표와 직결되어야 하며, 그렇지 않은 프로세스 단계는 존재 자체를 재검토해야 한다.",
      "highlights": ["디자인 의사결정이 항상 측정 가능한 비즈니스 지표와 직결되어야 한다.", "그렇지 않은 프로세스 단계는 존재 자체를 재검토해야 한다."],
      "quote": None
    },
    {
      "heading": "AI 시대 디자이너의 새로운 역할",
      "body": "AI가 리서치, 퍼소나 생성, 와이어프레임 제작을 대신할 수 있다면 디자이너의 가치는 AI 결과물을 비판적으로 판단하고, 사용자 맥락을 읽으며, 비즈니스 목표와 연결하는 판단력에 있다. 도구를 사용하는 능력이 아니라 무엇을 만들지 결정하는 능력, 그리고 AI가 놓친 것을 포착하는 직관이 디자이너의 핵심 경쟁력이 된다. 퍼소나에 가짜 이름과 AI 생성 사진을 넣는 것이 아니라, 실제 사용자 맥락을 해석하는 능력이 차별화 요소다.",
      "highlights": ["디자이너의 가치는 AI 결과물을 비판적으로 판단하고, 사용자 맥락을 읽으며, 비즈니스 목표와 연결하는 판단력에 있다.", "무엇을 만들지 결정하는 능력, 그리고 AI가 놓친 것을 포착하는 직관이 디자이너의 핵심 경쟁력이 된다."],
      "quote": None
    },
    {
      "heading": "적응형 디자인: 프로세스를 버리고 원칙을 남기는 법",
      "body": "프로세스를 버린다는 것이 방법론적 무정부주의를 의미하지는 않는다. 고정된 단계 대신 상황에 맞게 적응하는 원칙 기반 접근법이 현대 디자이너의 역량이다. 빠른 프로토타이핑이 필요할 때, 깊은 리서치가 필요할 때, AI 결과물을 검증해야 할 때 각각 다른 도구와 방법을 유연하게 선택하는 것이 핵심이다.",
      "highlights": ["고정된 단계 대신 상황에 맞게 적응하는 원칙 기반 접근법이 현대 디자이너의 역량이다.", "단계를 따르는 것이 아니라 목적에 맞는 방법을 선택하는 판단력이 핵심이다."],
      "quote": None
    },
    {
      "heading": "디자이너가 살아남는 법: 실행자에서 판단자로",
      "body": "AI 시대에 디자이너가 생존하려면 실행 역량(AI가 대체 가능)보다 전략적 판단력(AI가 대체 불가)을 강화해야 한다. 사용자 인터뷰를 직접 진행하고, 데이터를 해석하고, 비즈니스 이해관계자를 설득하는 능력은 여전히 인간만이 가능한 영역이다. Jenny Wen은 디자이너가 실행자에서 판단자로 역할을 전환해야 한다고 결론짓는다.",
      "highlights": ["실행 역량(AI가 대체 가능)보다 전략적 판단력(AI가 대체 불가)을 강화해야 한다.", "디자이너가 실행자에서 판단자로 역할을 전환해야 한다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "전통적 6단계 디자인 프로세스는 AI가 대체 가능해졌고, 프로세스 준수 자체가 경쟁 우위가 아니게 됨",
    "디자이너의 새 핵심 역량: AI 결과물 비판적 판단, 사용자 맥락 해석, 비즈니스 목표 연결",
    "고정 프로세스 대신 상황 적응형 원칙 기반 접근으로 전환이 생존 전략"
  ],
  "tech_stack": ["Figma", "AI 디자인 도구"],
  "apply_points": [
    {"text": "AI가 생성한 결과물을 비판적으로 검증하는 습관은 mcp-memory 온톨로지 설계나 Claude Code 결과물 리뷰 시 동일하게 적용됨", "key": True},
    {"text": "orchestration 파이프라인 설계 시 단계 준수 강박 대신 목적 달성을 기준으로 단계를 선택하는 원칙 반영 고려", "key": False},
    {"text": "portfolio 사이트 디자인 작업 시 퍼소나 여정지도보다 OKR 기반 의사결정을 우선시하는 접근 적용 가능", "key": False}
  ],
  "smart_brevity": {
    "why": "프로세스 신앙은 불확실성을 통제하려는 방어 기제였다. AI가 그 불확실성을 처리하자 프로세스 자체의 가치가 증발했다. 남은 것은 판단력이다.",
    "what": "디자인 프로세스의 종말을 선언하고, AI 시대 디자이너의 새로운 역할과 생존 전략을 제시하는 컨퍼런스 강연.",
    "axioms": [
      {"label": "The big picture", "content": "AI가 방법론을 대체하는 속도보다 판단력을 키우는 속도가 빠른 사람이 살아남는다."}
    ]
  }
}

summaries["How to easily use the hot Claude skill and Open Claw in Silicon Valley"] = {
  "sections": [
    {
      "heading": "주의: 제목-내용 불일치 (자막 오염 영상)",
      "body": "이 영상의 자막은 제목(Claude 스킬 사용법)과 전혀 다른 내용인 척추지압사 Dr. Jen의 목 통증 해결 가이드를 담고 있다. 자막 내용 기준으로 요약한다. Dr. Jen은 스마트폰과 컴퓨터 사용으로 인한 자세 불량이 목 통증의 주원인이라고 설명하며, 집에서 실천 가능한 3가지 자세 교정 방법을 소개한다.",
      "highlights": ["이 영상의 자막은 제목과 전혀 다른 내용인 척추지압사 Dr. Jen의 목 통증 해결 가이드를 담고 있다.", "Dr. Jen은 스마트폰과 컴퓨터 사용으로 인한 자세 불량이 목 통증의 주원인이라고 설명한다."],
      "quote": "The number one cause of neck pain is poor posture."
    },
    {
      "heading": "목 통증의 원인: 현대인의 자세 문제",
      "body": "매일 수시간 동안 스마트폰, 컴퓨터, 책상 앞에 구부정하게 앉는 습관이 시간이 지남에 따라 목 통증을 유발한다. 앞으로 숙인 자세는 목에 과도한 하중을 가하며, 이는 근육 긴장과 만성 통증으로 이어진다. 단순히 장시간 사용이 문제가 아니라 자세 자체가 근본 원인이며, 자세 교정이 가장 효과적인 해결책이다.",
      "highlights": ["앞으로 숙인 자세는 목에 과도한 하중을 가하며, 이는 근육 긴장과 만성 통증으로 이어진다.", "자세 교정이 가장 효과적인 해결책이다."],
      "quote": None
    },
    {
      "heading": "3가지 실천 방법: 자세 교정, 스트레칭, 인체공학",
      "body": "첫째, 화면 높이를 눈높이에 맞추고 귀가 어깨 위에 직접 위치하도록 자세를 조정한다. 둘째, 목 근육을 이완시키는 간단한 스트레칭을 정기적으로 실시한다. 셋째, 작업 환경의 인체공학적 설정을 통해 자연스러운 자세를 유지할 수 있는 환경을 만든다.",
      "highlights": ["화면 높이를 눈높이에 맞추고 귀가 어깨 위에 직접 위치하도록 자세를 조정한다.", "작업 환경의 인체공학적 설정을 통해 자연스러운 자세를 유지할 수 있는 환경을 만든다."],
      "quote": None
    },
    {
      "heading": "장기 관리: 예방이 치료보다 중요하다",
      "body": "목 통증이 이미 있다면 먼저 원인을 파악하고 자세 교정부터 시작해야 한다. 통증이 없더라도 예방적 스트레칭과 자세 관리를 습관화하는 것이 장기적으로 훨씬 효과적이다. 작은 일상 습관의 변화가 만성 통증을 예방하는 가장 강력한 도구다.",
      "highlights": ["통증이 없더라도 예방적 스트레칭과 자세 관리를 습관화하는 것이 장기적으로 훨씬 효과적이다.", "작은 일상 습관의 변화가 만성 통증을 예방하는 가장 강력한 도구다."],
      "quote": None
    }
  ],
  "key_takeaways": [
    "자막 내용이 제목과 불일치 — Claude 스킬이 아닌 척추지압 콘텐츠 (오염 영상)",
    "자세 불량(목 앞으로 숙임)이 현대인 목 통증의 주원인",
    "화면 높이 조정, 정기 스트레칭, 인체공학적 환경 설정의 3가지 실천이 핵심"
  ],
  "tech_stack": [],
  "apply_points": [
    {"text": "장시간 개발 세션 중 WezTerm + tmux 환경에서 모니터 높이 및 자세 점검 리마인더 설정 고려", "key": False},
    {"text": "이 영상은 제목-내용 불일치 사례로, tech-review YouTube 인제스트 파이프라인에 콘텐츠 검증 단계 추가 필요성을 보여줌", "key": True}
  ],
  "smart_brevity": {
    "why": "자막 오염 사례. 제목은 AI 도구지만 내용은 척추지압. 인제스트 파이프라인의 콘텐츠 검증 필요성을 드러낸다.",
    "what": "자막 기준: 목 통증 예방을 위한 자세 교정 3가지 방법 소개 (척추지압사 Dr. Jen).",
    "axioms": [
      {"label": "Yes, but", "content": "자세 교정 조언 자체는 유효하지만, 이 영상은 AI 기술 리뷰 컨텍스트와 무관한 오염 콘텐츠다."}
    ]
  }
}

# Write back
for v in data:
    title = v.get("title", "")
    if title in summaries:
        v["summary"] = summaries[title]
        print(f"Updated: {title[:70]}")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done: youtube-2026-03-20.json")
