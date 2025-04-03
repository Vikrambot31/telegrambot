import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токен и порт из переменных окружения
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 5000))

# Главное меню
main_menu = [
    ["* Бесплатный разбор"],
    ["💎 Платный разбор от 15$"],
    ["🧠 Пакет VIP от 60$"],
    ["📝 Обо Мне / Система / Отзывы"]
]

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправляем стикер
    with open("sticker.webp", "rb") as sticker:
        await update.message.reply_sticker(sticker)

    # Отправляем аудио
    with open("voice.ogg", "rb") as voice:
        await update.message.reply_voice(voice)

    # Приветствие и главное меню
    await update.message.reply_text(
        "Приветствую вас! С вами Викрам!\n\nВыберите пункт меню:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Обработка ответов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "* Бесплатный разбор":
        await update.message.reply_text(
            "Ты выбрал бесплатный разбор.\n\n"
            "📝 Отправь дату и время рождения в формате: 01.01.2000, 15:45, Город.\n\n"
            "⚠️ Придётся немного подождать — если хочешь быстрее, подумай о пункте 2."
        )

    elif text == "💎 Платный разбор от 15$":
        await update.message.reply_text(
            "💎 Отлично! Чтобы оплатить — напишите Викраму лично:\n👉 https://t.me/Vikram_2027"
        )

    elif text == "🧠 Пакет VIP от 60$":
        await update.message.reply_text(
            "🔮 Пакет VIP включает:\n— Полный Zoom разбор\n— Индивидуальное сопровождение\n\n"
            "👉 Напишите Викраму: https://t.me/Vikram_2027"
        )

    elif text == "📝 Обо Мне / Система / Отзывы":
        with open("otziv.png", "rb") as photo:
            await update.message.reply_photo(photo)
        await update.message.reply_text(
            "Я Викрам. Работаю по системе Human Design, психогенетике и гештальт-подходу.\n"
            "🎓 12 лет практики, сотни клиентов.\n\n"
            "🔗 Подробнее — напишите: https://t.me/Vikram_2027"
        )

    else:
        await update.message.reply_text("Пожалуйста, выбери пункт из меню.")

# Основной запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен через Webhook.")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://vikrambot.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()
