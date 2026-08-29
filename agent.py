import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Bot


# =========================================================
# SETTINGS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@HoshMasnoeiAI6")

PORT = int(os.getenv("PORT", "10000"))


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =========================================================
# VALIDATE SETTINGS
# =========================================================

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")


# =========================================================
# WEB SERVER
# =========================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"Telegram Content Agent is running."
            )

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                b'{"status":"ok"}'
            )

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def start_web_server():
    server = HTTPServer(
        ("0.0.0.0", PORT),
        HealthHandler
    )

    logger.info("Web server started on port %s", PORT)

    server.serve_forever()


# =========================================================
# TELEGRAM TEST
# =========================================================

async def test_telegram():

    bot = Bot(token=BOT_TOKEN)

    me = await bot.get_me()

    logger.info(
        "Telegram connected successfully: @%s",
        me.username
    )


# =========================================================
# MAIN
# =========================================================

def main():

    import asyncio

    logger.info("Telegram Content Agent started.")

    web_thread = threading.Thread(
        target=start_web_server,
        daemon=True
    )

    web_thread.start()

    asyncio.run(test_telegram())

    web_thread.join()


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
