#!/usr/bin/env python3
"""
run-all-pipelines.py — Tech Review 마스터 파이프라인

3개 파이프라인을 순차 실행:
  1. Daily Post   (DR → Claude CLI → Jekyll → push)
  2. YouTube      (fetch → Whisper/Codex → push)
  3. Twitter      (CDP fetch → Codex → push)

Task Scheduler: 매일 05:00 KST (1개 태스크로 통합)
  - "Run whether user is logged on or not" 불가 (CDP Chrome 필요)
  - "Run task as soon as possible after a scheduled start is missed" 필수
  - "Wake the computer to run this task" 권장
"""

import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
LOG_DIR = SCRIPT_DIR / "_logs"
LOG_DIR.mkdir(exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = LOG_DIR / f"master-{TODAY}.log"

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PYTHON = sys.executable


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def ensure_cdp_chrome():
    """CDP Chrome 실행 확인 — 미실행 시 자동 시작"""
    import urllib.request
    CDP_URL = "http://127.0.0.1:9222/json/version"
    CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    CHROME_PROFILE = r"C:\Users\pauls\.chrome-twitter-auto"

    try:
        urllib.request.urlopen(CDP_URL, timeout=3)
        log("[CDP] 연결 OK")
        return True
    except Exception:
        log("[CDP] Chrome 미실행 — 자동 시작 중...")
        subprocess.Popen(
            [CHROME_EXE, "--remote-debugging-port=9222",
             f"--user-data-dir={CHROME_PROFILE}", "--force-dark-mode",
             "--no-first-run", "--disable-popup-blocking"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for _ in range(15):
            time.sleep(2)
            try:
                urllib.request.urlopen(CDP_URL, timeout=3)
                log("[CDP] Chrome 자동 시작 완료")
                return True
            except Exception:
                pass
        log("[CDP] Chrome 시작 실패")
        return False


def run_step(name, cmd, timeout=3600):
    """단일 파이프라인 실행"""
    log(f"\n{'='*50}")
    log(f"[{name}] 시작")
    log(f"{'='*50}")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            cwd=str(BLOG_DIR), timeout=timeout,
        )
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                log(f"  {line}")
        if result.returncode != 0:
            log(f"[{name}] 실패 (exit {result.returncode})")
            if result.stderr:
                for line in result.stderr.strip().split("\n")[-5:]:
                    log(f"  ERR: {line}")
            return False
        log(f"[{name}] 완료")
        return True
    except subprocess.TimeoutExpired:
        log(f"[{name}] 타임아웃 ({timeout}초)")
        return False
    except Exception as e:
        log(f"[{name}] 오류: {e}")
        return False


LOCK_FILE = BLOG_DIR / "_tmp" / "master-pipeline.lock"


def acquire_lock():
    """중복 실행 방지. 이미 돌고 있으면 즉시 종료."""
    LOCK_FILE.parent.mkdir(exist_ok=True)
    if LOCK_FILE.exists():
        try:
            lock_data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            lock_pid = lock_data.get("pid", 0)
            # 프로세스 살아있는지 확인
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.OpenProcess(0x1000, False, lock_pid)  # PROCESS_QUERY_LIMITED_INFORMATION
            if handle:
                kernel32.CloseHandle(handle)
                log(f"[ABORT] 이미 실행 중 (PID {lock_pid}, 시작: {lock_data.get('started','')})")
                sys.exit(0)
        except Exception:
            pass  # lock 파일 손상 — 무시하고 진행
    LOCK_FILE.write_text(json.dumps({
        "pid": os.getpid(),
        "started": datetime.now().isoformat(),
    }), encoding="utf-8")


def release_lock():
    LOCK_FILE.unlink(missing_ok=True)


def main():
    acquire_lock()
    try:
        _run_main()
    finally:
        release_lock()


def _run_main():
    log(f"{'='*60}")
    log(f"=== Tech Review 마스터 파이프라인 ({TODAY}) ===")
    log(f"{'='*60}")

    # CDP Chrome 보장 (Daily DR + Twitter에 필요)
    if not ensure_cdp_chrome():
        log("[WARN] CDP 없이 진행 — DR/Twitter 실패 가능")

    # git pull (최신 상태)
    os.chdir(BLOG_DIR)
    os.system("git pull --rebase origin master")

    results = {}

    # 1. Daily Post v3 (free-sources: RSS/Reddit/HN → Claude Sonnet)
    results["daily"] = run_step(
        "Daily Post",
        [PYTHON, str(SCRIPT_DIR / "run-daily-v3.py"), TODAY],
        timeout=1800,
    )

    # 2. YouTube v3 (yt-dlp + Groq Whisper + Gemini Flash + Claude AP)
    results["youtube"] = run_step(
        "YouTube",
        [PYTHON, str(SCRIPT_DIR / "analyze-youtube-v3.py")],
        timeout=3600,
    )

    # 3. Twitter (fetch + Codex 병렬, 최대 90분)
    results["twitter"] = run_step(
        "Twitter",
        [PYTHON, str(SCRIPT_DIR / "run-twitter-pipeline.py")],
        timeout=5400,
    )

    # 결과 요약
    log(f"\n{'='*60}")
    log("=== 결과 요약 ===")
    for name, ok in results.items():
        status = "OK" if ok else "FAIL"
        log(f"  {name}: {status}")

    failed = [n for n, ok in results.items() if not ok]
    if failed:
        log(f"실패: {', '.join(failed)}")
    else:
        log("전체 성공")

    log(f"{'='*60}")


if __name__ == "__main__":
    main()
