from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup
)


def contact_keyboard():

    keyboard = [
        [
            KeyboardButton(
                text="📱 Share Phone Number",
                request_contact=True
            )
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def main_menu_keyboard():

    keyboard = [

        ["🍽️ Book Table"],

        ["🛵 Order Online"],

        ["📖 View Menu"],

        ["🎁 Offers"],

        ["⭐ Reviews"]

    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
