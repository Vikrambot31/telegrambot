from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import telegram.error

# Токен напрямую в коде
TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

# Главное меню
keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📌 Обо мне / Отзывы"],
    ["📞 Связаться со мной"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Кнопка перехода в Telegram
def get_inline_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("написать Викраму лично", url="https://t.me/Vikram_2027")]]
    )

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)
    except Exception as e:
        print(f"[Ошибка стикера]: {e}")

    await update.message.reply_text("Приветствую вас, с вами Викрам!", reply_markup=markup)

    try:
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)
    except Exception as e:
        print(f"[Ошибка intro-0.ogg]: {e}")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.lower()

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор. Ожидайте инструкций.")
        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка изображения {fname}]: {e}")
        try:
            with open("intro-1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка intro-1]: {e}")

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка изображения {fname}]: {e}")
        try:
            with open("intro-2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка intro-2]: {e}")

    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")
        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка изображения {fname}]: {e}")
        try:
            with open("intro-3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка intro-3]: {e}")

    elif "отзывы" in text or "обо мне" in text:
        await update.message.reply_text("📌 Отзывы и информация:")
        try:
            with open("o1.png", "rb") as img:
                await context.bot.send_photo(chat_id, img)
            with open("primer_razbora.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка отзывов]: {e}")
        await update.message.reply_text("🔗 Instagram (скопируйте): https://www.instagram.com/vikram_hd_2027")

    elif "связаться" in text:
        await update.message.reply_text("Перейдите по ссылке, чтобы написать Викраму:")
        await update.message.reply_text("https://t.me/Vikram_2027")

    else:
        await update.message.reply_text("Выберите один из вариантов в меню ниже ⬇️")

# Запуск приложения
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        print("✅ Бот запущен. Ожидаем команды...")
        app.run_polling()
    except telegram.error.Conflict:
        print("⚠️ Конфликт: бот уже запущен где-то ещё.")
