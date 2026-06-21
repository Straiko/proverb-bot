import json
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from services.database import Database
from services.ai_matcher import AIMatcher
from config import Config

router = Router()


def load_proverbs(proverbs_path: str) -> dict:
    try:
        with open(proverbs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": [], "proverbs": []}


@router.message(Command("proverb"))
async def cmd_random_proverb(message: Message, db: Database, config: Config):
    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]
    proverb = random.choice(proverbs)

    await message.answer(
        f"📜 {proverb['text']}\n\n"
        f"⭐ Добавить в избранное",
        reply_markup={
            "inline_keyboard": [[
                {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"},
                {"text": "ℹ️ История", "callback_data": f"origin_{proverb['id']}"}
            ]]
        }
    )


@router.message(Command("daily"))
async def cmd_daily(message: Message, db: Database, config: Config):
    from datetime import date
    today = date.today().isoformat()

    daily_id = await db.get_daily_proverb_id(today)
    if daily_id:
        data = load_proverbs(config.PROVERBS_PATH)
        proverb = next((p for p in data["proverbs"] if p["id"] == daily_id), None)
        if proverb:
            await message.answer(f"📅 Пословица дня:\n\n📜 {proverb['text']}")
            return

    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]
    proverb = random.choice(proverbs)

    await db.set_daily_proverb(today, proverb["id"])

    await message.answer(
        f"📅 Пословица дня:\n\n📜 {proverb['text']}\n\n"
        f"⭐ Добавить в избранное",
        reply_markup={
            "inline_keyboard": [[
                {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"}
            ]]
        }
    )


@router.callback_query(F.data.startswith("fav_add_"))
async def add_favorite(callback: CallbackQuery, db: Database):
    proverb_id = int(callback.data.split("_")[2])
    await db.add_favorite(callback.from_user.id, proverb_id)
    await callback.answer("✅ Добавлено в избранное!")
    await callback.message.edit_reply_markup()


@router.message(F.text & ~F.text.startswith("/"))
async def match_proverb(message: Message, db: Database, config: Config, ai_matcher: AIMatcher):
    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]

    matched_text = ai_matcher.match_proverb(message.text, proverbs)

    matched_proverb = next(
        (p for p in proverbs if p["text"].lower() in matched_text.lower() or matched_text.lower() in p["text"].lower()),
        None
    )

    if matched_proverb:
        await message.answer(
            f"📜 {matched_proverb['text']}\n\n"
            f"⭐ Добавить в избранное",
            reply_markup={
                "inline_keyboard": [[
                    {"text": "⭐ В избранное", "callback_data": f"fav_add_{matched_proverb['id']}"}
                ]]
            }
        )
    else:
        await message.answer(f"📜 {matched_text}")
