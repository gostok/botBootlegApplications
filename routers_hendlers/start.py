import os

from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from routers_hendlers.main_menu.menu_kb import menu_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import Database
from dotenv import load_dotenv
from create_bot import bot

load_dotenv()

CHAT_ADMIN = int(os.getenv('CHAT_ADMIN'))

db = Database()

start_router = Router()


class AdPost(StatesGroup):
    awaiting_ad_photo_state = State()



cmd_message = (
    'Привет!\n'
    'Я - BCB: чат бот сообщества Bootleg Club (@bootlegclub).\n\n'
    'Чтобы отправить своё демо нам, используй меню ниже ↓↓↓'
)


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(cmd_message, reply_markup=menu_kb(message.from_user.id))


@start_router.message(Command('admin'))
async def cmd_admin(message: types.Message):
    await message.answer(f'Команды:\n'
                         f'/user_count - для получения информации о кол-ве пользователей и кол-ве отправленных демо работ.\n'
                         f'/ad_post - для отправки сообщений всем пользователям бота.\n')


@start_router.message(Command('user_count'))
async def cmd_user_count(message: types.Message):
    user_count = db.get_user_count()
    audio_count = db.get_total_audio_count()
    response = (
        f'Количество пользователей, загрузивших аудиофайлы: {user_count}\n'
        f'Общее количество загруженных аудиофайлов: {audio_count}'
    )
    await message.answer(response or 'Нет данных в БД')


@start_router.message(Command('ad_post'))
async def cmd_ad_post(message: types.Message, state: FSMContext):
    if message.chat.id != CHAT_ADMIN:
        await message.answer("Эта команда доступна только в группе администраторов.")
        return

    await message.answer("Введите текст рекламы или поста, который вы хотите отправить всем пользователям:")
    await state.set_state(AdPost.awaiting_ad_photo_state)


@start_router.message(StateFilter(AdPost.awaiting_ad_photo_state))
async def process_ad_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id if message.photo else None  # Проверяем, есть ли фото
    ad_text = message.text
    users = db.cursor.execute('SELECT user_id FROM users').fetchall()

    for user in users:
        user_id = user[0]
        try:
            if photo:
                await bot.send_photo(user_id, photo=photo)
            elif ad_text:
                await bot.send_message(user_id, ad_text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    await message.answer("Реклама успешно отправлена всем пользователям.")
    await state.clear()
