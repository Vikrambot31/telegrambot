import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
from dotenv import load_dotenv
from gen_keys import get_gate_description

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 446393818  # Только ты управляешь

used_ids = set()

# --- Хелпер для отправки медиа ---
def media_path(filename):
    return os.path.join(os.getcwd(), filename)

# --- Обработка команды /start ---
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in used_ids:
        used_ids.add(user_id)

    keyboard = [['📋 Бесплатный разбор'],
                ['💸 Платный разбор от 15$'],
                ['👑 Пакет VIP от 60$'],
                ['📜 Обо мне / Отзывы']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=reply_markup)

# --- Кнопка «Обновить страницу» ---
async def refresh(update: Update, context: CallbackContext.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    async for msg in context.bot.get_chat_history(chat_id):
        try:
            await context.bot.delete_message(chat_id, msg.message_id)
        except:
            continue
    await start(update, context)

# --- Главная логика ответов ---
async def handle_message(update: Update, context: CallbackContext.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("⛔️ Извините, бот доступен только автору.")
        return

    text = update.message.text

    if text == '📋 Бесплатный разбор':
        await context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(media_path("intro-0.ogg"), "rb"))
        await update.message.reply_text("🧠 Расшифровать самому", reply_markup=ReplyKeyboardMarkup(
            [['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '💸 Платный разбор от 15$':
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path("pic2.png"), "rb"))
        await update.message.reply_text("🔄 Обновить страницу", reply_markup=ReplyKeyboardMarkup(
            [['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '👑 Пакет VIP от 60$':
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path("pic3.png"), "rb"))
        await update.message.reply_text("🔄 Обновить страницу", reply_markup=ReplyKeyboardMarkup(
            [['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '📜 Обо мне / Отзывы':
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path("Voprosi.png"), "rb"))
        await update.message.reply_text("🔄 Обновить страницу", reply_markup=ReplyKeyboardMarkup(
            [['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '🧠 Расшифровать самому':
        await update.message.reply_text("✍️ ЖМИ СЮДА — заполни ФОРМУ")

    elif text == '🔄 Обновить страницу':
        await refresh(update, context)

    else:
        await update.message.reply_text("Не понял... Выберите действие из меню.")

# --- MAIN ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
