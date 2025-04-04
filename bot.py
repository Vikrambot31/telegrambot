import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")

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
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)
    except Exception as e:
        print(f"Ошибка при отправке стикера: {e}")

    # Отправка голосового (intro-0.ogg)
    try:
        with open("intro-0.ogg", "rb") as voice:
            await context.bot.send_voice(chat_id=chat_id, voice=voice)
    except Exception as e:
        print(f"Ошибка при отправке голосового: {e}")

    # Приветственное сообщение и кнопки
    await context.bot.send_message(
        chat_id=chat_id,
        text="Добрый день! нажмите слово 'разбор' для старта.",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Обработка всех сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "разбор" in text:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы выбрали 'разбор'. Ожидайте инструкций.")
    elif "отзывы" in text:
        await update.message.reply_text("Вот отзывы обо мне:")
        try:
            with open("o1.png", "rb") as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
        except Exception as e:
            print(f"Ошибка при отправке фото отзыва: {e}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, используйте кнопки меню.")

# Запуск через polling
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Бот запущен через polling.")
    app.run_polling()

if __name__ == "__main__":
    main()
