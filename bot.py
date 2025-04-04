import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен Telegram-бота
TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔗 Написать Викраму лично", url="https://t.me/Vikram_2027")]
    ]
    await update.message.reply_text(
        "Добро пожаловать!\nНажмите кнопку ниже, чтобы связаться со мной:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Команда /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔗 Написать Викраму лично", url="https://t.me/Vikram_2027")]
    ]
    await update.message.reply_text(
        "Меню сброшено. Нажмите кнопку ниже для связи:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Основная функция запуска
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.run_polling(close_loop=True)

if __name__ == "__main__":
    main()
