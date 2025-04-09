import os
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = 446393818

# Главное меню
def get_main_keyboard():
    keyboard = [
        ["🆓 Бесплатный разбор"],
        ["💸 Платный разбор от 15$"],
        ["👑 Пакет VIP от 60$"],
        ["📜 Обо мне / Отзывы"],
        ["🔄 Обновить страницу"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔ Доступ запрещён.")
        return

    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=InputFile("s1.webp"))
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=InputFile("intro-0.ogg"))
    await update.message.reply_text("👇 Выберите действие:", reply_markup=get_main_keyboard())

# Обработка всех сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔ У вас нет доступа.")
        return

    if text == "🆓 Бесплатный разбор":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic1.png"))
        await update.message.reply_text("🧠 Расшифровать самому", reply_markup=get_main_keyboard())

    elif text == "💸 Платный разбор от 15$":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic2.png"))
        await update.message.reply_text("💳 Для оплаты напишите мне", reply_markup=get_main_keyboard())

    elif text == "👑 Пакет VIP от 60$":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic3.png"))
        await update.message.reply_text("👑 VIP пакет включает всё!", reply_markup=get_main_keyboard())

    elif text == "📜 Обо мне / Отзывы":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic4.png"))
        await update.message.reply_text("🧠 Психолог. Аналитик. Гид по саморазвитию.", reply_markup=get_main_keyboard())

    elif text == "🔄 Обновить страницу":
        await start(update, context)

    else:
        await update.message.reply_text("Выберите действие из меню 👇", reply_markup=get_main_keyboard())

# Запуск
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
