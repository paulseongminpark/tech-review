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

import atexit, json, os, subprocess, sys, time, socket, threading
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

LOCK_MAX_AGE = 4 * 3600  # 4시간 이상 된 lock = stale


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # 로그 실패해도 파이프라인은 계속


def wait_for_network(timeout=120):
    """DNS가 응답할 때까지 대기. Modern Standby 웨이크 후 네트워크 지연 대응."""
    log("[NET] 네트워크 연결 확인 중...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3).close()
            log("[NET] 네트워크 OK")
            return True
        except OSError:
            time.sleep(5)
    log("[NET] 네트워크 연결 실패 — 타임아웃")
    return False


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
    """단일 파이프라인 실행 — 실시간 로깅"""
    log(f"\n{'='*50}")
    log(f"[{name}] 시작")
    log(f"{'='*50}")
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            cwd=str(BLOG_DIR), encoding="utf-8", errors="replace",
        )

        # 실시간으로 stdout 읽어서 로깅 (크래시 전 로그 보존)
        def _stream_output():
            try:
                for line in proc.stdout:
                    log(f"  {line.rstrip()}")
            except Exception:
                pass

        reader = threading.Thread(target=_stream_output, daemon=True)
        reader.start()
        proc.wait(timeout=timeout)
        reader.join(timeout=5)

        if proc.returncode != 0:
            log(f"[{name}] 실패 (exit {proc.returncode})")
            return False
        log(f"[{name}] 완료")
        return True
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)
        log(f"[{name}] 타임아웃 ({timeout}초)")
        return False
    except Exception as e:
        log(f"[{name}] 오류: {e}")
        try:
            proc.kill()
        except Exception:
            pass
        return False


LOCK_FILE = BLOG_DIR / "_tmp" / "master-pipeline.lock"


def acquire_lock():
    """중복 실행 방지. stale lock (4시간+) 자동 제거."""
    LOCK_FILE.parent.mkdir(exist_ok=True)
    if LOCK_FILE.exists():
        try:
            lock_data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            lock_pid = lock_data.get("pid", 0)
            lock_started = lock_data.get("started", "")

            # 타임스탬프 기반 만료 체크 (4시간 이상 = stale)
            if lock_started:
                lock_time = datetime.fromisoformat(lock_started)
                age_sec = (datetime.now() - lock_time).total_seconds()
                if age_sec > LOCK_MAX_AGE:
                    log(f"[LOCK] stale lock 제거 (PID {lock_pid}, {age_sec/3600:.1f}시간 전)")
                    LOCK_FILE.unlink(missing_ok=True)
                    # stale lock 제거 후 진행
                else:
                    # 프로세스 살아있는지 확인
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    handle = kernel32.OpenProcess(0x1000, False, lock_pid)
                    if handle:
                        kernel32.CloseHandle(handle)
                        log(f"[ABORT] 이미 실행 중 (PID {lock_pid}, 시작: {lock_started})")
                        sys.exit(0)
                    else:
                        log(f"[LOCK] dead lock 제거 (PID {lock_pid} 죽음)")
                        LOCK_FILE.unlink(missing_ok=True)
            else:
                LOCK_FILE.unlink(missing_ok=True)
        except Exception:
            LOCK_FILE.unlink(missing_ok=True)  # 손상된 lock 제거

    LOCK_FILE.write_text(json.dumps({
        "pid": os.getpid(),
        "started": datetime.now().isoformat(),
    }), encoding="utf-8")


def release_lock():
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def main():
    acquire_lock()
    atexit.register(release_lock)  # 비정상 종료 시에도 lock 정리 시도
    try:
        _run_main()
    finally:
        release_lock()


def _run_main():
    log(f"{'='*60}")
    log(f"=== Tech Review 마스터 파이프라인 ({TODAY}) ===")
    log(f"{'='*60}")

    # 네트워크 대기 (Modern Standby 웨이크 후 지연 대응)
    if not wait_for_network():
        log("[ABORT] 네트워크 없음 — 종료 (exit 1)")
        sys.exit(1)

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

    # 4. Health Check — 사고 패턴 자동 감지 (2026-04-20 추가)
    # 표시/분석 데이터 모순, hardcoded limit hit, front matter 래퍼 잔재 등을 즉시 감지.
    # — Why: 이전 사고들(4/5, 4/14, 4/20 front matter 래퍼 / 4/3~4/18 Twitter truncate / 4/17~4/20 마스터 거짓 OK)
    #         이 모두 사용자 점검 시에야 발견됨. 자동 감지로 사고 첫날에 알림.
    results["health"] = run_step(
        "Health Check",
        [PYTHON, str(SCRIPT_DIR / "health-check.py")],
        timeout=60,
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
        sys.exit(1)
    else:
        log("전체 성공")

    log(f"{'='*60}")


if __name__ == "__main__":
    main()
