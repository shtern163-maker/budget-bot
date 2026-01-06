import re
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import init_db, add_record, add_learning, get_learned_category

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

init_db()

category_map = {
    "еда": ["еда", "продукты", "магазин"],
    "алкоголь": ["алкоголь", "пиво", "вино"],
    "авто": ["авто", "бензин", "заправка", "дт"],
    "зарплата юг": ["юг"],
    "зарплата чоп": ["чоп"],
}


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Привет 👋\n"
        "Просто напиши, например:\n"
        "бензин 2500\n"
        "Юг 50000"
    )


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    text = message.text.lower()

    match = re.search(r"(\d+)", text)
    if not match:
        await message.answer("Не нашёл сумму. Пример: бензин 2500")
        return

    amount = int(match.group(1))

    # 1️⃣ пробуем обученные слова
    category = get_learned_category(text)

    # 2️⃣ пробуем словарь
    if not category:
        for cat, keys in category_map.items():
            if any(k in text for k in keys):
                category = cat
                break

    # 3️⃣ если всё равно не поняли — спрашиваем
    if not category:
        kb = InlineKeyboardMarkup(row_width=2)
        for cat in category_map.keys():
            kb.add(
                InlineKeyboardButton(
                    text=cat,
                    callback_data=f"learn:{cat}:{text}"
                )
            )

        await message.answer(
            "Я не уверен в категории. Выбери один раз — я запомню 👇",
