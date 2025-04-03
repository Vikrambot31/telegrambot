from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction
import os

TOKEN = os.getenv("TOKEN")

main_menu = [
    ["⭐️ Бесплатный разбор"],
    ["💸 Платный разбор от 15$"] ,
    ["👑 Пакет VIP от 60$"],
    ["ℹ️ Обо Мне / Система / Отзывы"]
]

markup_main = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

free_text = (
    "📌 2 ПРОСТЫХ ШАГА:\n"
    "1. Заполнить форму: https://forms.gle/9mEc5oEzdtpjLj1T6\n"
    "2. Прислать мне рисунок:\n"
    "📌 pic1.png\n📌 pic2.png\n📌 pic3.png\n🎧 Intro-1.mp3\n\n"
    "✉️ Написать мне – https://t.me/Vikram_2027"
)

paid_text = (
    "💰 Платные услуги для Вас:\n"
    "— 15 долларов (650 грн)\n"
    "📌 pic4.png\n📌 pic4-1.png\n📌 pic5.png\n🎧 Intro-2.mp3\n\n"
    "Реквизиты: PayPal / VISA / Mono / Крипто: USDC\n"
    "✉️ Написать мне – https://t.me/Vikram_2027\n\n"
    "📜 Вопросы до встречи: 📌 Voprosi.png"
)

vip_text = (
    "👑 VIP Услуги от 60$:\n"
    "📌 pic6.png\n📌 pic5.png\n🎧 Intro-3.mp3\n\n"
    "Реквизиты: PayPal / VISA / Mono / Крипто: USDC\n"
    "✉️ Написать мне – https://t.me/Vikram_2027\n\n"
    "📜 Вопросы до встречи: 📌 Voprosi.png"
)

info_text = (
    "ℹ️ Информация:\n"
    "— Как проходит встреча (online)\n"
    "— Не знаете время рождения?\n"
    "— Отзывы: 📌 otziv.png\n"
    "— Instagram: https://www.instagram.com/vikram_hd_2027\n"
    "— О системе: https://surl.gd/jlbtay"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker(sticker=open("Sticker1.webp", "rb"))
    await update.message.reply_audio(audio=open("Intro-0.mp3", "rb"))
    await update.message.reply_text(
        "👋 Добро пожаловать! Выберите нужный пункт:",
        reply_markup=markup_main
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "Бесплатный разбор" in text:
        await update.message.reply_text(free_text, disable_web_page_preview=True)
    elif "Платный разбор от 15$" in text:
        await update.message.reply_text(paid_text, disable_web_page_preview=True)
    elif "VIP" in text:
        await update.message.reply_text(vip_text, disable_web_page_preview=True)
    elif "Обо Мне" in text:
        await update.message.reply_text(info_text, disable_web_page_preview=True)
    else:
        await update.message.reply_text("❗️Пожалуйста, выберите вариант из меню.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущен. Ожидаю сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
