from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import logging
import os
from dotenv import load_dotenv

# 📦 Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ✅ Разрешённые пользователи
ALLOWED_IDS = [446393818]  # Твой Telegram ID
BLACKLIST = set()

# 📋 Логирование
logging.basicConfig(filename='bot.log', level=logging.INFO)

# 🛡️ Проверка на спам
def is_suspicious(text: str) -> bool:
    blacklist_words = ["http://", "https://", "vpn", "bot", "admin", "SpeeeedVPNbot"]
    return any(word in text.lower() for word in blacklist_words)

# ▶ Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    logging.info(f"Пользователь {user.id} вызвал /start")

    keyboard = [
        [KeyboardButton("🆓 Бесплатный разбор")],
        [KeyboardButton("💸 Платный разбор от 15$")],
        [KeyboardButton("👑 Пакет VIP от 60$")],
        [KeyboardButton("📜 Обо мне / Отзывы")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=user.id,
        text="👇 Выберите один из пунктов меню:",
        reply_markup=reply_markup
    )

# 💬 Обработка текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if is_suspicious(text):
        BLACKLIST.add(user.id)
        await context.bot.send_message(
            chat_id=user.id,
            text="⚠️ Обнаружен спам. Вы занесены в чёрный список."
        )
        logging.warning(f"[SPAM] User {user.id}: {text}")
        return

    if text == "🆓 Бесплатный разбор":
        await update.message.reply_text("🎁 Отправьте вашу дату рождения и вопрос — я сделаю бесплатный разбор.")
    elif text == "💸 Платный разбор от 15$":
        await update.message.reply_text("💸 Чтобы заказать платный разбор, напишите: /paid")
    elif text == "👑 Пакет VIP от 60$":
        await update.message.reply_text("👑 VIP-пакет включает личную встречу + поддержку 7 дней.")
    elif text == "📜 Обо мне / Отзывы":
        await update.message.reply_text("📜 Меня зовут Викрам. Я — психолог и аналитик по Human Design.\nОтзывы — https://t.me/VikramReviews")
    else:
        await update.message.reply_text("Выберите действие из меню ниже 👇")

# 🚀 Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
