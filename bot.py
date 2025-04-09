import os
import asyncio
from dotenv import load_dotenv

from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)

from gen_keys import get_gate_description

# Загрузка токена
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

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
        [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")]
    ])

def get_contact_button():
    return InlineKeyboardMarkup([ 
        [InlineKeyboardButton("📲 Написать в Telegram", url="https://t.me/Vikram_2027")],
        [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=menu_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "decode_self":
        await query.message.reply_text("Пока что функция в разработке.")
    elif query.data == "refresh":
        chat_id = update.effective_chat.id
        await context.bot.send_message(chat_id, "🔄 Обновление...")
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
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

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text(
            "Здесь вы можете прочитать про отзывы и систему — мой Instagram:\n"
            "https://www.instagram.com/vikram_hd_2027\n"
            "Ниже — примеры реальных сессий:"
        )
        for fname in ["Razbor_na_God.pdf", "primer_prognoz2.pdf"]:
            try:
                with open(fname, "rb") as doc:
                    await context.bot.send_document(chat_id, doc)
            except:
                pass
        await update.message.reply_text("👇", reply_markup=get_contact_button())

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Произошла ошибка: {context.error}")

def main():
    app = Application.builder().token(TOKEN).build()  # Creating the bot with the token provided
    app.add_handler(CommandHandler("start", start))  # Add handler for the /start command
    app.add_handler(CallbackQueryHandler(handle_callback))  # Add handler for button click callbacks
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Add handler for text messages
    app.add_error_handler(error_handler)  # Add error handler
    app.run_polling()  # Start polling for updates

if __name__ == "__main__":
    main()  # Run the bot
