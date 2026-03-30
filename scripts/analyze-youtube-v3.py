#!/usr/bin/env python3
"""
analyze-youtube-v3.py — YouTube 파이프라인 v3

Stage 1: yt-dlp 자막(1차) → Groq Whisper(2차) → transcript
Stage 2: Gemini Flash → 구조화 (structurize)
Stage 3: Claude Sonnet + recall() → apply_points 5W1H
Stage 4: OpenAI gpt-4.1-mini → 한글 번역
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

load_dotenv(Path("C:/dev/01_projects/06_mcp-memory/.env"))
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

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


# ── Step 3: 구조화 (Gemini Flash) ─────────────────────
def structurize(title, transcript):
    """Gemini 2.5 Flash로 Smart Brevity 구조화"""
    if not GEMINI_API_KEY:
        log("    [구조화] GEMINI_API_KEY 없음")
        return None

    prompt_template = (CONFIG_DIR / "structuring-prompt.md").read_text(encoding="utf-8")
    prompt = prompt_template.replace("{title}", title).replace("{transcript}", transcript[:50000])

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 32768},
    }).encode("utf-8")

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read().decode("utf-8"))
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            text = re.sub(r"^```json\s*", "", text)
            text = re.sub(r"\s*```$", "", text.strip())
            result = json.loads(text)
            return result
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                log(f"    [구조화] 429 — {30*(attempt+1)}초 대기")
                time.sleep(30 * (attempt + 1))
                continue
            log(f"    [구조화] HTTP {e.code}")
            return None
        except json.JSONDecodeError as e:
            log(f"    [구조화] JSON 파싱 실패")
            return None
        except Exception as e:
            log(f"    [구조화] 실패: {e}")
            return None
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
        result = subprocess.run(
            [CLAUDE_CMD, "-p", "--model", "claude-sonnet-4-6", "--output-format", "json",
             "--allowedTools", "mcp__memory__recall"],
            input=prompt.encode("utf-8"),
            capture_output=True, timeout=120, cwd=str(BLOG_DIR),
            env=env,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode("utf-8", errors="replace").strip()[:200]
            log(f"    [AP] CLI 실패 (rc={result.returncode}): {stderr}")
            return None
        raw = result.stdout.decode("utf-8", errors="replace").strip()
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


# ── Step 5: 번역 (OpenAI gpt-4.1-mini) ────────────────
def translate_transcript(transcript):
    """영어 transcript → 한글 번역"""
    if not OPENAI_API_KEY or not transcript:
        return None

    # 이미 한국어면 스킵
    ko_ratio = sum(1 for c in transcript[:500] if '\uac00' <= c <= '\ud7a3') / max(len(transcript[:500]), 1)
    if ko_ratio > 0.3:
        log("    [번역] 이미 한국어 — 스킵")
        return transcript

    body = json.dumps({
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "Translate English to natural Korean. Keep proper nouns/tech terms in English. Output only translated text."},
            {"role": "user", "content": transcript[:15000]}
        ],
        "temperature": 0.3,
        "max_completion_tokens": 16384,
    }).encode("utf-8")

    try:
        req = urllib.request.Request("https://api.openai.com/v1/chat/completions",
                                     data=body,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {OPENAI_API_KEY}"})
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read().decode("utf-8"))
        translated = data["choices"][0]["message"]["content"].strip()
        log(f"    [번역] {len(translated)}자")
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
        log("  [S2] 구조화 (Gemini Flash)...")
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


if __name__ == "__main__":
    main()
