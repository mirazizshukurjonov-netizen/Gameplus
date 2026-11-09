
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi! Hosting Variables bo‘limini tekshir.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

languages = {}
scores = {}
played = {}
searching = set()
quiz_index = {}
quiz_points = {}

TEXT = {
    "uz": {
        "welcome": "🎮 GAMEPULSE ga xush kelibsiz!",
        "games": "🎮 O‘yinlar",
        "trending": "🔥 Trenddagi o‘yinlar",
        "news": "📰 Gaming yangiliklari",
        "esports": "🏆 Esports",
        "quiz": "🧠 Quiz",
        "profile": "👤 Profil",
        "search": "🔎 O‘yin qidirish",
        "language": "🌍 Tilni tanlash",
        "back": "⬅️ Orqaga",
        "choose": "Platformani tanlang:",
        "pc": "💻 PC",
        "mobile": "📱 Mobile",
        "console": "🎮 Console",
        "soon": "🚧 Bu bo‘lim keyingi yangilanishda ishga tushadi!",
        "search_prompt": "🔎 O‘yin nomini yozing:",
        "not_found": "😕 O‘yin topilmadi.",
        "profile_text": "👤 Profil\n\n⭐ Ball: {score}\n🧠 Quizlar: {played}",
        "quiz_start": "🧠 Quiz boshlandi! Javobni tanlang:",
        "correct": "✅ To‘g‘ri!",
        "wrong": "❌ Noto‘g‘ri!",
        "finished": "🏁 Quiz tugadi!\n⭐ Natijangiz: {score}/3",
        "next": "➡️ Keyingi savol",
        "again": "🔄 Yana o‘ynash"
    },
    "en": {
        "welcome": "🎮 Welcome to GAMEPULSE!",
        "games": "🎮 Games",
        "trending": "🔥 Trending games",
        "news": "📰 Gaming news",
        "esports": "🏆 Esports",
        "quiz": "🧠 Quiz",
        "profile": "👤 Profile",
        "search": "🔎 Search games",
        "language": "🌍 Choose language",
        "back": "⬅️ Back",
        "choose": "Choose a platform:",
        "pc": "💻 PC",
        "mobile": "📱 Mobile",
        "console": "🎮 Console",
        "soon": "🚧 Coming in a future update!",
        "search_prompt": "🔎 Enter a game name:",
        "not_found": "😕 Game not found.",
        "profile_text": "👤 Profile\n\n⭐ Points: {score}\n🧠 Quizzes: {played}",
        "quiz_start": "🧠 Quiz started! Choose an answer:",
        "correct": "✅ Correct!",
        "wrong": "❌ Incorrect!",
        "finished": "🏁 Quiz finished!\n⭐ Your score: {score}/3",
        "next": "➡️ Next question",
        "again": "🔄 Play again"
    },
    "ru": {
        "welcome": "🎮 Добро пожаловать в GAMEPULSE!",
        "games": "🎮 Игры",
        "trending": "🔥 Популярные игры",
        "news": "📰 Игровые новости",
        "esports": "🏆 Киберспорт",
        "quiz": "🧠 Викторина",
        "profile": "👤 Профиль",
        "search": "🔎 Поиск игр",
        "language": "🌍 Выбрать язык",
        "back": "⬅️ Назад",
        "choose": "Выберите платформу:",
        "pc": "💻 PC",
        "mobile": "📱 Mobile",
        "console": "🎮 Console",
        "soon": "🚧 Скоро появится в обновлении!",
        "search_prompt": "🔎 Введите название игры:",
        "not_found": "😕 Игра не найдена.",
        "profile_text": "👤 Профиль\n\n⭐ Очки: {score}\n🧠 Викторины: {played}",
        "quiz_start": "🧠 Викторина началась! Выберите ответ:",
        "correct": "✅ Правильно!",
        "wrong": "❌ Неправильно!",
        "finished": "🏁 Викторина завершена!\n⭐ Ваш результат: {score}/3",
        "next": "➡️ Следующий вопрос",
        "again": "🔄 Играть снова"
    }
}

GAMES = {
    "pc": [
        "Minecraft", "Counter-Strike 2", "Grand Theft Auto V",
        "Valorant", "Fortnite", "Roblox", "Dota 2",
        "Red Dead Redemption 2"
    ],
    "mobile": [
        "PUBG Mobile", "Mobile Legends", "Brawl Stars",
        "Call of Duty Mobile", "Minecraft", "Roblox",
        "Clash Royale", "Free Fire"
    ],
    "console": [
        "God of War", "Spider-Man 2", "Gran Turismo 7",
        "The Legend of Zelda", "Mario Kart 8",
        "Minecraft", "Fortnite"
    ]
}

QUIZ = [
    {
        "q": {
            "uz": "Minecraft o‘yinida asosiy qurilish materiali nima?",
            "en": "What is a common building material in Minecraft?",
            "ru": "Какой материал часто используют для строительства в Minecraft?"
        },
        "a": ["Yog‘och / Wood", "Suv / Water", "Bulut / Cloud"],
        "correct": 0
    },
    {
        "q": {
            "uz": "PUBG Mobile qaysi janrga kiradi?",
            "en": "What genre is PUBG Mobile?",
            "ru": "К какому жанру относится PUBG Mobile?"
        },
        "a": ["Poyga / Racing", "Battle Royale", "Puzzle"],
        "correct": 1
    },
    {
        "q": {
            "uz": "Counter-Strike 2 qanday o‘yin?",
            "en": "What type of game is Counter-Strike 2?",
            "ru": "Что за игра Counter-Strike 2?"
        },
        "a": ["Sport", "Puzzle", "Taktik FPS"],
        "correct": 2
    }
]

def lang(uid):
    return languages.get(uid, "uz")

def t(uid, key):
    return TEXT[lang(uid)][key]

def button(label, data):
    return InlineKeyboardButton(text=label, callback_data=data)

def main_keyboard(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [button(t(uid, "games"), "games")],
        [button(t(uid, "trending"), "trending"),
         button(t(uid, "news"), "news")],
        [button(t(uid, "esports"), "esports"),
         button(t(uid, "quiz"), "quiz")],
        [button(t(uid, "profile"), "profile"),
         button(t(uid, "search"), "search")],
        [button(t(uid, "language"), "language")]
    ])

def back_keyboard(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [button(t(uid, "back"), "home")]
    ])

async def show_home(message, uid):
    await message.edit_text(
        t(uid, "welcome"),
        reply_markup=main_keyboard(uid)
    )

@dp.message(F.text == "/start")
async def start(message: Message):
    uid = message.from_user.id
    languages.setdefault(uid, "uz")
    scores.setdefault(uid, 0)
    played.setdefault(uid, 0)
    await message.answer(
        t(uid, "welcome"),
        reply_markup=main_keyboard(uid)
    )

@dp.callback_query(F.data == "home")
async def home(call: CallbackQuery):
    await call.answer()
    await show_home(call.message, call.from_user.id)

@dp.callback_query(F.data == "games")
async def games(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [button(t(uid, "pc"), "platform_pc")],
        [button(t(uid, "mobile"), "platform_mobile")],
        [button(t(uid, "console"), "platform_console")],
        [button(t(uid, "back"), "home")]
    ])
    await call.message.edit_text(t(uid, "choose"), reply_markup=kb)

@dp.callback_query(F.data.startswith("platform_"))
async def platform(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    category = call.data.split("_")[1]
    games_list = GAMES[category]
    title = "\n".join("🎮 " + game for game in games_list)
    await call.message.edit_text(
        title,
        reply_markup=back_keyboard(uid)
    )

@dp.callback_query(F.data.in_({"trending", "news", "esports"}))
async def future_sections(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    await call.message.edit_text(
        t(uid, "soon"),
        reply_markup=back_keyboard(uid)
    )

@dp.callback_query(F.data == "language")
async def language_menu(call: CallbackQuery):
    await call.answer()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [button("🇺🇿 O‘zbekcha", "lang_uz")],
        [button("🇬🇧 English", "lang_en")],
        [button("🇷🇺 Русский", "lang_ru")],
        [button(t(call.from_user.id, "back"), "home")]
    ])
    await call.message.edit_text("🌍 Choose your language / Tilni tanlang:", reply_markup=kb)

@dp.callback_query(F.data.startswith("lang_"))
async def set_language(call: CallbackQuery):
    uid = call.from_user.id
    languages[uid] = call.data.split("_")[1]
    await call.answer("✅")
    await show_home(call.message, uid)

@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    text = t(uid, "profile_text").format(
        score=scores.get(uid, 0),
        played=played.get(uid, 0)
    )
    await call.message.edit_text(text, reply_markup=back_keyboard(uid))

@dp.callback_query(F.data == "search")
async def search(call: CallbackQuery):
    uid = call.from_user.id
    searching.add(uid)
    await call.answer()
    await call.message.edit_text(
        t(uid, "search_prompt"),
        reply_markup=back_keyboard(uid)
    )

@dp.message(F.text & ~F.text.startswith("/"))
async def search_result(message: Message):
    uid = message.from_user.id
    if uid not in searching:
        return

    searching.discard(uid)
    query = message.text.lower()
    found = []

    for platform_name, game_list in GAMES.items():
        for game in game_list:
            if query in game.lower() and game not in found:
                found.append(game)

    if found:
        result = "🔎 " + "\n".join("🎮 " + game for game in found)
    else:
        result = t(uid, "not_found")

    await message.answer(result, reply_markup=main_keyboard(uid))

async def show_question(message, uid):
    index = quiz_index[uid]
    q = QUIZ[index]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button(answer, f"answer_{index}_{i}")]
        for i, answer in enumerate(q["a"])
    ])
    await message.edit_text(
        f"🧠 {index + 1}/3\n\n{q['q'][lang(uid)]}",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "quiz")
async def quiz_start(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    quiz_index[uid] = 0
    quiz_points[uid] = 0
    await show_question(call.message, uid)

@dp.callback_query(F.data.startswith("answer_"))
async def quiz_answer(call: CallbackQuery):
    uid = call.from_user.id
    await call.answer()
    _, index, choice = call.data.split("_")
    index = int(index)
    choice = int(choice)

    if index != quiz_index.get(uid):
        return

    if choice == QUIZ[index]["correct"]:
        quiz_points[uid] += 1
        scores[uid] = scores.get(uid, 0) + 1
        result = t(uid, "correct")
    else:
        result = t(uid, "wrong")

    next_index = index + 1

    if next_index < len(QUIZ):
        quiz_index[uid] = next_index
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [button(t(uid, "next"), "quiz_next")]
        ])
        await call.message.edit_text(result, reply_markup=kb)
    else:
        played[uid] = played.get(uid, 0) + 1
        final_score = quiz_points[uid]
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [button(t(uid, "again"), "quiz")],
            [button(t(uid, "back"), "home")]
        ])
        await call.message.edit_text(
            t(uid, "finished").format(score=final_score),
            reply_markup=kb
        )

@dp.callback_query(F.data == "quiz_next")
async def quiz_next(call: CallbackQuery):
    await call.answer()
    await show_question(call.message, call.from_user.id)

async def main():
    print("GAMEPULSE is running!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

    
