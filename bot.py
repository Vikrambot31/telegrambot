from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import logging
import os

# ✅ Загрузка переменных окружения
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# ✅ ID разрешённых пользователей
ALLOWED_IDS = [446393818]
BLACKLIST = set()

# ✅ Логирование
logging.basicConfig(filename='bot.log', level=logging.INFO)

# 🔍 Проверка на вредоносные фразы
def is_suspicious(text: str) -> bool:
    return any(word in text.lower() for word in ["http://", "https://", "vpn", "bot", "admin", "SpeeeedVPNbot"])

# 🧹 Автоочистка
async def clear_chat_history(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in ALLOWED_IDS:
        try:
            await context.bot.send_message(chat_id, "🧹 Автоочистка истории чата...")
        except Exception as e:
            logging.warning(f"[ОЧИСТКА] Ошибка: {e}")

# ▶ Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    logging.info(f"User {user.id} вызвал /start")

    # Кнопки для обычной клавиатуры
    keyboard = [
        [KeyboardButton("🆓 Бесплатный разбор")],
        [KeyboardButton("🐝 Платный разбор от 17$")],
        [KeyboardButton("👑 Пакет VIP от 60$")],
        [KeyboardButton("📜 Обо мне / Отзывы")],
        [KeyboardButton("🔄 Обновить страницу")]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=user.id,
        text="👇 Выберите действие:",
        reply_markup=reply_markup
    )

# 🔘 Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    text = update.message.text

    if text == "🔄 Обновить страницу":
        return await start(update, context)

    await context.bot.send_message(chat_id=user.id, text=f"Вы выбрали: {text}")

# 💬 Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if text.startswith("/"):
        return

    if is_suspicious(text):
        await context.bot.send_message(chat_id=user.id, text="⚠️ Обнаружена подозрительная активность. Вы занесены в чёрный список.")
        BLACKLIST.add(user.id)
        logging.warning(f"User {user.id} добавлен в BLACKLIST: {text}")
        return

    await context.bot.send_message(chat_id=user.id, text="✅ Я вас понял.")

# 🧠 post_init — JobQueue
async def setup_jobs(app):
    app.job_queue.run_repeating(clear_chat_history, interval=900, first=15)

# 🚀 Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(setup_jobs).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == '__main__':
    main()
