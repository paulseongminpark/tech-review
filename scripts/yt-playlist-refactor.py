"""
YouTube Playlist Refactor — blog/AI work/Ai design/Claude → claude/build/insight/ontology

Usage:
  1) python yt-playlist-refactor.py --scan          # 현재 상태 출력 + 분류 초안 생성
  2) (사용자가 plan.json 검토/수정)
  3) python yt-playlist-refactor.py --execute        # plan.json 기반 실행
  4) python yt-playlist-refactor.py --execute --dry   # 실행 없이 미리보기
"""
import argparse, json, os, sys, time, io
from pathlib import Path

# Windows cp949 출력 문제 해결
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCRIPT_DIR = Path(__file__).parent
CRED_DIR = SCRIPT_DIR / "_credentials"
TOKEN_PATH = CRED_DIR / "youtube_token.json"
KEYS_PATH = CRED_DIR / "gcp-oauth.keys.json"
PLAN_PATH = SCRIPT_DIR / "_credentials" / "refactor-plan.json"

# 소스 플레이리스트 (리팩토링 대상)
SOURCE_PLAYLISTS = {
    "blog":      "PLUeFkXBkSX_bgvVnbAFBvZZE03jCzzm5Q",
    "Claude":    "PLUeFkXBkSX_bxzWza71Mdb7JlOOg5xDDS",
    "AI work":   "PLUeFkXBkSX_b-vFTX8rDNnHBKCE-epz08",
    "Ai design": "PLUeFkXBkSX_ZShpRuJsbAqc8KCqVPK8Hn",
}

# 유지되는 플레이리스트
KEEP_PLAYLISTS = {
    "ontology": "PLUeFkXBkSX_ZFCfP8j0peOCeOlKVhwfFx",
}

# 새로 만들 플레이리스트
NEW_PLAYLISTS = ["build", "design", "insight"]

# 타겟 카테고리
TARGETS = ["claude", "build", "design", "insight", "ontology"]

# 플레이리스트 표시 이름 + description
PLAYLIST_META = {
    "claude": {
        "title": "BLOG - Claude",
        "description": "Claude Code, Skills, Teams 등 Claude 생태계 도구와 사용법을 배우는 영상입니다. Anthropic의 AI 도구를 깊이 이해하고 활용하는 데 관련된 영상을 모읍니다.",
    },
    "build": {
        "title": "BLOG - Build",
        "description": "AI를 활용해 서비스, 앱, 제품을 직접 만들고 런칭하는 과정을 담은 영상입니다. 바이브코딩, 1인 개발, 수익화 등 실전 빌드에 관련된 영상을 모읍니다.",
    },
    "design": {
        "title": "BLOG - Design",
        "description": "UI/UX 디자인, 디자인 시스템, 시각적 결과물에 초점을 맞춘 영상입니다. AI를 활용한 디자인 워크플로우와 디자인 사고에 관련된 영상을 모읍니다.",
    },
    "insight": {
        "title": "BLOG - Insight",
        "description": "AI 산업 동향, 개발자 커리어, 지식관리, 방법론 등 알아가고 생각하는 영상입니다. 기술의 방향과 일하는 방식에 대한 인사이트를 주는 영상을 모읍니다.",
    },
    "ontology": {
        "title": "BLOG - Ontology",
        "description": "Palantir AIP, 지식그래프, 온톨로지 등 데이터 구조화에 초점을 맞춘 영상입니다. 정보와 관계를 체계적으로 모델링하는 데 관련된 영상을 모읍니다.",
    },
}

# ── 키워드 기반 자동 분류 ──
CLAUDE_KW = [
    "claude code", "claude skill", "anthropic", "claude cowork",
    "claude agent", "claude team", "openclaw", "오픈클로", "클로드 코드",
    "클로드 스킬", "코워크", "앤트로픽", "claude 2.0", "claude code 2",
    "nano banana", "CLAUDE.md",
]
BUILD_KW = [
    "design system", "portfolio", "vibe cod", "바이브코딩", "바이브 코딩",
    "build", "만드는", "만들기", "구현", "런칭", "deploy", "상세페이지",
    "서비스", "stitch", "figma", "디자인", "1인 창업", "profitable app",
    "solo", "animated site", "animated website", "web design",
]
INSIGHT_KW = [
    "생존법", "생산성", "interview", "인터뷰", "산업", "전략",
    "note-taking", "노트", "제텔카스텐", "옵시디언", "obsidian",
    "pkm", "knowledge manage", "지식관리", "gtc", "career",
    "커리어", "future", "미래", "notebooklm", "rag",
    "saas", "스타링크", "투자", "주식", "경제", "전쟁",
    "agentic workflow", "ai agent", "ai 에이전트",
]
ONTOLOGY_KW = [
    "ontology", "온톨로지", "palantir", "aip", "knowledge graph",
    "지식그래프", "semantic search",
]


def get_youtube():
    """인증 후 YouTube API 클라이언트 반환."""
    token_data = json.loads(TOKEN_PATH.read_text())

    # keys 파일이 있으면 사용, 없으면 토큰에 내장된 client 정보 사용
    client_id = token_data.get("client_id")
    client_secret = token_data.get("client_secret")
    if KEYS_PATH.exists():
        keys_data = json.loads(KEYS_PATH.read_text())
        if "installed" in keys_data:
            client_id = keys_data["installed"]["client_id"]
            client_secret = keys_data["installed"]["client_secret"]

    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube"],
    )
    if creds.expired or not creds.valid:
        creds.refresh(Request())
        token_data["access_token"] = creds.token
        token_data["expires_at"] = int(time.time()) + 3600
        TOKEN_PATH.write_text(json.dumps(token_data, indent=2))
        print("[AUTH] 토큰 갱신 완료")

    return build("youtube", "v3", credentials=creds)


def fetch_playlist_items(yt, playlist_id):
    """플레이리스트의 모든 영상 반환."""
    items = []
    next_token = None
    while True:
        resp = yt.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_token,
        ).execute()
        for item in resp.get("items", []):
            s = item["snippet"]
            items.append({
                "playlistItemId": item["id"],
                "videoId": s["resourceId"]["videoId"],
                "title": s["title"],
                "channel": s.get("videoOwnerChannelTitle", ""),
            })
        next_token = resp.get("nextPageToken")
        if not next_token:
            break
    return items


def classify(title, channel):
    """키워드 기반 자동 분류. 확신 없으면 'review' 반환."""
    t = (title + " " + channel).lower()

    # ontology 먼저 (명확)
    if any(kw in t for kw in ONTOLOGY_KW):
        return "ontology"

    # claude 체크
    claude_score = sum(1 for kw in CLAUDE_KW if kw in t)
    build_score = sum(1 for kw in BUILD_KW if kw in t)
    insight_score = sum(1 for kw in INSIGHT_KW if kw in t)

    # claude + build 동시 → claude 우선 (Claude Code로 디자인하기 등)
    if claude_score > 0 and build_score > 0:
        return "claude"
    if claude_score > 0:
        return "claude"
    if build_score > insight_score and build_score > 0:
        return "build"
    if insight_score > build_score and insight_score > 0:
        return "insight"
    if build_score > 0:
        return "build"
    if insight_score > 0:
        return "insight"

    return "review"  # 수동 검토 필요


def cmd_scan(yt):
    """모든 소스 플레이리스트를 스캔하고 분류 초안 생성."""
    plan = {"videos": [], "new_playlists": NEW_PLAYLISTS, "source_playlists": SOURCE_PLAYLISTS}
    seen_ids = set()

    for name, pid in SOURCE_PLAYLISTS.items():
        print(f"\n📋 {name} ({pid})")
        items = fetch_playlist_items(yt, pid)
        print(f"   {len(items)}개 영상")
        for item in items:
            vid = item["videoId"]
            if vid in seen_ids:
                print(f"   ⏭ 중복 스킵: {item['title'][:40]}")
                continue
            seen_ids.add(vid)
            cat = classify(item["title"], item["channel"])
            entry = {
                "videoId": vid,
                "title": item["title"],
                "channel": item["channel"],
                "source": name,
                "target": cat,
                "playlistItemId": item["playlistItemId"],
                "sourcePlaylistId": pid,
            }
            plan["videos"].append(entry)
            marker = "⚠️" if cat == "review" else "✅"
            print(f"   {marker} [{cat:>8}] {item['title'][:60]}")

    # 통계
    from collections import Counter
    cats = Counter(v["target"] for v in plan["videos"])
    print(f"\n📊 분류 결과:")
    for cat in TARGETS + ["review"]:
        print(f"   {cat}: {cats.get(cat, 0)}개")
    print(f"   총 {len(plan['videos'])}개 (중복 제거)")

    PLAN_PATH.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n💾 plan 저장: {PLAN_PATH}")
    if cats.get("review", 0) > 0:
        print(f"⚠️  'review' {cats['review']}개는 수동 분류 필요 — plan.json에서 target을 수정하세요.")


def cmd_execute(yt, dry=False):
    """plan.json 기반으로 실행."""
    if not PLAN_PATH.exists():
        print("❌ plan.json 없음. --scan 먼저 실행하세요.")
        sys.exit(1)

    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))

    # review 남아있는지 체크
    reviews = [v for v in plan["videos"] if v["target"] == "review"]
    if reviews:
        print(f"❌ 'review' {len(reviews)}개 남아있음. plan.json에서 target을 수정하세요:")
        for v in reviews:
            print(f"   - {v['title'][:60]}")
        sys.exit(1)

    # 1) 기존 플레이리스트 업데이트 + 새 플레이리스트 생성
    target_ids = dict(KEEP_PLAYLISTS)  # ontology는 이미 있음

    # ontology 이름+description 업데이트
    meta = PLAYLIST_META["ontology"]
    if not dry:
        try:
            yt.playlists().update(
                part="snippet",
                body={
                    "id": target_ids["ontology"],
                    "snippet": {"title": meta["title"], "description": meta["description"]},
                },
            ).execute()
            print(f"✅ ontology → {meta['title']}")
        except Exception as e:
            print(f"⚠️  ontology 업데이트 실패: {e}")
    else:
        print(f"[DRY] 이름 변경: Ontology → {meta['title']}")

    # claude는 기존 것 재사용 (이름+description 업데이트)
    target_ids["claude"] = SOURCE_PLAYLISTS["Claude"]
    meta = PLAYLIST_META["claude"]
    if not dry:
        try:
            yt.playlists().update(
                part="snippet",
                body={
                    "id": target_ids["claude"],
                    "snippet": {"title": meta["title"], "description": meta["description"]},
                },
            ).execute()
            print(f"✅ claude → {meta['title']}")
        except Exception as e:
            print(f"⚠️  claude 업데이트 실패: {e}")
    else:
        print(f"[DRY] 이름 변경: Claude → {meta['title']}")

    for name in plan.get("new_playlists", []):
        if name in target_ids:
            continue
        meta = PLAYLIST_META.get(name, {"title": name, "description": ""})
        if dry:
            print(f"[DRY] 플레이리스트 생성: {meta['title']}")
            target_ids[name] = f"DRY_{name}"
        else:
            resp = yt.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {"title": meta["title"], "description": meta["description"]},
                    "status": {"privacyStatus": "private"},
                },
            ).execute()
            target_ids[name] = resp["id"]
            print(f"✅ 플레이리스트 생성: {meta['title']} → {resp['id']}")
            time.sleep(0.5)

    # 2) 영상 추가
    added = 0
    for v in plan["videos"]:
        target = v["target"]
        target_pid = target_ids.get(target)
        if not target_pid:
            print(f"❌ 타겟 플레이리스트 없음: {target}")
            continue

        # claude 플레이리스트에 이미 있는 영상은 스킵
        if target == "claude" and v["source"] == "Claude":
            continue

        if dry:
            print(f"[DRY] {v['title'][:50]} → {target}")
        else:
            try:
                yt.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": target_pid,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": v["videoId"],
                            },
                        }
                    },
                ).execute()
                added += 1
                print(f"✅ [{target}] {v['title'][:50]}")
                time.sleep(0.3)  # quota 보호
            except Exception as e:
                print(f"⚠️  실패: {v['title'][:40]} — {e}")

    # 3) 소스 플레이리스트에서 제거 (claude 제외 — 재사용)
    removed = 0
    for v in plan["videos"]:
        src = v["source"]
        if src == "Claude" and v["target"] == "claude":
            continue  # claude 플레이리스트는 그대로 유지
        if src == "Claude":
            # claude 플레이리스트에서 다른 카테고리로 간 영상은 제거
            pass
        item_id = v.get("playlistItemId")
        if not item_id:
            continue
        if dry:
            print(f"[DRY] 제거: {v['title'][:40]} from {src}")
        else:
            try:
                yt.playlistItems().delete(id=item_id).execute()
                removed += 1
                time.sleep(0.3)
            except Exception as e:
                print(f"⚠️  제거 실패: {v['title'][:40]} — {e}")

    print(f"\n📊 완료: {added}개 추가, {removed}개 제거")
    if not dry:
        # plan에 결과 기록
        plan["result"] = {
            "target_playlist_ids": target_ids,
            "added": added,
            "removed": removed,
        }
        PLAN_PATH.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"💾 결과 저장: {PLAN_PATH}")


def main():
    parser = argparse.ArgumentParser(description="YouTube Playlist Refactor")
    parser.add_argument("--scan", action="store_true", help="소스 플레이리스트 스캔 + 분류 초안")
    parser.add_argument("--execute", action="store_true", help="plan.json 기반 실행")
    parser.add_argument("--dry", action="store_true", help="실행 없이 미리보기")
    args = parser.parse_args()

    if not args.scan and not args.execute:
        parser.print_help()
        sys.exit(0)

    yt = get_youtube()
    print("[AUTH] YouTube API 연결 완료\n")

    if args.scan:
        cmd_scan(yt)
    elif args.execute:
        cmd_execute(yt, dry=args.dry)


if __name__ == "__main__":
    main()
