from telegram import Update
from telegram.ext import ContextTypes

from app.database import SessionLocal
from app.services.customer_service import (
    get_customer_by_telegram_id,
)

from app.ai.graph.service import RestaurantGraphService


async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message or not update.message.text:
        return

    db = SessionLocal()

    try:

        customer = get_customer_by_telegram_id(
            db,
            update.effective_user.id,
        )

        if customer is None:
            await update.message.reply_text(
                "Please use /start to register first."
            )
            return

        graph = RestaurantGraphService(db)

        response = graph.run(
            customer_id=customer.customer_id,
            user_message=update.message.text,
        )

        await update.message.reply_text(response)
    except Exception as e:

        print("=" * 60)
        print("GRAPH ERROR")
        print(e)
        print("=" * 60)

        raise

    finally:
        db.close()


# from telegram import Update
# from telegram.ext import ContextTypes
# from app.chatbot.conversation_manager import ConversationManager

# from app.database import SessionLocal
# from app.ai.graph.service import RestaurantGraphService

# async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

#     # Ignore non-text messages
#     if not update.message or not update.message.text:
#         return

#     # telegram_id = str(update.effective_user.id)
#     # message = update.message.text

#     db = SessionLocal()
#     try:
#         # manager = ConversationManager(db)

#         graph = RestaurantGraphService(db)
#         response = manager.handle_message(
#             telegram_id=update.effective_user.id,
#             message=update.message.text
#         )

#         if response:
#             await update.message.reply_text(response)

#     finally:
#         db.close()
# old architecture
