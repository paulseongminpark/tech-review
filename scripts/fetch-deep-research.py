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
            print("[DR] 전송 완료. Deep Research 시작 대기...")

            # 2.5. Deep Research 시작 확인 — 최소 30초 대기 후 리서치 진행 징후 확인
            dr_started = False
            for _ in range(12):  # 최대 60초 대기
                time.sleep(5)
                body_text = page.evaluate("() => document.body.innerText")
                # Deep Research 진행 징후: "리서치 중", "검색", "Browsing", "sources", iframe 등장
                if any(kw in body_text for kw in ["리서치", "검색 중", "Browsing", "출처", "sources found"]):
                    dr_started = True
                    print("[DR] Deep Research 시작 확인!")
                    break
                # 스트리밍 중지 버튼 = 무언가 생성 중
                stop_btn = page.locator('button[aria-label="스트리밍 중지"]')
                if stop_btn.count() > 0:
                    dr_started = True
                    print("[DR] 생성 시작 확인!")
                    break

            if not dr_started:
                print("[DR] Deep Research가 시작되지 않음 — 일반 응답일 수 있음")
                # 일반 응답이라도 결과가 있으면 수집
                time.sleep(10)

            # 3. 완료 대기 (최대 MAX_WAIT_MINUTES분)
            start = time.time()
            found_content = False
            while time.time() - start < MAX_WAIT_MINUTES * 60:
                time.sleep(15)
                elapsed = int(time.time() - start)

                # 스트리밍 중지 버튼이 있으면 아직 진행 중
                stop_btn = page.locator('button[aria-label="스트리밍 중지"]')
                if stop_btn.count() > 0:
                    print(f"  [{elapsed}s] 아직 진행 중...")
                    continue

                # 완료 감지 — iframe 전용 (메인 프레임은 사이드바 오염 위험)
                time.sleep(5)
                for frame in page.frames:
                    # 메인 프레임 스킵 (index 0 또는 URL이 chatgpt.com인 것)
                    try:
                        frame_url = frame.url
                    except Exception:
                        continue
                    if "chatgpt.com" in frame_url and "/c/" not in frame_url:
                        continue  # 메인 프레임 스킵

                    try:
                        text = frame.evaluate("() => document.body ? document.body.innerText : ''")
                        # 사이드바 오염 방지: "채팅 기록", "사이드바", "Ctrl" 등이 포함되면 스킵
                        if any(kw in text for kw in ["채팅 기록", "사이드바", "콘텐츠로 건너뛰기", "프로필 메뉴"]):
                            continue
                        # 실제 뉴스 콘텐츠 판별
                        if len(text) > 800 and ("Today in One Line" in text or ("## " in text and "matters" in text)):
                            print(f"[DR] 완료 (iframe)! ({elapsed}초, {len(text)}자)")
                            return text
                    except Exception:
                        continue

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
