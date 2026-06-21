from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from services.database import Database

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database):
    await db.add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "👋 Привет! Я бот с пословицами и поговорками.\n\n"
        "📝 Просто напиши мне вопрос или ситуацию, и я подберу подходящую пословицу.\n\n"
        "📌 Команды:\n"
        "/proverb - случайная пословица\n"
        "/categories - список категорий\n"
        "/category [название] - пословицы из категории\n"
        "/favorites - мои избранные\n"
        "/daily - пословица дня\n"
        "/help - помощь"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📚 Как пользоваться ботом:\n\n"
        "💬 Напиши любой вопрос или опиши ситуацию — я подберу пословицу.\n\n"
        "Команды:\n"
        "/proverb - получить случайную пословицу\n"
        "/categories - посмотреть список категорий\n"
        "/category [название] - пословицы по теме\n"
        "/favorites - твои избранные пословицы\n"
        "/daily - пословица дня\n\n"
        "⭐ Нажми на кнопку под пословицей, чтобы добавить в избранное."
    )
