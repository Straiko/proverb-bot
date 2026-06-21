import json
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from services.database import Database
from services.ai_matcher import AIMatcher
from config import Config

router = Router()

FALLBACK_CATEGORIES = [
    {"id": 1, "name": "времена года", "emoji": "🍂"},
    {"id": 2, "name": "короткие", "emoji": "📝"},
    {"id": 3, "name": "народные", "emoji": "🏠"},
    {"id": 4, "name": "об учении", "emoji": "📚"},
    {"id": 5, "name": "о глупости", "emoji": "🤦"},
    {"id": 6, "name": "о добре", "emoji": "😇"},
    {"id": 7, "name": "о дружбе", "emoji": "🤝"},
    {"id": 8, "name": "о здоровье", "emoji": "💪"},
    {"id": 9, "name": "о знаниях", "emoji": "🧠"},
    {"id": 10, "name": "о книге", "emoji": "📖"},
    {"id": 11, "name": "о лени", "emoji": "😴"},
    {"id": 12, "name": "о любви", "emoji": "❤️"},
    {"id": 13, "name": "о мире", "emoji": "☮️"},
    {"id": 14, "name": "о природе", "emoji": "🌿"},
    {"id": 15, "name": "о родине", "emoji": "🇷🇺"},
    {"id": 16, "name": "о русском языке", "emoji": "🗣️"},
    {"id": 17, "name": "о семье", "emoji": "👨‍👩‍👧‍👦"},
    {"id": 18, "name": "о силе разума", "emoji": "💡"},
    {"id": 19, "name": "о труде", "emoji": "💼"},
    {"id": 20, "name": "о трудолюбии", "emoji": "🔨"},
    {"id": 21, "name": "о человеке", "emoji": "🧑"},
    {"id": 22, "name": "о чтении", "emoji": "📖"},
    {"id": 23, "name": "о школе", "emoji": "🏫"},
    {"id": 24, "name": "о языке", "emoji": "🗣️"},
    {"id": 25, "name": "про слово", "emoji": "💬"},
    {"id": 26, "name": "про утро", "emoji": "🌅"},
    {"id": 27, "name": "русские", "emoji": "🇷🇺"},
]

FALLBACK_PROVERBS = [
    {"id": 1, "text": "Без труда не вытащишь и рыбку из пруда.", "category_id": 19},
    {"id": 2, "text": "Терпение и труд всё перетрут.", "category_id": 19},
    {"id": 3, "text": "Семь раз отмерь, один раз отрежь.", "category_id": 18},
    {"id": 4, "text": "Любовь зла, полюбишь и козла.", "category_id": 12},
    {"id": 5, "text": "Друг познаётся в беде.", "category_id": 7},
    {"id": 6, "text": "В гостях хорошо, а дома лучше.", "category_id": 17},
    {"id": 7, "text": "Деньги не пахнут.", "category_id": 6},
    {"id": 8, "text": "Здоровье — дороже золота.", "category_id": 8},
    {"id": 9, "text": "Лень — мать всех пороков.", "category_id": 11},
    {"id": 10, "text": "Тише едешь, дальше будешь.", "category_id": 19},
    {"id": 11, "text": "Ум — хорошо, а два лучше.", "category_id": 18},
    {"id": 12, "text": "Правда глаза колет.", "category_id": 6},
    {"id": 13, "text": "Смелость города берёт.", "category_id": 5},
    {"id": 14, "text": "Учение — свет, а неучение — тьма.", "category_id": 4},
    {"id": 15, "text": "Одна ласточка весны не делает.", "category_id": 18},
    {"id": 16, "text": "Не всё то золото, что блестит.", "category_id": 18},
    {"id": 17, "text": "Слово — серебро, молчание — золото.", "category_id": 25},
    {"id": 18, "text": "Слово не воробей: вылетит — не поймаешь.", "category_id": 25},
    {"id": 19, "text": "Доброе слово человеку — что дождь в засуху.", "category_id": 25},
    {"id": 20, "text": "Кто рано встаёт, тому Бог подаёт.", "category_id": 19},
]


def load_data(proverbs_path: str) -> dict:
    try:
        with open(proverbs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categories": FALLBACK_CATEGORIES, "proverbs": FALLBACK_PROVERBS}


@router.message(Command("proverb"))
async def cmd_random_proverb(message: Message, db: Database, config: Config):
    data = load_data(config.PROVERBS_PATH)
    proverb = random.choice(data["proverbs"])

    await message.answer(
        f"📜 {proverb['text']}\n\n⭐ Добавить в избранное",
        reply_markup={"inline_keyboard": [[
            {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"}
        ]]}
    )


@router.message(Command("daily"))
async def cmd_daily(message: Message, db: Database, config: Config):
    from datetime import date
    today = date.today().isoformat()

    daily_id = await db.get_daily_proverb_id(today)
    if daily_id:
        data = load_data(config.PROVERBS_PATH)
        proverb = next((p for p in data["proverbs"] if p["id"] == daily_id), None)
        if proverb:
            await message.answer(f"📅 Пословица дня:\n\n📜 {proverb['text']}")
            return

    data = load_data(config.PROVERBS_PATH)
    proverb = random.choice(data["proverbs"])
    await db.set_daily_proverb(today, proverb["id"])

    await message.answer(
        f"📅 Пословица дня:\n\n📜 {proverb['text']}\n\n⭐ Добавить в избранное",
        reply_markup={"inline_keyboard": [[
            {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"}
        ]]}
    )


@router.callback_query(F.data.startswith("fav_add_"))
async def add_favorite(callback: CallbackQuery, db: Database):
    proverb_id = int(callback.data.split("_")[2])
    await db.add_favorite(callback.from_user.id, proverb_id)
    await callback.answer("✅ Добавлено в избранное!")
    await callback.message.edit_reply_markup()


@router.message(F.text & ~F.text.startswith("/"))
async def match_proverb(message: Message, db: Database, config: Config, ai_matcher: AIMatcher):
    data = load_data(config.PROVERBS_PATH)
    proverbs = data["proverbs"]

    matched_text = ai_matcher.match_proverb(message.text, proverbs)

    matched_proverb = next(
        (p for p in proverbs if p["text"].lower() in matched_text.lower() or matched_text.lower() in p["text"].lower()),
        None
    )

    if matched_proverb:
        await message.answer(
            f"📜 {matched_proverb['text']}\n\n⭐ Добавить в избранное",
            reply_markup={"inline_keyboard": [[
                {"text": "⭐ В избранное", "callback_data": f"fav_add_{matched_proverb['id']}"}
            ]]}
        )
    else:
        await message.answer(f"📜 {matched_text}")
