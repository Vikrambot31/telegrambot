from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
import os
import logging
from dotenv import load_dotenv

# Сохрани сюда свой ключ (ОСТОРОЖНО, не выкладывай публично!)
secret_key = "tKSi68...VIVkE="  # <- вставь сюда свой секретный ключ

# Расшифровка файла .env.enc
if os.path.exists(".env.enc"):
    fernet = Fernet(secret_key)
    with open(".env.enc", "rb") as enc_file:
        decrypted_data = fernet.decrypt(enc_file.read())
    with open(".env", "wb") as dec_file:
        dec_file.write(decrypted_data)

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

ALLOWED_IDS = [446393818]  # твой ID
BLACKLIST = set()

# Логирование
logging.basicConfig(filename='bot.log', level=logging.INFO)

# 🚫 Проверка на вредоносные ссылки
def is_suspicious(text: str) -> bool:
    return any(word in text.lower() for word in ["http://", "https://", "SpeeeedVPNbot"])

# 🧹 Автоочистка
async def clear_chat_history(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in ALLOWED_IDS:
        try:
            await context.bot.send_message(chat_id, "🧹 Автоочистка истории чата...")
        except Exception as e:
            logging.warning(f"[ОЧИСТКА] Ошибка: {e}")

# 🔘 Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    logging.info(f"User {user.id} вызвал /start")

    keyboard = [
        [InlineKeyboardButton("🆓 Бесплатный разбор", callback_data="free")],
        [InlineKeyboardButton("🐝 Платный разбор от 17$", callback_data="paid")],
        [InlineKeyboardButton("👑 Пакет VIP от 60$", callback_data="vip")],
        [InlineKeyboardButton("📜 Обо мне / Отзывы", callback_data="about")],
        [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if os.path.exists("s1.webp"):
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id=user.id, sticker=sticker)

    await context.bot.send_message(chat_id=user.id, text="👇 Ниже вы можете выбрать действие:", reply_markup=reply_markup)

# 🖱 Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    if user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if query.data == "refresh":
        return await start(update, context)

    await context.bot.send_message(chat_id=user.id, text=f"Вы выбрали: {query.data}")

# 💬 Обработка обычных сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if text.startswith("/"):
        return

    if is_suspicious(text):
        await context.bot.send_message(chat_id=user.id, text="⚠️ Обнаружена подозрительная активность. Вы занесены в чёрный список.")
        BLACKLIST.add(user.id)
        logging.warning(f"User {user.id} добавлен в BLACKLIST: {text}")
        return

    await context.bot.send_message(chat_id=user.id, text="Я вас понял.")

# 🔧 post_init для JobQueue
async def setup_jobs(app):
    app.job_queue.run_repeating(clear_chat_history, interval=900, first=10)

# 🚀 Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(setup_jobs).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == '__main__':
    main()
