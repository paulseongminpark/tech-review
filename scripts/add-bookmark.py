#!/usr/bin/env python3
"""
add-bookmark.py — prinsss/twitter-web-exporter JSON → bookmarks.json 자동 추가

3-stage: Codex 구조화 → Claude -p WIM (Smart Brevity axiom)

Usage:
  python add-bookmark.py <bookmarks-raw.json>
  python add-bookmark.py  # inbox/ 폴더 최신 파일 자동 선택

Setup:
  pip install python-dotenv
"""

import json, os, re, subprocess, sys, tempfile, urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ── Paths ──────────────────────────────────────────────────────────────────
SCRIPT_DIR     = Path(__file__).parent
BLOG_DIR       = SCRIPT_DIR.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"

load_dotenv(BLOG_DIR / ".env")

# ── Prompt ─────────────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """\
다음 트위터 게시글을 아래 JSON 형식으로 처리해라.
반드시 JSON만 출력. 마크다운 코드블록 없이 순수 JSON만.

주의: why_it_matters 필드는 생성하지 마라. Why It Matters는 별도 단계에서 처리된다.

{{
  "whats_happening": "무슨 일인가 — 1-2문장, 핵심 사건·발표·발견을 구체적으로",
  "translation": "원문을 거의 그대로 한글로 번역. 요약 금지. 원문의 문장 구조·뉘앙스·어조를 최대한 살릴 것. 원문이 리스트면 리스트로, 문단이면 문단으로.",
  "tech_stack": ["언급된 실제 기술/도구/라이브러리명만"],
  "apply_points": ["개발자가 자신의 프로젝트에 적용할 수 있는 구체적 행동. 한 문장으로 간결하게. 파일 경로 금지. 일반론 금지."]
}}

규칙:
- whats_happening: 1-2문장. 사건 중심.
- translation: 번역이지 요약이 아님. 원문 길이의 90% 이상 유지. 영어 고유명사는 영어 유지.
- tech_stack: 없으면 []
- apply_points: 한 문장씩, 최대 3개. 파일 경로·backtick 금지. 50자 이내.
- 전부 한국어. 단, 고유명사(라이브러리명, 회사명, 인명)는 영어 유지.

트위터 내용:
{text}
"""

CLAUDE_PATH = "C:/Users/pauls/AppData/Roaming/npm/claude.cmd"
CODEX_CMD = r"C:\Users\pauls\AppData\Roaming\npm\codex.cmd"
WIM_PROMPT_PATH = BLOG_DIR / "config" / "wim-prompt.md"
ARTICLE_URL_RE = re.compile(r'^https?://(x\.com|twitter\.com)/i/article/\d+$')
CDP_URL = "http://127.0.0.1:9222"


def fetch_article_text(tweet_url: str) -> str | None:
    """CDP Chrome으로 X Article 본문을 가져온다.
    tweet_url: 트윗 URL (아티클이 포함된 트윗 페이지)
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None

    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP_URL)
            context = browser.contexts[0]
            page = context.new_page()
            try:
                page.goto(tweet_url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(5000)
                body = page.inner_text("body")

                # "Conversation" 이후 콘텐츠 추출
                idx = body.find("Conversation")
                content = body[idx + 12:].strip() if idx >= 0 else body

                # X UI 크롬 제거: author/handle/metrics 줄 스킵
                lines = content.split('\n')
                start = 0
                for i, line in enumerate(lines[:20]):
                    s = line.strip()
                    if re.match(r'^\d[\d,.]*[KMB]?$', s) or s in ('Subscribe', ''):
                        start = i + 1
                article = '\n'.join(lines[start:]).strip()

                return article[:4000] if len(article) > 100 else None
            finally:
                page.close()
                browser.close()
    except Exception as e:
        print(f" [CDP: {e}]", end="")
        return None


def generate_wim_twitter(summary: dict) -> str | None:
    """Claude -p로 Twitter 북마크 WIM 생성."""
    if not WIM_PROMPT_PATH.exists():
        return None
    wim_prompt = WIM_PROMPT_PATH.read_text(encoding="utf-8")
    compact = json.dumps({
        "title": summary.get("whats_happening", ""),
        "key_takeaways": [summary.get("whats_happening", "")],
        "tech_stack": summary.get("tech_stack", []),
        "apply_points": summary.get("apply_points", []),
        "sections": [],
    }, indent=2, ensure_ascii=False)
    full_prompt = wim_prompt + "\n" + compact
    try:
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)  # blog/.env의 만료 키 제거 → OAuth 사용
        result = subprocess.run(
            [CLAUDE_PATH, "-p", "--setting-sources", "user"],
            input=full_prompt.encode("utf-8"),
            capture_output=True, timeout=120,
            cwd="C:/windows/temp", env=env,
        )
        if result.returncode != 0:
            return None
        wim_text = result.stdout.decode("utf-8", errors="replace").strip()
        if not wim_text or len(wim_text) < 20:
            return None
        # 에러 메시지 거부
        if any(err in wim_text.lower() for err in ["credit balance", "rate limit", "unauthorized", "api key"]):
            return None
        # Why it matters 추출
        why_match = re.search(
            r"\*\*Why it matters:\*\*\s*(.+?)(?=\n\n|\n\*\*|\Z)",
            wim_text, re.DOTALL
        )
        return why_match.group(1).strip() if why_match else wim_text[:200]
    except Exception:
        return None

# ── Tweet extraction ────────────────────────────────────────────────────────
def extract_tweets(raw):
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict):
        items = raw.get("data") or raw.get("tweets") or raw.get("bookmarks") or []
    else:
        return []

    tweets = []
    for item in items:
        if not isinstance(item, dict):
            continue

        text = (
            item.get("full_text")
            or item.get("text")
            or item.get("legacy", {}).get("full_text", "")
        ).strip()
        if not text:
            continue

        user = item.get("user") or item.get("author") or {}
        if isinstance(user, str):
            author = user or "unknown"
        elif isinstance(user, dict):
            author = (
                user.get("screen_name")
                or user.get("username")
                or user.get("legacy", {}).get("screen_name", "unknown")
            )
        else:
            author = item.get("screen_name") or "unknown"

        tweet_id = item.get("rest_id") or item.get("id_str") or item.get("id") or ""

        url = (
            item.get("url")
            or item.get("tweet_url")
            or (f"https://x.com/{author}/status/{tweet_id}" if tweet_id else "")
        )

        created = item.get("created_at") or item.get("timestamp") or ""
        try:
            dt = datetime.strptime(created, "%a %b %d %H:%M:%S +0000 %Y")
            date = dt.strftime("%Y-%m-%d")
        except Exception:
            date = created[:10] if len(created) >= 10 else datetime.now().strftime("%Y-%m-%d")

        tweets.append({"id": tweet_id, "author": author, "text": text, "url": url, "date": date})

    return tweets


# ── Dedup ──────────────────────────────────────────────────────────────────
def load_existing(path):
    if not path.exists():
        return [], set()
    with open(path, encoding="utf-8") as f:
        bms = json.load(f)
    seen = set()
    for bm in bms:
        if bm.get("url"):
            seen.add(bm["url"])
        if bm.get("tweet_id"):
            seen.add(bm["tweet_id"])
    return bms, seen


# ── OpenAI API 직접 호출 ──────────────────────────────────────────────────────
def summarize_with_codex(text: str) -> dict | None:
    """OpenAI gpt-4.1-mini API 직접 호출로 분석 (Codex CLI sandbox 우회)"""
    from dotenv import load_dotenv as _ld
    _ld(Path("C:/dev/01_projects/06_mcp-memory/.env"))
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("  OPENAI_API_KEY 없음")
        return None

    prompt = PROMPT_TEMPLATE.format(text=text[:8000])

    try:
        body = json.dumps({
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "You are a tweet analyzer. Output ONLY valid JSON, no markdown code blocks."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_completion_tokens": 4096,
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        )
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read().decode("utf-8"))
        raw = data["choices"][0]["message"]["content"].strip()

        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())

        json_match = re.search(r"\{[\s\S]*\}", raw)
        if json_match:
            raw = json_match.group(0)

        return json.loads(raw)

    except json.JSONDecodeError as e:
        print(f"  JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        print(f"  오류: {e}")
        return None


# ── Codex CLI (ChatGPT 세션, OpenAI API 쿼터 우회) ────────────────────────────
def summarize_with_codex_cli(text: str) -> dict | None:
    """Codex CLI로 구조화. Windows cmd 래퍼 좀비 방지 위해 Thread.join + taskkill."""
    import tempfile, threading as _th
    tmp = Path(tempfile.mkdtemp(prefix="codex-bm-"))
    prompt_file = tmp / "prompt.txt"
    out_file = tmp / "out.json"
    try:
        prompt = (
            "아래 트윗 또는 기사 본문을 분석해 순수 JSON 객체 하나만 출력하라.\n"
            "마크다운 코드블록 금지. 설명 문장 금지. JSON만.\n\n"
            "필드 스펙:\n"
            "- whats_happening: 1-2문장. 사건·발표·발견 중심. 한국어.\n"
            "- translation: 한국어 번역. 요약 금지, 원문 90% 이상 유지. 영어 고유명사 영어 유지.\n"
            "- tech_stack: 언급된 실제 기술/도구/라이브러리/모델 배열. 없으면 빈 배열.\n"
            "- apply_points: 개발자 적용 행동. 한 문장씩 최대 3개, 각 50자 이내, 파일경로/backtick 금지.\n\n"
            f"본문:\n{text[:8000]}\n"
        )
        prompt_file.write_text(prompt, encoding="utf-8")

        result = [None]
        def _run():
            try:
                result[0] = subprocess.run(
                    [CODEX_CMD, "exec",
                     "--full-auto",
                     "--skip-git-repo-check",
                     "-o", str(out_file)],
                    stdin=open(str(prompt_file), "r", encoding="utf-8"),
                    capture_output=True, timeout=240,
                    text=True, encoding="utf-8", errors="replace",
                    cwd=str(BLOG_DIR),
                )
            except Exception as e:
                result[0] = e

        t = _th.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout=180)

        if t.is_alive():
            subprocess.run(
                "taskkill /F /IM codex.exe 2>nul & taskkill /F /IM Codex.exe 2>nul",
                shell=True, capture_output=True, timeout=10
            )
            print("  [Codex CLI] timeout (180s)")
            return None

        r = result[0]
        raw = ""
        if out_file.exists():
            raw = out_file.read_text(encoding="utf-8").strip()
        elif hasattr(r, "stdout"):
            raw = (r.stdout or "").strip()

        if not raw:
            rc = getattr(r, "returncode", "?")
            print(f"  [Codex CLI] 출력 없음 (rc={rc})")
            return None

        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        m = re.search(r"\{[\s\S]*\}", raw)
        if m:
            raw = m.group(0)
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  [Codex CLI] JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        print(f"  [Codex CLI] 오류: {e}")
        return None
    finally:
        try:
            prompt_file.unlink(missing_ok=True)
            out_file.unlink(missing_ok=True)
            tmp.rmdir()
        except Exception:
            pass


# ── Gemini API fallback ──────────────────────────────────────────────────────
def summarize_with_gemini(text: str) -> dict | None:
    """Gemini 2.5 Flash API로 구조화 (Codex 대체)"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("  [Gemini API] GEMINI_API_KEY 없음")
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = PROMPT_TEMPLATE.format(text=text[:8000])
        resp = model.generate_content(prompt)
        raw = resp.text.strip()
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  [Gemini API] JSON 파싱 실패: {e}")
        return None
    except Exception as e:
        err_str = str(e)
        if "429" in err_str or "quota" in err_str.lower():
            print("  [Gemini API] 쿼터 초과")
            return None
        print(f"  [Gemini API] 실패: {e}")
        return None


# ── Main ───────────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=None,
                        help="bookmarks-raw.json 경로 (없으면 inbox/ 자동 선택)")
    parser.add_argument("--use-gemini", action="store_true",
                        help="Codex 대신 Gemini Flash API로 구조화")
    parser.add_argument("--use-codex-cli", action="store_true",
                        help="OpenAI API 대신 Codex CLI로 구조화 (API 쿼터 우회, ChatGPT 세션)")
    args = parser.parse_args()

    if args.input_file:
        raw_path = Path(args.input_file)
    else:
        inbox = BLOG_DIR / "inbox"
        files = sorted(inbox.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not files:
            print("inbox/ 폴더에 JSON 파일 없음. bookmarks-raw.json을 inbox/에 넣어주세요.")
            sys.exit(1)
        raw_path = files[0]
        print(f"파일 자동 선택: {raw_path.name}")

    if not raw_path.exists():
        print(f"파일 없음: {raw_path}")
        sys.exit(1)

    with open(raw_path, encoding="utf-8") as f:
        raw = json.load(f)

    tweets = extract_tweets(raw)
    print(f"로드: {len(tweets)}개 트윗")

    bookmarks, seen = load_existing(BOOKMARKS_JSON)
    next_num = len(bookmarks) + 1
    added = 0

    # 신규 트윗 필터
    new_tweets = []
    for tw in tweets:
        key = tw["url"] or tw["id"]
        if key and key in seen:
            print(f"  스킵 (중복): @{tw['author']}")
            continue
        new_tweets.append(tw)

    if not new_tweets:
        print("새 북마크 없음.")
        return

    if args.use_gemini:
        summarize_fn = summarize_with_gemini
        engine_name = "Gemini"
    elif args.use_codex_cli:
        summarize_fn = summarize_with_codex_cli
        engine_name = "Codex CLI"
    else:
        summarize_fn = summarize_with_codex
        engine_name = "Codex"
    print(f"신규 {len(new_tweets)}개 → {engine_name} 순차 분석...")

    for tw in new_tweets:
        print(f"  분석 중: @{tw['author']} ...", end="", flush=True)
        analysis_text = tw["text"]

        # X Article 감지 — CDP로 본문 가져오기
        if ARTICLE_URL_RE.match(tw["text"].strip()):
            article = fetch_article_text(tw["url"])
            if article:
                tw["text"] = article[:500]   # 북마크 표시용
                analysis_text = article       # 분석용 전문
                print(" [Article→CDP]", end="", flush=True)
            else:
                print(" SKIP (X Article -- CDP 실패)")
                continue

        summary = summarize_fn(analysis_text)
        if not summary:
            print(" FAIL")
            continue
        # Stage 2: Claude WIM
        wim = generate_wim_twitter(summary)
        if wim:
            summary["why_it_matters"] = wim
            print(f" OK  WIM {summary.get('whats_happening', '')[:40]}")
        else:
            print(f" OK  WIM✗ {summary.get('whats_happening', '')[:40]}")
        bm = {
            "id": f"bm-{next_num:03d}",
            "author": tw["author"],
            "date": tw["date"],
            "added_at": datetime.now().strftime("%Y-%m-%d"),
            "url": tw["url"],
            "text": tw["text"],
            **summary,
        }
        if tw["id"]:
            bm["tweet_id"] = tw["id"]

        bookmarks.append(bm)
        key = tw["url"] or tw["id"]
        seen.add(key)
        next_num += 1
        added += 1

    if added == 0:
        print("새 북마크 없음.")
        return

    with open(BOOKMARKS_JSON, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)
    print(f"\n{added}개 추가 → {BOOKMARKS_JSON}")

    if os.environ.get("SKIP_GIT_PUSH") == "1":
        print("git push 스킵 (SKIP_GIT_PUSH=1)")
    else:
        os.chdir(BLOG_DIR)
        os.system("git add _data/bookmarks.json")
        os.system(f'git commit -m "[tech-review] Twitter Bookmarks {added}개 추가 ({engine_name})"')
        os.system("git push")
        print("git push 완료")


if __name__ == "__main__":
    main()
