#!/usr/bin/env python3
"""500자 truncate 피해 X Article 북마크 backfill.

2026-04-20 사고: add-bookmark.py:444에서 X Article 본문을 [:500]으로 잘라 저장.
translation은 풀 본문 번역(2500자)이지만 text는 500자 미리보기 → 모순.
이 스크립트로 text=500자인 항목을 CDP로 재fetch하여 전문(최대 4000자)으로 교체한다.

사용:
  python scripts/backfill-article-text.py             # dry-run (대상만 출력)
  python scripts/backfill-article-text.py --apply     # 실제 적용
"""
import argparse, json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
add_bm = import_module("add-bookmark")  # fetch_article_text 재사용

BLOG_DIR = Path(__file__).parent.parent
BOOKMARKS_JSON = BLOG_DIR / "_data" / "bookmarks.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="실제 파일 수정")
    args = ap.parse_args()

    data = json.loads(BOOKMARKS_JSON.read_text(encoding="utf-8"))
    victims = [b for b in data if len(b.get("text", "") or "") == 500]
    print(f"500자 truncate 피해: {len(victims)}개")

    if not victims:
        print("대상 없음.")
        return

    if not args.apply:
        for v in victims:
            print(f"  {v['id']} @{v['author']} {v['url']}")
        print("\n(dry-run) --apply 추가하면 실제 fetch 시작")
        return

    by_id = {b["id"]: b for b in data}
    success = 0
    fail = []
    for i, v in enumerate(victims, 1):
        url = v["url"]
        print(f"[{i}/{len(victims)}] {v['id']} @{v['author']} ... ", end="", flush=True)
        article = add_bm.fetch_article_text(url)
        if article and len(article) > 500:
            by_id[v["id"]]["text"] = article
            print(f"OK {len(article)}자 (was 500)")
            success += 1
            # checkpoint: 매 5개마다 저장 (네트워크 실패 시 진행 보존)
            if success % 5 == 0:
                BOOKMARKS_JSON.write_text(
                    json.dumps(list(by_id.values()), ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                print(f"  [checkpoint saved]")
            time.sleep(2)  # rate limit 회피
        else:
            print(f"FAIL ({'본문 너무 짧음' if article else 'CDP 실패'})")
            fail.append(v["id"])

    # 최종 저장
    BOOKMARKS_JSON.write_text(
        json.dumps(list(by_id.values()), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n완료: 성공 {success}/{len(victims)}, 실패 {len(fail)}")
    if fail:
        print(f"실패 ID: {', '.join(fail)}")


if __name__ == "__main__":
    main()
