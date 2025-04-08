from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters
from gen_keys import get_gate_description
import asyncio

TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

used_ids = set()

# Главное меню
keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📜 Обо мне / Отзывы"]
]

menu_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_form_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 ЖМИ СЮДА — заполни ФОРМУ", url="https://freehumandesignchart.com/")],
        [InlineKeyboardButton("🧠 Расшифровать самому", callback_data="decode_self")]
    ])

def get_contact_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📲 Написать в Telegram", url="https://t.me/Vikram_2027")]
    ])

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отправка стикера
    try:
        with open("sticker.webp", "rb") as sticker:
            await context.bot.send_sticker(update.effective_chat.id, sticker)
    except:
        pass

    # Отправка первого аудиофайла
    try:
        with open("p1.ogg", "rb") as audio:
            await context.bot.send_audio(update.effective_chat.id, audio)
    except:
        pass

    await update.message.reply_text("Выберите интересующий вас пункт меню:", reply_markup=menu_markup)

# Обработка кнопки
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "decode_self":
        context.user_data["awaiting_gates"] = True
        await query.message.reply_text("(Функция в разработке)")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Обработка ввода ворот
    if context.user_data.get("awaiting_gates"):
        try:
            gates = [int(x.strip()) for x in text.split(",")][:5]
            result = get_gate_description(gates)
            used_ids.add(user_id)
            context.user_data["awaiting_gates"] = False
            await update.message.reply_text(result)
            return
        except:
            context.user_data["awaiting_gates"] = False

    # Если выбран "бесплатный разбор"
    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор.")

        # Отправляем картинки с паузами
        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)  # Пауза между картинками
            except:
                pass

        # Отправляем pic7.png
        try:
            with open("pic7.png", "rb") as img:
                await context.bot.send_photo(chat_id, img)
                await asyncio.sleep(0.5)  # Пауза после pic7.png
        except:
            pass

        # Пауза перед аудио
        await asyncio.sleep(1)  # Пауза перед аудиофайлом

        # Отправляем аудиофайл
        try:
            with open("x1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass

        # Пауза перед кнопками
        await asyncio.sleep(1)

        # Отправляем кнопки
        await update.message.reply_text(
            "👇 Ниже вы можете выбрать действие:",
            reply_markup=get_form_buttons()
        )

    # Если выбран "платный разбор"
    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)  # Пауза между картинками
            except:
                pass
        try:
            with open("x2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    # Если выбран "VIP"
    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")
        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)  # Пауза между картинками
            except:
                pass
        try:
            with open("x3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    # Если "Обо мне" или "Отзывы"
    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text(
            "Здесь вы можете прочитать про отзывы и систему — мой Instagram:\n"
            "https://www.instagram.com/vikram_hd_2027\n"
            "Ниже — примеры реальных сессий:"
        )

        # Пауза перед отправкой документа
        await asyncio.sleep(1)

        # Отправка PDF файла "Razbor_na_God.pdf"
        try:
            with open("Razbor_na_God.pdf", "rb") as pdf:
                await context.bot.send_document(chat_id, pdf)
        except:
            pass

        await update.message.reply_text("👇", reply_markup=get_contact_button())

# Обработка ошибок
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Произошла ошибка: {context.error}")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
