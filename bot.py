import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler, filters
from gen_keys import get_gate_description
import asyncio

# Загружаем токен
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Твой Telegram ID
OWNER_ID = 446393818

# Проверка на владельца
def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

# Кнопки меню
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

def get_refresh_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_owner(user_id):
        await update.message.reply_text("⛔ У вас нет доступа к этой функции.")
        return

    chat_id = update.effective_chat.id

    try:
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)
    except:
        pass

    try:
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)
    except:
        pass

    await update.message.reply_text("Выберите интересующий вас пункт меню:", reply_markup=menu_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "decode_self":
        user_id = update.effective_user.id
        if not is_owner(user_id):
            await query.message.reply_text("⛔ Доступ только для администратора.")
            return
        await query.message.reply_text("Пока что функция в разработке")

    elif query.data == "refresh":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🔁 Перезапускаем..."
        )
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор.")

        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)
            except:
                pass

        try:
            with open("x1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass

        await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=get_form_buttons())

        await asyncio.sleep(1)
        await update.message.reply_text("🔄 Обновить страницу:", reply_markup=get_refresh_button())

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")

        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)
            except:
                pass

        try:
            with open("x2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass

        await update.message.reply_text("👇", reply_markup=get_contact_button())

        await asyncio.sleep(1)
        await update.message.reply_text("🔄 Обновить страницу:", reply_markup=get_refresh_button())

    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")

        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            try:
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)
            except:
                pass

        try:
            with open("x3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)
        except:
            pass

        await update.message.reply_text("👇", reply_markup=get_contact_button())

        await asyncio.sleep(1)
        await update.message.reply_text("🔄 Обновить страницу:", reply_markup=get_refresh_button())

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text(
            "Здесь вы можете прочитать про отзывы и систему — мой Instagram:\n"
            "https://www.instagram.com/vikram_hd_2027\n"
            "Ниже — примеры реальных сессий:"
        )

        try:
            with open("Razbor_na_God.pdf", "rb") as pdf:
                await context.bot.send_document(chat_id, pdf)
        except:
            pass

        try:
            with open("primer_prognoz2.pdf", "rb") as pdf:
                await context.bot.send_document(chat_id, pdf)
        except:
            pass

        await update.message.reply_text("👇", reply_markup=get_contact_button())

        await asyncio.sleep(1)
        await update.message.reply_text("🔄 Обновить страницу:", reply_markup=get_refresh_button())

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Произошла ошибка: {context.error}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
