import os
import logging
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Логирование
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Загрузка .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_IDS = [446393818]  # Твой Telegram ID

# Клавиатура
MAIN_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("🆓 Бесплатный разбор", callback_data="free")],
    [InlineKeyboardButton("🐝 Платный разбор от 17$", callback_data="paid")],
    [InlineKeyboardButton("👑 Пакет VIP от 60$", callback_data="vip")],
    [InlineKeyboardButton("📜 Обо мне / Отзывы", callback_data="about")]
])

UPDATE_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")]
])

# Очистка чата
async def clear_chat_history(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in ALLOWED_IDS:
        try:
            await context.bot.send_message(chat_id, "🧹 Автоочистка истории чата...")
        except:
            pass

# Обработка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    if chat_id not in ALLOWED_IDS:
        return

    logging.info(f"User {chat_id} вызвал /start")

    if os.path.exists("s1.webp"):
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)

    await context.bot.send_voice(chat_id, voice=open("intro-0.ogg", "rb"))
    await context.bot.send_message(chat_id, "👇 Ниже вы можете выбрать действие:", reply_markup=MAIN_KEYBOARD)

# Обработка нажатий
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id not in ALLOWED_IDS:
        return

    choice = query.data
    if choice == "free":
        await query.message.reply_audio(audio=open("primer_razbora.ogg", "rb"))
        await query.message.reply_text("✏️ ЖМИ СЮДА — заполни ФОРМУ", reply_markup=UPDATE_BUTTON)
    elif choice == "paid":
        await query.message.reply_document(document=open("primer_prognoz2.pdf", "rb"))
        await query.message.reply_text("🔄 Обновить страницу", reply_markup=UPDATE_BUTTON)
    elif choice == "vip":
        await query.message.reply_document(document=open("Prognoz_Love_god.pdf", "rb"))
        await query.message.reply_text("🔄 Обновить страницу", reply_markup=UPDATE_BUTTON)
    elif choice == "about":
        await query.message.reply_document(document=open("Razbor_na_God.pdf", "rb"))
        await query.message.reply_text("🔄 Обновить страницу", reply_markup=UPDATE_BUTTON)
    elif choice == "refresh":
        await start(update, context)

# Обработка сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    if chat_id not in ALLOWED_IDS:
        return

    if update.message.text.startswith("/"):
        return

    text = update.message.text.lower()
    if "speeeedvpnbot" in text or "http://" in text or "https://" in text:
        await context.bot.send_message(chat_id, "⚠️ Обнаружена подозрительная активность. Завершаю.")
        return

    await context.bot.send_message(chat_id, "🔁 Введите команду или нажмите кнопку.")

# Инициализация job_queue
async def post_init(app: Application):
    app.job_queue.run_repeating(clear_chat_history, interval=900, first=10)

# Основной запуск
def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
