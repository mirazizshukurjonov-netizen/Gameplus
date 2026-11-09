
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN Railway Variables da topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Games", callback_data="games")],
        [InlineKeyboardButton(text="🔥 Trending", callback_data="trending")],
        [InlineKeyboardButton(text="📰 Gaming News", callback_data="news")],
        [InlineKeyboardButton(text="🏆 Esports", callback_data="esports")],
        [InlineKeyboardButton(text="🌍 Languages", callback_data="languages")]
    ])


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎮 Welcome to GAMEPULSE!\n\n"
        "Gaming world starts here!\n"
        "Choose a section below:",
        reply_markup=menu()
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ GAMEPULSE Help\n\n"
        "/start - Open main menu\n"
        "/help - Show help"
    )


@dp.callback_query(F.data)
async def buttons(call: CallbackQuery):
    pages = {
        "games": "🎮 GAMES\n\nGame collection is coming soon!",
        "trending": "🔥 TRENDING\n\nTrending games are coming soon!",
        "news": "📰 GAMING NEWS\n\nLatest gaming news is coming soon!",
        "esports": "🏆 ESPORTS\n\nEsports updates are coming soon!",
        "languages": "🌍 LANGUAGES\n\nUzbek | English | Русский"
    }

    text = pages.get(call.data)

    if text is None:
        await call.answer("Unknown button", show_alert=True)
        return

    await call.answer()
    await call.message.answer(text, reply_markup=menu())


async def main():
    async with bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
