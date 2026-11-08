import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Games", callback_data="games")],
        [InlineKeyboardButton(text="📰 Gaming News", callback_data="news")],
        [InlineKeyboardButton(text="🔥 Trending Games", callback_data="trending")],
        [InlineKeyboardButton(text="🏆 Esports", callback_data="esports")],
        [InlineKeyboardButton(text="🌍 Languages", callback_data="languages")]
    ])
    await message.answer(
        "🎮 GAMEPULSE\nFeel the Game!\n\nWelcome to the world of gaming!",
        reply_markup=keyboard
    )

@dp.callback_query()
async def buttons(call):
    texts = {
        "games": "🎮 Games\nComing soon!",
        "news": "📰 Gaming News\nComing soon!",
        "trending": "🔥 Trending Games\nComing soon!",
        "esports": "🏆 Esports\nComing soon!",
        "languages": "🌍 Uzbek | English | Русский"
    }
    await call.answer()
    await call.message.answer(texts.get(call.data, "GAMEPULSE"))

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
