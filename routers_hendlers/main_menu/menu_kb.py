
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

def menu_kb(user_telegram_id):
    kb_list = [
        [KeyboardButton(text="🌀 Отправить демо")],
        [KeyboardButton(text="❤️ О нас")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def inline_about_us():
    kb_list = [
        [InlineKeyboardButton(text="BOOTLEG CLUB VA", url="https://band.link/BootlegClubVA")],
        [InlineKeyboardButton(text="BOOTLEG CLUB VA 2", url="https://band.link/BootlegClubVA2")],
        [InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/bootleg__club/")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)


# def article_kb(user_telegram_id: int):
#     kb_list = [
#         [KeyboardButton(text="👀 YouTube"), KeyboardButton(text="⭐ SoundCloud")],
#         [KeyboardButton(text="‼️ Полезные ссылки ‼️"), KeyboardButton(text="⬅️ Назад")]
#     ]
#     keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
#     return keyboard
#
# def youtube_in():
#     kb_list = [
#         [InlineKeyboardButton(text='Bootleg Club', url='https://t.me/bootlegclub')],
#         # [InlineKeyboardButton(text='Ютуб ссылка 2')],
#         # [InlineKeyboardButton(text='Ютуб ссылка 3')],
#         # [InlineKeyboardButton(text='Ютуб ссылка 4')]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=kb_list)
#
# def soundcloud_in():
#     kb_list = [
#         [InlineKeyboardButton(text='Cloud ссылка 1')],
#         [InlineKeyboardButton(text='Cloud ссылка 2')],
#         [InlineKeyboardButton(text='Cloud ссылка 3')],
#         [InlineKeyboardButton(text='Cloud ссылка 4')]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=kb_list)
#
# def useful_links():
#     kb_list = [
#         [InlineKeyboardButton(text='Полезная ссылка 1')],
#         [InlineKeyboardButton(text='Полезная ссылка 2')],
#         [InlineKeyboardButton(text='Полезная ссылка 3')],
#         [InlineKeyboardButton(text='Полезная ссылка 4')]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=kb_list)