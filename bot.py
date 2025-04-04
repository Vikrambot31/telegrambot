import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")  # Убедитесь, что .env содержит строку: TOKEN=ваш_новый_токен

# Меню кнопок
keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📌 Обо мне / Отзывы"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)
    except Exception as e:
        print(f"[Ошибка] Стикер: {e}")

    await update.message.reply_text("Приветствую вас, с вами Викрам!", reply_markup=markup)

    try:
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)
    except Exception as e:
        print(f"[Ошибка] Аудио приветствия: {e}")

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.lower()

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали 'бесплатный разбор'. Ожидайте инструкций.")
        try:
            with open("pic1.png", "rb") as img:
                await context.bot.send_photo(chat_id, img)
            with open("intro-1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка] Бесплатный разбор: {e}")

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор: Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка] {fname}: {e}")
        try:
            with open("intro-2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка] Аудио платного разбора: {e}")

    elif "vip" in text:
        await update.message.reply_text("👑 VIP пакет: смотрите материалы.")
        for fname in ["pic6.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка] {fname}: {e}")
        try:
            with open("intro-3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка] Аудио VIP: {e}")

    elif "отзывы" in text or "обо мне" in text:
        await update.message.reply_text("📌 Отзывы и информация:")
        try:
            with open("o1.png", "rb") as img:
                await context.bot.send_photo(chat_id, img)
        except Exception as e:
            print(f"[Ошибка] Картинка отзывов: {e}")
        await update.message.reply_text("🔗 Instagram: https://www.instagram.com/vikram_hd_2027")

    else:
        await update.message.reply_text("Выберите вариант из меню 👇")

# Основная функция запуска
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен. Ожидаем пользователей...")
    app.run_polling()

if __name__ == "__main__":
    main()
