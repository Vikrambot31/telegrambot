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

    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)
    except Exception as e:
        print(f"Ошибка при отправке стикера: {e}")

    try:
        with open("intro-0.ogg", "rb") as voice:
            await context.bot.send_voice(chat_id=chat_id, voice=voice)
    except Exception as e:
        print(f"Ошибка при отправке голосового: {e}")

    await context.bot.send_message(
        chat_id=chat_id,
        text="Добрый день! нажмите слово 'разбор' для старта.",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Обработка всех сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "* Бесплатный разбор":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы выбрали 'бесплатный разбор'. Ожидайте инструкций.")
        # При необходимости добавь: await context.bot.send_voice(...) или другое действие

    elif text == "💸 Платный разбор от 15$":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Платный разбор стоит от 15$. Напишите, что хотите разобрать.")

    elif text == "👑 Пакет VIP от 60$":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пакет VIP от 60$ включает личную сессию и подробный анализ.")

    elif "отзывы" in text.lower():
        await update.message.reply_text("Вот отзывы обо мне:")
        try:
            with open("o1.png", "rb") as photo:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
        except Exception as e:
            print(f"Ошибка при отправке фото отзыва: {e}")

    elif "обо мне" in text.lower() or "система" in text.lower():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Я Викрам, гештальт-психолог. Использую Human Design. Подробнее — см. профиль.")

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, используйте кнопки меню.")

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Бот запущен через polling.")
    app.run_polling()

if __name__ == "__main__":
    main()
