import re
import os
from aiogram import Bot, Dispatcher, executor, types

from config import BOT_TOKEN
from db import add_record, get_month_stats, get_month_total
from categories import EXPENSES, INCOME
from voice import voice_to_text

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def parse_text(text):
    text = text.lower()
    nums = re.findall(r"\d+", text)
    if not nums:
        return None

    amount = float(nums[0])

    for c in EXPENSES:
        if c in text:
            return amount, c, "expense"

    for c in INCOME:
        if c in text:
            return amount, c, "income"

    return None


@dp.message_handler(commands=["month"])
async def month_stats(message: types.Message):
    totals = get_month_total()
    text = "📅 Итоги за месяц:\n\n"
    for t, s in totals:
        label = "Расходы" if t == "expense" else "Доходы"
        text += f"{label}: {int(s)} ₽\n"
    await message.answer(text)


@dp.message_handler(commands=["stats"])
async def category_stats(message: types.Message):
    stats = get_month_stats()
    if not stats:
        await message.answer("Пока нет данных")
        return

    text = "📊 Расходы по категориям:\n\n"
    for cat, total in stats:
        text += f"{cat}: {int(total)} ₽\n"
    await message.answer(text)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def text_handler(message: types.Message):
    parsed = parse_text(message.text)
    if not parsed:
        await message.answer("Не понял. Пример: еда 450")
        return

    amount, category, rtype = parsed
    add_record(amount, category, rtype)
    await message.answer(f"Записал: {category} — {amount} ₽")


@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_handler(message: types.Message):
    file = await bot.get_file(message.voice.file_id)
    path = f"voice_{message.message_id}.ogg"
    await bot.download_file(file.file_path, path)

    text = voice_to_text(path)
    os.remove(path)

    parsed = parse_text(text)
    if not parsed:
        await message.answer(f"Распознал: {text}\nНо не понял запись.")
        return

    amount, category, rtype = parsed
    add_record(amount, category, rtype)
    await message.answer(f"🎤 {text}\nЗаписал: {category} — {amount} ₽")


if __name__ == "__main__":
    executor.start_polling(dp)
