from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters, JobQueue
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
import os
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_IDS = [446393818]

# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Очистка чата каждые 15 минут
async def clear_chat_history(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in ALLOWED_IDS:
        try:
            await context.bot.send_message(chat_id, "🧹 Автоочистка истории чата...")
        except Exception as e:
            logging.warning(f"Ошибка при очистке: {e}")

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    if chat_id not in ALLOWED_IDS:
        return

    logging.info(f"User {chat_id} вызвал /start")

    keyboard = [
        [InlineKeyboardButton("🆓 Бесплатный разбор", callback_data="free")],
        [InlineKeyboardButton("🐝 Платный разбор от 17$", callback_data="paid")],
        [InlineKeyboardButton("👑 Пакет VIP от 60$", callback_data="vip")],
        [InlineKeyboardButton("📜 Обо мне / Отзывы", callback_data="about")],
        [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка картинки и стикера
    if os.path.exists("s1.webp"):
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)

    await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=reply_markup)

# Обработка нажатия кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id

    if chat_id not in ALLOWED_IDS:
        return

    data = query.data
    if data == "refresh":
        await context.bot.send_message(chat_id, "♻️ Обновление страницы...")
        return await start(update, context)

    await context.bot.send_message(chat_id, f"Вы выбрали: {data}")

# Обработка обычных сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_user.id

    if chat_id not in ALLOWED_IDS:
        return
    if text.startswith("/"):
        return
    if "SpeeeedVPNbot" in text or "http://" in text or "https://" in text:
        await context.bot.send_message(chat_id, "⚠️ Обнаружена подозрительная активность. Завершаю.")
        return

    await context.bot.send_message(chat_id, "Я вас понял.")

# 🚀 Основная функция запуска
async def post_init(application):
    # Явное создание и регистрация задачи в job_queue
    application.job_queue.run_repeating(clear_chat_history, interval=900, first=10)

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == '__main__':
    main()
