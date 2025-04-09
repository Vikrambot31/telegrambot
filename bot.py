import os
from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    MessageHandler, filters
)
import logging

# --- Настройки и защита ---
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_IDS = [446393818]
BLACKLIST = set()

logging.basicConfig(filename='bot.log', level=logging.INFO)

def is_suspicious(text: str) -> bool:
    return any(w in text.lower() for w in ["http://", "https://", "vpn", "bot", "admin", "SpeeeedVPNbot"])

# --- Главное меню ---
main_menu = ReplyKeyboardMarkup([
    ["🆓 Бесплатный разбор"],
    ["🐝 Быстрый Разбор от 17 $"],
    ["👑 Разбор VIP от 60 $"],
    ["📜 Обо мне / Отзывы"]
], resize_keyboard=True)

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return
    await update.message.reply_text("👋 Добро пожаловать! Выберите вариант ниже:", reply_markup=main_menu)

# --- Обработка сообщений ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if not user or user.id not in ALLOWED_IDS or user.id in BLACKLIST:
        return

    if is_suspicious(text):
        await update.message.reply_text("⚠️ Подозрительная активность. Вы заблокированы.")
        BLACKLIST.add(user.id)
        logging.warning(f"BLACKLIST: {user.id} | {text}")
        return

    if text == "🆓 Бесплатный разбор":
        await send_files(update, ["s1.webp", "intro-0.ogg"])
        await update.message.reply_text("📝 Форма: https://freehumandesignchart.com/")
        await update.message.reply_text("📩 Написать мне: https://t.me/Vikram_2027")

    elif text == "🐝 Быстрый Разбор от 17 $":
        await send_files(update, ["pic4.png", "pic5.png", "x2.ogg"])
        await update.message.reply_text("📩 Написать мне: https://t.me/Vikram_2027")

    elif text == "👑 Разбор VIP от 60 $":
        await send_files(update, ["pic6.png", "pic5.png", "Voprosi.png", "x3.ogg"])
        await update.message.reply_text("📩 Написать мне: https://t.me/Vikram_2027")

    elif text == "📜 Обо мне / Отзывы":
        await update.message.reply_text(
            "📜 Здесь вы можете прочитать про отзывы и систему:\n"
            "Instagram: https://www.instagram.com/vikram_hd_2027\n\n"
            "📎 Примеры:"
        )
        await send_files(update, ["Prognoz_Love_god.pdf", "primer_prognoz2.pdf", "primer_razbora.ogg"])
        await update.message.reply_text("📩 Написать мне: https://t.me/Vikram_2027")

    else:
        await update.message.reply_text("Пожалуйста, выбери один из пунктов меню.")

# --- Вспомогательная функция отправки медиа ---
async def send_files(update, filenames):
    for name in filenames:
        try:
            if name.endswith(".ogg"):
                await update.message.reply_voice(voice=open(name, "rb"))
            elif name.endswith(".webp"):
                await update.message.reply_sticker(sticker=open(name, "rb"))
            elif name.endswith(".png") or name.endswith(".jpg"):
                await update.message.reply_photo(photo=open(name, "rb"))
            elif name.endswith(".pdf"):
                await update.message.reply_document(document=open(name, "rb"))
        except Exception as e:
            logging.warning(f"Ошибка при отправке {name}: {e}")

# --- Запуск бота ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == '__main__':
    main()
