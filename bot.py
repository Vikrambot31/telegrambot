import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv
import logging

# ✅ Загрузка переменных окружения
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

# ▶ Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    logging.info(f"User {user.id} вызвал /start")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["🆓 Бесплатный разбор"],
            ["💸 Платный разбор от 17$"],
            ["👑 Пакет VIP от 60$"],
            ["📜 Обо мне / Отзывы"]
        ],
        resize_keyboard=True
    )

    await context.bot.send_message(
        chat_id=user.id,
        text="👇 Ниже выбери нужное действие:",
        reply_markup=keyboard
    )

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

    await context.bot.send_message(chat_id=user.id, text=f"✅ Получено: {text}")

# 🚀 Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
