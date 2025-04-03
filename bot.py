from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Получаем токен из переменной окружения
TOKEN = os.getenv("TOKEN")  # Убедись, что переменная окружения TOKEN задана правильно

# Главное меню
main_menu = [
    ["* Бесплатный разбор"],
    ["💎 Платный разбор от 15$"],
    ["🧠 Пакет VIP от 60$"],
    ["📝 Обо Мне / Система / Отзывы"]
]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Выбери пункт меню:",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Обработка всех текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "* Бесплатный разбор":
        await update.message.reply_text("Ты выбрал бесплатный разбор. Отправь дату и время рождения.")
    elif text == "💎 Платный разбор от 15$":
        await update.message.reply_text("Платный разбор стоит от 15$. Оплата и подробности — по ссылке.")
    elif text == "🧠 Пакет VIP от 60$":
        await update.message.reply_text("VIP-разбор включает Zoom и полное сопровождение.")
    elif text == "📝 Обо Мне / Система / Отзывы":
        with open("otziv.png", "rb") as photo:
            await update.message.reply_photo(photo)
        await update.message.reply_text("Я Викрам. Работаю с Human Design, психогенетикой, гештальт-подходом.")
    else:
        await update.message.reply_text("Пожалуйста, выбери пункт из меню.")

# Главная точка входа
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен через Webhook.")

    # Настройка Webhook для Render
    PORT = int(os.environ.get("PORT", 5000))
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://<ТВОЙ-ДОМЕН>.onrender.com/{TOKEN}"  # ЗАМЕНИ <ТВОЙ-ДОМЕН>
    )

if __name__ == "__main__":
    main()
