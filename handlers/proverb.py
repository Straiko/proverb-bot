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
        return get_builtin_proverbs()


def get_builtin_proverbs() -> dict:
    return {
        "categories": [
            {"id": 1, "name": "мудрость", "emoji": "🧠"},
            {"id": 2, "name": "любовь", "emoji": "❤️"},
            {"id": 3, "name": "работа", "emoji": "💼"},
            {"id": 4, "name": "дружба", "emoji": "🤝"},
            {"id": 5, "name": "семья", "emoji": "👨‍👩‍👧‍👦"},
            {"id": 6, "name": "деньги", "emoji": "💰"},
            {"id": 7, "name": "удача", "emoji": "🍀"},
            {"id": 8, "name": "здоровье", "emoji": "💪"},
            {"id": 9, "name": "лень", "emoji": "😴"},
            {"id": 10, "name": "терпение", "emoji": "⏳"},
        ],
        "proverbs": [
            {"id": 1, "text": "Не откладывай на завтра то, что можешь сделать сегодня.", "category_id": 3},
            {"id": 2, "text": "Терпение и труд всё перетрут.", "category_id": 10},
            {"id": 3, "text": "Без труда не вытащишь и рыбку из пруда.", "category_id": 3},
            {"id": 4, "text": "Голова без ума — как фонарь без свечи.", "category_id": 1},
            {"id": 5, "text": "Друг познаётся в беде.", "category_id": 4},
            {"id": 6, "text": "Лучше поздно, чем никогда.", "category_id": 10},
            {"id": 7, "text": "На бога надейся, а сам не плошай.", "category_id": 7},
            {"id": 8, "text": "Одна ласточка весны не делает.", "category_id": 1},
            {"id": 9, "text": "Под лежачий камень вода не течёт.", "category_id": 3},
            {"id": 10, "text": "Семь раз отмерь, один раз отрежь.", "category_id": 1},
            {"id": 11, "text": "Тише едешь, дальше будешь.", "category_id": 10},
            {"id": 12, "text": "Ум — хорошо, а два лучше.", "category_id": 1},
            {"id": 13, "text": "Хочешь есть калачи — не сиди на печи.", "category_id": 3},
            {"id": 14, "text": "Что посеешь, то и пожнёшь.", "category_id": 1},
            {"id": 15, "text": "Язык до Киева доведёт.", "category_id": 1},
            {"id": 16, "text": "Любовь зла, полюбишь и козла.", "category_id": 2},
            {"id": 17, "text": "Влюблённому всё не спится.", "category_id": 2},
            {"id": 18, "text": "Сердцу не прикажешь.", "category_id": 2},
            {"id": 19, "text": "Любовь — не картошка, не выбросишь из огорода.", "category_id": 2},
            {"id": 20, "text": "Где любовь, там и Бог.", "category_id": 2},
            {"id": 21, "text": "Работа — не волк, в лес не убежит.", "category_id": 3},
            {"id": 22, "text": "Труд кормит, а лень портит.", "category_id": 3},
            {"id": 23, "text": "Кто не работает, тот не ест.", "category_id": 3},
            {"id": 24, "text": "Дело мастера боится.", "category_id": 3},
            {"id": 25, "text": "Один в поле не воин.", "category_id": 4},
            {"id": 26, "text": "Старый друг лучше новых двух.", "category_id": 4},
            {"id": 27, "text": "Друзья познаются в беде.", "category_id": 4},
            {"id": 28, "text": "Не имей сто рублей, а имей сто друзей.", "category_id": 4},
            {"id": 29, "text": "В семье союз, так и дом не разрушится.", "category_id": 5},
            {"id": 30, "text": "Семья — крепость, пока в ней любовь.", "category_id": 5},
            {"id": 31, "text": "В гостях хорошо, а дома лучше.", "category_id": 5},
            {"id": 32, "text": "Дитя — цветок жизни.", "category_id": 5},
            {"id": 33, "text": "Деньги не пахнут.", "category_id": 6},
            {"id": 34, "text": "Деньги — не всё, но без них — ничего.", "category_id": 6},
            {"id": 35, "text": "Грех да беда, кому нет и холода.", "category_id": 6},
            {"id": 36, "text": "Везёт тому, кто ждёт.", "category_id": 7},
            {"id": 37, "text": "Счастье любит тишину.", "category_id": 7},
            {"id": 38, "text": "Кто ищет, тот найдёт.", "category_id": 7},
            {"id": 39, "text": "Здоровье — дороже золота.", "category_id": 8},
            {"id": 40, "text": "Болен — лечись, а здоров берегись.", "category_id": 8},
            {"id": 41, "text": "Движение — жизнь.", "category_id": 8},
            {"id": 42, "text": "В здоровом теле — здоровый дух.", "category_id": 8},
            {"id": 43, "text": "Лень — мать всех пороков.", "category_id": 9},
            {"id": 44, "text": "Ленивому всё не успеть.", "category_id": 9},
            {"id": 45, "text": "Терпение — золото.", "category_id": 10},
            {"id": 46, "text": "Жди и дождёшься.", "category_id": 10},
            {"id": 47, "text": "Время — лучший лекарь.", "category_id": 10},
            {"id": 48, "text": "Мудрость приходит с опытом.", "category_id": 1},
            {"id": 49, "text": "Знание — сила.", "category_id": 1},
            {"id": 50, "text": "Учение — свет, а неучение — тьма.", "category_id": 1},
            {"id": 51, "text": "Кто хочет — тот добьётся.", "category_id": 1},
            {"id": 52, "text": "Не всё то золото, что блестит.", "category_id": 1},
            {"id": 53, "text": "Правда глаза колет.", "category_id": 1},
            {"id": 54, "text": "Кто рано встаёт, тому Бог подаёт.", "category_id": 3},
            {"id": 55, "text": "Поспешай медленно.", "category_id": 10},
            {"id": 56, "text": "В тесноте, да не в обиде.", "category_id": 1},
            {"id": 57, "text": "Не всё сразу, а всё по порядку.", "category_id": 10},
            {"id": 58, "text": "Лучше синица в руках, чем журавль в небе.", "category_id": 7},
            {"id": 59, "text": "Мал золотник, да дорог.", "category_id": 6},
            {"id": 60, "text": "Бережёного Бог бережёт.", "category_id": 8},
            {"id": 61, "text": "Голь на выдумки хитра.", "category_id": 6},
            {"id": 62, "text": "Не всё коту масленица.", "category_id": 1},
            {"id": 63, "text": "На чужой каравай рот не разевай.", "category_id": 6},
            {"id": 64, "text": "Пока гром не грянет, мужик не перекрестится.", "category_id": 10},
            {"id": 65, "text": "Волков бояться — в лес не ходить.", "category_id": 7},
            {"id": 66, "text": "Дарёному коню в зубы не смотрят.", "category_id": 6},
            {"id": 67, "text": "Конец — делу венец.", "category_id": 3},
            {"id": 68, "text": "Не спи — смотри, не зевай — слушай.", "category_id": 1},
            {"id": 69, "text": "Одна голова хорошо, а две лучше.", "category_id": 1},
            {"id": 70, "text": "Кто не рискует, тот не пьёт шампанского.", "category_id": 7},
        ],
    }


@router.message(Command("proverb"))
async def cmd_random_proverb(message: Message, db: Database, config: Config):
    data = load_proverbs(config.PROVERBS_PATH)
    proverbs = data["proverbs"]
    proverb = random.choice(proverbs)

    await message.answer(
        f"📜 {proverb['text']}\n\n⭐ Добавить в избранное",
        reply_markup={
            "inline_keyboard": [[
                {"text": "⭐ В избранное", "callback_data": f"fav_add_{proverb['id']}"},
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
        f"📅 Пословица дня:\n\n📜 {proverb['text']}\n\n⭐ Добавить в избранное",
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
            f"📜 {matched_proverb['text']}\n\n⭐ Добавить в избранное",
            reply_markup={
                "inline_keyboard": [[
                    {"text": "⭐ В избранное", "callback_data": f"fav_add_{matched_proverb['id']}"}
                ]]
            }
        )
    else:
        await message.answer(f"📜 {matched_text}")
