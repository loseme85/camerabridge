import json
import os
import requests
from http.server import BaseHTTPRequestHandler

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GH_PAT = os.environ.get("GH_PAT")
GH_REPO = "loseme85/camerabridge"
GH_WORKFLOW = "crawl.yml"

def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text}
    )

def trigger_crawl():
    res = requests.post(
        f"https://api.github.com/repos/{GH_REPO}/actions/workflows/{GH_WORKFLOW}/dispatches",
        headers={
            "Authorization": f"token {GH_PAT}",
            "Accept": "application/vnd.github.v3+json"
        },
        json={"ref": "main"}
    )
    return res.status_code == 204

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            update = json.loads(body)
            message = update.get("message", {})
            chat_id = str(message.get("chat", {}).get("id", ""))
            text = message.get("text", "").strip()

            # 허용된 chat_id만 처리
            if chat_id != TELEGRAM_CHAT_ID:
                self.send_response(200)
                self.end_headers()
                return

            if text == "/crawl":
                if trigger_crawl():
                    send_telegram("🚀 크롤링 시작했어요!\n잠시 후 시작 알림이 올 거예요.")
                else:
                    send_telegram("❌ 크롤링 실행 실패. GitHub Actions를 확인해줘요.")
            elif text == "/help" or text == "/start":
                send_telegram(
                    "📷 Camera Bridge Bot\n\n"
                    "/crawl — 크롤링 즉시 실행\n"
                    "/help — 도움말"
                )
            else:
                send_telegram("❓ 모르는 명령어예요. /help 를 입력해보세요.")

        except Exception as e:
            print(f"Error: {e}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Telegram Webhook OK")
