#!/usr/bin/env python3
"""Daily Post v3 — 무료 소스 + Claude Sonnet 파이프라인"""
import json, sys, os, subprocess, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

BLOG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(BLOG, "_tmp")
SCRIPTS = os.path.join(BLOG, "scripts")
POST_DATE = sys.argv[1] if len(sys.argv) > 1 else datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
UA = "Mozilla/5.0 (TechReview Bot)"
LOG = []

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.append(line)

def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")

def fetch_body(url, max_chars=3000):
    """URL에서 텍스트 본문 추출 (간이)"""
    try:
        html = fetch_url(url, timeout=10)
        # 간이 HTML→텍스트: 태그 제거
        import re
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except Exception as e:
        return f"[FETCH_FAIL: {e}]"

# ==== Step 1: 소스 수집 ====
log(f"=== Daily Post v3 시작 ({POST_DATE}) ===")
log("[Step 1] 소스 수집...")

sources = {}

# HN
try:
    top_ids = json.loads(fetch_url("https://hacker-news.firebaseio.com/v0/topstories.json"))[:30]
    hn = []
    for sid in top_ids:
        item = json.loads(fetch_url(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"))
        if item.get("score", 0) >= 50:
            hn.append({"title": item.get("title",""), "url": item.get("url",""), "score": item.get("score",0), "comments": item.get("descendants",0)})
    sources["hackernews"] = hn
    log(f"  HN: {len(hn)}건")
except Exception as e:
    log(f"  HN FAIL: {e}")

# TechCrunch RSS
try:
    xml = fetch_url("https://techcrunch.com/feed/")
    root = ET.fromstring(xml)
    tc = [{"title": i.find("title").text, "url": i.find("link").text} for i in root.findall(".//item")[:10]]
    sources["techcrunch"] = tc
    log(f"  TC: {len(tc)}건")
except Exception as e:
    log(f"  TC FAIL: {e}")

# The Verge
try:
    xml = fetch_url("https://www.theverge.com/rss/index.xml")
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    verge = [{"title": e.find("a:title",ns).text.strip(), "url": e.find("a:link",ns).get("href","")} for e in root.findall("a:entry",ns)[:10]]
    sources["theverge"] = verge
    log(f"  Verge: {len(verge)}건")
except Exception as e:
    log(f"  Verge FAIL: {e}")

# Lobsters
try:
    data = json.loads(fetch_url("https://lobste.rs/hottest.json"))
    lob = [{"title": i["title"], "url": i["url"], "score": i["score"], "tags": i.get("tags",[])} for i in data[:15]]
    sources["lobsters"] = lob
    log(f"  Lobsters: {len(lob)}건")
except Exception as e:
    log(f"  Lobsters FAIL: {e}")

total = sum(len(v) for v in sources.values())
log(f"  수집 완료: {total}건")

# ==== Step 2: 선별 + 본문 추출 ====
log("[Step 2] 선별 + 본문 추출...")

# 교차 출현 감지 (제목 유사도 기반 간이)
all_items = []
for src, items in sources.items():
    for item in items:
        item["_source"] = src
        all_items.append(item)

# HN score 기준 + TC/Verge 가산점으로 정렬
for item in all_items:
    base = item.get("score", 0)
    # 다른 소스에도 비슷한 제목 있으면 가산
    title_lower = item["title"].lower()
    cross = sum(1 for other in all_items if other["_source"] != item["_source"] and
                any(w in other["title"].lower() for w in title_lower.split()[:3] if len(w) > 4))
    item["_rank"] = base + cross * 100

all_items.sort(key=lambda x: x["_rank"], reverse=True)
selected = all_items[:10]

log(f"  선별 {len(selected)}건:")
for i, item in enumerate(selected):
    log(f"    {i+1}. [{item['_source']}] {item['title'][:60]} (rank={item['_rank']})")

# 본문 추출
log("  본문 추출 중...")
for item in selected:
    if item.get("url") and not item["url"].startswith("https://news.ycombinator.com"):
        item["body"] = fetch_body(item["url"])
        log(f"    {item['title'][:40]}... → {len(item.get('body',''))}자")
    else:
        item["body"] = ""

selected_path = os.path.join(TMP, f"sources-selected-{POST_DATE}.json")
with open(selected_path, "w", encoding="utf-8") as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)
log(f"  저장: {selected_path}")

# ==== Step 3: Claude Sonnet 가공 ====
log("[Step 3] Claude Sonnet 가공...")

wim_prompt_path = os.path.join(BLOG, "config", "wim-prompt.md")
wim_prompt = ""
if os.path.exists(wim_prompt_path):
    with open(wim_prompt_path, "r", encoding="utf-8") as f:
        wim_prompt = f.read()

claude_prompt = f"""너는 tech-review 블로그의 Daily Post 작성자다. 한국어로 작성한다.

## 입력 데이터
아래 JSON은 오늘 수집한 테크 뉴스 상위 10건이다. 각 항목에 title, url, body(기사 본문 일부)가 있다.

```json
{json.dumps(selected, ensure_ascii=False)[:15000]}
```

## 작업
1. 10건 중 가장 중요한 3건을 선택 (AI/테크/개발자 생태계 영향도 기준)
2. 각 3건에 대해 아래 Smart Brevity 형식으로 작성

## 형식 (정확히 지켜라)
```
---
layout: post
title: "3건 요약 한 문장"
date: {POST_DATE}
lang: ko
permalink: /ko/{POST_DATE.replace('-','/')}/daily-tech-review/
pair: {POST_DATE}-daily-tech-review
tags: ["관련태그"]
source_type: free-sources
---

## Today in One Line
한 문장 요약

---

## 1. 제목

본문 설명 (최소 3문장, 기사 본문의 구체적 팩트·수치·인용 포함)

**Why it matters:** Paul의 프로젝트(orchestration, mcp-memory, tech-review, portfolio, context-cascade)와 연결. 일반론 금지. 구체적으로 어떤 시스템/설계와 관련되는지.

- 불릿 1 (기사 본문에서 추출한 구체적 팩트)
- 불릿 2
- 불릿 3

**What's next:** 전망 1-2문장

**Source:** [제목](URL)

---

(2, 3도 동일 형식)

## Comments

```

## 규칙
- body 필드의 실제 내용만 사용. body에 없는 팩트를 지어내지 마라.
- 수치, 날짜, 고유명사는 body에서 그대로 가져와라.
- Why it matters는 Paul의 시스템과 연결: mcp-memory(4685+ 노드 지식그래프), orchestration(멀티AI 조율), tech-review(자동 수집 파이프라인), portfolio(Next.js)
- 전체 한국어 (고유명사는 영어 유지)
- front matter의 tags는 영어 소문자
- 인라인 코드 백틱(`) 사용 금지. 파일명, 패키지명, 기술 용어 모두 일반 텍스트로 쓴다. 이것은 블로그 글이지 기술 문서가 아니다.

마크다운 파일 전체를 출력해라. 설명이나 부연 없이 파일 내용만."""

# claude -p 실행
post_path = os.path.join(TMP, f"final-{POST_DATE}.md")
prompt_path = os.path.join(TMP, f"prompt-{POST_DATE}.txt")
with open(prompt_path, "w", encoding="utf-8") as f:
    f.write(claude_prompt)
log(f"  프롬프트 저장: {len(claude_prompt)}자 → {prompt_path}")

try:
    with open(prompt_path, "r", encoding="utf-8") as prompt_file:
        result = subprocess.run(
            [r"C:\Users\pauls\AppData\Roaming\npm\claude.cmd", "-p", "--model", "claude-sonnet-4-6", "--output-format", "text"],
            stdin=prompt_file,
            capture_output=True, timeout=300,
            cwd=BLOG
        )
    output = result.stdout.decode("utf-8", errors="replace").strip()
    stderr = result.stderr.decode("utf-8", errors="replace").strip() if result.stderr else ""
    if len(output) < 200:
        log(f"  [WARN] Claude 출력 부족 ({len(output)}자)")
        log(f"  stderr: {stderr[:500]}")
    else:
        # ``` 블록 제거 (Claude가 감싸는 경우)
        if output.startswith("```"):
            output = "\n".join(output.split("\n")[1:])
        if output.endswith("```"):
            output = "\n".join(output.split("\n")[:-1])
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(output)
        log(f"  [OK] {post_path} ({len(output)}자)")
except subprocess.TimeoutExpired:
    log("  [FAIL] Claude 타임아웃 (300초)")
except Exception as e:
    log(f"  [FAIL] Claude 실행 오류: {e}")

# ==== Step 4: Jekyll 빌드 ====
if os.path.exists(post_path):
    log("[Step 4] Jekyll 포스트 생성...")
    post_dest = os.path.join(BLOG, "_posts", "ko", f"{POST_DATE}-daily-tech-review.md")

    import re as re2
    with open(post_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 인라인 코드 백틱 제거 — 블로그 글에 모노스페이스 금지
    content = re2.sub(r'(?<!`)`([^`\n]+)`(?!`)', r'\1', content)
    # 날짜 강제 교정 — Sonnet이 프롬프트 날짜를 무시하는 경우 대비
    content = re2.sub(r'date: \d{4}-\d{2}-\d{2}', f'date: {POST_DATE}', content)
    content = re2.sub(r'permalink: /ko/\d{4}/\d{2}/\d{2}/', f'permalink: /ko/{POST_DATE.replace("-","/")}/', content)
    content = re2.sub(r'pair: \d{4}-\d{2}-\d{2}-daily', f'pair: {POST_DATE}-daily', content)
    with open(post_dest, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"  날짜 교정 완료: {POST_DATE}")
    log(f"  [OK] {post_dest}")

    # extract-sections
    try:
        r = subprocess.run(["node", os.path.join(SCRIPTS, "extract-sections.js"), "--date", POST_DATE],
                          capture_output=True, text=True, timeout=30, cwd=BLOG, encoding="utf-8")
        log(f"  sections: {r.stdout.strip()[:100]}")
    except Exception as e:
        log(f"  sections FAIL: {e}")
else:
    log("[Step 4] 스킵 — 포스트 파일 없음")

# ==== Step 5: 검증 ====
log("[Step 5] 검증...")
post_dest = os.path.join(BLOG, "_posts", "ko", f"{POST_DATE}-daily-tech-review.md")
if os.path.exists(post_dest):
    with open(post_dest, "r", encoding="utf-8") as f:
        content = f.read()
    checks = {
        "파일 존재": True,
        "500자 이상": len(content) >= 500,
        "Today in One Line": "Today in One Line" in content,
        "Why it matters": "Why it matters" in content,
        "What's next": "What" in content and "next" in content,
        "Source": "Source:" in content or "**Source" in content,
    }
    for k, v in checks.items():
        log(f"  {'[OK]' if v else '[FAIL]'} {k}")

    if all(checks.values()):
        log("  검증 통과")
    else:
        log("  [WARN] 일부 검증 실패")
else:
    log("  [FAIL] 포스트 파일 없음")

# ==== Step 6: git push ====
log("[Step 6] git commit + push...")
try:
    subprocess.run(["git", "add", "_posts/ko/", "_data/sections/"], cwd=BLOG, capture_output=True, timeout=10)
    r = subprocess.run(["git", "commit", "-m", f"[auto] {POST_DATE} daily post (free-sources v3)"],
                      cwd=BLOG, capture_output=True, text=True, timeout=30, encoding="utf-8")
    log(f"  commit: {r.stdout.strip()[:100]}")
    r = subprocess.run(["git", "push"], cwd=BLOG, capture_output=True, text=True, timeout=60, encoding="utf-8")
    log(f"  push: {r.stdout.strip()[:100] or r.stderr.strip()[:100]}")
except Exception as e:
    log(f"  git FAIL: {e}")

log(f"=== 완료 ({POST_DATE}) ===")

# 로그 저장
log_path = os.path.join(SCRIPTS, "_logs", f"daily-v3-{POST_DATE}.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))
log(f"로그: {log_path}")
