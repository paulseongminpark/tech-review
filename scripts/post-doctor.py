#!/usr/bin/env python3
"""
post-doctor.py — Daily Post 사후 검증 + 장애 진단 + GitHub Issue 알림

run-daily-pipeline.py Step 6으로 자동 실행되거나, 수동 실행 가능.

검증 항목:
  1. frontmatter 필수 필드 (layout, title, date, lang, permalink, pair, tags)
  2. Today in One Line 존재 + 길이 (20~200자)
  3. 섹션 3개 (## 1. ~ ## 3.)
  4. Why it matters 존재 + 길이 (항목당 50~300자)
  5. What's next 존재
  6. Source URL 존재 + http 시작
  7. source_type frontmatter (perplexity/gemini/chatgpt)
  8. ## Comments 존재

장애 진단:
  - DR raw 파일 존재 여부 + provider 확인
  - fallback 발생 여부 (SOURCE 헤더)

알림:
  - 검증 실패 시 gh issue create
  - 성공 시 무음

Usage:
  python scripts/post-doctor.py [--date YYYY-MM-DD] [--fix] [--no-issue]
"""

import json, os, re, sys, argparse, subprocess
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
POSTS_DIR = BLOG_DIR / "_posts" / "ko"
TMP_DIR = BLOG_DIR / "_tmp"
LOGS_DIR = SCRIPT_DIR / "_logs"

REPO = "paulseongminpark/tech-review"


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# ── 검증 함수들 ─────────────────────────────────────────────

def check_frontmatter(content: str) -> list[str]:
    """frontmatter 필수 필드 검증"""
    issues = []
    if not content.startswith("---"):
        issues.append("frontmatter 없음")
        return issues

    fm_end = content.find("---", 3)
    if fm_end == -1:
        issues.append("frontmatter 닫힘 태그 없음")
        return issues

    fm = content[3:fm_end]
    required = ["layout", "title", "date", "lang", "permalink", "pair", "tags"]
    for field in required:
        if f"{field}:" not in fm:
            issues.append(f"frontmatter 누락: {field}")

    return issues


def check_today_in_one_line(content: str) -> list[str]:
    """Today in One Line 존재 + 길이"""
    issues = []
    match = re.search(r"## Today in One Line\s*\n+(.+?)(?:\n|$)", content)
    if not match:
        issues.append("Today in One Line 없음")
        return issues

    line = match.group(1).strip()
    if len(line) < 20:
        issues.append(f"Today in One Line 너무 짧음 ({len(line)}자)")
    if len(line) > 200:
        issues.append(f"Today in One Line 너무 길음 ({len(line)}자)")

    return issues


def check_sections(content: str) -> list[str]:
    """섹션 3개 + Why it matters + What's next + Source"""
    issues = []
    sections = re.findall(r"## \d+\.", content)
    if len(sections) < 3:
        issues.append(f"섹션 {len(sections)}개 (3개 필요)")

    # Why it matters
    wim_matches = re.findall(r"\*\*Why it matters:\*\*(.+?)(?:\n\n|\n-)", content, re.DOTALL)
    if len(wim_matches) == 0:
        # **Why it matters:** 없이 Why it matters: 로 된 경우도 체크
        wim_matches = re.findall(r"Why it matters:(.+?)(?:\n\n|\n-)", content, re.DOTALL)

    if len(wim_matches) < 3:
        issues.append(f"Why it matters {len(wim_matches)}개 (3개 필요)")

    for i, wim in enumerate(wim_matches):
        wim_len = len(wim.strip())
        if wim_len < 30:
            issues.append(f"Why it matters #{i+1} 너무 짧음 ({wim_len}자)")
        if wim_len > 400:
            issues.append(f"Why it matters #{i+1} 너무 길음 ({wim_len}자)")

    # What's next
    wn_count = content.count("What's next:")
    if wn_count < 3:
        issues.append(f"What's next {wn_count}개 (3개 필요)")

    # Source
    source_matches = re.findall(r"\*\*Source:\*\*", content)
    if len(source_matches) < 3:
        issues.append(f"Source {len(source_matches)}개 (3개 필요)")

    # Source URL
    urls = re.findall(r"\*\*Source:\*\*.*?\((https?://[^)]+)\)", content)
    for url in urls:
        if not url.startswith("http"):
            issues.append(f"Source URL 이상: {url[:50]}")

    return issues


def check_comments(content: str) -> list[str]:
    """## Comments 존재"""
    if "## Comments" not in content:
        return ["## Comments 섹션 없음"]
    return []


def check_source_type(content: str) -> list[str]:
    """source_type frontmatter"""
    if "source_type:" not in content:
        return ["source_type frontmatter 없음 (perplexity/gemini/chatgpt 중 하나)"]
    return []


# ── 장애 진단 ────────────────────────────────────────────────

def diagnose_dr(post_date: str) -> dict:
    """DR raw 파일 분석"""
    raw_file = TMP_DIR / f"deep-research-{post_date}.md"
    diag = {"raw_exists": False, "provider": "unknown", "fallback": False}

    if raw_file.exists():
        diag["raw_exists"] = True
        content = raw_file.read_text(encoding="utf-8")
        for line in content.split("\n")[:5]:
            if line.startswith("SOURCE:"):
                diag["provider"] = line.replace("SOURCE:", "").strip()
                break
        # Perplexity가 아니면 fallback 발생
        if diag["provider"] != "perplexity":
            diag["fallback"] = True

    return diag


# ── 자동 수리 ────────────────────────────────────────────────

def auto_fix(post_file: Path, issues: list[str]) -> list[str]:
    """수리 가능한 문제 자동 수리. 수리된 항목 반환."""
    content = post_file.read_text(encoding="utf-8")
    fixed = []

    # ## Comments 없으면 추가
    if "## Comments 섹션 없음" in issues:
        if "## Comments" not in content:
            content = content.rstrip() + "\n\n## Comments\n"
            fixed.append("## Comments 추가")

    # source_type 없으면 unknown 추가
    if "source_type frontmatter 없음" in issues:
        if "source_type:" not in content and content.startswith("---"):
            content = content.replace("---\n", "---\nsource_type: unknown\n", 1)
            fixed.append("source_type: unknown 추가")

    if fixed:
        post_file.write_text(content, encoding="utf-8")

    return fixed


# ── GitHub Issue 알림 ────────────────────────────────────────

def create_issue(post_date: str, issues: list[str], diag: dict):
    """검증 실패 시 GitHub Issue 생성"""
    title = f"[post-doctor] {post_date} 검증 실패 ({len(issues)}건)"

    body_lines = [
        f"## Daily Post 검증 결과 — {post_date}",
        "",
        f"**Provider**: {diag.get('provider', 'unknown')}",
        f"**Fallback 발생**: {'⚠️ YES' if diag.get('fallback') else '✅ NO'}",
        f"**Raw 파일**: {'✅ 존재' if diag.get('raw_exists') else '❌ 없음'}",
        "",
        "## 검증 실패 항목",
        "",
    ]
    for issue in issues:
        body_lines.append(f"- ❌ {issue}")

    body_lines.extend([
        "",
        "---",
        f"*자동 생성: post-doctor.py ({datetime.now().strftime('%Y-%m-%d %H:%M')} KST)*",
    ])

    body = "\n".join(body_lines)

    try:
        result = subprocess.run(
            ["gh", "issue", "create", "--repo", REPO,
             "--title", title, "--body", body,
             "--label", "post-doctor"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=30,
        )
        if result.returncode == 0:
            log(f"  [Issue] 생성 완료: {result.stdout.strip()}")
        else:
            log(f"  [Issue] 생성 실패: {result.stderr[:200]}")
            # label이 없으면 label 없이 재시도
            if "label" in result.stderr.lower():
                result = subprocess.run(
                    ["gh", "issue", "create", "--repo", REPO,
                     "--title", title, "--body", body],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=30,
                )
                if result.returncode == 0:
                    log(f"  [Issue] 재시도 성공: {result.stdout.strip()}")
    except Exception as e:
        log(f"  [Issue] 에러: {e}")


# ── 메인 ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--fix", action="store_true", help="자동 수리 활성화")
    parser.add_argument("--no-issue", action="store_true", help="GitHub Issue 생성 안 함")
    parser.add_argument("--batch", help="여러 날짜 검증 (YYYY-MM-DD,YYYY-MM-DD,...)")
    args = parser.parse_args()

    dates = [args.date]
    if args.batch:
        dates = [d.strip() for d in args.batch.split(",")]

    LOGS_DIR.mkdir(exist_ok=True)

    for post_date in dates:
        log(f"=== post-doctor ({post_date}) ===")

        # 포스트 파일 확인
        post_file = POSTS_DIR / f"{post_date}-daily-tech-review.md"
        if not post_file.exists():
            log(f"  [SKIP] 포스트 없음: {post_file.name}")
            if not args.no_issue:
                create_issue(post_date, ["포스트 파일 자체가 없음"], diagnose_dr(post_date))
            continue

        content = post_file.read_text(encoding="utf-8")

        # 검증 실행
        all_issues = []
        all_issues.extend(check_frontmatter(content))
        all_issues.extend(check_today_in_one_line(content))
        all_issues.extend(check_sections(content))
        all_issues.extend(check_comments(content))
        all_issues.extend(check_source_type(content))

        # 장애 진단
        diag = diagnose_dr(post_date)

        if diag["fallback"]:
            log(f"  [WARN] DR fallback 발생 — provider: {diag['provider']}")

        if not diag["raw_exists"]:
            log(f"  [WARN] DR raw 파일 없음")

        # 결과 출력
        if all_issues:
            log(f"  [FAIL] {len(all_issues)}건 실패:")
            for issue in all_issues:
                log(f"    - {issue}")

            # 자동 수리
            if args.fix:
                fixed = auto_fix(post_file, all_issues)
                if fixed:
                    log(f"  [FIX] {len(fixed)}건 수리:")
                    for f in fixed:
                        log(f"    - {f}")
                    # 수리된 항목 제거
                    remaining = [i for i in all_issues if not any(f in i for f in fixed)]
                    all_issues = remaining

            # GitHub Issue
            if all_issues and not args.no_issue:
                create_issue(post_date, all_issues, diag)
        else:
            log(f"  [OK] 모든 검증 통과 (provider: {diag['provider']})")

        # 로그 저장
        log_file = LOGS_DIR / f"post-doctor-{post_date}.log"
        log_data = {
            "date": post_date,
            "issues": all_issues,
            "diagnosis": diag,
            "timestamp": datetime.now().isoformat(),
        }
        log_file.write_text(json.dumps(log_data, ensure_ascii=False, indent=2), encoding="utf-8")

    log("=== post-doctor 완료 ===")


if __name__ == "__main__":
    main()
