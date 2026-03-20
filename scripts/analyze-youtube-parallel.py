#!/usr/bin/env python3
"""
analyze-youtube-parallel.py — 병렬 3-stage YouTube pipeline

Stage 1: 트랜스크립트 (yt-dlp → Gemini → Whisper) — 병렬
Stage 2: Codex 구조화 — 병렬 (max workers)
Stage 3: Claude WIM — 병렬 (max workers)

Usage:
  python analyze-youtube-parallel.py --reprocess          # 전체 재처리
  python analyze-youtube-parallel.py --reprocess --workers 5  # 동시 5개
  python analyze-youtube-parallel.py                      # 신규만
"""
import argparse, json, os, re, subprocess, sys, tempfile, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
DATA_DIR = BLOG_DIR / "_data" / "sources"
WIM_PROMPT_PATH = BLOG_DIR / "config" / "wim-prompt.md"
CLAUDE_PATH = "C:/Users/pauls/AppData/Roaming/npm/claude.cmd"
GEMINI_PATH = "C:/Users/pauls/AppData/Roaming/npm/gemini.cmd"
STATUS_FILE = BLOG_DIR / "_data" / "analyze-status.json"

# ── 상태 추적 ──
progress = {"done": 0, "total": 0, "current": ""}

def write_status(step, video_title, done, total, detail=""):
    progress["done"] = done
    progress["current"] = video_title
    try:
        STATUS_FILE.write_text(json.dumps({
            "step": step, "video": video_title,
            "done": done, "total": total, "detail": detail
        }, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


# ── Stage 1: 트랜스크립트 추출 ──
def extract_transcript_ytdlp(video_url, video_id):
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
             "--sub-format", "vtt", "-o", str(base), video_url],
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
                if line.startswith("<"):
                    line = re.sub(r"<[^>]+>", "", line)
                if line:
                    lines.append(line)
            deduped = []
            for ln in lines:
                if not deduped or ln != deduped[-1]:
                    deduped.append(ln)
            transcript = " ".join(deduped).strip()
            for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
                f.unlink(missing_ok=True)
            if len(transcript) > 100:
                return transcript[:100000]
    for f in tmp_dir.glob(f"yt_sub_{video_id}*"):
        f.unlink(missing_ok=True)
    return None


def extract_transcript_gemini(video_url):
    prompt = (
        "You are a transcript extractor. Output the full spoken transcript "
        "of this YouTube video. Output EVERY word in the ORIGINAL language. "
        "No summary, no formatting, no commentary. Raw spoken text only. "
        "Do NOT use any tools except for fetching the video content. "
        f"Video: {video_url}"
    )
    try:
        result = subprocess.run(
            [GEMINI_PATH, "-p", prompt, "-y"],
            capture_output=True, timeout=300,
            cwd="C:/windows/temp", env={**os.environ}
        )
        text = result.stdout.decode("utf-8", errors="replace").strip()
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
            return transcript[:100000]
        return None
    except Exception:
        return None


# ── Stage 2: Codex 구조화 ──
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
      "body": "최소 5문장 이상, 해당 주제에서 등장한 모든 논거·수치·사례·발언을 빠짐없이 서술.",
      "highlights": ["핵심 문장 (body에서 그대로 복사, 변형 금지)"],
      "quote": "자막에서 가장 임팩트 있는 발언 1문장 그대로 복사. 없으면 생략."
    }}
  ],
  "key_takeaways": ["핵심 요점 1", "핵심 요점 2", "핵심 요점 3", "핵심 요점 4", "핵심 요점 5"],
  "tech_stack": ["언급된 실제 기술/도구/서비스명"],
  "apply_points": [
    {{"text": "적용 포인트. Paul 프로젝트와 직접 연결.", "key": false}},
    {{"text": "당장 반영 가능한 것 (key=true 최대 2개)", "key": true}}
  ]
}}

규칙:
- sections 최소 6개. body 최소 5문장. 수치·인명·사례 생략 없이 기록.
- highlights는 body에서 그대로 복사만. apply_points는 Paul 프로젝트와 연결.
- 전부 한국어 (기술명·고유명사 영어 유지)
- 영상을 안 봐도 될 수준으로.

영상 제목: {title}

자막 내용:
{transcript}
"""


def analyze_with_codex(title, transcript, video_id):
    prompt = PROMPT_TEMPLATE.format(title=title, transcript=transcript[:100000])
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8", dir=BLOG_DIR
    ) as tf:
        tf.write(prompt)
        tf_path = tf.name
    try:
        out_path = BLOG_DIR / f"_codex_out_{video_id}.json"
        result = subprocess.run(
            f'codex exec "파일 {tf_path} 을 읽고 지시대로 JSON을 만들어서 {out_path} 에 저장해라. 순수 JSON만." --full-auto',
            capture_output=True, text=True, timeout=1800,
            encoding="utf-8", errors="replace",
            cwd=str(BLOG_DIR), shell=True,
        )
        if out_path.exists():
            raw = out_path.read_text(encoding="utf-8").strip()
            out_path.unlink()
        else:
            raw = (result.stdout or "").strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        return json.loads(raw)
    except subprocess.TimeoutExpired:
        return None
    except json.JSONDecodeError:
        return None
    except Exception:
        return None
    finally:
        try:
            os.unlink(tf_path)
        except Exception:
            pass


# ── Stage 3: Claude WIM ──
def generate_wim(summary, title):
    if not WIM_PROMPT_PATH.exists():
        return None
    wim_prompt = WIM_PROMPT_PATH.read_text(encoding="utf-8")
    compact = json.dumps({
        "title": title,
        "key_takeaways": summary.get("key_takeaways", []),
        "tech_stack": summary.get("tech_stack", []),
        "apply_points": summary.get("apply_points", []),
        "sections": [{"heading": s["heading"]} for s in summary.get("sections", [])],
    }, indent=2, ensure_ascii=False)
    full_prompt = wim_prompt + "\n" + compact
    try:
        result = subprocess.run(
            [CLAUDE_PATH, "-p", "--setting-sources", "user"],
            input=full_prompt.encode("utf-8"),
            capture_output=True, timeout=120,
            cwd="C:/windows/temp", env={**os.environ}
        )
        wim_text = result.stdout.decode("utf-8", errors="replace").strip()
        if not wim_text or len(wim_text) < 20:
            return None
        smart_brevity = {"why": "", "what": "", "axioms": []}
        why_match = re.search(
            r"\*\*Why it matters:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)",
            wim_text, re.DOTALL
        )
        if why_match:
            smart_brevity["why"] = why_match.group(1).strip()
        for match in re.finditer(
            r"\*\*([^*]+):\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)", wim_text, re.DOTALL
        ):
            label = match.group(1).strip()
            content = match.group(2).strip()
            if label == "Why it matters":
                continue
            smart_brevity["axioms"].append({"label": label, "content": content})
        return smart_brevity
    except Exception:
        return None


# ── quote 검증 ──
def _norm(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip()

def validate_quotes(summary, transcript):
    norm_tr = _norm(transcript)
    for sec in summary.get("sections", []):
        q = sec.get("quote", "")
        if q and _norm(q) not in norm_tr:
            sec.pop("quote", None)


# ── 단일 영상 처리 (워커) ──
def process_one(video_data, reprocess=False):
    """단일 영상 전체 파이프라인. 결과 dict 반환."""
    video = video_data
    video_id = video.get("video_id", "")
    title = video.get("title", "")
    result = {"video_id": video_id, "status": "ok", "title": title}

    try:
        # Stage 1: 트랜스크립트
        if not video.get("transcript"):
            video_url = video.get("url", "")
            print(f"  [{video_id}] Stage 1: 트랜스크립트 추출...")
            transcript = extract_transcript_ytdlp(video_url, video_id)
            if not transcript:
                print(f"  [{video_id}] yt-dlp 실패 → Gemini")
                transcript = extract_transcript_gemini(video_url)
            if not transcript:
                result["status"] = "transcript_fail"
                print(f"  [{video_id}] 트랜스크립트 실패")
                return result
            video["transcript"] = transcript

        # Stage 2: Codex 구조화
        print(f"  [{video_id}] Stage 2: Codex 구조화...")
        summary = analyze_with_codex(title, video["transcript"], video_id)
        if not summary:
            result["status"] = "codex_fail"
            print(f"  [{video_id}] Codex 실패")
            return result
        validate_quotes(summary, video["transcript"])

        # Stage 3: Claude WIM
        print(f"  [{video_id}] Stage 3: Claude WIM...")
        wim = generate_wim(summary, title)
        if wim:
            summary["smart_brevity"] = wim
        else:
            print(f"  [{video_id}] WIM 실패 — smart_brevity 없이 저장")

        video["summary"] = summary
        result["status"] = "ok"
        print(f"  [{video_id}] 완료: {title[:40]}")

    except Exception as e:
        result["status"] = f"error: {e}"
        print(f"  [{video_id}] 오류: {e}")

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reprocess", action="store_true")
    parser.add_argument("--workers", type=int, default=5, help="동시 처리 수 (기본 5)")
    parser.add_argument("--no-fetch", action="store_true")
    args = parser.parse_args()

    os.system("git pull --rebase origin master")

    # fetch
    if not args.no_fetch:
        fetch_script = SCRIPT_DIR / "fetch-youtube.js"
        if fetch_script.exists():
            print("=== YouTube fetch ===")
            subprocess.run(
                ["node", str(fetch_script)],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                cwd=str(BLOG_DIR), timeout=120,
            )

    # 대상 수집
    all_videos = []  # (filepath, video_dict)
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
            if args.reprocess or not v.get("summary"):
                all_videos.append((f, v))

    total = len(all_videos)
    print(f"\n=== 병렬 처리 시작: {total}개, workers={args.workers} ===\n")
    write_status("parallel_start", "", 0, total, f"workers={args.workers}")

    # 파일별 비디오 맵 (저장용)
    file_map = {}  # filepath → [videos]
    for f in sorted(DATA_DIR.glob("youtube-*.json")):
        try:
            file_map[f] = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue

    # 병렬 실행
    done = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {}
        for (filepath, video) in all_videos:
            future = executor.submit(process_one, video, args.reprocess)
            futures[future] = (filepath, video)

        for future in as_completed(futures):
            filepath, video = futures[future]
            result = future.result()
            if result["status"] == "ok":
                done += 1
                # 해당 파일 즉시 저장
                filepath.write_text(
                    json.dumps(file_map[filepath], ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
            else:
                failed += 1

            write_status("parallel", result.get("title", ""), done, total,
                         f"완료={done}, 실패={failed}")
            print(f"[{done+failed}/{total}] {result['status']}: {result.get('title','')[:40]}")

    print(f"\n=== 완료: {done}개 성공, {failed}개 실패 ===")

    # git push
    if done > 0:
        write_status("pushing", "", done, total, "git push 중...")
        os.chdir(BLOG_DIR)
        os.system("git add _data/sources/")
        os.system(f'git commit -m "[auto] youtube parallel reprocess {done}개 분석"')
        os.system("git push")
        write_status("complete", "", done, total, f"완료 {done}개")
        print("git push 완료")


if __name__ == "__main__":
    main()
