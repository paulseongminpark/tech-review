#!/usr/bin/env python3
"""
fetch-deep-research.py — 3-Tier Fallback Deep Research Pipeline

Fallback chain: Perplexity(1차) → Gemini(2차) → ChatGPT(3차)
Playwright + CDP Chrome 자동화.

Usage:
  python scripts/fetch-deep-research.py [--date YYYY-MM-DD] [--provider perplexity|gemini|chatgpt]

Task Scheduler: 매일 05:00 KST (컴퓨터 wake 포함)
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

PERPLEXITY_URL = "https://www.perplexity.ai/"
GEMINI_URL = "https://gemini.google.com/app"
CHATGPT_DR_URL = "https://chatgpt.com/deep-research"

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
POLL_INTERVAL = 15


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
    day = date(y, m, d).weekday()
    js_day = (day + 1) % 7

    filename = PROMPT_FILES.get(js_day, "01-monday-ai-ml.md")
    filepath = PROMPT_DIR / filename
    if not filepath.exists():
        print(f"[WARN] 프롬프트 파일 없음: {filepath}, 기본 사용")
        filepath = PROMPT_DIR / "01-monday-ai-ml.md"

    prompt = filepath.read_text(encoding="utf-8")

    lines = prompt.split("\n")
    tags = ""
    prompt_lines = []
    for line in lines:
        if line.startswith("TAGS:"):
            tags = line.replace("TAGS:", "").strip()
        elif line.startswith("TITLE:"):
            pass
        else:
            prompt_lines.append(line)

    prompt = "\n".join(prompt_lines).strip()
    prompt = prompt.replace("{KEYWORDS_BLOCK}", "")
    prompt = prompt.replace("{DATE}", post_date)

    sources_file = CONFIG_DIR / "news-sources.json"
    if sources_file.exists():
        sources = json.loads(sources_file.read_text(encoding="utf-8"))
        day_key = str(js_day)
        if day_key in sources:
            source_list = "\n".join(f"- {s}" for s in sources[day_key])
            prompt = f"아래 소스를 우선 확인하되, 추가로 공신력 있는 소스에서 자유롭게 수집 가능.\n필수 소스:\n{source_list}\n\n{prompt}"

    return prompt, tags


def validate_content(text: str) -> bool:
    """DR 결과가 유효한 daily post 콘텐츠인지 판별"""
    if not text or len(text) < 800:
        return False
    if "Today in One Line" in text:
        return True
    if "## " in text and "matters" in text:
        return True
    if text.count("## ") >= 3:
        return True
    return False


# ── 1차: Perplexity ──────────────────────────────────────────

def run_perplexity_dr(prompt: str, post_date: str) -> str | None:
    """Perplexity Deep Research (Pro 500/일). 메인 페이지에 결과 출력 — iframe 없음."""
    from playwright.sync_api import sync_playwright

    print("[1차] Perplexity Deep Research 시도...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()

        try:
            page.goto(PERPLEXITY_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)

            # 입력창 찾기
            textarea = page.locator("textarea").first
            if textarea.count() == 0:
                print("[Perplexity] 입력창 없음")
                return None

            textarea.click()
            time.sleep(0.5)

            # "/" 입력 → 포커스 모드 메뉴 트리거
            textarea.press("/")
            time.sleep(2)

            # "심층 리서치" 선택
            dr_clicked = False
            for label in ["심층 리서치", "Deep Research", "deep research"]:
                try:
                    option = page.get_by_text(label, exact=False)
                    if option.count() > 0:
                        option.first.click()
                        dr_clicked = True
                        print(f"[Perplexity] '{label}' 모드 선택")
                        time.sleep(1)
                        break
                except Exception:
                    continue

            if not dr_clicked:
                print("[Perplexity] 심층 리서치 메뉴 없음 — Escape 후 일반 모드 시도")
                page.keyboard.press("Escape")
                time.sleep(0.5)
                # textarea 재취득 ("/" 입력이 남아있을 수 있음)
                textarea = page.locator("textarea").first
                textarea.fill("")
                time.sleep(0.3)

            # 프롬프트 입력
            textarea = page.locator("textarea").first
            textarea.fill(prompt)
            time.sleep(0.5)

            # 전송: 버튼 우선, 없으면 Enter
            submit = page.locator('button[aria-label="제출"], button[aria-label="Submit"]')
            if submit.count() > 0:
                submit.first.click()
            else:
                textarea.press("Enter")

            print("[Perplexity] 전송 완료. 결과 대기...")

            # 결과 대기 — .prose 요소 polling
            start = time.time()
            last_len = 0
            stable_count = 0

            while time.time() - start < MAX_WAIT_MINUTES * 60:
                time.sleep(POLL_INTERVAL)
                elapsed = int(time.time() - start)

                text = page.evaluate("""() => {
                    const els = document.querySelectorAll('.prose');
                    let t = '';
                    els.forEach(el => t += el.innerText + '\\n');
                    return t;
                }""")

                curr_len = len(text)

                if validate_content(text):
                    if curr_len == last_len and curr_len > 0:
                        stable_count += 1
                        if stable_count >= 2:
                            print(f"[Perplexity] 완료! ({elapsed}초, {curr_len}자)")
                            return text
                    else:
                        stable_count = 0
                    print(f"  [{elapsed}s] 수신 중... ({curr_len}자)")
                else:
                    stable_count = 0
                    print(f"  [{elapsed}s] 대기... ({curr_len}자)")

                last_len = curr_len

            # 타임아웃이어도 유효 콘텐츠면 반환
            text = page.evaluate("""() => {
                const els = document.querySelectorAll('.prose');
                let t = '';
                els.forEach(el => t += el.innerText + '\\n');
                return t;
            }""")
            if validate_content(text):
                print(f"[Perplexity] 타임아웃이지만 유효 콘텐츠 ({len(text)}자)")
                return text

            print(f"[Perplexity] 타임아웃 ({MAX_WAIT_MINUTES}분)")
            return None

        except Exception as e:
            print(f"[Perplexity] 에러: {e}")
            return None
        finally:
            page.close()


# ── 2차: Gemini ──────────────────────────────────────────────

def run_gemini_dr(prompt: str, post_date: str) -> str | None:
    """Gemini Deep Research (Pro 20/일)."""
    from playwright.sync_api import sync_playwright

    print("[2차] Gemini Deep Research 시도...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()

        try:
            page.goto(GEMINI_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)

            # Deep Research 모드 활성화 시도
            dr_activated = False
            for label in ["Deep Research", "심층 연구", "심층 리서치"]:
                try:
                    el = page.get_by_text(label, exact=False)
                    if el.count() > 0:
                        el.first.click()
                        dr_activated = True
                        print(f"[Gemini] '{label}' 모드 활성화")
                        time.sleep(2)
                        break
                except Exception:
                    continue

            if not dr_activated:
                # 모델 드롭다운에서 Deep Research 찾기
                model_btn = page.locator('button:has-text("모델"), button:has-text("Model"), [class*="model-selector"]')
                if model_btn.count() > 0:
                    model_btn.first.click()
                    time.sleep(1)
                    for label in ["Deep Research", "심층 연구"]:
                        try:
                            opt = page.get_by_text(label, exact=False)
                            if opt.count() > 0:
                                opt.first.click()
                                dr_activated = True
                                print(f"[Gemini] 모델 메뉴에서 '{label}' 선택")
                                time.sleep(2)
                                break
                        except Exception:
                            continue

            if not dr_activated:
                print("[Gemini] Deep Research 모드를 찾을 수 없음 — 일반 모드로 시도")

            # 입력창 찾기
            input_el = None
            for sel in [".ql-editor", "[contenteditable='true']", "textarea", 'div[role="textbox"]']:
                try:
                    el = page.locator(sel).first
                    if el.count() > 0:
                        input_el = el
                        break
                except Exception:
                    continue

            if not input_el:
                print("[Gemini] 입력창 없음")
                return None

            input_el.click()
            time.sleep(0.5)

            # 프롬프트 입력
            try:
                input_el.fill(prompt)
            except Exception:
                page.keyboard.type(prompt, delay=5)

            time.sleep(0.5)

            # 전송
            sent = False
            for sel in ['button[aria-label="전송"]', 'button[aria-label="Send"]',
                        'button[aria-label="메시지 전송"]', 'button[aria-label="Send message"]',
                        '.send-button', 'button[data-test-id="send-button"]']:
                try:
                    btn = page.locator(sel)
                    if btn.count() > 0:
                        btn.first.click()
                        sent = True
                        break
                except Exception:
                    continue

            if not sent:
                page.keyboard.press("Enter")

            print("[Gemini] 전송 완료. 결과 대기...")

            # 결과 대기
            start = time.time()
            last_len = 0
            stable_count = 0

            while time.time() - start < MAX_WAIT_MINUTES * 60:
                time.sleep(POLL_INTERVAL)
                elapsed = int(time.time() - start)

                text = page.evaluate("""() => {
                    // Gemini 응답 영역 탐색
                    const selectors = [
                        '.model-response-text', '.response-content',
                        '.markdown-main-panel', 'message-content',
                        '.conversation-container .model-response',
                        '[class*="response"]', '[class*="message-text"]',
                    ];
                    for (const sel of selectors) {
                        const els = document.querySelectorAll(sel);
                        if (els.length > 0) {
                            let t = '';
                            els.forEach(el => t += el.innerText + '\\n');
                            if (t.trim().length > 100) return t;
                        }
                    }
                    // Fallback: 마지막 응답 블록
                    const all = document.querySelectorAll('[class*="response"], [class*="model"]');
                    if (all.length > 0) return all[all.length - 1].innerText;
                    return '';
                }""")

                curr_len = len(text)

                if validate_content(text):
                    if curr_len == last_len and curr_len > 0:
                        stable_count += 1
                        if stable_count >= 2:
                            print(f"[Gemini] 완료! ({elapsed}초, {curr_len}자)")
                            return text
                    else:
                        stable_count = 0
                    print(f"  [{elapsed}s] 수신 중... ({curr_len}자)")
                else:
                    stable_count = 0
                    print(f"  [{elapsed}s] 대기... ({curr_len}자)")

                last_len = curr_len

            text = page.evaluate("""() => {
                const all = document.querySelectorAll('[class*="response"], [class*="model"]');
                if (all.length > 0) return all[all.length - 1].innerText;
                return '';
            }""")
            if validate_content(text):
                print(f"[Gemini] 타임아웃이지만 유효 콘텐츠 ({len(text)}자)")
                return text

            print(f"[Gemini] 타임아웃 ({MAX_WAIT_MINUTES}분)")
            return None

        except Exception as e:
            print(f"[Gemini] 에러: {e}")
            return None
        finally:
            page.close()


# ── 3차: ChatGPT ─────────────────────────────────────────────

def run_chatgpt_dr(prompt: str, post_date: str) -> str | None:
    """ChatGPT Deep Research (Plus 25/월). iframe에서 결과 추출."""
    from playwright.sync_api import sync_playwright

    print("[3차] ChatGPT Deep Research 시도...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()

        try:
            page.goto(CHATGPT_DR_URL, wait_until="networkidle", timeout=30000)
            time.sleep(3)

            textarea = page.locator("#prompt-textarea")
            textarea.click()
            time.sleep(0.5)
            textarea.fill(prompt)
            time.sleep(0.5)
            textarea.press("Enter")
            print("[ChatGPT] 전송 완료. Deep Research 시작 대기...")

            # DR 시작 확인
            dr_started = False
            for _ in range(12):
                time.sleep(5)
                body_text = page.evaluate("() => document.body.innerText")
                if any(kw in body_text for kw in ["리서치", "검색 중", "Browsing", "출처", "sources found"]):
                    dr_started = True
                    print("[ChatGPT] Deep Research 시작 확인!")
                    break
                stop_btn = page.locator('button[aria-label="스트리밍 중지"]')
                if stop_btn.count() > 0:
                    dr_started = True
                    print("[ChatGPT] 생성 시작 확인!")
                    break

            if not dr_started:
                print("[ChatGPT] Deep Research가 시작되지 않음")
                time.sleep(10)

            # 완료 대기
            start = time.time()
            while time.time() - start < MAX_WAIT_MINUTES * 60:
                time.sleep(POLL_INTERVAL)
                elapsed = int(time.time() - start)

                stop_btn = page.locator('button[aria-label="스트리밍 중지"]')
                if stop_btn.count() > 0:
                    print(f"  [{elapsed}s] 진행 중...")
                    continue

                time.sleep(5)
                for frame in page.frames:
                    try:
                        frame_url = frame.url
                    except Exception:
                        continue
                    if "chatgpt.com" in frame_url and "/c/" not in frame_url:
                        continue

                    try:
                        text = frame.evaluate("() => document.body ? document.body.innerText : ''")
                        if any(kw in text for kw in ["채팅 기록", "사이드바", "콘텐츠로 건너뛰기", "프로필 메뉴"]):
                            continue
                        if validate_content(text):
                            print(f"[ChatGPT] 완료! ({elapsed}초, {len(text)}자)")
                            return text
                    except Exception:
                        continue

                print(f"  [{elapsed}s] 완료 감지 대기...")

            print(f"[ChatGPT] 타임아웃 ({MAX_WAIT_MINUTES}분)")
            return None

        except Exception as e:
            print(f"[ChatGPT] 에러: {e}")
            return None
        finally:
            page.close()


# ── Main ─────────────────────────────────────────────────────

def save_raw(content: str, post_date: str, tags: str, provider: str):
    """raw 결과 저장"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    raw_file = OUTPUT_DIR / f"deep-research-{post_date}.md"
    header = f"TAGS: {tags}\nSOURCE: {provider}\n\n"
    raw_file.write_text(header + content, encoding="utf-8")
    print(f"[저장] {raw_file} (source: {provider})")
    return raw_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--provider", choices=["perplexity", "gemini", "chatgpt"],
                        help="특정 provider만 사용 (fallback 건너뜀)")
    args = parser.parse_args()
    post_date = args.date

    print(f"=== Deep Research 3-Tier Fallback ({post_date}) ===")

    if not ensure_cdp_chrome():
        sys.exit(1)

    prompt, tags = load_prompt(post_date)
    print(f"[프롬프트] {len(prompt)}자, tags: {tags}")

    # Fallback chain: Perplexity → Gemini → ChatGPT
    providers = [
        ("perplexity", run_perplexity_dr),
        ("gemini", run_gemini_dr),
        ("chatgpt", run_chatgpt_dr),
    ]

    if args.provider:
        providers = [(n, f) for n, f in providers if n == args.provider]

    result = None
    used_provider = None
    for name, func in providers:
        result = func(prompt, post_date)
        if result:
            used_provider = name
            break
        print(f"[{name}] 실패 — 다음 provider로 fallback\n")

    if not result:
        print("[FAIL] 모든 provider 실패")
        sys.exit(1)

    raw_file = save_raw(result, post_date, tags, used_provider)
    print(f"=== 완료: {raw_file} (provider: {used_provider}) ===")
    print(f"다음 단계: run-daily-pipeline.py Step 2 (Why it matters 재작성)")


if __name__ == "__main__":
    main()
