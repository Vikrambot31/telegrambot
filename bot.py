from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from gen_keys import get_gate_description

TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

keyboard = [
    ["🆓 Бесплатный разбор"],
    ["💸 Платный разбор от 15$"],
    ["👑 Пакет VIP от 60$"],
    ["📌 Обо мне / Отзывы"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Храним ID, которые уже получали доступ
used_ids = set()

def get_form_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 ЖМИ СЮДА — заполни ФОРМУ", url="https://freehumandesignchart.com/")],
        [InlineKeyboardButton("🧠 Расшифровать самому", callback_data="decode_self")]
    ])

def get_contact_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 Написать Викраму лично", url="https://t.me/Vikram_2027")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("Приветствую вас, с вами Викрам!", reply_markup=markup)
    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)
    except: pass
    try:
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)
    except: pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text.lower()

    # Обработка ввода ворот
    if context.user_data.get("awaiting_gates"):
        context.user_data["awaiting_gates"] = False
        if user_id in used_ids:
            await update.message.reply_text("Вы уже использовали возможность бесплатной расшифровки.")
            return
        try:
            gates = [int(x.strip()) for x in text.split(",")][:5]
            result = get_gate_description(gates)
            used_ids.add(user_id)
            await update.message.reply_text(result)
        except:
            await update.message.reply_text("Ошибка. Введите до 5 чисел через запятую, например: 10, 34, 57, 20, 16")
        return

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор.")
        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except: pass
        try:
            with open("x1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except: pass
        await update.message.reply_text("👇", reply_markup=get_form_buttons())

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except: pass
        try:
            with open("x2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except: pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")
        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
            except: pass
        try:
            with open("x3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except: pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text(
            "Здесь вы можете прочитать про отзывы и систему — мой Instagram:\n"
            "https://www.instagram.com/vikram_hd_2027\n"
            "Ниже — примеры реальных сессий:"
        )
        for fname in ["p1.ogg", "primer_razbora.ogg"]:
            try:
                with open(fname, "rb") as audio:
                    await context.bot.send_audio(chat_id, audio)
            except: pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "decode_self":
        user_id = query.from_user.id
        if user_id in used_ids:
            await query.message.reply_text("Вы уже использовали возможность бесплатной расшифровки.")
        else:
            context.user_data["awaiting_gates"] = True
            await query.message.reply_text("Введите до 5 ворот через запятую, например: 10, 34, 57, 20, 16")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Произошла ошибка: {context.error}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработка команды /start
    app.add_handler(CommandHandler("start", start))

    # Обработка нажатия кнопки "Расшифровать самому"
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Обработка ввода ворот и любых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Обработка ошибок
    app.add_error_handler(error_handler)

    # Запуск бота
    app.run_polling()


if __name__ == "__main__":
    main()

