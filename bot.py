import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 8443))


# Главное меню
main_menu = [
    ["* Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📍 Обо Мне / Система / Отзывы"]
]

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Отправка стикера
    try:
        with open("sticker1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)
    except Exception as e:
        print(f"Ошибка при отправке стикера: {e}")

    # Отправка голосового
    try:
        with open("intro-0.mp3", "rb") as voice:
            await context.bot.send_audio(chat_id=chat_id, audio=voice)
    except Exception as e:
        print(f"Ошибка при отправке аудио: {e}")

    # Отправка приветствия и меню
    await context.bot.send_message(
        chat_id=chat_id,
        text="Добрый день! нажмите слово 'разбор' для старта.",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Обработка сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "разбор" in text:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы выбрали 'разбор'. Ожидайте инструкций.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, используйте кнопки меню.")

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://vikrambot.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()
