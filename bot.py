import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from services.database import Database
from services.ai_matcher import AIMatcher
from handlers import start, proverb, categories, favorites


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    config = load_config()

    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN не установлен. Установите переменную окружения BOT_TOKEN.")
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY не установлен. Установите переменную окружения GROQ_API_KEY.")

    db = Database(config.DB_PATH)
    await db.init()

    ai_matcher = AIMatcher(config.GROQ_API_KEY, config.GROQ_MODEL)

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp["db"] = db
    dp["config"] = config
    dp["ai_matcher"] = ai_matcher

    dp.include_router(start.router)
    dp.include_router(proverb.router)
    dp.include_router(categories.router)
    dp.include_router(favorites.router)

    logging.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
