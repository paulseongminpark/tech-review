#!/usr/bin/env python3
"""
verify-pipelines.py — 3개 파이프라인 통합 검증

Usage:
  python verify-pipelines.py                  # 오늘 날짜
  python verify-pipelines.py --date 2026-03-31
  python verify-pipelines.py --date 2026-03-31 --fix  # 실패 항목 자동 재실행

검증 항목:
  [Daily]   포스트 존재 + frontmatter + 구조 + 분량 + push 여부
  [YouTube] 데이터 존재 + sections + AP + transcript + 번역
  [Twitter] bookmarks.json 무결성 + sources.json + WIM 정상
  [Deploy]  GitHub Pages 배포 상태 (HTTP 200)

종료 코드: 0=전체 통과, 1=경고 있음, 2=실패 있음
"""

import json, os, re, sys, argparse, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
POSTS_DIR = BLOG_DIR / "_posts" / "ko"
DATA_DIR = BLOG_DIR / "_data"
SOURCES_DIR = DATA_DIR / "sources"
LOG_DIR = SCRIPT_DIR / "_logs"
TMP = BLOG_DIR / "_tmp"

KST = timezone(timedelta(hours=9))

# ── 결과 집계 ────────────────────────────────────────────
PASS = []
WARN = []
FAIL = []


def ok(pipeline, msg):
    PASS.append(f"[{pipeline}] {msg}")
    print(f"  \u2705 {msg}")


def warn(pipeline, msg):
    WARN.append(f"[{pipeline}] {msg}")
    print(f"  \u26a0\ufe0f  {msg}")


def fail(pipeline, msg):
    FAIL.append(f"[{pipeline}] {msg}")
    print(f"  \u274c {msg}")


# ── 로그 파싱 ────────────────────────────────────────────
def parse_log(path):
    """로그 파일에서 FAIL/WARN/OK 줄 추출"""
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return {
        "lines": lines,
        "fails": [l for l in lines if "FAIL" in l or "실패" in l],
        "warns": [l for l in lines if "WARN" in l],
        "last": lines[-1] if lines else "",
    }


# ── Daily Post 검증 ──────────────────────────────────────
def verify_daily(date):
    print(f"\n[Daily Post] {date}")
    post_file = POSTS_DIR / f"{date}-daily-tech-review.md"

    # 1. 파일 존재
    if not post_file.exists():
        fail("Daily", f"포스트 파일 없음: {post_file.name}")
        return
    ok("Daily", "포스트 파일 존재")

    content = post_file.read_text(encoding="utf-8")

    # 2. 분량
    if len(content) < 500:
        fail("Daily", f"분량 부족: {len(content)}자 (최소 500)")
    else:
        ok("Daily", f"분량 OK: {len(content)}자")

    # 3. frontmatter
    fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        fail("Daily", "frontmatter 없음")
    else:
        fm = fm_match.group(1)
        for field in ["layout", "title", "date", "lang", "permalink", "tags", "source_type"]:
            if field not in fm:
                fail("Daily", f"frontmatter 누락: {field}")
        if f"date: {date}" not in fm:
            warn("Daily", f"날짜 불일치: frontmatter date ≠ {date}")
        else:
            ok("Daily", "frontmatter 정상")

    # 4. 구조
    if "## Today in One Line" not in content:
        fail("Daily", "Today in One Line 누락")
    else:
        ok("Daily", "Today in One Line 존재")

    sections = re.findall(r"^## \d+\.", content, re.MULTILINE)
    if len(sections) < 3:
        fail("Daily", f"섹션 {len(sections)}개 (최소 3)")
    else:
        ok("Daily", f"섹션 {len(sections)}개")

    wim_count = len(re.findall(r"\*\*Why it matters", content))
    if wim_count < 3:
        warn("Daily", f"Why it matters {wim_count}개 (기대 3)")
    else:
        ok("Daily", f"Why it matters {wim_count}개")

    source_count = len(re.findall(r"\*\*Source:\*\*.*https?://", content))
    if source_count < 3:
        warn("Daily", f"Source URL {source_count}개 (기대 3)")
    else:
        ok("Daily", f"Source URL {source_count}개")

    # 5. sections 데이터
    sections_dir = DATA_DIR / "sections"
    section_files = list(sections_dir.glob(f"{date}-*.json")) if sections_dir.exists() else []
    if not section_files:
        warn("Daily", "sections JSON 없음")
    else:
        ok("Daily", f"sections JSON {len(section_files)}개")

    # 6. 로그
    log = parse_log(LOG_DIR / f"daily-v3-{date}.log")
    if log is None:
        warn("Daily", "실행 로그 없음")
    elif log["fails"]:
        for f_line in log["fails"][:3]:
            warn("Daily", f"로그: {f_line.strip()[:80]}")
    else:
        ok("Daily", "로그 에러 없음")


# ── YouTube 검증 ─────────────────────────────────────────
def verify_youtube(date):
    print(f"\n[YouTube] {date}")
    yt_file = SOURCES_DIR / f"youtube-{date}.json"

    # 1. 파일 존재
    if not yt_file.exists():
        # 신규 영상 없으면 파일 미생성 — 정상
        warn("YouTube", f"데이터 파일 없음 (신규 영상 없을 수 있음)")
        return

    try:
        data = json.loads(yt_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        fail("YouTube", "JSON 파싱 실패")
        return

    if not data:
        warn("YouTube", "빈 데이터")
        return

    ok("YouTube", f"데이터 파일 존재: {len(data)}건")

    # 오늘 추가된 것만 검증
    today_videos = [v for v in data if v.get("fetched_at") == date]
    if not today_videos:
        warn("YouTube", "오늘 추가된 영상 없음")
        return

    for v in today_videos:
        title = v.get("title", "?")[:40]
        summary = v.get("summary", {})

        # transcript
        tr_len = len(v.get("transcript", ""))
        if tr_len < 500:
            fail("YouTube", f"[{title}] transcript {tr_len}자 (최소 500)")
        else:
            ok("YouTube", f"[{title}] transcript {tr_len}자")

        # sections
        sec_count = len(summary.get("sections", []))
        if sec_count < 6:
            warn("YouTube", f"[{title}] sections {sec_count}개 (기대 6+)")
        else:
            ok("YouTube", f"[{title}] sections {sec_count}개")

        # key_takeaways
        kt_count = len(summary.get("key_takeaways", []))
        if kt_count < 3:
            warn("YouTube", f"[{title}] key_takeaways {kt_count}개")
        else:
            ok("YouTube", f"[{title}] key_takeaways {kt_count}개")

        # apply_points
        if "apply_points" not in summary or not summary["apply_points"]:
            warn("YouTube", f"[{title}] apply_points 누락")
        else:
            ap = summary["apply_points"]
            ok("YouTube", f"[{title}] AP L{ap.get('level','?')}")

        # 번역
        tr_ko = v.get("transcript_ko", "")
        if not tr_ko:
            warn("YouTube", f"[{title}] 한국어 번역 없음")
        else:
            ok("YouTube", f"[{title}] 번역 {len(tr_ko)}자")

    # 로그
    log = parse_log(LOG_DIR / f"youtube-v3-{date}.log")
    if log is None:
        warn("YouTube", "실행 로그 없음")
    elif log["fails"]:
        for f_line in log["fails"][:3]:
            warn("YouTube", f"로그: {f_line.strip()[:80]}")


# ── Twitter 검증 ─────────────────────────────────────────
def verify_twitter(date):
    print(f"\n[Twitter] {date}")
    bm_file = DATA_DIR / "bookmarks.json"

    # 1. bookmarks.json 존재 + 유효
    if not bm_file.exists():
        fail("Twitter", "bookmarks.json 없음")
        return

    try:
        bookmarks = json.loads(bm_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        fail("Twitter", "bookmarks.json JSON 파싱 실패")
        return

    ok("Twitter", f"bookmarks.json: {len(bookmarks)}개")

    # 2. 깨진 북마크 확인
    error_phrases = ["credit balance", "rate limit", "unauthorized", "api key", "error"]
    broken = []
    for bm in bookmarks:
        wim = bm.get("why_it_matters", "")
        if any(err in wim.lower() for err in error_phrases):
            broken.append(bm.get("id", "?"))
        elif not wim and bm.get("added_at", "") >= "2026-03-15":  # 최근 것만
            broken.append(f"{bm.get('id','?')} (WIM 없음)")

    if broken:
        fail("Twitter", f"깨진 북마크 {len(broken)}개: {', '.join(broken[:5])}")
    else:
        ok("Twitter", "북마크 무결성 OK")

    # 3. category 비어있는 것
    empty_cat = [bm["id"] for bm in bookmarks if not bm.get("category") and bm.get("added_at", "") >= "2026-03-15"]
    if empty_cat:
        warn("Twitter", f"category 비어있음 {len(empty_cat)}개")

    # 4. sources.json
    sources_file = BLOG_DIR / "sources.json"
    if not sources_file.exists():
        fail("Twitter", "sources.json 없음")
    else:
        try:
            sources = json.loads(sources_file.read_text(encoding="utf-8"))
            if isinstance(sources, dict):
                twitter_items = sources.get("twitter", [])
            else:
                twitter_items = [s for s in sources if s.get("source_type") == "twitter"]
            ok("Twitter", f"sources.json: twitter {len(twitter_items)}개")
        except Exception:
            fail("Twitter", "sources.json 파싱 실패")

    # 5. 오늘 추가된 북마크
    today_bm = [bm for bm in bookmarks if bm.get("added_at") == date]
    if today_bm:
        ok("Twitter", f"오늘 추가: {len(today_bm)}개")
    else:
        warn("Twitter", "오늘 추가된 북마크 없음 (북마크 안 했을 수 있음)")

    # 6. 로그
    log = parse_log(TMP / f"twitter-pipeline-{date}.log")
    if log is None:
        warn("Twitter", "실행 로그 없음")
    elif log["fails"]:
        for f_line in log["fails"][:3]:
            warn("Twitter", f"로그: {f_line.strip()[:80]}")


# ── 배포 검증 ────────────────────────────────────────────
def verify_deploy(date):
    print(f"\n[Deploy] {date}")
    url = f"https://paulseongminpark.github.io/tech-review/ko/{date.replace('-','/')}/daily-tech-review/"
    try:
        req = Request(url, headers={"User-Agent": "TechReview-Verify/1.0"})
        resp = urlopen(req, timeout=10)
        if resp.status == 200:
            ok("Deploy", f"GitHub Pages 200 OK")
        else:
            warn("Deploy", f"HTTP {resp.status}")
    except URLError as e:
        warn("Deploy", f"접근 불가: {e.reason}")
    except Exception as e:
        warn("Deploy", f"확인 실패: {e}")


# ── 마스터 로그 검증 ─────────────────────────────────────
def verify_master_log(date):
    print(f"\n[Master] {date}")
    log = parse_log(LOG_DIR / f"master-{date}.log")
    if log is None:
        warn("Master", "마스터 로그 없음 (MasterPipeline 미실행?)")
        return

    # 결과 요약 줄 찾기
    for line in log["lines"]:
        if "daily:" in line.lower() or "youtube:" in line.lower() or "twitter:" in line.lower():
            if "FAIL" in line:
                fail("Master", line.strip()[:80])
            elif "OK" in line:
                ok("Master", line.strip()[:80])

    if log["fails"]:
        for f_line in log["fails"][:3]:
            fail("Master", f"로그: {f_line.strip()[:80]}")
    else:
        ok("Master", "마스터 로그 에러 없음")


# ── git push 검증 ────────────────────────────────────────
def verify_git(date):
    print(f"\n[Git] {date}")
    try:
        r = subprocess.run(
            ["git", "log", "--oneline", "--since", f"{date}T00:00:00", "--until", f"{date}T23:59:59"],
            capture_output=True, text=True, encoding="utf-8", cwd=str(BLOG_DIR), timeout=10,
        )
        commits = [l for l in r.stdout.strip().splitlines() if l]
        if commits:
            ok("Git", f"오늘 커밋 {len(commits)}개")
            for c in commits[:5]:
                print(f"       {c}")
        else:
            warn("Git", "오늘 커밋 없음")

        # unpushed 확인
        r2 = subprocess.run(
            ["git", "diff", "origin/master..HEAD", "--stat"],
            capture_output=True, text=True, encoding="utf-8", cwd=str(BLOG_DIR), timeout=10,
        )
        if r2.stdout.strip():
            fail("Git", f"미푸시 커밋 있음: {r2.stdout.strip()[:80]}")
        else:
            ok("Git", "origin/master 동기화 완료")
    except Exception as e:
        warn("Git", f"git 확인 실패: {e}")


# ── 요약 ─────────────────────────────────────────────────
def print_summary():
    print(f"\n{'='*60}")
    print(f"=== 검증 결과 요약 ===")
    print(f"{'='*60}")
    print(f"  PASS: {len(PASS)}  |  WARN: {len(WARN)}  |  FAIL: {len(FAIL)}")
    print()

    if FAIL:
        print("[FAIL]")
        for f in FAIL:
            print(f"  {f}")
        print()

    if WARN:
        print("[WARN]")
        for w in WARN:
            print(f"  {w}")
        print()

    if not FAIL and not WARN:
        print("ALL PASS")

    return 2 if FAIL else (1 if WARN else 0)


# ── main ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Tech Review 파이프라인 통합 검증")
    parser.add_argument("--date", default=datetime.now(KST).strftime("%Y-%m-%d"),
                        help="검증 대상 날짜 (YYYY-MM-DD)")
    args = parser.parse_args()
    date = args.date

    print(f"{'='*60}")
    print(f"=== Tech Review Pipeline Verify ({date}) ===")
    print(f"{'='*60}")

    verify_master_log(date)
    verify_daily(date)
    verify_youtube(date)
    verify_twitter(date)
    verify_git(date)
    verify_deploy(date)

    exit_code = print_summary()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
