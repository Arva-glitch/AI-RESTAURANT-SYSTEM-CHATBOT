from telegram import Update
from app.chatbot.keyboards import contact_keyboard


async def send_intro(update: Update):

    text = """
🏝️ ALOHA WELCOMES YOU!!

We serve delicious food made with fresh ingredients.

We offer:

🍕 Dine In
🛵 Online Delivery
🥡 Takeaway
🎉 Party Bookings

To get started, please share your phone number.
"""

    await update.message.reply_text(
        text,
        reply_markup=contact_keyboard()
    )
