
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

LANGUAGES = {
    "uz": {
        "welcome": "🎮 GAMEPULSE ga xush kelibsiz!\n\nO'yinlar dunyosi shu yerdan boshlanadi!",
        "games": "🎮 O'yinlar",
        "trending": "🔥 Trenddagi o'yinlar",
        "news": "📰 Gaming yangiliklari",
        "esports": "🏆 Kibersport",
        "languages": "🌍 Tillar",
        "choose": "Bo'limni tanlang:",
        "selected": "🇺🇿 O'zbek tili tanlandi!",
        "coming": "Tez orada qo'shiladi!"
    },
    "en": {
        "welcome": "🎮 Welcome to GAMEPULSE!\n\nThe gaming world starts here!",
        "games": "🎮 Games",
        "trending": "🔥 Trending",
        "news": "📰 Gaming News",
        "esports": "🏆 Esports",
        "languages": "🌍 Languages",
        "choose": "Choose a section:",
        "selected": "🇬🇧 English selected!",
        "coming": "Coming soon!"
    },
    "ru": {
        "welcome": "🎮 Добро пожаловать в GAMEPULSE!\n\nМир игр начинается здесь!",
        "games": "🎮 Игры",
        "trending": "🔥 В тренде",
        "news": "📰 Игровые новости",
        "esports": "🏆 Киберспорт",
        "languages": "🌍 Языки",
        "choose": "Выберите раздел:",
        "selected": "🇷🇺 Русский язык выбран!",
        "coming": "Скоро появится!"
    }
}

user_languages = {}


def menu(lang):
    t = LANGUAGES[lang]

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["games"], callback_data="games")],
        [InlineKeyboardButton(text=t["trending"], callback_data="trending")],
        [InlineKeyboardButton(text=t["news"], callback_data="news")],
        [InlineKeyboardButton(text=t["esports"], callback_data="esports")],
        [InlineKeyboardButton(text=t["languages"], callback_data="languages")]
    ])


def language_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")]
    ])


async def show_menu(message, lang):
    t = LANGUAGES[lang]
    await message.edit_text(
        t["welcome"] + "\n\n" + t["choose"],
        reply_markup=menu(lang)
    )


@dp.message(CommandStart())
async def start(message: Message):
    user_languages[message.from_user.id] = "uz"
    t = LANGUAGES["uz"]

    await message.answer(
        t["welcome"] + "\n\n" + t["choose"],
        reply_markup=menu("uz")
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "GAMEPULSE Help\n\n/start - Main menu\n/help - Help"
    )


@dp.callback_query(F.data.startswith("lang_"))
async def select_language(call: CallbackQuery):
    lang = call.data.replace("lang_", "")

    if lang not in LANGUAGES:
        await call.answer("Unknown language", show_alert=True)
        return

    user_languages[call.from_user.id] = lang

    await call.answer(LANGUAGES[lang]["selected"])
    await show_menu(call.message, lang)


@dp.callback_query(F.data == "languages")
async def languages(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "🌍 Choose your language / Tilni tanlang / Выберите язык:",
        reply_markup=language_menu()
    )


@dp.callback_query(F.data.in_({"games", "trending", "news", "esports"}))
async def buttons(call: CallbackQuery):
    lang = user_languages.get(call.from_user.id, "uz")
    t = LANGUAGES[lang]

    names = {
        "games": t["games"],
        "trending": t["trending"],
        "news": t["news"],
        "esports": t["esports"]
    }

    await call.answer()
    await call.message.edit_text(
        f"{names[call.data]}\n\n{t['coming']}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="⬅️ " + t["choose"],
                callback_data="back"
            )]
        ])
    )


@dp.callback_query(F.data == "back")
async def back(call: CallbackQuery):
    lang = user_languages.get(call.from_user.id, "uz")
    await call.answer()
    await show_menu(call.message, lang)


async def main():
    async with bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

