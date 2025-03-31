from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatAction

TOKEN = "7697775190:AAGG5BfEhwNC6Pq0mBhROhvyY3xuyqJhMXo"

keyboard = [
    ["1️⃣ Ждать бесплатный РАЗБОР. заполнить анкету"],
    ["2️⃣ Ускорить⚡️в 4 раза⚡️.Заполнить форму, прислать мне схему-рисунок. (Тоже бесплатно)..🔣справится и школьник"],
    ["3️⃣ Обогнать всех. За 15 💟долларов - 20 мин./онлайн/ получить макс. глубокую онлайн сессию со мной лично. С точными ответами"],
    ["4️⃣ Стать 📱 VIP.клиентом, взять расширенный формат сессий. разборы глубокие"],
    ["5️⃣ Я выбрал УСКОРИТЬ РАЗБОР – готов выслать схему!"]
]

markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добрый день! Вы по консультации?\nВыберите один из вариантов ниже 👇",
        reply_markup=markup
    )

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "1️⃣" in text:
        await update.message.reply_text(
            "Вот Форма для Заявки на консультацию для ожидания.\n🇺🇦\nСсылка: https://forms.gle/9mEc5oEzdtpjLj1T6\n\n"
            "По ссылке нажмите и заполните анкету.\n\n"
            "❗️Ждать придётся долго — подумайте про 2-й вариант.\n\nС уважением, Викрам 🏆"
        )

    elif "2️⃣" in text:
        await update.message.reply_text(
            "🔣🔣Ускорить консультацию.🔣\n\n(Самому рассчитать карту и прислать МНЕ рисунок (бодиграф)).\n"
            "Если не нашли свой ГОРОД: если вы родились в Украине, просто пишите 'Kiev, Ukraine'.\n"
            "Пишите просто столицу страны на английском.\n\n🌐 Сайт где сделать: https://www.jovianarchive.com/get_your_chart"
        )
        await update.message.chat.send_action(action=ChatAction.UPLOAD_VIDEO)
        with open("HDtest.mp4", "rb") as video:
            await update.message.reply_video(video)

    elif "3️⃣" in text or "4️⃣" in text:
        await update.message.reply_text(
            "Отлично, вы выбрали платный вариант.\nНапишите лично Викраму 👉 https://t.me/Vikram_2027"
        )

    elif "5️⃣" in text:
        await update.message.reply_text(
            "Отлично, вы выбрали УСКОРИТЬ РАЗБОР — готов выслать схему.\n"
            "Пришлите мне ваш бодиграф, написав лично Викраму 👉 https://t.me/Vikram_2027"
        )

    else:
        await update.message.reply_text("Пожалуйста, выберите один из предложенных вариантов.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    print("🤖 Бот запущен и ждёт сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()

