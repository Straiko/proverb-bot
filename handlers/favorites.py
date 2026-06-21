from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from services.database import Database

router = Router()


@router.message(Command("favorites"))
async def cmd_favorites(message: Message, db: Database):
    favorites = await db.get_favorites(message.from_user.id)

    if not favorites:
        await message.answer(
            "⭐ У вас пока нет избранных пословиц.\n\n"
            "Нажмите ⭐ под пословицей, чтобы добавить её в избранное."
        )
        return

    text = "⭐ Ваши избранные пословиц:\n\n"

    for i, p in enumerate(favorites, 1):
        text += f"{i}. {p['text']}\n"

    await message.answer(text)


@router.callback_query(F.data.startswith("fav_remove_"))
async def remove_favorite(callback: CallbackQuery, db: Database):
    proverb_id = int(callback.data.split("_")[2])
    await db.remove_favorite(callback.from_user.id, proverb_id)
    await callback.answer("❌ Удалено из избранного")
    await callback.message.edit_reply_markup()
