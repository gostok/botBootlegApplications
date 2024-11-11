from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from routers_hendlers.main_menu.menu_kb import menu_kb
from aiogram.fsm.context import FSMContext
from database.db import get_user_count, get_audio_count


start_router = Router()

cmd_message = (
    'Привет!\n'
    'Я - BCB: чат бот сообщества Bootleg Club (@bootlegclub).\n\n'
    'Чтобы отправить своё демо нам, используй меню ниже ↓↓↓'
)

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(cmd_message, reply_markup=menu_kb(message.from_user.id))

@start_router.message(Command('user_count'))
async def cmd_user_count(message: types.Message):
    user_count = get_user_count()
    audio_count = get_audio_count()
    response = (
        f'Количество пользователей, загрузивших аудиофайлы: {user_count}\n'
        f'Общее количество загруженных аудиофайлов: {audio_count}'
    )
    await message.answer(response or 'Нет данных в БД')