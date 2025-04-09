import os
import asyncio
import logging
from dotenv import load_dotenv

from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, JobQueue
)
from gen_keys import get_gate_description

# Загрузка токена
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(filename='bot.log', level=logging.INFO)

ALLOWED_IDS = [446393818]

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
    if update.effective_user.id not in ALLOWED_IDS:
        return
    logging.info(f"User {chat_id} вызвал /start")

    if os.path.exists("s1.webp"):
        with open("s1.webp", "rb") as sticker:
            await context.bot.send_sticker(chat_id, sticker)

    if os.path.exists("intro-0.ogg"):
        with open("intro-0.ogg", "rb") as audio:
            await context.bot.send_audio(chat_id, audio)

    await context.bot.send_message(chat_id, "👇 Ниже вы можете выбрать действие:", reply_markup=menu_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_IDS:
        return
    query = update.callback_query
    await query.answer()

    if query.data == "decode_self":
        await query.message.reply_text("Пока что функция в разработке.")
    elif query.data == "refresh":
        await context.bot.send_message(update.effective_chat.id, "🔄 Обновление...")
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if update.effective_user.id not in ALLOWED_IDS:
        return

    text = update.message.text.lower()
    if update.message.text.startswith("/"):
        return

    if "speeeedvpnbot" in text or "http://" in text:
        await context.bot.send_message(chat_id, "⚠️ Обнаружена подозрительная активность. Завершаю.")
        return

    if "бесплатный" in text:
        await update.message.reply_text("Вы выбрали бесплатный разбор.")
        for fname in ["pic1.png", "pic2.png", "pic3.png"]:
            if os.path.exists(fname):
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)
        if os.path.exists("x1.ogg"):
            with open("x1.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)

        await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=get_form_buttons())

    elif "платный" in text:
        await update.message.reply_text("💸 Платный разбор. Информация ниже.")
        for fname in ["pic4.png", "pic4-1.png", "pic5.png"]:
            if os.path.exists(fname):
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)
        if os.path.exists("x2.ogg"):
            with open("x2.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)

        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "vip" in text:
        await update.message.reply_text("👑 Пакет VIP: смотрите материалы ниже.")
        for fname in ["pic6.png", "pic5.png", "Voprosi.png"]:
            if os.path.exists(fname):
                with open(fname, "rb") as img:
                    await context.bot.send_photo(chat_id, img)
                    await asyncio.sleep(0.5)
        if os.path.exists("x3.ogg"):
            with open("x3.ogg", "rb") as audio:
                await context.bot.send_audio(chat_id, audio)

        await update.message.reply_text("👇", reply_markup=get_contact_button())

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text("Здесь вы можете прочитать про отзывы и систему — мой Instagram:\nhttps://www.instagram.com/vikram_hd_2027\nНиже — примеры реальных сессий:")
        for fname in ["Razbor_na_God.pdf", "primer_prognoz2.pdf"]:
            if os.path.exists(fname):
                with open(fname, "rb") as doc:
                    await context.bot.send_document(chat_id, doc)
        await update.message.reply_text("👇", reply_markup=get_contact_button())

async def clear_chat_history(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in ALLOWED_IDS:
        try:
            await context.bot.send_message(chat_id, "🧹 Автоочистка истории чата...")
        except Exception as e:
            logging.warning(f"Ошибка при автоочистке: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Произошла ошибка: {context.error}")

def main():
    app = Application.builder().token(TOKEN).post_init(lambda app: app.job_queue.run_repeating(clear_chat_history, interval=900, first=10)).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
