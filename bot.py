import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gen_keys import get_gate_description

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 446393818  # Только ты управляешь

used_ids = set()

def media_path(filename):
    return os.path.join(os.getcwd(), filename)

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in used_ids:
        used_ids.add(user_id)

    keyboard = [['📋 Бесплатный разбор'],
                ['💸 Платный разбор от 15$'],
                ['👑 Пакет VIP от 60$'],
                ['📜 Обо мне / Отзывы']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=reply_markup)

def refresh(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/start")

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id != OWNER_ID:
        update.message.reply_text("⛔️ Извините, бот доступен только автору.")
        return

    if text == '📋 Бесплатный разбор':
        context.bot.send_voice(chat_id=update.effective_chat.id, voice=open(media_path("intro-0.ogg"), "rb"))
        update.message.reply_text("🧠 Расшифровать самому", reply_markup=ReplyKeyboardMarkup([['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '💸 Платный разбор от 15$':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path("pic2.png"), "rb"))
        update.message.reply_text("🔄 Обновить страницу", reply_markup=ReplyKeyboardMarkup([['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '👑 Пакет VIP от 60$':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path("pic3.png"), "rb"))
        update.message.reply_text("🔄 Обновить страницу", reply_markup=ReplyKeyboardMarkup([['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '📜 Обо мне / Отзывы':
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path("Voprosi.png"), "rb"))
        update.message.reply_text("🔄 Обновить страницу", reply_markup=ReplyKeyboardMarkup([['🔄 Обновить страницу']], resize_keyboard=True))

    elif text == '🧠 Расшифровать самому':
        update.message.reply_text("✍️ ЖМИ СЮДА — заполни ФОРМУ")

    elif text == '🔄 Обновить страницу':
        refresh(update, context)

    else:
        update.message.reply_text("Не понял... Выберите действие из меню.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
