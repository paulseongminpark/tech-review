#!/usr/bin/env python3
"""
fetch-deep-research.py — ChatGPT Deep Research → daily post raw content

Playwright + CDP Chrome으로 ChatGPT Deep Research 자동화.
Perplexity API 대체.

Usage: python scripts/fetch-deep-research.py [--date YYYY-MM-DD]

Task Scheduler: 매일 06:30 KST
사전 조건: CDP Chrome 실행 중 (자동 시작 로직 포함)
"""

import json, os, re, subprocess, sys, time, argparse
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).parent
BLOG_DIR = SCRIPT_DIR.parent
CONFIG_DIR = BLOG_DIR / "config"
PROMPT_DIR = BLOG_DIR / "perplexity-prompts" / "ko"
OUTPUT_DIR = BLOG_DIR / "_tmp"

CDP_URL = "http://127.0.0.1:9222"
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_PROFILE = r"C:\Users\pauls\.chrome-twitter-auto"

CHATGPT_DR_URL = "https://chatgpt.com/deep-research"

# 요일 → 프롬프트 파일
PROMPT_FILES = {
    0: "07-sunday-weekly.md",
    1: "01-monday-ai-ml.md",
    2: "02-tuesday-bigtech.md",
    3: "03-wednesday-startup.md",
    4: "04-thursday-opensource.md",
    5: "05-friday-hardware.md",
    6: "06-saturday-usecase.md",
}

MAX_WAIT_MINUTES = 25


def ensure_cdp_chrome():
    """CDP Chrome 실행 확인, 미실행 시 자동 시작"""
    import urllib.request
    try:
        urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=3)
        print("[CDP] 연결 OK")
        return True
    except Exception:
        print("[CDP] Chrome 미실행 — 자동 시작 중...")
        subprocess.Popen(
            [CHROME_EXE, f"--remote-debugging-port=9222",
             f"--user-data-dir={CHROME_PROFILE}", "--force-dark-mode"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for _ in range(10):
            time.sleep(2)
            try:
                urllib.request.urlopen(f"{CDP_URL}/json/version", timeout=3)
                print("[CDP] Chrome 자동 시작 완료")
                return True
            except Exception:
                pass
        print("[CDP] Chrome 시작 실패")
        return False


def load_prompt(post_date: str) -> tuple[str, str]:
    """요일별 프롬프트 로드 + 소스 리스트 주입"""
    y, m, d = map(int, post_date.split("-"))
    from datetime import date
    day = date(y, m, d).weekday()  # 0=월 ... 6=일
    # Python weekday: 0=Mon, JS getUTCDay: 0=Sun. 변환:
    js_day = (day + 1) % 7

    filename = PROMPT_FILES.get(js_day, "01-monday-ai-ml.md")
    filepath = PROMPT_DIR / filename
    if not filepath.exists():
        print(f"[WARN] 프롬프트 파일 없음: {filepath}, 기본 사용")
        filepath = PROMPT_DIR / "01-monday-ai-ml.md"

    prompt = filepath.read_text(encoding="utf-8")

    # TITLE/TAGS 라인 분리
    lines = prompt.split("\n")
    tags = ""
    prompt_lines = []
    for line in lines:
        if line.startswith("TAGS:"):
            tags = line.replace("TAGS:", "").strip()
        elif line.startswith("TITLE:"):
            pass  # skip
        else:
            prompt_lines.append(line)

    prompt = "\n".join(prompt_lines).strip()
    prompt = prompt.replace("{KEYWORDS_BLOCK}", "")
    prompt = prompt.replace("{DATE}", post_date)

    # 소스 리스트 주입 (있으면)
    sources_file = CONFIG_DIR / "news-sources.json"
    if sources_file.exists():
        sources = json.loads(sources_file.read_text(encoding="utf-8"))
        day_key = str(js_day)
        if day_key in sources:
            source_list = "\n".join(f"- {s}" for s in sources[day_key])
            prompt = f"아래 소스를 우선 확인하되, 추가로 공신력 있는 소스에서 자유롭게 수집 가능.\n필수 소스:\n{source_list}\n\n{prompt}"

    return prompt, tags


def run_deep_research(prompt: str, post_date: str) -> str | None:
    """Playwright로 ChatGPT Deep Research 실행 → 결과 텍스트 반환"""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()

        try:
            # 1. Deep Research 페이지 이동
            print("[DR] ChatGPT Deep Research 페이지 이동...")
            page.goto(CHATGPT_DR_URL, wait_until="networkidle", timeout=30000)
            time.sleep(3)

            # 2. 프롬프트 입력
            print("[DR] 프롬프트 입력 중...")
            textarea = page.locator("#prompt-textarea")
            textarea.click()
            time.sleep(0.5)
            textarea.fill(prompt)
            time.sleep(0.5)
            textarea.press("Enter")
            print("[DR] 전송 완료. Deep Research 대기 중...")

            # 3. 완료 대기 (최대 MAX_WAIT_MINUTES분)
            start = time.time()
            while time.time() - start < MAX_WAIT_MINUTES * 60:
                time.sleep(15)
                elapsed = int(time.time() - start)
                # 스트리밍 중지 버튼이 사라지면 완료
                stop_btn = page.locator('button[aria-label="스트리밍 중지"]')
                if stop_btn.count() > 0:
                    print(f"  [{elapsed}s] 아직 진행 중...")
                    continue

                # 완료 감지 — playwright frames로 iframe 콘텐츠 직접 접근
                time.sleep(3)
                for frame in page.frames:
                    try:
                        text = frame.evaluate("() => document.body ? document.body.innerText : ''")
                        if len(text) > 500 and ("Today in One Line" in text or "##" in text):
                            print(f"[DR] 완료! ({elapsed}초, {len(text)}자)")
                            return text
                    except Exception:
                        continue

                # iframe에 없으면 메인 페이지에서 찾기
                main_text = page.evaluate("""() => {
                    const articles = document.querySelectorAll('article');
                    for (let i = articles.length - 1; i >= 0; i--) {
                        const h = articles[i].querySelector('h5, h6');
                        if (h && h.textContent.includes('ChatGPT')) {
                            return articles[i].innerText;
                        }
                    }
                    return '';
                }""")
                if main_text and len(main_text) > 500:
                    print(f"[DR] 완료 (메인 페이지)! ({elapsed}초, {len(main_text)}자)")
                    return main_text

                print(f"  [{elapsed}s] 완료 감지 대기...")

            print(f"[DR] 타임아웃 ({MAX_WAIT_MINUTES}분)")
            return None

        finally:
            page.close()


def save_raw(content: str, post_date: str, tags: str):
    """raw 결과 저장"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    raw_file = OUTPUT_DIR / f"deep-research-{post_date}.md"
    header = f"TAGS: {tags}\n\n" if tags else ""
    raw_file.write_text(header + content, encoding="utf-8")
    print(f"[저장] {raw_file}")
    return raw_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()
    post_date = args.date

    print(f"=== Deep Research 파이프라인 시작 ({post_date}) ===")

    # CDP Chrome 확인
    if not ensure_cdp_chrome():
        sys.exit(1)

    # 프롬프트 로드
    prompt, tags = load_prompt(post_date)
    print(f"[프롬프트] {len(prompt)}자, tags: {tags}")

    # Deep Research 실행
    result = run_deep_research(prompt, post_date)
    if not result:
        print("[실패] Deep Research 결과 없음")
        sys.exit(1)

    # 저장
    raw_file = save_raw(result, post_date, tags)

    print(f"=== 완료: {raw_file} ===")
    print(f"다음 단계: claude -p 로 Why it matters 재작성")


if __name__ == "__main__":
    main()
