#!/usr/bin/env python3
"""
translate-transcripts.py — YouTube transcript 한글 번역 (OpenAI gpt-4.1-mini)

Usage:
  python scripts/translate-transcripts.py                  # 전체 (미번역만)
  python scripts/translate-transcripts.py --batch 1        # 배치 1만
  python scripts/translate-transcripts.py --video VIDEO_ID # 특정 1건
"""

import json, os, sys, glob, time, argparse, urllib.request
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BLOG_DIR = Path(__file__).parent.parent
DATA_DIR = BLOG_DIR / "_data" / "sources"

load_dotenv("C:/dev/01_projects/06_mcp-memory/.env")
API_KEY = os.environ.get("OPENAI_API_KEY", "")

MODEL = "gpt-4.1-mini"
BATCH_SIZE = 21

SYSTEM_PROMPT = """You are a professional translator. Translate the following English YouTube transcript into natural Korean.

Rules:
- Keep proper nouns, technical terms, product names, and brand names in English (e.g. Claude Code, Palantir AIP, Nano Banana 2, JSON, API)
- Translate naturally as if writing a Korean blog post, not word-by-word
- Keep the original paragraph structure (paragraphs are separated by double newlines)
- Do not add, remove, or summarize any content
- Output only the translated text, no explanations"""


def call_openai(text: str, max_retries: int = 2) -> str | None:
    url = "https://api.openai.com/v1/chat/completions"
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.3,
        "max_completion_tokens": 16384,
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            resp = urllib.request.urlopen(req, timeout=180)
            data = json.loads(resp.read().decode("utf-8"))
            text_out = data["choices"][0]["message"]["content"].strip()
            usage = data.get("usage", {})
            print(f"    tokens: in={usage.get('prompt_tokens',0)} out={usage.get('completion_tokens',0)}")
            return text_out
        except urllib.error.HTTPError as e:
            body_err = e.read().decode("utf-8", errors="replace")
            if e.code == 429 and attempt < max_retries:
                wait = 30 * (attempt + 1)
                print(f"  429 rate limit — {wait}s wait...")
                time.sleep(wait)
                continue
            print(f"  HTTP {e.code}: {body_err[:200]}")
            return None
        except Exception as e:
            print(f"  error: {e}")
            if attempt < max_retries:
                time.sleep(10)
                continue
            return None
    return None


def paragraphize(text: str) -> str:
    """4-5문장마다 단락 분리"""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    paragraphs = []
    current = []
    for s in sentences:
        current.append(s)
        if len(current) >= 4:
            paragraphs.append(' '.join(current))
            current = []
    if current:
        paragraphs.append(' '.join(current))
    return '\n\n'.join(paragraphs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, help="batch number")
    parser.add_argument("--video", type=str, help="single video_id")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not API_KEY:
        print("ERROR: OPENAI_API_KEY not found")
        sys.exit(1)

    # Load all videos
    json_files = sorted(DATA_DIR.glob("youtube-*.json"))
    all_videos = []
    for f in json_files:
        with open(f, encoding="utf-8") as fh:
            items = json.load(fh)
        for item in items:
            all_videos.append((f, item))

    print(f"total videos: {len(all_videos)}")

    # Filter
    if args.video:
        all_videos = [(f, v) for f, v in all_videos if v["video_id"] == args.video]
    elif args.batch:
        start = (args.batch - 1) * BATCH_SIZE
        end = start + BATCH_SIZE
        all_videos = all_videos[start:end]
        print(f"batch {args.batch}: items {start+1}-{min(end, len(all_videos)+start)}")

    # Skip already translated
    to_process = [(f, v) for f, v in all_videos if v.get("transcript") and not v.get("transcript_ko")]
    print(f"to process: {len(to_process)} (skipping {len(all_videos) - len(to_process)} already done or no transcript)")

    success = 0
    fail = 0

    for i, (filepath, video) in enumerate(to_process, 1):
        vid = video["video_id"]
        title = video.get("title", "")
        transcript = video.get("transcript", "")

        if not transcript:
            continue

        # Paragraphize first
        para_text = paragraphize(transcript)

        print(f"\n[{i}/{len(to_process)}] {vid} | {title[:50]}")
        print(f"  transcript: {len(transcript)} chars, {len(para_text.split(chr(10)+chr(10)))} paragraphs")

        if args.dry_run:
            continue

        translated = call_openai(para_text)
        if not translated:
            fail += 1
            print(f"  FAIL")
            continue

        # Save to file
        with open(filepath, encoding="utf-8") as fh:
            all_items = json.load(fh)

        for item in all_items:
            if item["video_id"] == vid:
                item["transcript_ko"] = translated
                break

        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(all_items, fh, ensure_ascii=False, indent=2)

        success += 1
        print(f"  OK: {len(translated)} chars")

        time.sleep(1)

    print(f"\n=== done: {success} ok, {fail} fail ===")


if __name__ == "__main__":
    main()
