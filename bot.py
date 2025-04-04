import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import telegram.error

# Прямо вписываем токен
TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

# Клавиатура меню
keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📌 Обо мне / Отзывы"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Универсальная кнопка "написать Викраму лично"
def get_inline_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("написать Викраму лично", url="https://t.me/Vikram_2027")]])

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Стикер
    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)
    except Exception as e:
        print(f"[Стикер ошибка]: {e}")

    # Приветствие
    await update.message.reply_text("Приветствую вас, с вами Викрам!", reply_markup=markup)

    # Аудио
    try:
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)
    except Exception as e:
        print(f"[Аудио приветствия ошибка]: {e}")

# Обработка всех кнопок
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
        await update.message.reply_text(" ", reply_markup=get_inline_button())

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
        await update.message.reply_text(" ", reply_markup=get_inline_button())

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
        await update.message.reply_text(" ", reply_markup=get_inline_button())

    elif "отзывы" in text or "обо мне" in text:
        await update.message.reply_text("📌 Отзывы и информация:")
        try:
            with open("o1.png", "rb") as img:
                await context.bot.send_photo(chat_id, img)
            with open("primer_razbora.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка отзывов]: {e}")
        await update.message.reply_text("🔗 Instagram: https://www.instagram.com/vikram_hd_2027")
        await update.message.reply_text(" ", reply_markup=get_inline_button())

    else:
        await update.message.reply_text("Выберите вариант из меню ниже 👇")

# Запуск
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        print("Бот запущен.")
        app.run_polling()
    except telegram.error.Conflict:
        print("⚠️ Бот уже работает где-то ещё. Остановите второй экземпляр.")
