#!/usr/bin/env python3
"""
analyze-youtube.py — transcript → Codex CLI (GPT-5.4 xhigh) → summary JSON

매일 09:00 KST Task Scheduler 자동 실행
GitHub Actions가 07:00에 transcript 추출 → 09:00에 분석

Usage: python scripts/analyze-youtube.py
"""

import json, os, re, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

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

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR   = SCRIPT_DIR.parent
DATA_DIR   = BLOG_DIR / "_data" / "sources"

PROMPT_TEMPLATE = """\
먼저 mcp-memory의 recall 도구를 호출해서 Paul의 현재 프로젝트 컨텍스트를 파악하라.
recall 쿼리: "Paul orchestration mcp-memory tech-review 프로젝트 현재 작업"

recall 결과를 바탕으로 아래 작업을 수행하라.

다음은 YouTube 영상의 자막 전체 텍스트다.
영상을 보지 않아도 내용을 완전히 파악할 수 있을 만큼 빠짐없이 포괄적인 분석 리포트를 아래 JSON 형식으로 만들어라.
자막에 등장하는 모든 주요 주제, 주장, 수치, 사례, 논거를 빠뜨리지 말 것.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

{{
  "smart_brevity": {{
    "why": "한 문장 핵심 (왜 중요한가, 임팩트·의미 중심, 구체적 수치나 결과 포함)",
    "what": "3-5줄 설명 (무슨 내용인가 — 영상 전체를 관통하는 핵심 논지, 구조, 차별점을 명확하게)"
  }},
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
- apply_points: recall 기반, Paul 프로젝트와 연결. backtick·파일경로·코드 금지. 한 문장으로 읽기 좋게. key=true는 최대 2개 — orchestration·mcp-memory·tech-review 중 당장 반영 가능한 것만.
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

def find_pending():
    """summary 없는 영상 목록 반환 (transcript 없으면 Whisper 대상 포함)"""
    pending = []
    for f in sorted(DATA_DIR.glob("youtube-*.json")):
        try:
            videos = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for v in videos:
            if not v.get("summary"):
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
            capture_output=True, text=True, timeout=600,
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
        print("  Codex 타임아웃 (10분 초과)")
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

def main():
    pending = find_pending()
    print(f"분석 대상: {len(pending)}개 영상")

    if not pending:
        print("처리할 영상 없음.")
        return

    total = len(pending)
    done = 0
    updated_files = set()

    # filepath → videos 맵 (in-memory 수정용)
    file_videos = {filepath: videos for (filepath, videos, _) in pending}

    for (filepath, videos, video) in pending:
        title = video.get("title", "")
        print(f"\n[{done}/{total}] 분석 중: {title}")

        # transcript 없으면 Whisper로 추출
        if not video.get("transcript"):
            video_id = video.get("video_id") or ""
            transcript = extract_transcript_whisper(video.get("url", ""), video_id)
            if transcript:
                video["transcript"] = transcript
            else:
                print("  Whisper 실패 — 건너뜀")
                continue

        summary = analyze_with_codex(title, video["transcript"])
        if not summary:
            print("  실패 — 건너뜀")
            continue

        validate_quotes(summary, video["transcript"])
        video["summary"] = summary
        done += 1
        print(f"  [{done}/{total}] 완료: {title[:50]}")

        # 영상 1개 완료될 때마다 즉시 저장
        filepath.write_text(json.dumps(file_videos[filepath], ensure_ascii=False, indent=2), encoding="utf-8")
        updated_files.add(filepath)
        print(f"  저장: {filepath.name}")

    if not updated_files:
        print("\n저장된 파일 없음.")
        return

    # git push
    os.chdir(BLOG_DIR)
    os.system("git add _data/sources/")
    os.system(f'git commit -m "[auto] youtube summary {done}개 분석"')
    os.system("git push")
    print("git push 완료")

if __name__ == "__main__":
    main()
