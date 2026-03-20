#!/usr/bin/env python3
"""
analyze-youtube.py — 3-stage YouTube pipeline

Stage 1: yt-dlp 자막 → (fallback) Gemini 트랜스크립트
Stage 2: Codex CLI (GPT-5.4) → 구조화 JSON (sections, takeaways, tech_stack, apply_points)
Stage 3: Claude -p → Why It Matters (Smart Brevity axiom)

매일 09:00 KST Task Scheduler 자동 실행

Usage: python scripts/analyze-youtube.py
"""

import json, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# ── yt-dlp 자막 추출 (1차) ────────────────────────────────────────────────
def extract_transcript_ytdlp(video_url: str, video_id: str) -> str | None:
    """yt-dlp로 YouTube 자막(수동 + 자동생성) 추출. 없으면 None."""
    tmp_dir = Path(tempfile.gettempdir())
    base = tmp_dir / f"yt_sub_{video_id}"

    # 이전 임시 파일 정리
    for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
        f.unlink(missing_ok=True)

    # 수동 자막 우선, 없으면 자동생성 자막
    for sub_args in [
        ["--write-sub", "--sub-lang", "en,ko"],
        ["--write-auto-sub", "--sub-lang", "en,ko"],
    ]:
        r = subprocess.run(
            ["yt-dlp", "--skip-download", *sub_args,
             "--sub-format", "vtt", "-o", str(base), video_url],
            capture_output=True, text=True, timeout=60,
        )
        # vtt 파일 찾기
        for vtt in sorted(tmp_dir.glob(f"yt_sub_{video_id}*.vtt")):
            raw = vtt.read_text(encoding="utf-8", errors="replace")
            # VTT 헤더/타임스탬프 제거 → 순수 텍스트
            lines = []
            for line in raw.splitlines():
                line = line.strip()
                if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                    continue
                if re.match(r"^\d{2}:\d{2}", line) or line == "-->" or "-->" in line:
                    continue
                if line.startswith("<"):
                    line = re.sub(r"<[^>]+>", "", line)
                if line:
                    lines.append(line)
            # 연속 중복 제거 (자동생성 자막의 반복 라인)
            deduped = []
            for ln in lines:
                if not deduped or ln != deduped[-1]:
                    deduped.append(ln)
            transcript = " ".join(deduped).strip()
            # 정리
            for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
                f.unlink(missing_ok=True)
            if len(transcript) > 100:
                lang = "ko" if "ko" in vtt.name else "en"
                print(f"  [yt-dlp 자막] 완료: {len(transcript)}자 ({lang})")
                return transcript[:100000]

    # 정리
    for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
        f.unlink(missing_ok=True)
    return None


# ── Whisper fallback (자막 없는 영상) ─────────────────────────────────────
def extract_transcript_whisper(video_url: str, video_id: str) -> str | None:
    """yt-dlp 오디오 추출 → openai-whisper STT → transcript 반환"""
    import imageio_ffmpeg
    ffmpeg_dir = str(Path(imageio_ffmpeg.get_ffmpeg_exe()).parent)
    # openai-whisper가 내부적으로 ffmpeg를 subprocess로 호출하므로 PATH에 추가
    if ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    tmp_dir = Path(tempfile.gettempdir())
    audio_path = tmp_dir / f"yt_audio_{video_id}.mp3"

    # 이전 임시 파일 정리
    for f in tmp_dir.glob(f"yt_audio_{video_id}*"):
        f.unlink(missing_ok=True)

    # 오디오 다운로드
    print("  [Whisper] 오디오 다운로드 중...")
    r = subprocess.run(
        [
            "yt-dlp", "-x", "--audio-format", "mp3",
            "--ffmpeg-location", ffmpeg_dir,
            "-o", str(audio_path), video_url,
        ],
        capture_output=True, text=True, timeout=120,
    )
    if not audio_path.exists():
        print(f"  [Whisper] 다운로드 실패: {r.stderr[-200:]}")
        return None

    # Whisper STT
    print("  [Whisper] STT 처리 중 (medium, GPU)...")
    try:
        import whisper, torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("medium", device=device)
        result = model.transcribe(str(audio_path), fp16=(device == "cuda"))
        transcript = result["text"].strip()
        print(f"  [Whisper] 완료: {len(transcript)}자 ({result.get('language','?')})")
        return transcript[:80000]
    except Exception as e:
        print(f"  [Whisper] STT 실패: {e}")
        return None
    finally:
        audio_path.unlink(missing_ok=True)

# ── Gemini fallback (Whisper 대체 — 자막 없는 영상) ────────────────────────
def extract_transcript_gemini(video_url: str) -> str | None:
    """Gemini CLI로 YouTube 영상에서 원문 트랜스크립트 추출."""
    gemini_path = "C:/Users/pauls/AppData/Roaming/npm/gemini.cmd"
    prompt = (
        "You are a transcript extractor. Output the full spoken transcript "
        "of this YouTube video. Output EVERY word in the ORIGINAL language. "
        "No summary, no formatting, no commentary. Raw spoken text only. "
        "Do NOT use any tools except for fetching the video content. "
        f"Video: {video_url}"
    )
    try:
        print("  [Gemini] 트랜스크립트 추출 중...")
        result = subprocess.run(
            [gemini_path, "-p", prompt, "-y"],
            capture_output=True, timeout=300,
            cwd="C:/windows/temp",
            env={**os.environ}
        )
        text = result.stdout.decode("utf-8", errors="replace").strip()
        # Gemini CLI 헤더 라인 제거 (YOLO mode, Loading extension 등)
        lines = text.split("\n")
        content_lines = []
        started = False
        for line in lines:
            if not started:
                if any(skip in line for skip in [
                    "YOLO mode", "Loaded cached", "Loading extension",
                    "Server '", "I will"
                ]):
                    continue
                started = True
            if started:
                content_lines.append(line)
        transcript = "\n".join(content_lines).strip()
        if len(transcript) > 100:
            print(f"  [Gemini] 완료: {len(transcript)}자")
            return transcript[:100000]
        print("  [Gemini] 추출 결과 부족")
        return None
    except subprocess.TimeoutExpired:
        print("  [Gemini] 타임아웃 (5분 초과)")
        return None
    except Exception as e:
        print(f"  [Gemini] 실패: {e}")
        return None


SCRIPT_DIR = Path(__file__).parent
BLOG_DIR   = SCRIPT_DIR.parent
DATA_DIR   = BLOG_DIR / "_data" / "sources"

PROMPT_TEMPLATE = """\
다음은 YouTube 영상의 자막 전체 텍스트다.
영상을 보지 않아도 내용을 완전히 파악할 수 있을 만큼 빠짐없이 포괄적인 분석 리포트를 아래 JSON 형식으로 만들어라.
자막에 등장하는 모든 주요 주제, 주장, 수치, 사례, 논거를 빠뜨리지 말 것.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

주의: smart_brevity 필드는 생성하지 마라. Why It Matters는 별도 단계에서 처리된다.

{{
  "sections": [
    {{
      "heading": "섹션 제목 (명확하고 구체적으로 — 영상에서 다루는 실제 주제명)",
      "body": "최소 5문장 이상, 해당 주제에서 등장한 모든 논거·수치·사례·발언을 빠짐없이 서술. 표면 요약 금지 — 왜 이 주장을 하는지, 어떤 근거를 드는지, 어떤 반론을 다루는지 전부 포함.",
      "highlights": ["핵심 문장 (body에서 그대로 복사, 변형 금지)", "핵심 문장 2"],
      "quote": "아래 자막 텍스트에서 가장 임팩트 있는 발언 1문장을 단어 하나도 바꾸지 말고 그대로 복사. 재구성·요약·창작 절대 금지. 자막 텍스트에 해당 문장이 그대로 없으면 이 필드 생략."
    }}
  ],
  "key_takeaways": ["핵심 요점 1", "핵심 요점 2", "핵심 요점 3", "핵심 요점 4", "핵심 요점 5"],
  "tech_stack": ["언급된 실제 기술/도구/서비스명"],
  "apply_points": [
    {{"text": "적용 포인트 내용. Paul의 실제 프로젝트와 직접 연결. 일반론 금지.", "key": false}},
    {{"text": "당장 시스템에 반영 가능한 것 (key=true는 최대 2개)", "key": true}}
  ]
}}

규칙:
- sections는 영상에서 다루는 모든 주요 주제를 커버해야 함. 최소 6개, 내용에 따라 10개 이상도 가능.
- body는 최소 5문장 이상. 해당 섹션에서 발언자가 한 모든 주요 주장과 근거를 포함. 한 단락만으로 부족하면 여러 단락 사용.
- body에 등장한 수치·인명·사례는 생략 없이 전부 기록.
- highlights는 반드시 body에서 그대로 복사한 문장만. 요약·변형 금지. body에 없는 문장은 highlights 불가.
- apply_points: Paul의 프로젝트(orchestration, mcp-memory, tech-review, portfolio)와 연결. backtick·파일경로·코드 금지. 한 문장으로 읽기 좋게. key=true는 최대 2개.
- 전부 한국어 (기술명·인명·고유명사는 영어 유지)
- 영상을 안 봐도 될 수준 = 이 JSON만으로 영상의 모든 주요 내용이 복원 가능해야 함

영상 제목: {title}

자막 내용:
{transcript}
"""

def _norm(text: str) -> str:
    """구두점 제거 + 공백 정규화 (quote 검증용)"""
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip()

def validate_quotes(summary: dict, transcript: str) -> None:
    """각 섹션 quote가 transcript에 실제로 존재하는지 확인. 없으면 제거."""
    norm_tr = _norm(transcript)
    for sec in summary.get("sections", []):
        q = sec.get("quote", "")
        if q and _norm(q) not in norm_tr:
            sec.pop("quote", None)

def find_pending(reprocess=False):
    """분석 대상 영상 목록 반환.
    reprocess=True: 기존 summary 있는 영상도 전부 포함 (재구조화용)
    """
    pending = []
    seen = set()
    for f in sorted(DATA_DIR.glob("youtube-*.json")):
        try:
            videos = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for v in videos:
            vid = v.get("video_id", "")
            if vid in seen:
                continue
            seen.add(vid)
            if reprocess or not v.get("summary"):
                pending.append((f, videos, v))
    return pending

def analyze_with_codex(title: str, transcript: str) -> dict | None:
    """Codex CLI (GPT-5.4 xhigh) 로 분석"""
    prompt = PROMPT_TEMPLATE.format(
        title=title,
        transcript=transcript[:100000]  # 토큰 제한 여유
    )

    # 임시 파일로 전달 (프롬프트 길이 제한 우회)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BLOG_DIR
    ) as tf:
        tf.write(prompt)
        tf_path = tf.name

    try:
        out_path = BLOG_DIR / "_codex_out.json"
        result = subprocess.run(
            f'codex exec "파일 {tf_path} 을 읽고 지시대로 JSON을 만들어서 {out_path} 에 저장해라. 순수 JSON만." --full-auto',
            capture_output=True, text=True, timeout=1800,  # 30분
            encoding="utf-8", errors="replace",
            cwd=str(BLOG_DIR), shell=True,
        )

        # 출력 파일 우선 시도
        if out_path.exists():
            raw = out_path.read_text(encoding="utf-8").strip()
            out_path.unlink()
        else:
            raw = (result.stdout or "").strip()

        # 코드블록 제거
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())

        # JSON 파싱
        return json.loads(raw)

    except subprocess.TimeoutExpired:
        print("  Codex 타임아웃 (30분 초과)")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON 파싱 실패: {e}")
        print(f"  출력: {raw[:300]}")
        return None
    except Exception as e:
        print(f"  오류: {e}")
        return None
    finally:
        try:
            os.unlink(tf_path)
        except Exception:
            pass

WIM_PROMPT_PATH = BLOG_DIR / "config" / "wim-prompt.md"
CLAUDE_PATH = "C:/Users/pauls/AppData/Roaming/npm/claude.cmd"


def generate_wim(summary: dict, title: str) -> dict | None:
    """Claude -p로 Smart Brevity WIM 생성. summary에 smart_brevity 필드 추가."""
    if not WIM_PROMPT_PATH.exists():
        print("  [WIM] wim-prompt.md 없음 — 건너뜀")
        return None

    wim_prompt = WIM_PROMPT_PATH.read_text(encoding="utf-8")
    # Codex 구조화 결과에서 WIM에 필요한 부분만 추출
    compact = json.dumps({
        "title": title,
        "key_takeaways": summary.get("key_takeaways", []),
        "tech_stack": summary.get("tech_stack", []),
        "apply_points": summary.get("apply_points", []),
        "sections": [{"heading": s["heading"]} for s in summary.get("sections", [])],
    }, indent=2, ensure_ascii=False)

    full_prompt = wim_prompt + "\n" + compact

    try:
        print("  [WIM] Claude -p 생성 중...")
        result = subprocess.run(
            [CLAUDE_PATH, "-p", "--setting-sources", "user"],
            input=full_prompt.encode("utf-8"),
            capture_output=True, timeout=120,
            cwd="C:/windows/temp",
            env={**os.environ}
        )
        wim_text = result.stdout.decode("utf-8", errors="replace").strip()
        if not wim_text or len(wim_text) < 20:
            print("  [WIM] 결과 부족")
            return None

        # smart_brevity 필드 구성
        smart_brevity = {"why": "", "what": "", "axioms": []}

        # Why it matters 추출
        why_match = re.search(
            r"\*\*Why it matters:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)",
            wim_text, re.DOTALL
        )
        if why_match:
            smart_brevity["why"] = why_match.group(1).strip()

        # 추가 axiom 추출
        axiom_pattern = r"\*\*([^*]+):\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)"
        for match in re.finditer(axiom_pattern, wim_text, re.DOTALL):
            label = match.group(1).strip()
            content = match.group(2).strip()
            if label == "Why it matters":
                continue  # 이미 처리
            smart_brevity["axioms"].append({
                "label": label,
                "content": content
            })

        print(f"  [WIM] 완료: why={len(smart_brevity['why'])}자, axioms={len(smart_brevity['axioms'])}개")
        return smart_brevity

    except subprocess.TimeoutExpired:
        print("  [WIM] 타임아웃 (2분 초과)")
        return None
    except Exception as e:
        print(f"  [WIM] 실패: {e}")
        return None


STATUS_FILE = BLOG_DIR / "_data" / "analyze-status.json"

def write_status(step: str, video_title: str, done: int, total: int, detail: str = ""):
    STATUS_FILE.write_text(
        json.dumps({
            "step": step,
            "video": video_title,
            "done": done,
            "total": total,
            "detail": detail
        }, ensure_ascii=False),
        encoding="utf-8"
    )

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--reprocess", action="store_true",
                        help="기존 영상 포함 전체 재구조화 + WIM 재작성")
    parser.add_argument("--wim-only", action="store_true",
                        help="기존 summary 유지, WIM만 재작성")
    parser.add_argument("--no-fetch", action="store_true",
                        help="fetch-youtube.js 실행 건너뜀")
    args = parser.parse_args()

    # 최신 데이터 받기
    os.system("git pull --rebase origin master")

    # fetch-youtube.js 실행 (신규 영상 수집)
    if not args.no_fetch:
        fetch_script = SCRIPT_DIR / "fetch-youtube.js"
        if fetch_script.exists():
            print("=== YouTube fetch 실행 ===")
            r = subprocess.run(
                ["node", str(fetch_script)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                cwd=str(BLOG_DIR), timeout=120,
            )
            if r.stdout.strip():
                for line in r.stdout.strip().split("\n")[-5:]:
                    print(f"  {line}")
            if r.returncode != 0 and r.stderr.strip():
                print(f"  fetch 경고: {r.stderr.strip()[-200:]}")

    pending = find_pending(reprocess=args.reprocess or args.wim_only)
    print(f"분석 대상: {len(pending)}개 영상")

    if not pending:
        print("처리할 영상 없음.")
        write_status("idle", "", 0, 0, "처리할 영상 없음")
        return

    total = len(pending)
    done = 0
    updated_files = set()
    file_videos = {filepath: videos for (filepath, videos, _) in pending}

    # ── 조립 라인: 3단계 큐 ──
    from threading import Thread
    from queue import Queue

    q_transcript = Queue()   # Stage 1 → Stage 2
    q_codex = Queue()        # Stage 2 → Stage 3
    q_save = Queue()         # Stage 3 → 저장

    POISON = None  # 종료 신호

    # 리밋 감지 + 재시도
    def retry_with_backoff(fn, *a, max_retries=3, **kw):
        for attempt in range(max_retries):
            result = fn(*a, **kw)
            if result is not None:
                return result
            wait = 60 * (attempt + 1)  # 1분, 2분, 3분
            print(f"    재시도 대기 {wait}초 (attempt {attempt+1}/{max_retries})...")
            import time; time.sleep(wait)
        return None

    # Stage 1: 트랜스크립트 추출 (Gemini/yt-dlp)
    def stage1_worker():
        for (filepath, videos, video) in pending:
            title = video.get("title", "")
            if not video.get("transcript"):
                video_id = video.get("video_id", "")
                video_url = video.get("url", "")
                print(f"  [S1] 트랜스크립트: {title[:40]}")
                transcript = extract_transcript_ytdlp(video_url, video_id)
                if not transcript:
                    transcript = retry_with_backoff(extract_transcript_gemini, video_url)
                if not transcript:
                    transcript = extract_transcript_whisper(video_url, video_id)
                if transcript:
                    video["transcript"] = transcript
                else:
                    print(f"  [S1] 실패: {title[:40]}")
                    continue
            q_transcript.put((filepath, videos, video, args.wim_only))
        q_transcript.put(POISON)

    # Stage 2: Codex 구조화
    def stage2_worker():
        while True:
            item = q_transcript.get()
            if item is POISON:
                q_codex.put(POISON)
                break
            filepath, videos, video, wim_only = item
            title = video.get("title", "")
            if wim_only and video.get("summary"):
                summary = video["summary"]
                print(f"  [S2] WIM-only: {title[:40]}")
            else:
                print(f"  [S2] Codex: {title[:40]}")
                summary = retry_with_backoff(
                    analyze_with_codex, title, video["transcript"]
                )
                if not summary:
                    print(f"  [S2] 실패: {title[:40]}")
                    continue
                validate_quotes(summary, video["transcript"])
            q_codex.put((filepath, videos, video, summary))

    # Stage 3: Claude WIM
    def stage3_worker():
        nonlocal done
        while True:
            item = q_codex.get()
            if item is POISON:
                q_save.put(POISON)
                break
            filepath, videos, video, summary = item
            title = video.get("title", "")
            print(f"  [S3] WIM: {title[:40]}")
            wim = retry_with_backoff(generate_wim, summary, title)
            if wim:
                summary["smart_brevity"] = wim
            else:
                print(f"  [S3] WIM 실패: {title[:40]}")
            video["summary"] = summary
            done += 1
            write_status("pipeline", title, done, total, f"완료={done}")
            # 즉시 저장
            filepath.write_text(
                json.dumps(file_videos[filepath], ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            updated_files.add(filepath)
            print(f"  [{done}/{total}] 완료: {title[:40]}")

    # 3 스레드 동시 시작
    print(f"\n=== 조립 라인 시작: {total}개 ===")
    t1 = Thread(target=stage1_worker, daemon=True)
    t2 = Thread(target=stage2_worker, daemon=True)
    t3 = Thread(target=stage3_worker, daemon=True)
    t1.start(); t2.start(); t3.start()
    t1.join(); t2.join(); t3.join()

    if not updated_files:
        print("\n저장된 파일 없음.")
        return

    # git push
    write_status("pushing", "", done, total, "git push 중...")
    os.chdir(BLOG_DIR)
    os.system("git add _data/sources/")
    os.system(f'git commit -m "[auto] youtube pipeline {done}개 분석"')
    os.system("git push")
    write_status("complete", "", done, total, "완료")
    print("git push 완료")

if __name__ == "__main__":
    main()
