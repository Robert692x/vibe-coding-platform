from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    labels = [
        "Кошелёк",
        "Аналитика",
        "Цена",
        "Киты",
        "DEX",
        "Алерты",
        "AI Аналитик",
        "Premium",
        "Профиль",
        "English",
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=label)] for label in labels],
        resize_keyboard=True,
    )
