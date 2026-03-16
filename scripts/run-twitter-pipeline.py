#!/usr/bin/env python3
"""
run-twitter-pipeline.py — Twitter 북마크 전체 자동화 파이프라인

1. CDP Chrome 연결 확인
2. fetch-twitter-pw.py → inbox/ 수집
3. add-bookmark.py → Codex 분석 (신규만)
4. build-sources-feed.js → portfolio sources.json 갱신
5. git commit + push

Task Scheduler: 매일 10:00 (TechReview-TwitterPipeline)
사전 조건: CDP Chrome 실행 중 (바탕화면 "Chrome - Twitter Auto")
"""

import json, os, subprocess, sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
INBOX_DIR = BLOG_DIR / "inbox"
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"
TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = BLOG_DIR / "_tmp" / f"twitter-pipeline-{TODAY}.log"

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_FILE.parent.mkdir(exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(cmd, **kwargs):
    """subprocess 실행 + 로그"""
    log(f"  실행: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(BLOG_DIR), timeout=kwargs.get("timeout", 600),
    )
    if result.stdout.strip():
        for line in result.stdout.strip().split("\n")[-5:]:
            log(f"    {line}")
    if result.returncode != 0 and result.stderr.strip():
        for line in result.stderr.strip().split("\n")[-3:]:
            log(f"    ERR: {line}")
    return result


def count_bookmarks():
    if not BOOKMARKS_JSON.exists():
        return 0
    with open(BOOKMARKS_JSON, encoding="utf-8") as f:
        return len(json.load(f))


def main():
    os.chdir(BLOG_DIR)
    log(f"=== Twitter Pipeline 시작 ({TODAY}) ===")

    # Step 1: CDP 연결 확인
    log("[1/4] CDP Chrome 연결 확인")
    import urllib.request
    try:
        urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=3)
        log("  CDP 연결 OK")
    except Exception:
        log("  CDP Chrome 미실행 — 파이프라인 중단")
        log("  바탕화면 'Chrome - Twitter Auto' 실행 후 재시도하세요")
        sys.exit(1)

    # Step 2: 북마크 수집
    log("[2/4] 북마크 수집 (fetch-twitter-pw.py)")
    r = run([sys.executable, str(SCRIPT_DIR / "fetch-twitter-pw.py")], timeout=300)
    if r.returncode != 0:
        log("  수집 실패 — 파이프라인 중단")
        sys.exit(1)

    inbox_file = INBOX_DIR / f"bookmarks-raw-{TODAY}.json"
    if not inbox_file.exists():
        log("  수집 파일 없음 — 파이프라인 중단")
        sys.exit(1)

    with open(inbox_file, encoding="utf-8") as f:
        fetched = len(json.load(f))
    log(f"  수집 완료: {fetched}개")

    # Step 3: Codex 분석 (신규만)
    log("[3/4] Codex 분석 (add-bookmark.py)")
    before = count_bookmarks()
    r = run(
        [sys.executable, str(SCRIPT_DIR / "add-bookmark.py"), str(inbox_file)],
        timeout=600,
    )
    after = count_bookmarks()
    added = after - before
    log(f"  신규 {added}개 추가 (총 {after}개)")

    if added == 0:
        log("  신규 없음 — sources 갱신 스킵")
        log("=== 파이프라인 완료 (변경 없음) ===")
        return

    # Step 4: sources.json 갱신 + git
    log("[4/4] sources.json 갱신 + git push")
    run(["node", str(SCRIPT_DIR / "build-sources-feed.js")])

    # add-bookmark.py가 이미 commit+push 하므로, sources.json만 추가 커밋
    run(["git", "add", "sources.json"])
    run(["git", "commit", "-m", f"[auto] sources.json 갱신 (twitter +{added})"])
    r = run(["git", "push"])
    if r.returncode != 0:
        log("  push 실패 — pull 후 재시도")
        run(["git", "pull", "--rebase"])
        run(["git", "push"])

    log(f"=== 파이프라인 완료 (+{added}개) ===")


if __name__ == "__main__":
    main()
