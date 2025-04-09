import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv
import logging

# ✅ Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

print(f"✅ Загружен токен: {TOKEN}")

# ✅ ID разрешённых пользователей
ALLOWED_IDS = [446393818]
BLACKLIST = set()

# ✅ Логирование
logging.basicConfig(filename='bot.log', level=logging.INFO)

# 🔍 Проверка на вредоносные фразы
def is_suspicious(text: str) -> bool:
    return any(word in text.lower() for word in ["http://", "https://", "vpn", "bot", "admin", "SpeeeedVPNbot"])

# ▶ Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            ["🆓 Бесплатный разбор"],
            ["💸 Платный разбор от 17$"],
            ["👑 Пакет VIP от 60$"],
            ["📜 Обо мне / Отзывы"]
        ],
        resize_keyboard=True
    )

    await context.bot.send_message(
        chat_id=user.id,
        text="👇 Ниже выбери нужное действие:",
        reply_markup=keyboard
    )

# 💬 Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if text.startswith("/"):
        return

    if is_suspicious(text):
        await context.bot.send_message(chat_id=user.id, text="⚠️ Подозрительная активность. Вы занесены в чёрный список.")
        BLACKLIST.add(user.id)
        logging.warning(f"User {user.id} добавлен в BLACKLIST: {text}")
        return

    # Реакции на каждую кнопку
    if text == "🆓 Бесплатный разбор":
        for file in ["pic1.png", "pic2.png", "pic3.png"]:
            await context.bot.send_photo(chat_id=user.id, photo=open(file, "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("x1.ogg", "rb"))
        await context.bot.send_message(chat_id=user.id, text="📥 Заполнить форму: https://freehumandesignchart.com/")
        await context.bot.send_message(chat_id=user.id, text="👉 Написать мне: https://t.me/Vikram_2027")

    elif text == "💸 Платный разбор от 17$":
        for file in ["pic4.png", "pic5.png"]:
            await context.bot.send_photo(chat_id=user.id, photo=open(file, "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("x2.ogg", "rb"))
        await context.bot.send_message(chat_id=user.id, text="👉 Написать мне: https://t.me/Vikram_2027")

    elif text == "👑 Пакет VIP от 60$":
        for file in ["pic6.png", "pic5.png", "Voprosi.png"]:
            await context.bot.send_photo(chat_id=user.id, photo=open(file, "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("x3.ogg", "rb"))
        await context.bot.send_message(chat_id=user.id, text="👉 Написать мне: https://t.me/Vikram_2027")

    elif text == "📜 Обо мне / Отзывы":
        await context.bot.send_message(chat_id=user.id, text="📄 Здесь вы можете прочитать про отзывы и систему — мой Instagram:\nhttps://www.instagram.com/vikram_hd_2027\n\nНиже — примеры:")
        for file in ["Prognoz_Love_god.pdf", "primer_prognoz2.pdf"]:
            await context.bot.send_document(chat_id=user.id, document=open(file, "rb"))
        await context.bot.send_voice(chat_id=user.id, voice=open("primer_razbora.ogg", "rb"))
        await context.bot.send_message(chat_id=user.id, text="👉 Написать мне: https://t.me/Vikram_2027")

    else:
        await context.bot.send_message(chat_id=user.id, text="✅ Я вас понял.")

# 🚀 Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
