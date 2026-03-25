#!/usr/bin/env python3
"""
structurize.py — YouTube transcript를 Smart Brevity 구조로 변환

Step 1: 원본 transcript → Smart Brevity 구조화 (Gemini Flash)
Step 2: Claude가 apply_points 작성 (별도 스크립트)

Usage:
  python scripts/structurize.py                    # 전체 (summary 없는 것만)
  python scripts/structurize.py --batch 1          # 배치 1만
  python scripts/structurize.py --video VIDEO_ID   # 특정 영상 1건
  python scripts/structurize.py --all              # 전체 강제 (기존 summary 덮어쓰기)
"""

import json, os, sys, re, glob, time, argparse, urllib.request
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
DATA_DIR = BLOG_DIR / "_data" / "sources"
PROMPT_PATH = BLOG_DIR / "config" / "structuring-prompt.md"

load_dotenv(BLOG_DIR / ".env")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# 배치 정의
BATCHES = {
    1: ["youtube-2026-03-05.json", "youtube-2026-03-07.json", "youtube-2026-03-08.json",
        "youtube-2026-03-09.json", "youtube-2026-03-12.json", "youtube-2026-03-14.json"],
    2: ["youtube-2026-03-16.json"],
    3: ["youtube-2026-03-17.json", "youtube-2026-03-18.json", "youtube-2026-03-19.json"],
    4: ["youtube-2026-03-20.json"],
    5: ["youtube-2026-03-21.json", "youtube-2026-03-22.json", "youtube-2026-03-23.json",
        "youtube-2026-03-24.json", "youtube-2026-03-25.json"],
}


def load_prompt_template():
    raw = PROMPT_PATH.read_text(encoding="utf-8")
    # {title}과 {transcript} 플레이스홀더 앞까지가 템플릿
    return raw


def call_gemini(prompt: str, max_retries: int = 2) -> str | None:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 8192},
    }).encode("utf-8")

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read().decode("utf-8"))
            text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            return text
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                wait = 30 * (attempt + 1)
                print(f"  429 쿼터 — {wait}초 대기...")
                time.sleep(wait)
                continue
            raise
    return None


def parse_json_response(text: str) -> dict | None:
    # 코드블록 제거
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text.strip())
    # 첫 번째 JSON 객체 추출
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None


def structurize_video(template: str, title: str, transcript: str) -> dict | None:
    prompt = template.replace("{title}", title).replace("{transcript}", transcript[:50000])

    raw = call_gemini(prompt)
    if not raw:
        return None

    result = parse_json_response(raw)
    if not result:
        print(f"  JSON 파싱 실패")
        return None

    # 기본 검증
    sections = result.get("sections", [])
    sb = result.get("smart_brevity", {})
    if len(sections) < 3:
        print(f"  sections {len(sections)}개 — 부족")
        return None
    if not sb.get("why"):
        print(f"  WIM 없음")
        return None

    return result


def get_unique_videos(files: list[str] | None = None):
    """유니크 영상 목록 반환 (첫 출현 기준)"""
    seen = set()
    videos = []

    json_files = sorted(DATA_DIR.glob("youtube-*.json"))
    if files:
        json_files = [DATA_DIR / f for f in files if (DATA_DIR / f).exists()]

    for f in json_files:
        data = json.load(open(f, encoding="utf-8"))
        if not isinstance(data, list):
            data = [data]
        for v in data:
            vid = v.get("video_id", "")
            if vid and vid not in seen:
                seen.add(vid)
                videos.append((f, vid, v))

    return videos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, help="배치 번호 (1-5)")
    parser.add_argument("--video", type=str, help="특정 video_id")
    parser.add_argument("--all", action="store_true", help="전체 강제 (기존 summary 덮어쓰기)")
    parser.add_argument("--dry", action="store_true", help="실행 안 하고 대상만 출력")
    args = parser.parse_args()

    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY 없음")
        sys.exit(1)

    template = load_prompt_template()

    # 대상 결정
    files = None
    if args.batch:
        files = BATCHES.get(args.batch)
        if not files:
            print(f"배치 {args.batch} 없음. 가능: {list(BATCHES.keys())}")
            sys.exit(1)

    videos = get_unique_videos(files)

    # 필터
    targets = []
    for f, vid, v in videos:
        if args.video and vid != args.video:
            continue
        if not v.get("transcript") or len(v.get("transcript", "")) < 100:
            continue
        if not args.all and v.get("summary"):
            continue
        targets.append((f, vid, v))

    print(f"=== 구조화 대상: {len(targets)}건 ===\n")

    if args.dry:
        for f, vid, v in targets:
            print(f"  {vid} | {v.get('title','')[:50]}")
        return

    success = 0
    fail = 0

    for i, (first_file, vid, v) in enumerate(targets):
        title = v.get("title", "")
        transcript = v.get("transcript", "")

        sys.stdout.write(f"[{i+1}/{len(targets)}] {vid} {title[:40]}... ")
        sys.stdout.flush()

        start = time.time()
        result = structurize_video(template, title, transcript)
        elapsed = time.time() - start

        if result:
            sec_count = len(result.get("sections", []))
            print(f"OK ({elapsed:.1f}초, {sec_count}sec)")

            # 모든 JSON 파일에서 해당 video_id에 summary 저장
            for f in sorted(DATA_DIR.glob("youtube-*.json")):
                data = json.load(open(f, encoding="utf-8"))
                if not isinstance(data, list):
                    data = [data]
                changed = False
                for item in data:
                    if item.get("video_id") == vid:
                        item["summary"] = result
                        changed = True
                if changed:
                    json.dump(data, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

            success += 1
        else:
            print(f"FAIL ({elapsed:.1f}초)")
            fail += 1

        time.sleep(1.5)  # rate limit

    print(f"\n=== 완료: 성공 {success}, 실패 {fail} ===")


if __name__ == "__main__":
    main()
