# This will be the entry point of your Telegram bot.
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from app.handlers.start_handler import start
from app.handlers.message_handler import message_handler
from app.handlers.contact_handler import contact_handler

from dotenv import load_dotenv
import os


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def run_bot():

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        MessageHandler(
            filters.CONTACT,
            contact_handler
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("🤖 Restaurant Bot Started...")

    application.run_polling()


if __name__ == "__main__":
    run_bot()
