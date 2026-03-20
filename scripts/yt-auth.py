"""
YouTube OAuth 인증 — 브라우저에서 구글 로그인 후 토큰 저장.

Usage: python yt-auth.py
"""
import json, io, sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
KEYS_PATH = SCRIPT_DIR / "_credentials" / "gcp-oauth.keys.json"
TOKEN_PATH = SCRIPT_DIR / "_credentials" / "youtube_token.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]


def main():
    # 기존 토큰 있으면 갱신 시도
    if TOKEN_PATH.exists():
        token_data = json.loads(TOKEN_PATH.read_text())
        if token_data.get("refresh_token") and token_data.get("client_id"):
            creds = Credentials(
                token=token_data.get("access_token"),
                refresh_token=token_data["refresh_token"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=token_data["client_id"],
                client_secret=token_data["client_secret"],
                scopes=SCOPES,
            )
            if creds.expired or not creds.valid:
                try:
                    creds.refresh(Request())
                    save_token(creds)
                    print("토큰 갱신 완료")
                    return
                except Exception as e:
                    print(f"갱신 실패, 새로 인증합니다: {e}")

    # 새 인증
    flow = InstalledAppFlow.from_client_secrets_file(str(KEYS_PATH), SCOPES)
    creds = flow.run_local_server(port=8090, prompt="consent")
    save_token(creds)
    print("인증 완료! 토큰 저장됨:", TOKEN_PATH)


def save_token(creds):
    token_data = {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "token_uri": creds.token_uri,
        "scopes": list(creds.scopes) if creds.scopes else SCOPES,
    }
    TOKEN_PATH.write_text(json.dumps(token_data, indent=2))


if __name__ == "__main__":
    main()
