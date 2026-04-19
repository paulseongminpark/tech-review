#!/usr/bin/env python3
"""
analyze-youtube-v3.py — YouTube 파이프라인 v3

Stage 1: yt-dlp 자막(1차) → Groq Whisper(2차) → transcript
Stage 2: Codex CLI gpt-5.4 → 구조화 (structurize)
Stage 3: Claude Sonnet + recall() → apply_points 5W1H
Stage 4: Claude 4.5 Sonnet (OAuth) → 한글 번역
Stage 5: 검증 + push

Task Scheduler 05:20 KST
"""

import json, os, re, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BLOG_DIR = Path(__file__).parent.parent
DATA_DIR = BLOG_DIR / "_data" / "sources"
CONFIG_DIR = BLOG_DIR / "config"
TMP = BLOG_DIR / "_tmp"
SCRIPTS = BLOG_DIR / "scripts"
KST = timezone(timedelta(hours=9))
TODAY = datetime.now(KST).strftime("%Y-%m-%d")

load_dotenv(BLOG_DIR / ".env")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

CLAUDE_CMD = r"C:\Users\pauls\AppData\Roaming\npm\claude.cmd"
FFMPEG = r"C:\Users\pauls\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

PLAYLISTS = [
    ("claude",   "PLUeFkXBkSX_bxzWza71Mdb7JlOOg5xDDS"),
    ("build",    "PLUeFkXBkSX_Znh-9HE9iIEzq23h3Y2eBw"),
    ("design",   "PLUeFkXBkSX_aH1TmJ1iOolxwkJsP6DwXf"),
    ("insight",  "PLUeFkXBkSX_bhASv37IvjLnXfCVwqQT8h"),
    ("ontology", "PLUeFkXBkSX_ZFCfP8j0peOCeOlKVhwfFx"),
]

LOG = []
ANY_FAIL = False

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.append(line)


# ── 기존 video_id 로드 (dedup) ─────────────────────────
def load_processed_ids():
    seen = set()
    for f in sorted(DATA_DIR.glob("youtube-*.json")):
        try:
            for v in json.loads(f.read_text(encoding="utf-8")):
                seen.add(v.get("video_id", ""))
        except:
            pass
    return seen


# ── Step 1: 신규 영상 감지 ─────────────────────────────
def fetch_new_videos():
    log("[Step 1] 신규 영상 감지...")
    processed = load_processed_ids()
    log(f"  기존: {len(processed)}건")

    new_videos = []
    for label, playlist_id in PLAYLISTS:
        try:
            r = subprocess.run(
                ["yt-dlp", "--flat-playlist", "--print", "%(id)s %(title)s",
                 f"https://www.youtube.com/playlist?list={playlist_id}"],
                capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace"
            )
            for line in r.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split(" ", 1)
                vid = parts[0].strip()
                title = parts[1].strip() if len(parts) > 1 else ""
                if vid and vid not in processed:
                    new_videos.append({"video_id": vid, "title": title, "playlist": label})
                    processed.add(vid)
            log(f"  {label}: 스캔 완료")
        except Exception as e:
            log(f"  {label}: FAIL ({e})")

    log(f"  신규: {len(new_videos)}건")
    return new_videos


# ── Step 2: Transcript 추출 ────────────────────────────
def extract_transcript_ytdlp(video_id):
    """yt-dlp로 자막 추출 (수동 → 자동생성)"""
    tmp_dir = Path(tempfile.gettempdir())
    base = tmp_dir / f"yt_sub_{video_id}"

    for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
        f.unlink(missing_ok=True)

    for sub_args in [
        ["--write-sub", "--sub-lang", "en,ko"],
        ["--write-auto-sub", "--sub-lang", "en,ko"],
    ]:
        subprocess.run(
            ["yt-dlp", "--skip-download", *sub_args,
             "--sub-format", "vtt", "-o", str(base),
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=60,
        )
        for vtt in sorted(tmp_dir.glob(f"yt_sub_{video_id}*.vtt")):
            raw = vtt.read_text(encoding="utf-8", errors="replace")
            lines = []
            for line in raw.splitlines():
                line = line.strip()
                if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                    continue
                if re.match(r"^\d{2}:\d{2}", line) or "-->" in line:
                    continue
                line = re.sub(r"<[^>]+>", "", line)
                if line:
                    lines.append(line)
            deduped = [lines[0]] if lines else []
            for ln in lines[1:]:
                if ln != deduped[-1]:
                    deduped.append(ln)
            transcript = " ".join(deduped).strip()
            for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
                f.unlink(missing_ok=True)
            if len(transcript) > 100:
                return transcript[:100000]

    for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
        f.unlink(missing_ok=True)
    return None


def extract_transcript_groq(video_id):
    """Groq Whisper로 transcript 추출 (자막 없을 때)"""
    if not GROQ_API_KEY:
        log("    [Groq] API key 없음")
        return None

    tmp_dir = Path(tempfile.gettempdir())
    audio_path = tmp_dir / f"yt_audio_{video_id}.mp3"

    # 오디오 추출
    log("    [Groq] 오디오 추출 중...")
    subprocess.run(
        ["yt-dlp", "-x", "--audio-format", "mp3",
         "--ffmpeg-location", str(Path(FFMPEG).parent),
         "-o", str(audio_path),
         f"https://www.youtube.com/watch?v={video_id}"],
        capture_output=True, timeout=120,
    )
    if not audio_path.exists():
        log("    [Groq] 오디오 추출 실패")
        return None

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        file_size = audio_path.stat().st_size / (1024 * 1024)
        log(f"    [Groq] 파일: {file_size:.1f}MB")

        if file_size > 24:
            # 분할
            log("    [Groq] 25MB 초과 — 분할...")
            part_pattern = tmp_dir / f"groq_part_{video_id}_%03d.mp3"
            subprocess.run(
                [FFMPEG, "-i", str(audio_path), "-f", "segment",
                 "-segment_time", "600", "-c", "copy", "-y", str(part_pattern)],
                capture_output=True,
            )
            parts = sorted(tmp_dir.glob(f"groq_part_{video_id}_*.mp3"))
            texts = []
            for p in parts:
                with open(p, "rb") as f:
                    result = client.audio.transcriptions.create(
                        file=(p.name, f), model="whisper-large-v3"
                    )
                texts.append(result.text)
                p.unlink(missing_ok=True)
            transcript = " ".join(texts)
        else:
            with open(audio_path, "rb") as f:
                result = client.audio.transcriptions.create(
                    file=("audio.mp3", f), model="whisper-large-v3"
                )
            transcript = result.text

        log(f"    [Groq] 완료: {len(transcript)}자")
        return transcript[:100000] if len(transcript) > 100 else None

    except Exception as e:
        log(f"    [Groq] 실패: {e}")
        return None
    finally:
        audio_path.unlink(missing_ok=True)


# ── Step 3: 구조화 (Codex gpt-5.4) ───────────────────
CODEX_CMD = r"C:\Users\pauls\AppData\Roaming\npm\codex.cmd"

def structurize(title, transcript):
    """Codex CLI gpt-5.4로 Smart Brevity 구조화 (Plus 구독 내)"""
    prompt_template = (CONFIG_DIR / "structuring-prompt.md").read_text(encoding="utf-8")
    prompt = prompt_template.replace("{title}", title).replace("{transcript}", transcript[:50000])

    out_file = TMP / f"structurize-{TODAY}-{int(time.time())}.json"

    try:
        full_prompt = prompt + "\n\n순수 JSON만 출력. 마크다운 코드블록 없이."
        # Windows .cmd 래퍼: communicate() timeout이 안 먹음
        # -o 파일로 출력 받고, threading.Timer로 강제 kill
        import threading as _th

        # 프롬프트를 임시 파일로 전달 (stdin pipe 대신)
        prompt_file = TMP / f"prompt-struct-{int(time.time())}.txt"
        prompt_file.write_text(full_prompt, encoding="utf-8")

        result = [None]
        def _run_codex():
            result[0] = subprocess.run(
                [CODEX_CMD, "exec",
                 "-m", "gpt-5.4",
                 "--full-auto",
                 "--skip-git-repo-check",
                 "-o", str(out_file)],
                stdin=open(str(prompt_file), "r", encoding="utf-8"),
                capture_output=True, timeout=600,
                text=True, encoding="utf-8",
                cwd=str(BLOG_DIR),
            )

        t = _th.Thread(target=_run_codex, daemon=True)
        t.start()
        t.join(timeout=300)
        prompt_file.unlink(missing_ok=True)

        if t.is_alive():
            # 타임아웃 — taskkill로 Codex 프로세스 트리 전체 kill
            subprocess.run("taskkill /F /IM codex.exe 2>nul & taskkill /F /IM Codex.exe 2>nul",
                          shell=True, capture_output=True, timeout=10)
            log("    [구조화] Codex 타임아웃 (300초)")
            out_file.unlink(missing_ok=True)
            return None

        r = result[0]
        # 출력 파일 우선, 없으면 stdout
        if out_file.exists():
            raw = out_file.read_text(encoding="utf-8").strip()
            out_file.unlink(missing_ok=True)
        elif r:
            raw = (r.stdout or "").strip()
        else:
            raw = ""

        if r and r.returncode != 0 and not raw:
            log(f"    [구조화] Codex 실패 (rc={r.returncode}): {(r.stderr or '').strip()[:200]}")
            return None

        # JSON 추출
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            raw = m.group(0)
        return json.loads(raw)

    except json.JSONDecodeError as e:
        log(f"    [구조화] JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        log(f"    [구조화] 실패: {e}")
        return None


# ── Step 4: Apply Points 5W1H (Claude Sonnet) ─────────
def generate_apply_points(summary, title):
    """Claude Sonnet + recall() → 5W1H apply_points"""
    compact = json.dumps({
        "title": title,
        "key_takeaways": summary.get("key_takeaways", []),
        "tech_stack": summary.get("tech_stack", []),
        "sections": [s.get("heading", "") for s in summary.get("sections", [])],
    }, ensure_ascii=False, indent=2)

    prompt = f"""mcp-memory에서 recall('Paul 프로젝트 시스템')로 현재 상태를 조회해라.

아래 YouTube 영상 분석 결과를 보고, Paul의 프로젝트에 적용할 수 있는 포인트를 1개만 5W1H 형식으로 작성해라.

영상 분석:
{compact}

출력 형식 (순수 JSON만, 설명 없이):
{{
  "level": 1,
  "where": "대상 프로젝트/시스템",
  "what": "구체적 액션",
  "why": "근거",
  "how": "실행 방법",
  "when": "시점"
}}

규칙:
- Level 1(시스템 액션): 5필드 전부. 즉시 적용.
- Level 2(설계 참고): where/what/why만. 당장 아님.
- Level 3(사고 자극): what/why만.
- 가장 높은 레벨 우선. 억지 L1 금지.
- 1개만."""

    try:
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)
        import threading as _th

        result = [None]
        def _run_claude():
            result[0] = subprocess.run(
                [CLAUDE_CMD, "-p", "--model", "claude-sonnet-4-6", "--output-format", "json",
                 "--allowedTools", "mcp__memory__recall"],
                input=prompt.encode("utf-8"),
                capture_output=True, timeout=600, cwd=str(BLOG_DIR), env=env,
            )

        t = _th.Thread(target=_run_claude, daemon=True)
        t.start()
        t.join(timeout=240)

        if t.is_alive():
            subprocess.run("taskkill /F /IM claude.exe 2>nul & taskkill /F /IM node.exe /FI \"WINDOWTITLE eq claude*\" 2>nul",
                          shell=True, capture_output=True, timeout=10)
            log("    [AP] Claude 타임아웃 (240초)")
            return None

        r = result[0]
        if not r or r.returncode != 0:
            stderr = r.stderr.decode("utf-8", errors="replace").strip()[:200] if r else "no result"
            log(f"    [AP] CLI 실패: {stderr}")
            return None
        raw = r.stdout.decode("utf-8", errors="replace").strip()
        if not raw:
            log("    [AP] 실패: 빈 응답")
            return None
        # --output-format json → {"result": "..."} 구조. result 추출
        wrapper = json.loads(raw)
        text = wrapper.get("result", raw) if isinstance(wrapper, dict) else raw
        # JSON 코드펜스 제거
        text = re.sub(r"^```json\s*", "", str(text).strip())
        text = re.sub(r"```\s*$", "", text.strip())
        # JSON 객체만 추출 (앞뒤 자연어 텍스트 제거)
        match = re.search(r'\{[^{}]*"level"\s*:', text)
        if match:
            brace = 0
            start = match.start()
            for i in range(start, len(text)):
                if text[i] == '{': brace += 1
                elif text[i] == '}': brace -= 1
                if brace == 0:
                    text = text[start:i+1]
                    break
        ap = json.loads(text)
        log(f"    [AP] L{ap.get('level','?')}: {ap.get('what','')[:40]}")
        return ap
    except Exception as e:
        log(f"    [AP] 실패: {e}")
        # 디버깅용: 원본 응답 로그
        try:
            log(f"    [AP] raw: {raw[:200]}")
        except Exception:
            pass
        return None


# ── Step 5: 번역 (Claude 4.5 Sonnet, OAuth) ────────────────
def translate_transcript(transcript):
    """영어 transcript → 한글 번역 (Claude 4.5 Sonnet via OAuth)."""
    if not transcript:
        return None

    # 이미 한국어면 스킵
    ko_ratio = sum(1 for c in transcript[:500] if '\uac00' <= c <= '\ud7a3') / max(len(transcript[:500]), 1)
    if ko_ratio > 0.3:
        log("    [번역] 이미 한국어 — 스킵")
        return transcript

    prompt = (
        "다음 영문 transcript를 자연스러운 한국어로 번역하라.\n\n"
        "규칙:\n"
        "- 고유명사/기술용어/라이브러리명/회사명은 영어 그대로 유지\n"
        "- 요약 금지. 원문 구조·길이를 유지.\n"
        "- 번역문만 출력. 설명·인사말·메타코멘트 금지.\n\n"
        "원문:\n" + transcript[:30000]
    )

    try:
        import threading as _th
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)  # blog/.env의 만료 키 제거 → OAuth 사용

        result = [None]
        def _run_claude():
            result[0] = subprocess.run(
                [CLAUDE_CMD, "-p", "--model", "claude-sonnet-4-5"],
                input=prompt.encode("utf-8"),
                capture_output=True, timeout=600, cwd=str(BLOG_DIR), env=env,
            )

        t = _th.Thread(target=_run_claude, daemon=True)
        t.start()
        t.join(timeout=360)

        if t.is_alive():
            subprocess.run(
                'taskkill /F /IM claude.exe 2>nul & taskkill /F /IM node.exe /FI "WINDOWTITLE eq claude*" 2>nul',
                shell=True, capture_output=True, timeout=10
            )
            log("    [번역] Claude 타임아웃 (360초)")
            return None

        r = result[0]
        if not r or r.returncode != 0:
            stderr = (r.stderr.decode("utf-8", errors="replace").strip()[:200] if r else "no result")
            log(f"    [번역] Claude 실패: {stderr}")
            return None
        translated = r.stdout.decode("utf-8", errors="replace").strip()
        if not translated or len(translated) < 20:
            log("    [번역] 빈/짧은 응답")
            return None
        low = translated.lower()
        if any(e in low for e in ["credit balance", "rate limit", "unauthorized", "api key"]):
            log("    [번역] 에러 응답 감지")
            return None
        log(f"    [번역] {len(translated)}자 (Claude 4.5 Sonnet)")
        return translated
    except Exception as e:
        log(f"    [번역] 실패: {e}")
        return None


# ── Quote 검증 ─────────────────────────────────────────
def validate_quotes(summary, transcript):
    norm_tr = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', transcript)).strip().lower()
    for sec in summary.get("sections", []):
        q = sec.get("quote", "")
        if q:
            norm_q = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', q)).strip().lower()
            if norm_q not in norm_tr:
                sec.pop("quote", None)


# ── 메인 파이프라인 ────────────────────────────────────
def main():
    global ANY_FAIL
    log(f"=== YouTube v3 시작 ({TODAY}) ===")

    # Step 1: 신규 감지
    new_videos = fetch_new_videos()
    if not new_videos:
        log("신규 없음 — 종료")
        return

    # 오늘 날짜 파일에 저장
    out_file = DATA_DIR / f"youtube-{TODAY}.json"
    existing = json.loads(out_file.read_text(encoding="utf-8")) if out_file.exists() else []

    processed_count = 0
    for i, video in enumerate(new_videos):
        vid = video["video_id"]
        title = video["title"]
        log(f"\n--- [{i+1}/{len(new_videos)}] {title[:50]} ---")

        # Step 2: Transcript
        log("  [S1] Transcript...")
        transcript = extract_transcript_ytdlp(vid)
        if transcript:
            log(f"    yt-dlp: {len(transcript)}자")
        else:
            log("    yt-dlp: 자막 없음 → Groq fallback")
            transcript = extract_transcript_groq(vid)

        if not transcript:
            log("    Transcript 추출 실패 — 스킵")
            continue

        # Step 3: 구조화
        log("  [S2] 구조화 (Codex gpt-5.4)...")
        summary = structurize(title, transcript)
        if not summary:
            log("    구조화 실패 — 스킵")
            continue
        log(f"    sections: {len(summary.get('sections',[]))}개")

        # Quote 검증
        validate_quotes(summary, transcript)

        # Step 4: Apply Points
        log("  [S3] Apply Points (Claude Sonnet)...")
        ap = generate_apply_points(summary, title)
        if ap:
            summary["apply_points"] = ap

        # Step 5: 번역
        log("  [S4] 번역...")
        transcript_ko = translate_transcript(transcript)

        # 레코드 조립
        record = {
            "video_id": vid,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "playlist": video.get("playlist", ""),
            "fetched_at": TODAY,
            "transcript": transcript,
            "transcript_ko": transcript_ko or "",
            "summary": summary,
        }
        existing.append(record)
        processed_count += 1
        log(f"  [OK] 완료")

    # 저장
    if processed_count > 0:
        out_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        log(f"\n저장: {out_file} ({processed_count}건 추가)")

        # Step 6: push
        log("[Step 6] 배포...")
        try:
            subprocess.run(["git", "pull", "--rebase", "origin", "master"],
                          cwd=str(BLOG_DIR), capture_output=True, timeout=30)
            subprocess.run(["git", "add", str(DATA_DIR)],
                          cwd=str(BLOG_DIR), capture_output=True, timeout=10)
            r = subprocess.run(
                ["git", "commit", "-m", f"[auto] {TODAY} youtube ({processed_count}건 분석)"],
                cwd=str(BLOG_DIR), capture_output=True, text=True, timeout=30, encoding="utf-8")
            log(f"  commit: {r.stdout.strip()[:80]}")
            r = subprocess.run(["git", "push"],
                              cwd=str(BLOG_DIR), capture_output=True, text=True, timeout=60, encoding="utf-8")
            log(f"  push: {(r.stdout or r.stderr).strip()[:80]}")
        except Exception as e:
            log(f"  git FAIL: {e}")
            ANY_FAIL = True
    else:
        log("처리된 영상 없음")

    log(f"\n=== {'완료' if not ANY_FAIL else 'FAIL'} ({TODAY}, {processed_count}건) ===")

    # 로그 저장
    log_path = SCRIPTS / "_logs" / f"youtube-v3-{TODAY}.log"
    log_path.parent.mkdir(exist_ok=True)
    log_path.write_text("\n".join(LOG), encoding="utf-8")

    if ANY_FAIL:
        (TMP / f"alert-youtube-{TODAY}.txt").write_text(
            f"YouTube FAIL: {TODAY}\n" + "\n".join(l for l in LOG if "FAIL" in l), encoding="utf-8")
        sys.exit(1)


if __name__ == "__main__":
    main()
