from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.db import Database

db = Database()

def menu_demo_kb():
    kb_list = [
        [KeyboardButton(text="🌀 Отправить демо"), KeyboardButton(text="⁉️ Инструкция")],
        [KeyboardButton(text="⬅️ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def admin_kb(user_id, demo_id):
    if not user_id or not isinstance(user_id, int):
        raise ValueError("Неверный user_id.")

    kb_list = [
        [InlineKeyboardButton(text="Принять", callback_data=f"accept_audio_file_{user_id}_{demo_id}")],
        [InlineKeyboardButton(text="Отказать", callback_data=f"reject_audio_file_{user_id}_{demo_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb_list)

def back_menu_demo_kb():
    kb_list = [
        [KeyboardButton(text="⤵️ Назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb