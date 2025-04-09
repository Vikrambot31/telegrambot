import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CallbackContext, CommandHandler,
    CallbackQueryHandler, MessageHandler, filters
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 446393818  # Ваш Telegram ID

# Главное меню
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🆓 Бесплатный разбор", callback_data="free_analysis")],
        [InlineKeyboardButton("💸 Платный разбор от 15$", callback_data="paid_analysis")],
        [InlineKeyboardButton("👑 Пакет VIP от 60$", callback_data="vip_package")],
        [InlineKeyboardButton("📜 Обо мне / Отзывы", callback_data="about_me")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Кнопка обновления
def refresh_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh_page")]])

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    if update.effective_user.id in blacklist:
        await update.message.reply_text("Доступ запрещён.")
        return
    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=open("s1.webp", "rb"))
    await asyncio.sleep(1)
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open("intro-0.ogg", "rb"))
    await asyncio.sleep(1)
    await update.message.reply_text("👇 Ниже вы можете выбрать действие:", reply_markup=main_menu())

# Обработчик кнопок
async def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "free_analysis":
        await query.message.reply_audio(audio=open("primer_razbora.ogg", "rb"))
        await asyncio.sleep(1)
        await query.message.reply_text("📝 ЖМИ СЮДА — заполни ФОРМУ", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🧠 Расшифровать самому", callback_data="manual_decode")],
             [InlineKeyboardButton("🔄 Обновить страницу", callback_data="refresh_page")]]
        ))

    elif query.data == "paid_analysis":
        await query.message.reply_text("Платный разбор от 15$", reply_markup=refresh_button())

    elif query.data == "vip_package":
        await query.message.reply_text("Пакет VIP от 60$", reply_markup=refresh_button())

    elif query.data == "about_me":
        await query.message.reply_audio(audio=open("about.ogg", "rb"))
        await asyncio.sleep(1)
        await context.bot.send_document(chat_id=query.message.chat_id, document=open("primer_prognoz2.pdf", "rb"))
        await query.message.reply_text("Отзывы и примеры разборов", reply_markup=refresh_button())

    elif query.data == "manual_decode":
        await query.message.reply_text("Пока что функция в разработке", reply_markup=refresh_button())

    elif query.data == "refresh_page":
        await clear_chat_history(context, query.message.chat_id)
        await context.bot.send_message(chat_id=query.message.chat_id, text="Бот перезапущен.")
        await start(update, context)

# Функция очистки переписки
async def clear_chat_history(context: CallbackContext, chat_id: int):
    try:
        messages = await context.bot.get_chat_history(chat_id, limit=100)
        for msg in messages:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
            except:
                continue
    except:
        pass

# Чёрный список ID
blacklist = set()

# Основной запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
