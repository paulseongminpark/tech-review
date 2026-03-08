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
이 내용을 읽고, 팟캐스트/영상을 전혀 보지 않아도 될 만큼 깊이 있는 분석 리포트를 아래 JSON 형식으로 만들어라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

{{
  "why_watch": "한 문장 — 이 영상을 왜 봐야 하는가 (임팩트 중심)",
  "sections": [
    {{
      "heading": "섹션 제목 (명확하고 구체적으로)",
      "body": "2-4문단 분량의 깊이 있는 설명. 수치, 사례, 맥락 전부 포함.",
      "highlights": ["핵심 문장 1 (그대로 인용 또는 핵심 요약)", "핵심 문장 2"],
      "quote": "인상적인 발언 (있을 경우만, 없으면 생략)"
    }}
  ],
  "key_takeaways": ["핵심 요점 1", "핵심 요점 2", "핵심 요점 3"],
  "tech_stack": ["언급된 실제 기술/도구명"],
  "apply_points": ["recall로 파악한 Paul의 실제 프로젝트(orchestration, mcp-memory, tech-review 등)에 구체적으로 적용 가능한 것. 일반론 금지 — Paul의 현재 작업과 직접 연결되는 것만."]
}}

규칙:
- sections는 영상 흐름에 따라 3-6개
- body는 최소 3문장 이상, 표면적 요약 금지 — 왜 중요한지, 어떻게 작동하는지 깊이 분석
- highlights는 섹션당 1-3개, 독자가 밑줄 칠 문장
- apply_points는 반드시 recall 결과 기반 — Paul의 실제 프로젝트명, 파일명, 패턴을 그대로 언급
- 전부 한국어 (기술명/고유명사는 영어 유지)
- 팟캐스트 안 봐도 될 수준으로 완성도 높게

영상 제목: {title}

자막 내용:
{transcript}
"""

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
        transcript=transcript[:60000]  # 토큰 제한 여유
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
            [
                "codex", "exec",
                f"파일 {tf_path} 을 읽고 지시대로 JSON을 만들어서 {out_path} 에 저장해라. 순수 JSON만.",
                "--full-auto",
            ],
            capture_output=True, text=True, timeout=300,
            cwd=str(BLOG_DIR),
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
        print("  Codex 타임아웃 (5분 초과)")
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

    updated_files = set()

    for (filepath, videos, video) in pending:
        title = video.get("title", "")
        print(f"\n분석 중: {title}")

        # transcript 없으면 Whisper로 추출
        if not video.get("transcript"):
            video_id = video.get("video_id") or ""
            transcript = extract_transcript_whisper(video.get("url", ""), video_id)
            if transcript:
                video["transcript"] = transcript
                updated_files.add(filepath)
            else:
                print("  Whisper 실패 — 건너뜀")
                continue

        summary = analyze_with_codex(title, video["transcript"])
        if not summary:
            print("  실패 — 건너뜀")
            continue

        video["summary"] = summary
        updated_files.add(filepath)
        print(f"  완료: {summary.get('why_watch', '')[:60]}")

    if not updated_files:
        print("\n저장된 파일 없음.")
        return

    # pending의 videos는 이미 in-memory 수정됨 — 파일 재읽기 없이 직접 저장
    file_videos = {filepath: videos for (filepath, videos, _) in pending}
    for filepath in updated_files:
        videos = file_videos[filepath]
        filepath.write_text(json.dumps(videos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"저장: {filepath.name}")

    # git push
    os.chdir(BLOG_DIR)
    os.system("git add _data/sources/")
    os.system(f'git commit -m "[auto] youtube summary {len(updated_files)}개 분석"')
    os.system("git push")
    print("git push 완료")

if __name__ == "__main__":
    main()
