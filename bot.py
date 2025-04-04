import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Вставляем токен напрямую
TOKEN = "7419809164:AAHofDyitmblhjCszawIJpzdHTmwgANIHrw"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔗 Написать Викраму лично", url="https://t.me/Vikram_2027")]
    ]
    await update.message.reply_text(
        "Добро пожаловать!
Нажмите кнопку ниже, чтобы связаться со мной:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Команда /reset для сброса старого интерфейса
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔗 Написать Викраму лично", url="https://t.me/Vikram_2027")]
    ]
    await update.message.reply_text("Меню сброшено:", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset))
    application.run_polling(close_loop=True)

if __name__ == "__main__":
    main()