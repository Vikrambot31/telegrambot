import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Получаем токен и порт из переменных окружения
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 8443))

# Главное меню
main_menu = [
    ["✴* Бесплатный разбор"],
    ["💎 Платный разбор от 15$"],
    ["🧠 Пакет VIP от 60$"],
    ["🔍 Обо Мне / Система / Отзывы"]
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Отправляем стикер
    with open("sticker1.webp", "rb") as sticker:
        await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)

    # Отправляем аудио (mp3 как аудио-файл)
    with open("intro-0.mp3", "rb") as voice:
        await context.bot.send_audio(chat_id=chat_id, audio=voice)

    # Отправляем текстовое приветствие
    await update.message.reply_text(
        "Приветствую вас! С вами Викрам!\n\nВыберите пункт меню:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    if "разбор" in user_text:
        await update.message.reply_text("Вы выбрали 'Разбор'. Введите ваши данные для начала.")
    else:
        await update.message.reply_text("Пожалуйста, выберите один из пунктов меню.")

# Основная точка входа
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота через Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://vikrambot.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()
