from telegram import Update, ReplyKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import asyncio

# ✅ Токен бота
TOKEN = os.getenv("BOT_TOKEN") or "7419809164:AAFq1oaDm6KUWp57kQhaPt1I6gwIo1ihnB4"

# ✅ Пользователи
ALLOWED_IDS = [446393818]
BLACKLIST = set()

# ✅ Клавиатура (меню внизу)
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        ["🆓 Бесплатный разбор"],
        ["💸 Платный разбор от 15$"],
        ["👑 Пакет VIP от 60$"],
        ["📜 Обо мне / Отзывы"]
    ],
    resize_keyboard=True
)

# ✅ Проверка текста на спам
def is_suspicious(text: str) -> bool:
    return any(word in text.lower() for word in ["http://", "https://", "vpn", "bot", "admin"])

# 🟢 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return
    await context.bot.send_photo(chat_id=user.id, photo=open("s1.webp", "rb"))
    await context.bot.send_voice(chat_id=user.id, voice=open("intro-0.ogg", "rb"))
    await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=menu_keyboard)

# 💬 Обработка текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if is_suspicious(text):
        await update.message.reply_text("⚠️ Подозрительное сообщение. Вы заблокированы.")
        BLACKLIST.add(user.id)
        return

    if text == "🆓 Бесплатный разбор":
        await context.bot.send_media_group(chat_id=user.id, media=[
            InputMediaPhoto(open("pic1.png", "rb")),
            InputMediaPhoto(open("pic2.png", "rb")),
            InputMediaPhoto(open("pic3.png", "rb")),
        ])
        await context.bot.send_voice(chat_id=user.id, voice=open("x1.ogg", "rb"))
        await update.message.reply_text("Форма: https://freehumandesignchart.com/")
        await update.message.reply_text("Написать мне 👉 https://t.me/Vikram_2027")

    elif text == "💸 Платный разбор от 15$":
        await context.bot.send_photo(chat_id=user.id, photo=open("pic4.png", "rb"))
        await context.bot.send_photo(chat_id=user.id, photo=open("pic5.png", "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("x2.ogg", "rb"))
        await update.message.reply_text("Написать мне 👉 https://t.me/Vikram_2027")

    elif text == "👑 Пакет VIP от 60$":
        await context.bot.send_photo(chat_id=user.id, photo=open("pic6.png", "rb"))
        await context.bot.send_photo(chat_id=user.id, photo=open("pic5.png", "rb"))
        await context.bot.send_photo(chat_id=user.id, photo=open("Voprosi.png", "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("x3.ogg", "rb"))
        await update.message.reply_text("Написать мне 👉 https://t.me/Vikram_2027")

    elif text == "📜 Обо мне / Отзывы":
        await update.message.reply_text("Отзывы и система:\nhttps://www.instagram.com/vikram_hd_2027")
        await context.bot.send_document(chat_id=user.id, document=open("Prognoz_Love_god.pdf", "rb"))
        await context.bot.send_document(chat_id=user.id, document=open("primer_prognoz2.pdf", "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("primer_razbora.ogg", "rb"))
        await update.message.reply_text("Написать мне 👉 https://t.me/Vikram_2027")

# 🚀 Запуск
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print(f"✅ Бот запущен с токеном: {TOKEN}")
    await app.run_polling()

# 🔧 Без конфликтов в asyncio
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e).startswith("This event loop is already running"):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
