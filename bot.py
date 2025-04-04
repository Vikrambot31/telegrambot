import os
from telegram import Update, ReplyKeyboardMarkup, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging

# Включаем логирование (чтобы видеть ошибки в Railway)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ Используем переменную окружения (установи BOT_TOKEN в Railway)
TOKEN = os.getenv("BOT_TOKEN") or "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"  # временно вшит

# Главное меню
main_menu = [["Бесплатный разбор"], ["Платный разбор от 15 $"], ["Пакет ВИП от 60 $"], ["Обо мне и отзывы"], ["Связаться со мной"]]

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        await context.bot.send_sticker(chat_id=chat_id, sticker=InputFile("s1.webp"))
        await context.bot.send_audio(chat_id=chat_id, audio=InputFile("intro-0.ogg"))
    except Exception as e:
        logging.error(f"Ошибка при отправке приветствия: {e}")
    await update.message.reply_text(
        "Приветствую вас! С вами Викрам!",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

# Ответы на кнопки
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    chat_id = update.effective_chat.id

    if "бесплатный" in text:
        await update.message.reply_text("Ожидайте инструкцию 👇")
        await send_files(context, chat_id, ["pic2.png", "pic3.png"], "intro-1.ogg")

    elif "платный" in text:
        await update.message.reply_text("Детали платного разбора 👇")
        await send_files(context, chat_id, ["pic4.png", "pic4.1.png", "pic5.png"], "intro-2.ogg")

    elif "вип" in text:
        await update.message.reply_text("Пакет ВИП включает всё 👇")
        await send_files(context, chat_id, ["pic6.png", "Voprosi.png"], "intro-3.ogg")

    elif "обо мне" in text or "отзывы" in text:
        await update.message.reply_text("Отзывы обо мне и пример консультации 👇")
        try:
            await context.bot.send_photo(chat_id=chat_id, photo=InputFile("o1.png"))
            await context.bot.send_audio(chat_id=chat_id, audio=InputFile("primer_razbora.ogg"))
        except Exception as e:
            logging.error(f"Ошибка при отправке отзывов: {e}")

    elif "связаться" in text:
        # ⛔️ Ссылка без автоформатирования
        await update.message.reply_text(
            "t.me/Vikram_2027",
            disable_web_page_preview=True
        )

# Вспомогательная функция
async def send_files(context, chat_id, images, audio_file):
    for img in images:
        try:
            await context.bot.send_photo(chat_id=chat_id, photo=InputFile(img))
        except Exception as e:
            logging.warning(f"Ошибка при отправке изображения {img}: {e}")
    try:
        await context.bot.send_audio(chat_id=chat_id, audio=InputFile(audio_file))
    except Exception as e:
        logging.warning(f"Ошибка при отправке аудио {audio_file}: {e}")
    await context.bot.send_message(chat_id=chat_id, text="написать Викраму лично", reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("написать Викраму лично", url="https://t.me/Vikram_2027")]]
    ))

# Запуск
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ✅ Только polling — без webhook, чтобы исключить конфликты
    print("✅ Бот запущен. Ожидаем команды...")
    app.run_polling()

if __name__ == "__main__":
    main()
