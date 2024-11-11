from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Router, F, types
from routers_hendlers.main_menu.menu_kb import *
from routers_hendlers.main_menu.info_booking import *


main_router = Router()

@main_router.message(F.text.startswith("⬅️ Назад"))
async def back_kb(message: types.Message):
    user_id = message.from_user.id
    if message.text == "⬅️ Назад":
        await message.answer('Ты вернулся в главное меню:', reply_markup=menu_kb(message.from_user.id))

@main_router.message(F.text.startswith("❤️ О нас"))
async def about_us(message: types.Message):
    await message.answer(info_about_us, reply_markup=menu_kb(message.from_user.id))
    await message.answer('Наши ссылки:',
                         reply_markup=inline_about_us())


# @main_router.message(F.text.startswith("📝 Статьи"))
# async def show_contacts(message: types.Message):
#     await message.answer('Ты вошёл в пункт "Статьи".\n\nВыбери из меню ниже, о чем хотел бы узнать:',
#                          reply_markup=article_kb(message.from_user.id))
#
# @main_router.message(F.text.startswith("👀 YouTube"))
# async def show_youtube(message: types.Message):
#     await message.answer('YouTube каналы:\n', reply_markup=youtube_in())
#
# @main_router.message(F.text.startswith("⭐ SoundCloud"))
# async def show_youtube(message: types.Message):
#     await message.answer('SoundCloud:\n', reply_markup=soundcloud_in())
#
# @main_router.message(F.text.startswith("‼️ Полезные ссылки ‼️"))
# async def show_youtube(message: types.Message):
#     await message.answer('Полезные ссылки:\n', reply_markup=useful_links())