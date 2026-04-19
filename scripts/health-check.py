#!/usr/bin/env python3
"""tech-review 파이프라인 사후 health check.

마스터 파이프라인 끝에서 자동 실행. 사고 패턴이 다시 발생하면 즉시 감지.
모든 검사가 통과하면 exit 0, 하나라도 실패하면 exit 1 + alert 파일 작성.

검사 항목:
  A. 오늘 daily post 정상 (마스터가 오늘 생성한 경우)
  B. bookmarks.json 데이터 일관성 (모순/limit hit 감지)
  C. (확장 가능) YouTube 분석 일관성

사용:
  python scripts/health-check.py             # 오늘 기준
  python scripts/health-check.py 2026-04-20  # 특정 날짜
"""
import json, re, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

BLOG = Path(__file__).parent.parent
KST = timezone(timedelta(hours=9))
TODAY = sys.argv[1] if len(sys.argv) > 1 else datetime.now(KST).strftime("%Y-%m-%d")

# 표시용 텍스트가 분석 결과보다 비정상적으로 짧을 때의 임계값.
# translation이 text의 N배 이상이면 모순으로 간주 (한국어는 보통 영문의 0.6~0.8배).
TEXT_TRANS_RATIO_MAX = 3.0
# 정확히 이 길이로 끝나면 hardcoded limit에 hit한 의심 (truncate 사고의 시그니처).
SUSPICIOUS_LENS = {500, 1000, 2000, 4000, 8000}

issues = []


def check_daily_post(date):
    """오늘 daily post 형식·길이·front matter·trailing 메타텍스트 검증."""
    post = BLOG / "_posts" / "ko" / f"{date}-daily-tech-review.md"
    if not post.exists():
        # 파일이 없는 건 정상일 수 있음(마스터가 daily 안 돌렸거나 실패).
        # 마스터 returncode로 따로 판정되므로 여기서는 SKIP.
        return f"SKIP daily post — {post.name} 없음"

    content = post.read_text(encoding="utf-8")
    fails = []

    if len(content) < 1500:
        fails.append(f"본문 너무 짧음 ({len(content)}자, 최소 1500)")
    if not re.match(r'^---\s*\n\s*layout:\s*post', content):
        fails.append("front matter 시작 비정상 (---\\nlayout: post 패턴 없음)")
    if re.search(r'^[ \t]*```[a-zA-Z]*[ \t]*$', content, flags=re.MULTILINE):
        fails.append("``` 코드블록 래퍼 잔재 (정제 실패)")
    if "## Comments" not in content:
        fails.append("`## Comments` 섹션 누락")
    if re.search(r'## Comments[\s\S]+\S', content):
        # ## Comments 이후에 trailing 텍스트가 있으면 정제 누락
        tail = content.split("## Comments", 1)[1].strip()
        if tail:
            fails.append(f"## Comments 이후 trailing 메타텍스트 ({len(tail)}자)")
    sections = BLOG / "_data" / "sections" / f"{date}-ko.json"
    if not sections.exists():
        fails.append("sections JSON 누락")

    return fails or f"daily post {date} OK ({len(content)}자)"


def check_bookmarks_consistency():
    """bookmarks.json 전체에 대한 모순/limit hit 검사.

    판정 원칙:
    - FAIL: text:translation 비율이 비정상(>3.0)이면 텍스트 잘림 의심 → 즉시 신호.
    - FAIL: 필수 필드 누락.
    - WARN: text가 hardcoded limit에 정확히 hit (참고 정보, 비율이 정상이면 false positive).
    """
    bm_path = BLOG / "_data" / "bookmarks.json"
    if not bm_path.exists():
        return "SKIP bookmarks — 파일 없음"

    data = json.loads(bm_path.read_text(encoding="utf-8"))
    fails = []
    warns = []

    # 1) FAIL: text가 너무 짧고 translation이 비정상적으로 김 (truncate 사고의 직접 시그니처)
    inconsistent = []
    for b in data:
        text_n = len(b.get("text", "") or "")
        trans_n = len(b.get("translation", "") or "")
        if text_n > 0 and trans_n / text_n > TEXT_TRANS_RATIO_MAX:
            inconsistent.append((b["id"], text_n, trans_n, trans_n / text_n))
    if inconsistent:
        sample = ", ".join(f"{i}(text={t}/trans={tr}={r:.1f}x)" for i, t, tr, r in inconsistent[:3])
        fails.append(f"text:translation 비율 비정상(>{TEXT_TRANS_RATIO_MAX}x) {len(inconsistent)}건: {sample}{'...' if len(inconsistent)>3 else ''}")

    # 2) FAIL: 필수 필드 누락
    missing_fields = []
    for b in data:
        for f in ("id", "url", "text"):
            if not b.get(f):
                missing_fields.append((b.get("id", "?"), f))
                break
    if missing_fields:
        fails.append(f"필수 필드 누락 {len(missing_fields)}건: {missing_fields[:3]}{'...' if len(missing_fields)>3 else ''}")

    # 3) WARN: text가 hardcoded limit 정확히 hit (참고 — backfill 흔적 또는 신규 limit 사고)
    # 비율이 정상이면 false positive 가능성 높음 (이전 backfill로 일관성은 OK).
    inconsistent_ids = {x[0] for x in inconsistent}
    suspicious = [b for b in data if len(b.get("text", "") or "") in SUSPICIOUS_LENS and b["id"] not in inconsistent_ids]
    if suspicious:
        ids = ", ".join(b["id"] for b in suspicious[:5])
        warns.append(f"text 길이가 hardcoded limit({sorted(SUSPICIOUS_LENS)}) hit {len(suspicious)}건 (비율 정상, 참고): {ids}{'...' if len(suspicious)>5 else ''}")

    if fails:
        return fails
    msg = f"bookmarks 일관성 OK ({len(data)}건 검사, 모순 0)"
    if warns:
        msg += "\n      WARN: " + " | ".join(warns)
    return msg


def main():
    print(f"=== Health Check ({TODAY}) ===\n")

    checks = [
        ("Daily Post", check_daily_post(TODAY)),
        ("Bookmarks 일관성", check_bookmarks_consistency()),
    ]

    overall_ok = True
    for name, result in checks:
        if isinstance(result, list):
            overall_ok = False
            print(f"[FAIL] {name}:")
            for f in result:
                print(f"   - {f}")
                issues.append(f"{name}: {f}")
        elif isinstance(result, str) and result.startswith("SKIP"):
            print(f"[SKIP] {name}: {result[5:]}")
        else:
            print(f"[OK]   {name}: {result}")

    print()
    if overall_ok:
        print("=== 전체 PASS ===")
        sys.exit(0)
    else:
        print(f"=== {len(issues)}개 이슈 감지 — alert 작성 ===")
        alert_path = BLOG / "_tmp" / f"alert-health-{TODAY}.txt"
        alert_path.parent.mkdir(exist_ok=True)
        alert_path.write_text(
            f"Health Check FAIL: {TODAY}\n" + "\n".join(f"- {i}" for i in issues),
            encoding="utf-8",
        )
        print(f"alert: {alert_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
