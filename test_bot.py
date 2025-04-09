from telegram.ext import ApplicationBuilder, CommandHandler

import os
from dotenv import load_dotenv
load_dotenv()

async def start(update, context):
    await update.message.reply_text("Привет! Бот работает!")

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
