from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import logging
import os
from dotenv import load_dotenv

# ✅ Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

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

    reply_keyboard = [
        ["🆓 Бесплатный разбор"],
        ["💸 Платный разбор от 17$"],
        ["👑 Пакет VIP от 60$"],
        ["📜 Обо мне / Отзывы"],
        ["🔄 Обновить страницу"]
    ]
    await context.bot.send_message(
        chat_id=user.id,
        text="👇 Ниже выберите один из пунктов меню:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
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

    if text == "🆓 Бесплатный разбор":
        await context.bot.send_message(
            chat_id=user.id,
            text="Для заполнения формы нажмите на кнопку ниже:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 Заполнить форму", url="https://freehumandesignchart.com/")]
            ])
        )

    elif text == "💸 Платный разбор от 17$":
        await context.bot.send_message(
            chat_id=user.id,
            text="Нажмите на кнопку ниже, чтобы написать мне:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👉 Написать мне", url="https://t.me/Vikram_2027")]
            ])
        )

    elif text == "👑 Пакет VIP от 60$":
        await context.bot.send_message(
            chat_id=user.id,
            text="Нажмите на кнопку ниже, чтобы оформить VIP:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👉 Написать мне", url="https://t.me/Vikram_2027")]
            ])
        )

    elif text == "📜 Обо мне / Отзывы":
        await context.bot.send_message(
            chat_id=user.id,
            text="Отзывы и информация — по кнопке ниже:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👉 Написать мне", url="https://t.me/Vikram_2027")]
            ])
        )

    elif text == "🔄 Обновить страницу":
        await start(update, context)

    else:
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
