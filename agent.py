import os
import logging

from telegram import Bot


# =========================================================
# SETTINGS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID", "@HoshMasnoeiAI6")

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

    asyncio.run(test_telegram())


if __name__ == "__main__":
    main()
