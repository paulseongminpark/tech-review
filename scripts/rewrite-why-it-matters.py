#!/usr/bin/env python3
"""
rewrite-why-it-matters.py — Claude Code CLI로 Why it matters 일괄 재작성

모든 YouTube, Twitter, Daily Post의 Why it matters를
Paul의 프로젝트 맥락 기반으로 재작성한다.

Usage: python scripts/rewrite-why-it-matters.py [--target youtube|twitter|daily|all]
"""

import json, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
DATA_DIR = BLOG_DIR / "_data"
POSTS_DIR = BLOG_DIR / "_posts" / "ko"

CONTEXT_BRIEF = """
Paul의 프로젝트 맥락:
- orchestration: Claude Code 중심 멀티AI 오케스트레이션 시스템 (Workers 3개, Skills 13개, Hook Framework)
- mcp-memory: 외부 메모리 MCP 서버 (지식 그래프, 온톨로지 기반 관찰→시그널→패턴→원칙 성숙 파이프라인)
- Context Engineering: 200K→1M 토큰 컨텍스트를 화폐처럼 관리. Gate A/B/C 전략, Progressive Reading
- tech-review: 매일 자동 AI/테크 뉴스 수집 시스템 (Perplexity→ChatGPT DR 전환 중, Playwright 자동화)
- portfolio: Next.js 포트폴리오 사이트
- daily-memo: 모바일 메모 수집·처리
- 멀티AI 협업: Claude(설계/결정) + Codex(추출/분석) + Gemini(2nd opinion)
- 5단계 파이프라인: Ideation→Impl Design→Impl Review→구현→Code Review
- 핵심 관심사: 에이전트 자율성, 컨텍스트 효율, 지식 그래프 진화, 자동화, 비용 최적화
"""

REWRITE_PROMPT = """
아래 뉴스/영상의 "Why it matters"를 Paul의 프로젝트 맥락 관점에서 재작성해라.

{context}

규칙:
1. ~다 체 고정
2. Paul의 실제 프로젝트(orchestration, mcp-memory, Context Engineering 등)와 연결
3. 일반론 금지. "이 기술이 Paul의 XX에 YY 영향을 줄 수 있다" 수준의 구체성
4. 1-2문장. 간결하게.
5. JSON 배열로 출력. 각 항목은 {{"id": "원본id", "why": "새 Why it matters"}}

대상 목록:
{items}

반드시 JSON 배열만 출력. 마크다운 코드블록 없이.
"""


def rewrite_batch_with_claude(items: list, context: str) -> list:
    """Claude Code CLI로 배치 재작성"""
    prompt = REWRITE_PROMPT.format(context=context, items=json.dumps(items, ensure_ascii=False))

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        result = subprocess.run(
            f'claude -p "{prompt_file}" --output-format text',
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=300, shell=True,
        )
        output = result.stdout.strip()
        # JSON 추출
        if output.startswith('['):
            return json.loads(output)
        # 코드블록 안에 있을 수 있음
        match = re.search(r'\[[\s\S]*\]', output)
        if match:
            return json.loads(match.group())
        print(f"  [WARN] JSON 파싱 실패: {output[:200]}")
        return []
    except Exception as e:
        print(f"  [ERROR] Claude CLI 실패: {e}")
        return []
    finally:
        os.unlink(prompt_file)


def rewrite_youtube():
    """YouTube Why it matters 재작성"""
    print("\n=== YouTube Why it matters 재작성 ===")
    batch_file = BLOG_DIR / "_tmp" / "yt-why-batch.json"
    entries = json.loads(batch_file.read_text(encoding="utf-8"))

    items = [{"id": e["video_id"], "title": e["title"], "what": e.get("what", "")[:150]} for e in entries]

    # 10개씩 배치
    all_results = []
    for i in range(0, len(items), 10):
        batch = items[i:i+10]
        print(f"  배치 {i//10+1}/{(len(items)+9)//10} ({len(batch)}건)...")
        results = rewrite_batch_with_claude(batch, CONTEXT_BRIEF)
        all_results.extend(results)
        print(f"    → {len(results)}건 완료")

    # 결과 적용
    why_map = {r["id"]: r["why"] for r in all_results}
    updated = 0
    for f in sorted((DATA_DIR / "sources").glob("youtube-*.json")):
        videos = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for v in videos:
            vid = v.get("video_id")
            if vid in why_map and v.get("summary", {}).get("smart_brevity"):
                v["summary"]["smart_brevity"]["why"] = why_map[vid]
                changed = True
                updated += 1
        if changed:
            f.write_text(json.dumps(videos, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  YouTube 완료: {updated}건 업데이트")


def rewrite_twitter():
    """Twitter Why it matters 재작성"""
    print("\n=== Twitter Why it matters 재작성 ===")
    bm_file = DATA_DIR / "bookmarks.json"
    bookmarks = json.loads(bm_file.read_text(encoding="utf-8"))

    items = [{"id": b["id"], "title": f"@{b.get('author','')}: {b.get('whats_happening','')[:100]}", "what": b.get("whats_happening", "")[:150]} for b in bookmarks if b.get("why_it_matters")]

    all_results = []
    for i in range(0, len(items), 10):
        batch = items[i:i+10]
        print(f"  배치 {i//10+1}/{(len(items)+9)//10} ({len(batch)}건)...")
        results = rewrite_batch_with_claude(batch, CONTEXT_BRIEF)
        all_results.extend(results)
        print(f"    → {len(results)}건 완료")

    why_map = {r["id"]: r["why"] for r in all_results}
    updated = 0
    for b in bookmarks:
        if b["id"] in why_map:
            b["why_it_matters"] = why_map[b["id"]]
            updated += 1

    bm_file.write_text(json.dumps(bookmarks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Twitter 완료: {updated}건 업데이트")


def rewrite_daily_posts():
    """Daily Posts Why it matters 재작성"""
    print("\n=== Daily Posts Why it matters 재작성 ===")

    # 모든 포스트에서 섹션별 Why it matters 추출
    posts = []
    for f in sorted(POSTS_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        sections = re.findall(r'## \d+\.\s*(.+?)(?:\n|$)', text)
        whys = re.findall(r'\*\*Why it matters:\*\*\s*(.+?)(?:\n|$)', text)
        for i, (sec, _) in enumerate(zip(sections, whys)):
            posts.append({"id": f"{f.stem}__s{i+1}", "file": f.name, "title": sec.strip()[:80], "what": ""})

    all_results = []
    for i in range(0, len(posts), 10):
        batch = posts[i:i+10]
        print(f"  배치 {i//10+1}/{(len(posts)+9)//10} ({len(batch)}건)...")
        results = rewrite_batch_with_claude(batch, CONTEXT_BRIEF)
        all_results.extend(results)
        print(f"    → {len(results)}건 완료")

    # 결과 적용 - 파일별로 Why it matters 교체
    why_map = {r["id"]: r["why"] for r in all_results}
    updated = 0
    for f in sorted(POSTS_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        sections = re.findall(r'## \d+\.\s*(.+?)(?:\n|$)', text)
        new_text = text
        for i in range(len(sections)):
            key = f"{f.stem}__s{i+1}"
            if key in why_map:
                # 해당 섹션의 Why it matters 교체
                pattern = r'(\*\*Why it matters:\*\*\s*).+?(?=\n)'
                matches = list(re.finditer(pattern, new_text))
                if i < len(matches):
                    m = matches[i]
                    new_text = new_text[:m.start()] + f"**Why it matters:** {why_map[key]}" + new_text[m.end():]
                    updated += 1

        if new_text != text:
            f.write_text(new_text, encoding="utf-8")

    print(f"  Daily Posts 완료: {updated}건 업데이트")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="all", choices=["youtube", "twitter", "daily", "all"])
    args = parser.parse_args()

    print(f"=== Why it matters 일괄 재작성 시작 (target: {args.target}) ===")

    if args.target in ("youtube", "all"):
        rewrite_youtube()
    if args.target in ("twitter", "all"):
        rewrite_twitter()
    if args.target in ("daily", "all"):
        rewrite_daily_posts()

    print("\n=== 전체 완료 ===")


if __name__ == "__main__":
    main()
