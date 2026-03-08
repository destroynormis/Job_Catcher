from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def confirm_keyboard():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Найти вакансии")],
            [KeyboardButton(text="Заполнить заново")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return kb