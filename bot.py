import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_ID = 446393818  # Только ваш Telegram ID

# Главное меню
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🆓 Бесплатный разбор", callback_data="free")],
        [InlineKeyboardButton("🐝 Платный разбор от 15$", callback_data="paid")],
        [InlineKeyboardButton("👑 Пакет VIP от 60$", callback_data="vip")],
        [InlineKeyboardButton("📜 Обо мне / Отзывы", callback_data="about")]
    ])

# Кнопка обновления
def get_refresh_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")]
    ])

# Проверка ID
def is_authorized(user_id: int) -> bool:
    return user_id == ALLOWED_USER_ID

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("⛔ Доступ запрещён.")
        return

    await update.message.reply_audio(audio=InputFile("intro-0.ogg"), caption="👇 Ниже вы можете выбрать действие:", reply_markup=get_main_keyboard())

# Обработка нажатий
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if not is_authorized(user_id):
        await query.message.reply_text("⛔ Доступ запрещён.")
        return

    # Удаление предыдущих сообщений
    try:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except Exception:
        pass

    # Переходы
    if query.data == "free":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic1.png"))
        await context.bot.send_message(chat_id=user_id, text="🧠 Расшифровать самому", reply_markup=get_refresh_keyboard())

    elif query.data == "paid":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic2.png"))
        await context.bot.send_message(chat_id=user_id, text="Платный разбор от 15$", reply_markup=get_refresh_keyboard())

    elif query.data == "vip":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic3.png"))
        await context.bot.send_message(chat_id=user_id, text="Пакет VIP от 60$", reply_markup=get_refresh_keyboard())

    elif query.data == "about":
        await context.bot.send_photo(chat_id=user_id, photo=InputFile("pic4.png"))
        await context.bot.send_message(chat_id=user_id, text="Отзывы и информация:", reply_markup=get_refresh_keyboard())

    elif query.data == "refresh":
        await context.bot.send_message(chat_id=user_id, text="🔄 Обновляем...", reply_markup=None)
        await start(update, context)

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
