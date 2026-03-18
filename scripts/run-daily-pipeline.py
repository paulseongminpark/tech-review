#!/usr/bin/env python3
"""
run-daily-pipeline.py — Daily Post 전체 자동화 파이프라인

Step 1: 3-Tier Deep Research (Perplexity → Gemini → ChatGPT fallback)
Step 2: Claude Code CLI → Why it matters 맥락 재작성 (5줄 이내)
Step 3: Jekyll 포스트 생성 (frontmatter + source_type)
Step 4: extract-sections.js → 섹션 데이터
Step 5: git commit + push

Task Scheduler: 매일 05:00 KST (컴퓨터 wake)
Usage: python scripts/run-daily-pipeline.py [--date YYYY-MM-DD] [--skip-dr]
"""

import json, os, re, subprocess, sys, time, argparse, tempfile
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
TMP_DIR = BLOG_DIR / "_tmp"
POSTS_DIR = BLOG_DIR / "_posts" / "ko"

# 요일 → 태그
DAY_TAGS = {
    0: "weekly-recap",
    1: "ai-ml, models, research, benchmarks",
    2: "bigtech, google, microsoft, meta, apple, nvidia",
    3: "ai-industry, startups, business",
    4: "opensource, developer, tools",
    5: "hardware, infrastructure, chips",
    6: "use-cases, healthcare, education, policy",
}


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def step1_deep_research(post_date: str) -> Path | None:
    """3-Tier Deep Research: Perplexity → Gemini → ChatGPT fallback"""
    log("[Step 1] 3-Tier Deep Research 실행 (Perplexity → Gemini → ChatGPT)...")
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "fetch-deep-research.py"), "--date", post_date],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=5400,  # 90분 (3개 provider × 25분 + 여유)
    )
    if result.stdout:
        for line in result.stdout.strip().split("\n")[-8:]:
            log(f"  {line}")
    if result.returncode != 0:
        log(f"  [FAIL] exit code {result.returncode}")
        if result.stderr:
            log(f"  {result.stderr[-200:]}")
        return None

    raw_file = TMP_DIR / f"deep-research-{post_date}.md"
    if raw_file.exists() and raw_file.stat().st_size > 500:
        log(f"  [OK] {raw_file} ({raw_file.stat().st_size}자)")
        return raw_file
    log("  [FAIL] raw 파일 없음 또는 너무 짧음")
    return None


def step2_rewrite_why(raw_file: Path, post_date: str) -> Path:
    """Claude Code CLI로 Why it matters 재작성"""
    log("[Step 2] Claude Code CLI → Why it matters 재작성...")

    raw_content = raw_file.read_text(encoding="utf-8")

    # 프롬프트 구성
    # raw에서 SOURCE 라인 추출
    source_type = "unknown"
    for line in raw_content.split("\n")[:5]:
        if line.startswith("SOURCE:"):
            source_type = line.replace("SOURCE:", "").strip()
            break

    prompt = f"""아래는 Deep Research가 수집한 오늘의 AI/테크 뉴스 raw 데이터다.

{raw_content}

이 내용을 아래 Jekyll 포스트 형식으로 변환하라.
변환 시 **Why it matters:** 부분만 Paul의 프로젝트 맥락으로 재작성한다.

Paul의 맥락:
- orchestration: Claude Code 중심 멀티AI 시스템 (Workers 3, Skills 13)
- mcp-memory: 지식 그래프 (관찰→시그널→패턴→원칙 성숙)
- Context Engineering: 1M 토큰 관리, Gate A/B/C
- tech-review: Playwright 3-Tier DR 자동화 (Perplexity→Gemini→ChatGPT fallback)
- 멀티AI: Claude(설계) + Codex(추출) + Gemini(검증)

규칙:
1. ~다 체
2. Why it matters만 재작성. 나머지 팩트는 그대로 유지.
3. Paul의 실제 프로젝트와 연결. 일반론 금지.
4. Why it matters는 항목당 1~2문장, 전체 합계 5줄 이내.
5. Jekyll frontmatter 포함 (layout, title, date, lang, permalink, pair, tags, source_type: {source_type})
6. 마크다운만 출력. 코드블록 없이.

날짜: {post_date}
tags: [{DAY_TAGS.get(datetime.strptime(post_date, '%Y-%m-%d').weekday(), 'ai-ml')}]
"""

    # 프롬프트를 파일로 저장 (너무 길어서 CLI 인자로 못 넘김)
    prompt_file = TMP_DIR / f"claude-prompt-{post_date}.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    # Claude Code CLI 실행
    result = subprocess.run(
        f'claude -p "$(cat {str(prompt_file).replace(chr(92), "/")})" --output-format text',
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=300, shell=True, cwd=str(BLOG_DIR),
    )

    output = result.stdout.strip()
    if not output or len(output) < 500:
        log(f"  [WARN] Claude 출력 부족 ({len(output)}자), raw 그대로 사용")
        # fallback: raw 내용을 기본 포스트 형식으로 래핑
        output = raw_content

    # 저장
    final_file = TMP_DIR / f"final-{post_date}.md"
    final_file.write_text(output, encoding="utf-8")
    log(f"  [OK] {final_file} ({len(output)}자)")
    return final_file


def step3_create_post(final_file: Path, post_date: str):
    """Jekyll 포스트 생성"""
    log("[Step 3] Jekyll 포스트 생성...")

    content = final_file.read_text(encoding="utf-8")

    # frontmatter가 없으면 추가
    if not content.startswith("---"):
        # Today in One Line에서 title 추출
        title_match = re.search(r"Today in One Line\s*\n+(.+?)(?:\n|$)", content)
        title = title_match.group(1).strip() if title_match else f"{post_date} Daily Tech Review"
        title = title[:150]

        weekday = datetime.strptime(post_date, "%Y-%m-%d").weekday()
        tags_str = DAY_TAGS.get(weekday, "ai-ml")
        tags = json.dumps([t.strip() for t in tags_str.split(",")], ensure_ascii=False)

        frontmatter = f"""---
layout: post
title: "{title}"
date: {post_date}
lang: ko
permalink: /ko/{post_date.replace('-', '/')}/daily-tech-review/
pair: {post_date}-daily-tech-review
tags: {tags}
---

"""
        content = frontmatter + content

    # ## Comments 없으면 추가
    if "## Comments" not in content:
        content = content.rstrip() + "\n\n## Comments\n"

    # 저장
    post_file = POSTS_DIR / f"{post_date}-daily-tech-review.md"
    post_file.write_text(content, encoding="utf-8")
    log(f"  [OK] {post_file}")


def step4_extract_sections(post_date: str):
    """섹션 추출"""
    log("[Step 4] 섹션 추출...")
    result = subprocess.run(
        ["node", str(SCRIPT_DIR / "extract-sections.js"), "--date", post_date],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(BLOG_DIR), timeout=30,
    )
    if result.stdout:
        log(f"  {result.stdout.strip()}")


def step5_git_push(post_date: str):
    """git commit + push"""
    log("[Step 5] git commit + push...")
    os.chdir(BLOG_DIR)
    os.system("git add _posts/ko/ _data/sections/")
    os.system(f'git commit -m "[tech-review] {post_date} daily post (3-Tier DR + Claude 맥락)"')
    os.system("git push")
    log("  [OK] push 완료")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--skip-dr", action="store_true", help="Deep Research 스킵 (기존 raw 사용)")
    args = parser.parse_args()
    post_date = args.date

    TMP_DIR.mkdir(exist_ok=True)
    log(f"=== Daily Pipeline 시작 ({post_date}) ===")

    # Step 1: Deep Research
    raw_file = TMP_DIR / f"deep-research-{post_date}.md"
    if args.skip_dr and raw_file.exists():
        log("[Step 1] 스킵 (--skip-dr, 기존 raw 사용)")
    else:
        raw_file = step1_deep_research(post_date)
        if not raw_file:
            log("[ABORT] Deep Research 실패. 파이프라인 중단.")
            sys.exit(1)

    # Step 2: Why it matters 재작성
    final_file = step2_rewrite_why(raw_file, post_date)

    # Step 3: Jekyll 포스트
    step3_create_post(final_file, post_date)

    # Step 4: 섹션 추출
    step4_extract_sections(post_date)

    # Step 5: git push
    step5_git_push(post_date)

    log(f"=== 완료 ({post_date}) ===")


if __name__ == "__main__":
    main()
