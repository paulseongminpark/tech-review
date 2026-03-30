#!/usr/bin/env python3
"""
verify-pipelines.py — 3개 파이프라인 단계별 진단

각 파이프라인의 스텝을 순서대로 추적해서 어디서 끊겼는지 정확히 찍어준다.
Claude Code가 이 출력만 보고 원인을 파악할 수 있어야 한다.

Usage:
  python verify-pipelines.py                    # 오늘, 전체
  python verify-pipelines.py --date 2026-03-31  # 특정 날짜
  python verify-pipelines.py --only daily       # 파이프라인 하나만
  python verify-pipelines.py --only youtube
  python verify-pipelines.py --only twitter
  python verify-pipelines.py --verbose          # 로그 원문 포함
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

VERBOSE = False
EXIT_CODE = 0


def header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def step(num, name, status, detail=""):
    """파이프라인 단계 출력. status: OK/WARN/FAIL/SKIP"""
    icons = {"OK": "\u2705", "WARN": "\u26a0\ufe0f ", "FAIL": "\u274c", "SKIP": "\u23ed\ufe0f "}
    icon = icons.get(status, "  ")
    line = f"  [{num}] {name}: {status}"
    if detail:
        line += f" — {detail}"
    print(f"  {icon} [{num}] {name}: {detail}" if detail else f"  {icon} [{num}] {name}")
    global EXIT_CODE
    if status == "FAIL":
        EXIT_CODE = 2
    elif status == "WARN" and EXIT_CODE < 1:
        EXIT_CODE = 1


def substep(msg):
    print(f"       {msg}")


def dump_log_section(log_lines, step_marker, next_marker=None):
    """로그에서 특정 Step 구간만 추출해서 출력"""
    if not VERBOSE or not log_lines:
        return
    capturing = False
    for line in log_lines:
        if step_marker in line:
            capturing = True
        elif next_marker and next_marker in line:
            capturing = False
        if capturing:
            print(f"       | {line.rstrip()[:100]}")


# ── 로그 로더 ────────────────────────────────────────────
def load_log(path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def find_in_log(lines, pattern):
    """로그에서 패턴 매칭되는 줄 반환"""
    if not lines:
        return []
    return [l for l in lines if re.search(pattern, l)]


# ══════════════════════════════════════════════════════════
#  DAILY POST 진단
# ══════════════════════════════════════════════════════════
def diagnose_daily(date):
    header(f"Daily Post 진단 ({date})")
    log_path = LOG_DIR / f"daily-v3-{date}.log"
    log = load_log(log_path)

    # Step 0: 실행 여부
    if log is None:
        step(0, "실행", "FAIL", f"로그 없음: {log_path.name}")
        substep("MasterPipeline이 실행되지 않았거나, Daily 단계 진입 전 실패")
        substep(f"확인: scripts/_logs/master-{date}.log")
        return
    step(0, "실행", "OK", f"로그 존재 ({len(log)}줄)")

    # Step 1: 소스 수집
    source_lines = find_in_log(log, r"수집 완료:|FAIL|건$")
    collected_match = find_in_log(log, r"수집 완료: (\d+)건")
    if collected_match:
        m = re.search(r"(\d+)건 from (\d+)개", collected_match[0])
        if m:
            items, sources = int(m.group(1)), int(m.group(2))
            if sources < 3:
                step(1, "소스 수집", "FAIL", f"{items}건 from {sources}개 소스 (최소 3)")
            elif sources < 8:
                step(1, "소스 수집", "WARN", f"{items}건 from {sources}개 소스")
            else:
                step(1, "소스 수집", "OK", f"{items}건 from {sources}개 소스")
    else:
        step(1, "소스 수집", "FAIL", "수집 완료 로그 없음")

    # 실패한 소스 상세
    failed_sources = find_in_log(log, r"FAIL")
    for fl in failed_sources:
        if "Step" not in fl and "FAIL" in fl:
            substep(f"실패: {fl.strip()[:80]}")
    dump_log_section(log, "[Step 1]", "[Step 2]")

    # Step 2: 선별
    selected_lines = find_in_log(log, r"선별 \d+건")
    if selected_lines:
        step(2, "선별", "OK", selected_lines[0].strip().split("]")[-1].strip()[:60])
    else:
        step(2, "선별", "SKIP", "로그에 선별 정보 없음")

    # Step 3: 본문 추출
    body_lines = find_in_log(log, r"→ \d+자")
    if body_lines:
        step(3, "본문 추출", "OK", f"{len(body_lines)}건 추출")
    else:
        step(3, "본문 추출", "SKIP")

    # Step 4: Claude Sonnet
    claude_ok = find_in_log(log, r"\[OK\].*자 \(attempt")
    claude_fail = find_in_log(log, r"\[FAIL\].*Claude|500자 미만")
    if claude_ok:
        m = re.search(r"(\d+)자 \(attempt (\d+)\)", claude_ok[0])
        if m:
            step(4, "Claude Sonnet 가공", "OK", f"{m.group(1)}자 (시도 {m.group(2)})")
    elif claude_fail:
        step(4, "Claude Sonnet 가공", "FAIL", claude_fail[0].strip()[:80])
        substep("원인: Claude CLI 응답 부족 또는 타임아웃")
        substep("확인: _tmp/prompt-{date}.txt (프롬프트), Claude CLI 인증 상태")
    else:
        step(4, "Claude Sonnet 가공", "SKIP")
    dump_log_section(log, "[Step 4]", "[Step 5]")

    # Step 5: 후처리
    post_ok = find_in_log(log, r"\[OK\] 후처리")
    if post_ok:
        step(5, "후처리", "OK")
    else:
        step(5, "후처리", "SKIP")

    # Step 6: 검증
    verify_lines = find_in_log(log, r"\[OK\].*|검증")
    step(6, "내부 검증", "OK" if verify_lines else "SKIP")

    # Step 7: 배포 (commit + push)
    commit_line = find_in_log(log, r"commit:")
    push_line = find_in_log(log, r"push:")
    push_fail = find_in_log(log, r"push 실패|rejected|\[FAIL\].*push")

    if commit_line:
        substep(f"commit: {commit_line[0].strip()[-60:]}")
    if push_fail:
        step(7, "배포 (push)", "FAIL", push_fail[0].strip()[:80])
        substep("원인: 다른 파이프라인이 먼저 push → rebase 필요")
        substep("확인: git log --oneline -5 (커밋 존재 여부)")
    elif push_line and "rejected" in push_line[0]:
        step(7, "배포 (push)", "FAIL", "push rejected")
    elif push_line:
        step(7, "배포 (push)", "OK")
    else:
        step(7, "배포 (push)", "SKIP")

    # 결과물 검증
    post_file = POSTS_DIR / f"{date}-daily-tech-review.md"
    if post_file.exists():
        content = post_file.read_text(encoding="utf-8")
        step("R", "결과물", "OK", f"{post_file.name} ({len(content)}자)")
    else:
        step("R", "결과물", "FAIL", f"{post_file.name} 없음")
        substep("Step 4(Claude) 또는 Step 5(후처리)에서 실패했을 가능성")

    # 최종 상태
    last = log[-1] if log else ""
    if "FAIL" in last:
        substep(f"최종: {last.strip()}")
    elif "완료" in last:
        substep(f"최종: {last.strip()}")


# ══════════════════════════════════════════════════════════
#  YOUTUBE 진단
# ══════════════════════════════════════════════════════════
def diagnose_youtube(date):
    header(f"YouTube 진단 ({date})")
    log_path = LOG_DIR / f"youtube-v3-{date}.log"
    log = load_log(log_path)

    if log is None:
        step(0, "실행", "FAIL", f"로그 없음: {log_path.name}")
        substep("MasterPipeline이 실행되지 않았거나, YouTube 단계 진입 전 실패")
        return
    step(0, "실행", "OK", f"로그 존재 ({len(log)}줄)")

    # Step 1: 신규 감지
    new_match = find_in_log(log, r"신규: \d+건")
    existing_match = find_in_log(log, r"기존: \d+건")
    if new_match:
        m = re.search(r"(\d+)건", new_match[0])
        count = int(m.group(1)) if m else 0
        if count == 0:
            step(1, "신규 감지", "OK", "신규 없음 — 정상 종료")
            return
        step(1, "신규 감지", "OK", f"{count}건")
    else:
        step(1, "신규 감지", "FAIL", "감지 로그 없음")
        substep("원인: yt-dlp 실행 실패 또는 플레이리스트 접근 불가")
        substep("확인: yt-dlp --version, 플레이리스트 URL 유효성")
        return

    if existing_match:
        substep(f"기존: {existing_match[0].strip().split(']')[-1].strip()}")

    # 영상별 진단
    video_blocks = re.split(r"--- \[(\d+/\d+)\] (.+?) ---", "\n".join(log))
    # video_blocks: [preamble, "1/2", "title1", block1, "2/2", "title2", block2, ...]
    i = 1
    while i < len(video_blocks) - 1:
        num = video_blocks[i]
        title = video_blocks[i+1].strip()[:45]
        block = video_blocks[i+2] if i+2 < len(video_blocks) else ""
        block_lines = block.splitlines()
        i += 3

        print(f"\n  --- [{num}] {title} ---")

        # S1: Transcript
        if "yt-dlp:" in block and "자" in block:
            tr_match = re.search(r"yt-dlp: (\d+)자", block)
            if tr_match:
                step("S1", "Transcript (yt-dlp)", "OK", f"{tr_match.group(1)}자")
            else:
                groq_match = re.search(r"\[Groq\] 완료: (\d+)자", block)
                if groq_match:
                    step("S1", "Transcript (Groq)", "OK", f"{groq_match.group(1)}자")
                else:
                    step("S1", "Transcript", "FAIL", "추출 실패")
                    substep("원인: yt-dlp 자막 없음 + Groq Whisper도 실패")
                    substep("확인: 영상 공개 상태, Groq API 키, 오디오 길이")
                    continue
        elif "Groq" in block:
            groq_match = re.search(r"\[Groq\] 완료: (\d+)자", block)
            if groq_match:
                step("S1", "Transcript (Groq fallback)", "OK", f"{groq_match.group(1)}자")
            elif "Transcript 추출 실패" in block:
                step("S1", "Transcript", "FAIL", "yt-dlp + Groq 모두 실패")
                substep("원인: 자막 없음 + 오디오 추출/Whisper 실패")
                continue
        elif "자막 없음" in block and "Transcript 추출 실패" in block:
            step("S1", "Transcript", "FAIL", "추출 불가")
            continue
        else:
            step("S1", "Transcript", "SKIP")

        # S2: 구조화 (Codex gpt-5.4)
        sec_match = re.search(r"sections: (\d+)개", block)
        if sec_match:
            cnt = int(sec_match.group(1))
            step("S2", "구조화 (Codex gpt-5.4)", "OK" if cnt >= 6 else "WARN", f"{cnt}개 섹션")
        elif "구조화 실패" in block:
            step("S2", "구조화 (Codex gpt-5.4)", "FAIL", "Codex 응답 없음 또는 JSON 파싱 실패")
            substep("원인: Codex CLI 인증 만료, 타임아웃, 또는 모델 응답 형식")
            substep("확인: codex.cmd exec -m gpt-5.4 'test' --full-auto")
            # 구조화 실패 → 이후 스텝 불가
            codex_fail = [l for l in block_lines if "구조화" in l and ("실패" in l or "FAIL" in l)]
            for cf in codex_fail:
                substep(f"로그: {cf.strip()[:80]}")
            continue
        else:
            step("S2", "구조화", "SKIP")

        # S3: Apply Points (Claude Sonnet)
        ap_ok = re.search(r"\[AP\] L(\d)", block)
        ap_fail = re.search(r"\[AP\] 실패: (.+)", block)
        ap_cli_fail = re.search(r"\[AP\] CLI 실패.+?: (.+)", block)
        ap_empty = "[AP] 실패: 빈 응답" in block

        if ap_ok:
            step("S3", "Apply Points (Claude)", "OK", f"Level {ap_ok.group(1)}")
        elif ap_cli_fail:
            step("S3", "Apply Points (Claude)", "FAIL", f"CLI 에러: {ap_cli_fail.group(1)[:60]}")
            substep("원인: Claude CLI 실행 실패 (인증, MCP 서버, 타임아웃)")
            substep("확인: claude -p --model claude-sonnet-4-6 'test'")
        elif ap_empty:
            step("S3", "Apply Points (Claude)", "FAIL", "빈 응답")
            substep("원인: Claude CLI가 빈 stdout 반환")
            substep("확인: --output-format json이 wrapper를 반환하는지")
        elif ap_fail:
            err = ap_fail.group(1)[:60]
            step("S3", "Apply Points (Claude)", "FAIL", err)
            if "Expecting value" in err:
                substep("원인: Claude 응답이 JSON이 아님 (자연어 텍스트 또는 에러 메시지)")
                # raw 로그 있으면 표시
                raw_lines = [l for l in block_lines if "[AP] raw:" in l]
                for rl in raw_lines:
                    substep(f"응답: {rl.strip()[:100]}")
            substep("확인: _tmp/ 에 AP 디버그 로그 확인")
        else:
            step("S3", "Apply Points", "WARN", "AP 관련 로그 없음")

        # S4: 번역
        tr_ok = re.search(r"\[번역\] (\d+)자", block)
        tr_skip = "이미 한국어" in block
        tr_fail = re.search(r"\[번역\] 실패: (.+)", block)

        if tr_ok:
            step("S4", "번역 (gpt-4.1-mini)", "OK", f"{tr_ok.group(1)}자")
        elif tr_skip:
            step("S4", "번역", "OK", "이미 한국어 — 스킵")
        elif tr_fail:
            step("S4", "번역 (gpt-4.1-mini)", "FAIL", tr_fail.group(1)[:60])
            substep("원인: OpenAI API 실패 (크레딧, 타임아웃, 키)")
            substep("확인: OPENAI_API_KEY 유효성, 무료 토큰 잔여량")
        else:
            step("S4", "번역", "SKIP")

    # 배포
    push_lines = find_in_log(log, r"push:|commit:")
    push_fail = find_in_log(log, r"FAIL|rejected")
    if find_in_log(log, r"push:.*master"):
        step(7, "배포 (push)", "OK")
    elif push_fail:
        step(7, "배포 (push)", "FAIL", push_fail[-1].strip()[:60])
    else:
        step(7, "배포", "SKIP")

    # 결과물
    yt_file = SOURCES_DIR / f"youtube-{date}.json"
    if yt_file.exists():
        try:
            data = json.loads(yt_file.read_text(encoding="utf-8"))
            today = [v for v in data if v.get("fetched_at") == date]
            step("R", "결과물", "OK", f"{yt_file.name} — 오늘 {len(today)}건 / 전체 {len(data)}건")
        except Exception:
            step("R", "결과물", "FAIL", "JSON 파싱 실패")
    else:
        step("R", "결과물", "WARN", "데이터 파일 없음 (신규 없었으면 정상)")


# ══════════════════════════════════════════════════════════
#  TWITTER 진단
# ══════════════════════════════════════════════════════════
def diagnose_twitter(date):
    header(f"Twitter 진단 ({date})")
    log_path = TMP / f"twitter-pipeline-{date}.log"
    log = load_log(log_path)

    if log is None:
        step(0, "실행", "FAIL", f"로그 없음: {log_path.name}")
        substep("MasterPipeline이 실행되지 않았거나, Twitter 단계 진입 전 실패")
        return
    step(0, "실행", "OK", f"로그 존재 ({len(log)}줄)")

    # Step 1: CDP Chrome
    cdp_ok = find_in_log(log, r"CDP 연결 OK|CDP Chrome 자동 시작 완료")
    cdp_fail = find_in_log(log, r"CDP Chrome 시작 실패|CDP.*실패")
    if cdp_ok:
        step(1, "CDP Chrome", "OK")
    elif cdp_fail:
        step(1, "CDP Chrome", "FAIL", "Chrome 연결/시작 실패")
        substep("원인: Chrome 프로세스 없음 + 자동 시작 실패")
        substep("확인: 'Chrome - Twitter Auto' 바탕화면 바로가기, 포트 9222")
        substep("수동: chrome.exe --remote-debugging-port=9222 --user-data-dir=...")
        return
    else:
        step(1, "CDP Chrome", "SKIP")

    # Step 2: 북마크 수집
    fetch_ok = find_in_log(log, r"수집 완료: \d+개")
    fetch_fail = find_in_log(log, r"수집 실패|수집 파일 없음")
    if fetch_ok:
        m = re.search(r"(\d+)개", fetch_ok[0])
        step(2, "북마크 수집", "OK", f"{m.group(1)}개" if m else "")
    elif fetch_fail:
        step(2, "북마크 수집", "FAIL", fetch_fail[0].strip()[:60])
        substep("원인: fetch-twitter-pw.py 실패 (로그인 만료, DOM 변경, 타임아웃)")
        substep("확인: CDP Chrome에서 수동으로 twitter.com/i/bookmarks 접근 가능한지")
        return
    else:
        step(2, "북마크 수집", "SKIP")

    # Step 3: 분석
    analysis_ok = find_in_log(log, r"신규 \d+개 추가")
    analysis_zero = find_in_log(log, r"신규 없음|변경 없음")
    if analysis_ok:
        m = re.search(r"신규 (\d+)개 추가 \(총 (\d+)개\)", analysis_ok[0])
        if m:
            step(3, "분석 (OpenAI + Claude WIM)", "OK", f"+{m.group(1)}개 (총 {m.group(2)})")
    elif analysis_zero:
        step(3, "분석", "OK", "신규 없음 — 정상 종료")
        return
    else:
        step(3, "분석", "SKIP")

    # Step 4: sources.json + push
    sources_ok = find_in_log(log, r"sources\.json 생성 완료")
    push_ok = find_in_log(log, r"파이프라인 완료")
    push_fail = find_in_log(log, r"push.*실패|\[FAIL\]")

    if sources_ok:
        substep(f"sources.json: {sources_ok[0].strip().split(']')[-1].strip()[:60]}")

    pull_fail = find_in_log(log, r"cannot pull|unstaged changes|pull.*실패")
    if pull_fail:
        step(4, "git pull --rebase", "WARN", pull_fail[0].strip()[-60:])
        substep("원인: 커밋 전에 pull 시도 → unstaged changes 에러")

    if push_fail:
        step(5, "배포 (push)", "FAIL", push_fail[0].strip()[:60])
    elif push_ok:
        step(5, "배포 (push)", "OK")
    else:
        step(5, "배포", "SKIP")

    # 데이터 무결성
    bm_file = DATA_DIR / "bookmarks.json"
    if bm_file.exists():
        try:
            bms = json.loads(bm_file.read_text(encoding="utf-8"))
            error_phrases = ["credit balance", "rate limit", "unauthorized", "api key"]
            broken = [b["id"] for b in bms if any(e in b.get("why_it_matters","").lower() for e in error_phrases)]
            no_wim = [b["id"] for b in bms if not b.get("why_it_matters") and b.get("added_at","") >= "2026-03-15"]

            if broken:
                step("D", "데이터 무결성", "FAIL", f"에러 메시지 WIM {len(broken)}개: {', '.join(broken[:5])}")
                substep("원인: Claude CLI에 만료 ANTHROPIC_API_KEY 전달, 또는 OpenAI 크레딧 부족")
                substep("수정: python scripts/reprocess-bookmarks.py")
            elif no_wim:
                step("D", "데이터 무결성", "WARN", f"WIM 없는 북마크 {len(no_wim)}개")
            else:
                step("D", "데이터 무결성", "OK", f"전체 {len(bms)}개 정상")
        except Exception as e:
            step("D", "데이터 무결성", "FAIL", f"bookmarks.json 파싱 실패: {e}")


# ══════════════════════════════════════════════════════════
#  MASTER 진단
# ══════════════════════════════════════════════════════════
def diagnose_master(date):
    header(f"Master Pipeline 진단 ({date})")
    log_path = LOG_DIR / f"master-{date}.log"
    log = load_log(log_path)

    if log is None:
        step(0, "실행", "FAIL", "마스터 로그 없음")
        substep("Task Scheduler 'TechReview-MasterPipeline' 미실행")
        substep("확인:")
        substep("  1. 컴퓨터 절전 상태였는지 (WakeToRun=True이므로 깨워야 함)")
        substep("  2. 로그인 상태였는지 (LogonType=Interactive)")
        substep("  3. PowerShell: Get-ScheduledTask -TaskName 'TechReview-MasterPipeline'")
        substep("  4. 이벤트 뷰어: TaskScheduler Operational 로그")
        return

    step(0, "실행", "OK", f"로그 존재 ({len(log)}줄)")

    # CDP Chrome
    cdp_ok = find_in_log(log, r"\[CDP\] 연결 OK|\[CDP\] Chrome 자동 시작")
    cdp_fail = find_in_log(log, r"\[CDP\] Chrome 시작 실패")
    if cdp_ok:
        step(1, "CDP Chrome", "OK")
    elif cdp_fail:
        step(1, "CDP Chrome", "WARN", "시작 실패 — Twitter 영향")

    # 각 파이프라인 결과
    for name, label in [("Daily Post", "daily"), ("YouTube", "youtube"), ("Twitter", "twitter")]:
        ok_lines = find_in_log(log, rf"\[{name}\] 완료")
        fail_lines = find_in_log(log, rf"\[{name}\] 실패")
        timeout_lines = find_in_log(log, rf"\[{name}\] 타임아웃")

        if ok_lines:
            step(label, name, "OK")
        elif fail_lines:
            step(label, name, "FAIL", fail_lines[0].strip()[-60:])
            substep(f"상세: scripts/_logs/{label}-v3-{date}.log 또는 _tmp/ 확인")
        elif timeout_lines:
            step(label, name, "FAIL", "타임아웃")
        else:
            step(label, name, "SKIP", "결과 로그 없음")

    # 최종
    last = log[-1] if log else ""
    substep(f"최종: {last.strip()[:80]}")


# ══════════════════════════════════════════════════════════
#  배포 상태
# ══════════════════════════════════════════════════════════
def diagnose_deploy(date):
    header(f"배포 상태 ({date})")

    # git 상태
    try:
        r = subprocess.run(
            ["git", "diff", "origin/master..HEAD", "--stat"],
            capture_output=True, text=True, encoding="utf-8", cwd=str(BLOG_DIR), timeout=10,
        )
        if r.stdout.strip():
            step(1, "git sync", "FAIL", "미푸시 커밋 있음")
            substep(r.stdout.strip()[:100])
            substep("수동: cd blog && git push")
        else:
            step(1, "git sync", "OK", "origin/master 동기화")
    except Exception:
        step(1, "git sync", "WARN", "확인 불가")

    # GitHub Pages
    url = f"https://paulseongminpark.github.io/tech-review/ko/{date.replace('-','/')}/daily-tech-review/"
    try:
        req = Request(url, headers={"User-Agent": "TechReview-Verify/1.0"})
        resp = urlopen(req, timeout=10)
        step(2, "GitHub Pages", "OK", f"HTTP {resp.status}")
    except URLError as e:
        step(2, "GitHub Pages", "WARN", f"접근 불가 ({e.reason})")
        substep("배포 지연 가능 (push 후 1-2분 소요)")
        substep("확인: https://github.com/paulseongminpark/tech-review/actions")
    except Exception as e:
        step(2, "GitHub Pages", "WARN", str(e)[:60])


# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════
def main():
    global VERBOSE

    parser = argparse.ArgumentParser(description="Tech Review 파이프라인 단계별 진단")
    parser.add_argument("--date", default=datetime.now(KST).strftime("%Y-%m-%d"))
    parser.add_argument("--only", choices=["daily", "youtube", "twitter", "master", "deploy"])
    parser.add_argument("--verbose", "-v", action="store_true", help="로그 원문 포함")
    args = parser.parse_args()

    VERBOSE = args.verbose
    date = args.date

    print(f"\n  Tech Review Pipeline Diagnosis — {date}")
    print(f"  {'='*50}")

    if args.only:
        {"master": diagnose_master, "daily": diagnose_daily, "youtube": diagnose_youtube,
         "twitter": diagnose_twitter, "deploy": diagnose_deploy}[args.only](date)
    else:
        diagnose_master(date)
        diagnose_daily(date)
        diagnose_youtube(date)
        diagnose_twitter(date)
        diagnose_deploy(date)

    # 요약
    print(f"\n{'='*60}")
    if EXIT_CODE == 0:
        print("  결과: ALL PASS")
    elif EXIT_CODE == 1:
        print("  결과: WARN 있음 (치명적 아님)")
    else:
        print("  결과: FAIL 있음 — 위 진단 참조")
    print(f"{'='*60}")

    sys.exit(EXIT_CODE)


if __name__ == "__main__":
    main()
