from telegram import Update
from telegram.ext import ContextTypes
from app.database import SessionLocal
from app.chatbot.handlers.register_handler import RegisterHandler
from app.chatbot.keyboards import main_menu_keyboard


async def contact_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    print("✅ CONTACT HANDLER CALLED")
    db = SessionLocal()

    try:
        phone = update.message.contact.phone_number

        handler = RegisterHandler(db)

        response = handler.register_contact(
            telegram_id=update.effective_user.id,

            username=update.effective_user.username,

            first_name=update.effective_user.first_name,

            phone=phone

        )

        await update.message.reply_text(
            response,
            reply_markup=main_menu_keyboard()

        )

    finally:
        db.close()
