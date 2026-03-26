#!/usr/bin/env python3
"""
generate-apply-points.py — GPT-5.4로 apply_points 생성
배치별 실행: python scripts/generate-apply-points.py --batch 1
"""

import json, os, sys, glob, time, argparse, urllib.request
from pathlib import Path
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
DATA_DIR = BLOG_DIR / "_data" / "sources"
WIM_PROMPT_PATH = BLOG_DIR / "config" / "wim-prompt.md"

# OpenAI key from mcp-memory .env
load_dotenv("C:/dev/01_projects/06_mcp-memory/.env")
API_KEY = os.environ.get("OPENAI_API_KEY", "")

MODEL = "gpt-5.4"
BATCH_SIZE = 21


def load_wim_prompt():
    return WIM_PROMPT_PATH.read_text(encoding="utf-8")


def call_openai(prompt: str, max_retries: int = 2) -> str | None:
    url = "https://api.openai.com/v1/chat/completions"
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_completion_tokens": 1024,
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=body, headers=headers)
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read().decode("utf-8"))
            text = data["choices"][0]["message"]["content"].strip()

            # usage logging
            usage = data.get("usage", {})
            inp = usage.get("prompt_tokens", 0)
            out = usage.get("completion_tokens", 0)
            print(f"    tokens: in={inp} out={out}")

            return text
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


def parse_apply_points(text: str) -> dict | None:
    """Parse WIM + axioms from GPT response into structured dict."""
    result = {"why_it_matters": "", "axioms": []}

    lines = text.strip().split("\n")
    current_label = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # **Why it matters:** ...
        if line.lower().startswith("**why it matters:**") or line.lower().startswith("why it matters:"):
            content = line.split(":", 1)[1].strip().strip("*").strip()
            result["why_it_matters"] = content
        elif line.startswith("**") and ":**" in line:
            # **The big picture:** ...
            parts = line.split(":**", 1)
            label = parts[0].strip("* ").strip()
            content = parts[1].strip().strip("*").strip() if len(parts) > 1 else ""
            if content:
                result["axioms"].append({"label": label, "content": content})

    if not result["why_it_matters"]:
        # fallback: just use the whole text
        result["why_it_matters"] = text.strip()

    return result


def get_all_videos():
    """Load all videos from all youtube JSON files."""
    videos = []
    files = sorted(DATA_DIR.glob("youtube-*.json"))
    for f in files:
        with open(f, encoding="utf-8") as fh:
            items = json.load(fh)
        for item in items:
            videos.append((f, item))
    return videos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, help="batch number (1-4)")
    parser.add_argument("--video", type=str, help="single video_id")
    parser.add_argument("--dry-run", action="store_true", help="show prompt only")
    args = parser.parse_args()

    if not API_KEY:
        print("ERROR: OPENAI_API_KEY not found")
        sys.exit(1)

    wim_prompt = load_wim_prompt()
    videos = get_all_videos()
    total = len(videos)
    print(f"total videos: {total}")

    # filter by batch or video
    if args.video:
        videos = [(f, v) for f, v in videos if v["video_id"] == args.video]
    elif args.batch:
        start = (args.batch - 1) * BATCH_SIZE
        end = start + BATCH_SIZE
        videos = videos[start:end]
        print(f"batch {args.batch}: items {start+1}-{min(end, total)}")

    # skip already processed
    to_process = [(f, v) for f, v in videos if not v.get("summary", {}).get("apply_points")]
    print(f"to process: {len(to_process)} (skipping {len(videos) - len(to_process)} already done)")

    success = 0
    fail = 0
    total_in = 0
    total_out = 0

    for i, (filepath, video) in enumerate(to_process, 1):
        vid = video["video_id"]
        title = video.get("title", "")
        summary = video.get("summary", {})

        # build input: summary without transcript
        summary_input = {
            "title": title,
            "sections": [{"heading": s.get("heading", ""), "body": s.get("body", "")[:500]}
                         for s in summary.get("sections", [])],
            "key_takeaways": summary.get("key_takeaways", []),
            "tech_stack": summary.get("tech_stack", []),
            "smart_brevity": summary.get("smart_brevity", {}),
        }

        prompt = wim_prompt + "\n\n" + json.dumps(summary_input, ensure_ascii=False, indent=2)

        print(f"\n[{i}/{len(to_process)}] {vid} | {title[:50]}")

        if args.dry_run:
            print(f"  prompt length: {len(prompt)} chars")
            continue

        result_text = call_openai(prompt)
        if not result_text:
            fail += 1
            print(f"  FAIL")
            continue

        apply_points = parse_apply_points(result_text)
        if not apply_points or not apply_points["why_it_matters"]:
            fail += 1
            print(f"  PARSE FAIL: {result_text[:100]}")
            continue

        # save back to file
        with open(filepath, encoding="utf-8") as fh:
            all_items = json.load(fh)

        for item in all_items:
            if item["video_id"] == vid:
                item["summary"]["apply_points"] = apply_points
                break

        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(all_items, fh, ensure_ascii=False, indent=2)

        success += 1
        print(f"  OK: {apply_points['why_it_matters'][:60]}...")

        # rate limit pause
        time.sleep(2)

    print(f"\n=== done: {success} ok, {fail} fail ===")


if __name__ == "__main__":
    main()
