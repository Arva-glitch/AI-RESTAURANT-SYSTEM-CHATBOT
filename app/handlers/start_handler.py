from telegram import Update
from telegram.ext import ContextTypes

# from app.chatbot.keyboards import main_menu_keyboard
# from app.chatbot.conversation_manager import ConversationManager

from app.handlers.common import send_intro
from app.database import SessionLocal
from app.services.customer_service import (
    get_customer_by_telegram_id,
)


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    db = SessionLocal()

    try:

        customer = get_customer_by_telegram_id(
            db,
            update.effective_user.id,
        )

        if customer is None:

            await send_intro(update)

        else:

            await update.message.reply_text(
                f"Welcome back, {customer.first_name}! 😊\n\n"
                "I'm your AI restaurant assistant.\n"
                "You can ask me anything about the restaurant, "
                "book a table, order food, or check our menu."
            )

    finally:
        db.close()

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     db = SessionLocal()

#     try:
#         manager = ConversationManager(db)

#         response = manager.start_conversation(
#             telegram_id=update.effective_user.id,
#             username=update.effective_user.username,
#             first_name=update.effective_user.first_name,
#         )

#         if response == "REGISTER":
#             await send_intro(update)
#         else:
#             await update.message.reply_text(response, reply_markup=main_menu_keyboard())

#     finally:
#         db.close()
