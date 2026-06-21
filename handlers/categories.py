import json
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

router = Router()

DATA_DIR = Path(__file__).parent.parent / "data"


def load_proverbs() -> dict:
    with open(DATA_DIR / "proverbs.json", "r", encoding="utf-8") as f:
        return json.load(f)


@router.message(Command("categories"))
async def cmd_categories(message: Message):
    data = load_proverbs()
    categories = data["categories"]

    text = "📂 Категории пословиц:\n\n"
    buttons = []

    for cat in categories:
        text += f"{cat['emoji']} {cat['name']}\n"
        buttons.append([{"text": f"{cat['emoji']} {cat['name']}", "callback_data": f"cat_{cat['id']}"}])

    await message.answer(text, reply_markup={"inline_keyboard": buttons})


@router.callback_query(F.data.startswith("cat_"))
async def show_category(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    data = load_proverbs()

    category = next((c for c in data["categories"] if c["id"] == category_id), None)
    proverbs = [p for p in data["proverbs"] if p["category_id"] == category_id]

    if not category:
        await callback.answer("Категория не найдена")
        return

    text = f"{category['emoji']} {category['name'].upper()}\n\n"

    for i, p in enumerate(proverbs[:10], 1):
        text += f"{i}. {p['text']}\n"

    if len(proverbs) > 10:
        text += f"\n... и ещё {len(proverbs) - 10} пословиц"

    await callback.message.edit_text(text)
    await callback.answer()


@router.message(Command("category"))
async def cmd_category(message: Message):
    data = load_proverbs()
    categories = data["categories"]

    buttons = []
    for cat in categories:
        buttons.append([{"text": f"{cat['emoji']} {cat['name']}", "callback_data": f"cat_{cat['id']}"}])

    await message.answer(
        "Выберите категорию:",
        reply_markup={"inline_keyboard": buttons}
    )
