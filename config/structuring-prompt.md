# YouTube Transcript 구조화 프롬프트

다음 YouTube 영상의 자막을 Smart Brevity 방법론에 따라 구조화해라. 순수 JSON만 출력.

## Smart Brevity란?

Axios가 만든 정보 전달 방법론이다.

핵심 원칙:
- 독자의 시간을 존중한다
- 가장 중요한 것을 먼저 전달한다
- 구조화된 레이블로 독자가 스캔할 수 있게 한다
- 깊이는 독자가 선택한다

### 4대 구조 (core_4)

1. **Muscular Tease** — 6단어 이하 헤드라인. 능동 동사, 도발적이면서 정확. 각 section의 heading이 이 역할.
2. **Single Lede** — 단 1문장으로 가장 중요한 메시지 전달. smart_brevity.what의 첫 문장이 이 역할.
3. **Why It Matters (WIM)** — 이 정보가 왜 중요한지. "So what?"에 대한 답. 최대 2문장. 직접적이고 선언적.
4. **Go Deeper** — 선택적 깊이. sections의 body가 이 역할. 더 읽을지는 독자가 결정.

### 12개 Axiom 레이블

콘텐츠에 해당되는 것만 선별 적용한다. 전부 쓰지 않는다. 개수 제한 없음.

| 레이블 | 사용 조건 |
|--------|----------|
| Why it matters | 항상 필수 — 핵심 맥락, 이것이 왜 중요한지 |
| The big picture | 거시적 맥락 — 산업 트렌드, 역사적 흐름 |
| What's next | 후속 전개가 명확할 때 — 로드맵, 예정된 변화 |
| Be smart | 전략적 인사이트 — 독자가 취할 행동/판단 기준 |
| By the numbers | 핵심 수치/데이터가 있을 때 |
| Between the lines | 표면 아래 숨겨진 의미가 있을 때 |
| The bottom line | 결론이 명확할 때 — 한 문장 결론 |
| Driving the news | 특정 사건이 이슈를 촉발했을 때 |
| Zoom in | 구체적 사례, 전문가 발언이 있을 때 |
| Yes, but | 반론, 주의사항, 단서가 있을 때 |
| What we're watching | 주목할 후속 전개가 있을 때 |
| Go deeper | 추가 자료, 원문 링크가 있을 때 |

## 규칙

1. 자막 내용을 독자 관점으로 재구성해라. 발화 순서가 아닌 주제별로 묶어라.
2. 자막에 없는 내용을 절대 만들지 마라.
3. sections 최소 6개. body 최소 5문장.
4. 전부 한국어 (고유명사는 영어 유지).
5. highlights는 body에서 그대로 복사한 문장이어야 한다.
6. quote는 자막 원문에서 단어 하나도 바꾸지 말고 그대로 복사. 없으면 생략.
7. tech_stack은 자막에서 실제 언급된 기술/도구명만. 없는 건 넣지 마라.
8. smart_brevity.why (WIM)는 이 영상의 정보가 왜 중요한지 1-2문장 선언적 판단.
9. smart_brevity.what은 핵심 주장 + 구조 + 사례 + 결론. 여러 문단 가능. 반드시 작성.
10. axiom은 해당되는 것 전부 사용. 레이블은 위 12개에서만 선택.

## 출력 JSON

```json
{
  "sections": [
    {
      "heading": "구체적 주제명 (Muscular Tease — 짧고 명확하게)",
      "body": "최소 5문장. 해당 주제의 모든 논거, 수치, 사례. (Go Deeper 역할)",
      "highlights": ["body에서 그대로 복사한 핵심 문장"],
      "quote": "자막에서 임팩트 있는 발언 그대로 복사. 없으면 생략."
    }
  ],
  "key_takeaways": ["핵심 요점 5개"],
  "tech_stack": ["자막에서 실제 언급된 기술/도구명만"],
  "smart_brevity": {
    "why": "WIM — 이 정보가 왜 중요한지 1-2문장 선언적 판단",
    "what": "What's happening — 첫 문장이 Single Lede(가장 중요한 메시지 1문장). 이후 핵심 주장 + 구조 + 사례 + 결론.",
    "axioms": [
      {"label": "12개 중 해당되는 것", "content": "1문장"}
    ]
  }
}
```

## 영상 제목

{title}

## 자막

{transcript}
