from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction

import os
TOKEN = os.getenv("TOKEN")


main_menu = [
    ["⭐️ Бесплатный разбор"],
    ["🌟 Платный разбор от 15$"],
    ["ℹ️ Обо Мне + Инфо!"]
]

markup_main = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# Дополнительные меню
free_menu_text = (
    "2 ПРОСТЫХ ШАГА.\n"
    "1. Заполнить форму.\n"
    "2. Прислать мне рисунок бодиграфа:\n"
    "+ картинка 1\n+ картинка 2\n+ голосовая запись (#1)\n\n"
    "Написать мне – https://t.me/Vikram_2027\n\n"
    "🔗 Форма: https://forms.gle/9mEc5oEzdtpjLj1T6"
)

paid_15_text = (
    "✨ Платные услуги для Вас ✨\n\n"
    "1. 15 долларов (650 грн)\n+ картинка 3\n+ картинка 4\n+ голосовая запись (#2)\n\n"
    "Реквизиты:\nPayPal / VISA / Mono / Крипто: USDC\n\n"
    "✉️ Написать: https://t.me/Vikram_2027"
)

paid_60_text = (
    "⭐️ Премиум услуга от 60$\n+ картинка 5\n+ картинка 6\n+ голосовая запись (#3)\n\n"
    "Формат: расширенный, индивидуальный подход.\n\n"
    "Реквизиты:\nPayPal / VISA / Mono / Крипто: USDC\n\n"
    "✉️ Написать: https://t.me/Vikram_2027"
)

info_text = (
    "ℹ️ Информация обо мне и системе:\n\n"
    "1. Как проходит встреча? (онлайн)\n"
    "2. Не знаете время рождения?\n"
    "3. Отзывы клиентов\n"
    "4. Как отправить перевод?\n"
    "5. Обо мне и системе ДЧ.\n\n"
    "🔗 https://t.me/Vikram_2027"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в бот Human Design от Викрама!\n\nВыберите один из пунктов меню:",
        reply_markup=markup_main
    )


async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "Бесплатный разбор" in text:
        await update.message.reply_text(free_menu_text)

    elif "Платный разбор от 15$" in text:
        await update.message.reply_text(paid_15_text)
        await update.message.reply_text(paid_60_text)

    elif "Обо Мне + Инфо" in text:
        await update.message.reply_text(info_text)

    else:
        await update.message.reply_text("Пожалуйста, выберите пункт из меню")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    print("🤖 Бот работает и ждёт сообщений...")
    app.run_polling()


if __name__ == "__main__":
    main()
