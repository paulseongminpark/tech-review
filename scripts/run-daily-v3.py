#!/usr/bin/env python3
"""Daily Post v3 — 요일별 무료 소스 + Claude Sonnet 파이프라인"""
import json, sys, os, re, subprocess, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

BLOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(BLOG, "_tmp")
SCRIPTS = os.path.join(BLOG, "scripts")
CONFIG = os.path.join(BLOG, "config")
KST = timezone(timedelta(hours=9))
POST_DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.now(KST).strftime("%Y-%m-%d")
DOW = datetime.strptime(POST_DATE, "%Y-%m-%d").weekday()  # 0=월 6=일
UA = "Mozilla/5.0 (TechReview Bot)"
CLAUDE_CMD = r"C:\Users\pauls\AppData\Roaming\npm\claude.cmd"
LOG = []
ANY_FAIL = False

os.makedirs(TMP, exist_ok=True)

# ── 요일별 설정 ──────────────────────────────────────────
DAY_CONFIG = {
    0: {"topic": "AI/ML",       "tags": "ai-ml, models, research, benchmarks"},
    1: {"topic": "BigTech",     "tags": "bigtech, google, microsoft, meta, apple, nvidia"},
    2: {"topic": "Startup",     "tags": "ai-industry, business-model, enterprise-ai, vertical-ai"},
    3: {"topic": "OpenSource",  "tags": "opensource, developer-tools, github, frameworks"},
    4: {"topic": "Hardware",    "tags": "hardware, chips, datacenter, cloud, infrastructure"},
    5: {"topic": "UseCase",     "tags": "ai-usecase, enterprise, adoption, regulation"},
    6: {"topic": "Weekly",      "tags": "weekly-review, ai-trends, tech-summary"},
}

DAY_TOPIC = DAY_CONFIG[DOW]["topic"]
DAY_TAGS = DAY_CONFIG[DOW]["tags"]
DAY_TAGS_LIST = [t.strip() for t in DAY_TAGS.split(",")]

# ── 요일별 소스 URL ──────────────────────────────────────
COMMON_SOURCES = {
    "hn": ("HN API", "https://hacker-news.firebaseio.com/v0/topstories.json", "hn"),
    "tc": ("TechCrunch RSS", "https://techcrunch.com/feed/", "rss"),
    "lobsters": ("Lobsters", "https://lobste.rs/hottest.json", "lobsters"),
}

DAY_SOURCES = {
    0: {  # 월 AI/ML
        "arxiv_ai": ("arXiv cs.AI", "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10", "arxiv"),
        "arxiv_cl": ("arXiv cs.CL", "https://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=10", "arxiv"),
        "r_ml": ("r/MachineLearning", "https://www.reddit.com/r/MachineLearning/hot.json?limit=15", "reddit"),
        "r_llama": ("r/LocalLLaMA", "https://www.reddit.com/r/LocalLLaMA/hot.json?limit=15", "reddit"),
        "r_claude": ("r/ClaudeAI", "https://www.reddit.com/r/ClaudeAI/hot.json?limit=10", "reddit"),
        "openai_blog": ("OpenAI Blog", "https://openai.com/blog/rss.xml", "rss"),
        "hf_blog": ("HuggingFace Blog", "https://huggingface.co/blog/feed.xml", "rss"),
        "deepmind": ("DeepMind Blog", "https://blog.google/technology/ai/rss/", "rss"),
        "vb": ("VentureBeat", "https://venturebeat.com/feed/", "rss"),
    },
    1: {  # 화 BigTech
        "verge": ("The Verge", "https://www.theverge.com/rss/index.xml", "atom"),
        "ars": ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "rss"),
        "r_tech": ("r/technology", "https://www.reddit.com/r/technology/hot.json?limit=15", "reddit"),
    },
    2: {  # 수 Startup
        "ph": ("Product Hunt", "https://www.producthunt.com/feed", "rss"),
        "r_startups": ("r/startups", "https://www.reddit.com/r/startups/hot.json?limit=10", "reddit"),
    },
    3: {  # 목 OpenSource
        "r_prog": ("r/programming", "https://www.reddit.com/r/programming/hot.json?limit=15", "reddit"),
        "r_selfhosted": ("r/SelfHosted", "https://www.reddit.com/r/selfhosted/hot.json?limit=10", "reddit"),
        "newstack": ("The New Stack", "https://thenewstack.io/feed/", "rss"),
        "infoq": ("InfoQ", "https://feed.infoq.com/", "rss"),
        "devto": ("Dev.to", "https://dev.to/feed", "rss"),
        "gh_blog": ("GitHub Blog", "https://github.blog/feed/", "rss"),
    },
    4: {  # 금 Hardware
        "ars": ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "rss"),
        "verge": ("The Verge", "https://www.theverge.com/rss/index.xml", "atom"),
        "vb": ("VentureBeat", "https://venturebeat.com/feed/", "rss"),
    },
    5: {  # 토 UseCase
        "mitr": ("MIT Tech Review", "https://www.technologyreview.com/feed/", "rss"),
        "vb": ("VentureBeat", "https://venturebeat.com/feed/", "rss"),
        "r_artificial": ("r/artificial", "https://www.reddit.com/r/artificial/hot.json?limit=10", "reddit"),
        "r_futuro": ("r/Futurology", "https://www.reddit.com/r/Futurology/hot.json?limit=10", "reddit"),
    },
    6: {},  # 아래서 합산
}

# 일요일은 월~토 전체 합산
_all = {}
for d in range(6):
    _all.update(DAY_SOURCES.get(d, {}))
DAY_SOURCES[6] = _all


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.append(line)


def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_body(url, max_chars=4000):
    try:
        html = fetch_url(url, timeout=10)
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except:
        return ""


# ── 파서 ────────────────────────────────────────────────
def parse_hn(url):
    items = []
    top_ids = json.loads(fetch_url(url))[:30]
    for sid in top_ids:
        item = json.loads(fetch_url(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"))
        if item.get("score", 0) >= 30:
            items.append({"title": item.get("title",""), "url": item.get("url",""),
                          "score": item.get("score",0), "comments": item.get("descendants",0)})
    return items

def parse_rss(url):
    xml = fetch_url(url)
    root = ET.fromstring(xml)
    return [{"title": i.find("title").text or "", "url": i.find("link").text or "", "score": 0}
            for i in root.findall(".//item")[:15] if i.find("title") is not None]

def parse_atom(url):
    xml = fetch_url(url)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    return [{"title": e.find("a:title",ns).text.strip(), "url": e.find("a:link",ns).get("href",""), "score": 0}
            for e in root.findall("a:entry",ns)[:15] if e.find("a:title",ns) is not None]

def parse_reddit(url):
    data = json.loads(fetch_url(url))
    items = []
    for child in data.get("data",{}).get("children",[]):
        d = child.get("data",{})
        items.append({"title": d.get("title",""), "url": d.get("url",""),
                       "score": d.get("score",0), "comments": d.get("num_comments",0)})
    return items

def parse_lobsters(url):
    data = json.loads(fetch_url(url))
    return [{"title": i["title"], "url": i["url"], "score": i["score"],
             "tags": i.get("tags",[])} for i in data[:15]]

def parse_arxiv(url):
    xml = fetch_url(url)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    items = []
    for e in root.findall("a:entry", ns)[:10]:
        title = e.find("a:title",ns).text.strip().replace("\n"," ")
        abstract = (e.find("a:summary",ns).text or "").strip().replace("\n"," ")[:300]
        link = e.find("a:id",ns).text.strip()
        items.append({"title": title, "url": link, "score": 0, "abstract": abstract})
    return items

PARSERS = {"hn": parse_hn, "rss": parse_rss, "atom": parse_atom,
           "reddit": parse_reddit, "lobsters": parse_lobsters, "arxiv": parse_arxiv}


# ── Step 1: 소스 수집 ──────────────────────────────────
log(f"=== Daily Post v3 시작 ({POST_DATE}, {['월','화','수','목','금','토','일'][DOW]} {DAY_TOPIC}) ===")
log("[Step 1] 소스 수집...")

all_sources = {**COMMON_SOURCES, **DAY_SOURCES.get(DOW, {})}
collected = []
source_count = 0

for key, (name, url, parser_type) in all_sources.items():
    try:
        items = PARSERS[parser_type](url)
        for item in items:
            item["_source"] = key
            item["_source_name"] = name
        collected.extend(items)
        source_count += 1
        log(f"  {name}: {len(items)}건")
    except Exception as e:
        log(f"  {name}: FAIL ({str(e)[:60]})")

log(f"  수집 완료: {len(collected)}건 from {source_count}개 소스")

if source_count < 3:
    log("[FAIL] 소스 3개 미만. 중단.")
    ANY_FAIL = True

# raw 저장
raw_path = os.path.join(TMP, f"sources-raw-{POST_DATE}.json")
with open(raw_path, "w", encoding="utf-8") as f:
    json.dump(collected, f, ensure_ascii=False, indent=2)


# ── Step 2: 선별 ───────────────────────────────────────
log("[Step 2] 선별...")

# news-sources.json 도메인 로드
ns_path = os.path.join(CONFIG, "news-sources.json")
ns_domains = []
if os.path.exists(ns_path):
    ns_data = json.loads(Path(ns_path).read_text(encoding="utf-8"))
    ns_domains = ns_data.get(str(DOW), ns_data.get(str(DOW+1), []))

# keywords-log.md 최근 7일 키워드 로드
kw_log_path = os.path.join(BLOG, "perplexity-prompts", "keywords-log.md")
recent_keywords = set()
if os.path.exists(kw_log_path):
    with open(kw_log_path, "r", encoding="utf-8") as f:
        for line in f.readlines()[-50:]:
            recent_keywords.update(w.lower().strip() for w in line.split(",") if len(w.strip()) > 3)

# 랭킹
for item in collected:
    base = item.get("score", 0)
    title_lower = item["title"].lower()
    words = [w for w in title_lower.split() if len(w) > 4]

    # 교차 출현 보너스
    cross = sum(1 for other in collected
                if other["_source"] != item["_source"]
                and any(w in other["title"].lower() for w in words[:3]))

    # 도메인 매치 보너스
    item_domain = ""
    try:
        from urllib.parse import urlparse
        item_domain = urlparse(item.get("url","")).netloc.replace("www.","")
    except:
        pass
    domain_match = 1 if any(d in item_domain for d in ns_domains) else 0

    # 최근 키워드 중복 감점
    keyword_dup = sum(1 for w in words if w in recent_keywords)

    item["_rank"] = base + cross * 200 + domain_match * 50 - keyword_dup * 20

collected.sort(key=lambda x: x["_rank"], reverse=True)
selected = collected[:10]

log(f"  선별 {len(selected)}건:")
for i, item in enumerate(selected):
    log(f"    {i+1}. [{item['_source_name']}] {item['title'][:55]} (rank={item['_rank']})")


# ── Step 3: 본문 추출 ──────────────────────────────────
log("[Step 3] 본문 추출...")
for item in selected:
    url = item.get("url", "")
    if url and "news.ycombinator.com" not in url and "arxiv.org/abs" not in url:
        item["body"] = fetch_body(url)
        log(f"    {item['title'][:35]}... → {len(item.get('body',''))}자")
    else:
        item["body"] = item.get("abstract", "")

selected_path = os.path.join(TMP, f"sources-selected-{POST_DATE}.json")
with open(selected_path, "w", encoding="utf-8") as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)


# ── Step 4: Claude Sonnet 가공 ──────────────────────────
log("[Step 4] Claude Sonnet 가공...")

wim_prompt = ""
wim_path = os.path.join(CONFIG, "wim-prompt.md")
if os.path.exists(wim_path):
    with open(wim_path, "r", encoding="utf-8") as f:
        wim_prompt = f.read()

claude_prompt = f"""너는 tech-review 블로그의 Daily Post 작성자다. 한국어로 작성한다.

오늘은 {['월','화','수','목','금','토','일'][DOW]}요일이다. 주제: {DAY_TOPIC}.

## 입력
아래 JSON은 오늘 수집한 테크 뉴스 상위 10건이다. 각 항목에 title, url, body(기사 본문 일부)가 있다.

```json
{json.dumps(selected, ensure_ascii=False)[:15000]}
```

## 작성자(Paul)의 프로젝트 컨텍스트 (Why it matters 작성용 — 독자에게 노출 금지)
멀티AI 조율 시스템, 외부 메모리 지식그래프(4685+ 노드), 자동 뉴스 수집 파이프라인, Next.js 포트폴리오, 컨텍스트 엔지니어링 전략. 개인 지식그래프 기반 AI 시스템을 운영하는 개발자.
주의: Why it matters에서 내부 프로젝트명(orchestration, mcp-memory 등)을 직접 쓰지 마라. "멀티AI 조율 시스템", "지식그래프 기반 메모리", "자동화 파이프라인" 등 독자가 이해할 수 있는 일반 표현으로 풀어 써라.

## 작업
1. 10건 중 가장 중요한 3건을 선택 ({DAY_TOPIC} 주제 우선)
3. 각 3건에 대해 Smart Brevity 형식으로 작성

## 출력 형식 (정확히 지켜라)
---
layout: post
title: "3건 제목 나열"
date: {POST_DATE}
lang: ko
permalink: /ko/{POST_DATE.replace('-','/')}/daily-tech-review/
pair: {POST_DATE}-daily-tech-review
tags: [{', '.join(f'"{t}"' for t in DAY_TAGS_LIST)}]
source_type: free-sources
---

## Today in One Line
한 문장 요약

---

## 1. 제목

본문 설명 (최소 3문장, body의 구체적 팩트/수치/인용)

**Why it matters:** 위 Paul 프로젝트 컨텍스트를 참고해 구체적으로 연결. 일반론 금지.

- 불릿 1 (body에서 추출)
- 불릿 2
- 불릿 3

**What's next:** 전망 1-2문장

**Source:** [제목](URL)

---

(2, 3도 동일)

## Comments

## 규칙
- body의 실제 내용만 사용. 없는 팩트 지어내기 금지.
- 인라인 코드 백틱 사용 금지. 기술 용어도 일반 텍스트.
- ~다 체.
- front matter는 위 형식 그대로. 수정하지 마라.
- 마크다운 파일 전체를 출력. 설명/부연 없이 파일 내용만."""

post_path = os.path.join(TMP, f"final-{POST_DATE}.md")
prompt_path = os.path.join(TMP, f"prompt-{POST_DATE}.txt")
Path(prompt_path).write_text(claude_prompt, encoding="utf-8")
log(f"  프롬프트: {len(claude_prompt)}자")

for attempt in range(2):
    try:
        with open(prompt_path, "r", encoding="utf-8") as pf:
            result = subprocess.run(
                [CLAUDE_CMD, "-p", "--model", "claude-sonnet-4-6", "--output-format", "text"],
                stdin=pf, capture_output=True, timeout=300, cwd=BLOG
            )
        output = result.stdout.decode("utf-8", errors="replace").strip()
        # 코드블록 감싸기 제거 (```markdown ... ```)
        output = re.sub(r'^```\w*\n', '', output)
        output = re.sub(r'\n```\s*$', '', output)
        # front matter(---) 이전 junk 제거
        fm_match = re.search(r'^---\s*\n', output, re.MULTILINE)
        if fm_match and fm_match.start() > 0:
            output = output[fm_match.start():]

        if len(output) >= 500:
            Path(post_path).write_text(output, encoding="utf-8")
            log(f"  [OK] {len(output)}자 (attempt {attempt+1})")
            break
        else:
            log(f"  [WARN] 출력 부족 ({len(output)}자), retry...")
    except subprocess.TimeoutExpired:
        log(f"  [WARN] 타임아웃 (attempt {attempt+1})")
    except Exception as e:
        log(f"  [FAIL] {e}")
        break
else:
    log("  [FAIL] Claude 2회 실패")
    ANY_FAIL = True


# ── Step 5: 후처리 ─────────────────────────────────────
if os.path.exists(post_path):
    log("[Step 5] 후처리...")
    content = Path(post_path).read_text(encoding="utf-8")

    # 백틱 제거
    content = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', r'\1', content)

    # 날짜 강제 교정
    content = re.sub(r'date: \d{4}-\d{2}-\d{2}', f'date: {POST_DATE}', content)
    content = re.sub(r'permalink: /ko/\d{4}/\d{2}/\d{2}/', f'permalink: /ko/{POST_DATE.replace("-","/")}/', content)
    content = re.sub(r'pair: \d{4}-\d{2}-\d{2}-daily', f'pair: {POST_DATE}-daily', content)

    # tags 강제 교정
    tags_str = "[" + ", ".join(f'"{t}"' for t in DAY_TAGS_LIST) + "]"
    content = re.sub(r'tags: \[.*?\]', f'tags: {tags_str}', content)

    # source_type 강제
    if "source_type:" not in content:
        content = content.replace("---\n\n##", "source_type: free-sources\n---\n\n##", 1)

    # lang 강제
    content = re.sub(r'lang: \w+', 'lang: ko', content)

    post_dest = os.path.join(BLOG, "_posts", "ko", f"{POST_DATE}-daily-tech-review.md")
    Path(post_dest).write_text(content, encoding="utf-8")
    log(f"  [OK] 후처리 완료 → {post_dest}")

    # sections
    try:
        subprocess.run(["node", os.path.join(SCRIPTS, "extract-sections.js"), "--date", POST_DATE],
                      capture_output=True, timeout=30, cwd=BLOG)
        log("  sections 생성 완료")
    except Exception as e:
        log(f"  sections FAIL: {e}")
else:
    log("[Step 5] 스킵 — 포스트 없음")
    ANY_FAIL = True


# ── Step 6: 검증 ───────────────────────────────────────
log("[Step 6] 검증...")
post_dest = os.path.join(BLOG, "_posts", "ko", f"{POST_DATE}-daily-tech-review.md")
if os.path.exists(post_dest):
    content = Path(post_dest).read_text(encoding="utf-8")
    checks = {
        "파일 존재": True,
        "500자 이상": len(content) >= 500,
        "Today in One Line": "Today in One Line" in content,
        "Why it matters": "Why it matters" in content,
        "Source": "Source" in content,
        "날짜 일치": POST_DATE in content,
    }
    for k, v in checks.items():
        log(f"  {'[OK]' if v else '[FAIL]'} {k}")
    if not all(checks.values()):
        ANY_FAIL = True
else:
    log("  [FAIL] 포스트 없음")
    ANY_FAIL = True


# ── Step 7: 배포 ───────────────────────────────────────
if os.path.exists(post_dest) and not ANY_FAIL:
    log("[Step 7] 배포...")
    try:
        subprocess.run(["git", "pull", "--rebase", "origin", "master"], cwd=BLOG, capture_output=True, timeout=30)
        subprocess.run(["git", "add", "_posts/ko/", "_data/sections/"], cwd=BLOG, capture_output=True, timeout=10)
        r = subprocess.run(["git", "commit", "-m", f"[auto] {POST_DATE} daily post ({DAY_TOPIC}, free-sources v3)"],
                          cwd=BLOG, capture_output=True, text=True, timeout=30, encoding="utf-8")
        log(f"  commit: {r.stdout.strip()[:80]}")
        r = subprocess.run(["git", "push"], cwd=BLOG, capture_output=True, text=True, timeout=60, encoding="utf-8")
        log(f"  push: {(r.stdout or r.stderr).strip()[:80]}")
    except Exception as e:
        log(f"  git FAIL: {e}")
        ANY_FAIL = True
else:
    log("[Step 7] 스킵")


# ── 마무리 ─────────────────────────────────────────────
log(f"=== {'완료' if not ANY_FAIL else 'FAIL'} ({POST_DATE}, {DAY_TOPIC}) ===")

# 로그 저장
log_path = os.path.join(SCRIPTS, "_logs", f"daily-v3-{POST_DATE}.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
Path(log_path).write_text("\n".join(LOG), encoding="utf-8")

# 실패 알림
if ANY_FAIL:
    alert_path = os.path.join(TMP, f"alert-{POST_DATE}.txt")
    Path(alert_path).write_text(f"Daily Post FAIL: {POST_DATE}\n" + "\n".join(l for l in LOG if "FAIL" in l), encoding="utf-8")
