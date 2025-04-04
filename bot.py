import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Клавиатура с меню
keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📌 Обо мне / Отзывы"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Обработка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Стикер
    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id=chat_id, sticker=sticker)
    except Exception as e:
        print("Ошибка при отправке стикера:", e)

    # Приветствие и аудио
    await update.message.reply_text("Приветствую вас, с вами Викрам!", reply_markup=markup)

    try:
        with open("intro.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id=chat_id, audio=audio)
    except Exception as e:
        print("Ошибка при отправке приветственного аудио:", e)

# Обработка выбора кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    chat_id = update.effective_chat.id

    if "бесплатный" in text:
        await update.message.reply_text("⏳ Ожидайте инструкцию…")
        try:
            with open("free1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id=chat_id, audio=audio)
            with open("pic1.png", "rb") as photo:
                await context.bot.send_photo(chat_id=chat_id, photo=photo)
        except Exception as e:
            print("Ошибка при отправке материалов бесплатного разбора:", e)

    elif "платный" in text:
        await update.message.reply_text("💸 Вы выбрали платный разбор. Смотрите ниже:")
        for file_name in ["pic4.png", "pic4_1.png", "pic5.png"]:
            try:
                with open(file_name, "rb") as photo:
                    await context.bot.send_photo(chat_id=chat_id, photo=photo)
            except Exception as e:
                print(f"Ошибка при загрузке {file_name}:", e)
        try:
            with open("pay.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id=chat_id, audio=audio)
        except Exception as e:
            print("Ошибка при отправке аудио к платному разбору:", e)

    elif "vip" in text:
        await update.message.reply_text("👑 Добро пожаловать в VIP-пакет:")
        for file_name in ["pic6.png", "pic5.png"]:
            try:
                with open(file_name, "rb") as photo:
                    await context.bot.send_photo(chat_id=chat_id, photo=photo)
            except Exception as e:
                print(f"Ошибка при загрузке {file_name}:", e)
        try:
            with open("vip.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id=chat_id, audio=audio)
        except Exception as e:
            print("Ошибка при отправке VIP аудио:", e)

    elif "отзывы" in text or "обо мне" in text:
        await update.message.reply_text("📌 Отзывы обо мне и мой Instagram:")
        try:
            with open("o1.png", "rb") as photo:
                await context.bot.send_photo(chat_id=chat_id, photo=photo)
        except Exception as e:
            print("Ошибка при загрузке o1.png:", e)
        await update.message.reply_text("🔗 Мой Instagram: https://www.instagram.com/vikram_hd_2027")

    else:
        await update.message.reply_text("Пожалуйста, выберите один из пунктов меню 👇")

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запускается…")
    app.run_polling()

# Подстраховка от повторного запуска
if __name__ == "__main__":
    import sys
    print("📌 Этот файл запущен как основной:", sys.argv[0])
    main()
