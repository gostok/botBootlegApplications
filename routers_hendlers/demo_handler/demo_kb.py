from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

def menu_demo_kb():
    kb_list = [
        [KeyboardButton(text="🌀 Отправить демо"), KeyboardButton(text="⁉️ Инструкция")],
        [KeyboardButton(text="⬅️ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def admin_kb():
    kb_list = [
        [InlineKeyboardButton(text="Принять", callback_data="accept_audio_file")],
        [InlineKeyboardButton(text="Отказать", callback_data="reject_audio_file")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def back_menu_demo_kb():
    kb_list = [
        [KeyboardButton(text="⤵️ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb