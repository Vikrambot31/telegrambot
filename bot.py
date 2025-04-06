from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

# Главное меню
keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📌 Обо мне / Отзывы"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Кнопка формы
def get_form_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 ЖМИ СЮДА — заполни ФОРМУ", url="https://freehumandesignchart.com/")]
    ])

# Кнопка связи с Викрамом
def get_contact_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Написать Викраму лично", url="https://t.me/Vikram_2027")]
    ])

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Приветствую вас, с вами Викрам!", reply_markup=markup)
    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)
    except Exception as e:
        print(f"[Ошибка стикера]: {e}")
    try:
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)
    except Exception as e:
        print(f"[Ошибка intro-0.ogg]: {e}")

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.lower()

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор.")
        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка изображения {fname}]: {e}")
        try:
            with open("x1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка x1.ogg]: {e}")
        await update.message.reply_text("👇", reply_markup=get_form_button())

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка изображения {fname}]: {e}")
        try:
            with open("x2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка x2.ogg]: {e}")
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")
        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except Exception as e:
                print(f"[Ошибка изображения {fname}]: {e}")
        try:
            with open("x3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка x3.ogg]: {e}")
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text(
            "Здесь вы можете прочитать про отзывы и систему — мой Instagram:\n"
            "https://www.instagram.com/vikram_hd_2027\n"
            "Ниже — примеры реальных сессий:"
        )
        try:
            with open("primer_razbora0.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка primer_razbora0.ogg]: {e}")
        try:
            with open("primer_razbora.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except Exception as e:
            print(f"[Ошибка primer_razbora.ogg]: {e}")
        await update.message.reply_text("👇", reply_markup=get_contact_button())

# Обработка ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Произошла ошибка: {context.error}")

# Точка входа
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
