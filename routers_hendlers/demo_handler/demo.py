import logging
import asyncio

from aiogram.types import InputFile, FSInputFile, Message
from aiogram import Router, F, types
import logging
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3NoHeaderError
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from routers_hendlers.main_menu.menu_kb import *
from routers_hendlers.demo_handler.demo_booking import *
from routers_hendlers.demo_handler.demo_kb import *
from booking.booking import *
from create_bot import bot, ALL_MEDIA_DIR
from database.db import Database


demo_router = Router()

db = Database()

load_dotenv()
chat_admin = os.getenv('CHAT_ADMIN')


@demo_router.message(F.text.startswith("⤵️ Назад"))
async def back_demo_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == "⤵️ Назад":
        await message.answer(
            "Ты вернулся назад", reply_markup=menu_kb(message.from_user.id)
        )
    await state.clear()


# -----------------------------------------------------------------------------------------------------------------------


class DemoStates(StatesGroup):
    name = State()
    text_info = State()
    audio = State()
    cancel = State()


@demo_router.message(F.text.startswith("🌀 Отправить демо"))
async def send_demo(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(DemoStates.audio)
    await message.answer(demo_send, reply_markup=back_menu_demo_kb())


@demo_router.message(StateFilter(DemoStates.audio))
async def process_audio_demo(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.AUDIO:
        user_id = message.from_user.id
        db.add_user(user_id)
        audio_count = db.get_audio_count(user_id)

        if audio_count >= MAX_AUDIO_FILES:
            await message.answer(
                "Ты достиг максимального кол-ва демок, которые можно отправить!",
                reply_markup=menu_kb(user_id),
            )
            await state.clear()
            return

        db.update_audio_count(user_id)
        audio_file_id = message.audio.file_id

        # Скачиваем аудиофайл
        audio_file = await bot.get_file(audio_file_id)
        audio_path = os.path.join(ALL_MEDIA_DIR, f"{user_id}_{audio_count}_original.mp3")
        await bot.download_file(audio_file.file_path, audio_path)

        # Обработка аудиофайла
        processing_message = await message.answer("Идет обработка твоего демо... Пожалуйста, подожди.")
        await asyncio.sleep(5)

        # Переименовываем файл в Unknown.mp3 и удаляем метаданные
        ren_au = os.path.join(ALL_MEDIA_DIR, "Unknown.mp3")
        os.rename(audio_path, ren_au)

        try:
            audio = MP3(ren_au, ID3=ID3)
            audio.delete()  # Удаляем все метаданные
            audio.save()
        except ID3NoHeaderError:
            pass  # Если метаданные отсутствуют, просто продолжаем

        # Сохраняем информацию о демо в базе данных
        db.add_demo(user_id, ren_au)

        # Получаем demo_id
        demo_id = db.cursor.lastrowid
        # Переименовываем файл в Unknown{demo_id}.mp3
        new_ren_au = os.path.join(ALL_MEDIA_DIR, f"Unknown-{demo_id}.mp3")
        os.rename(ren_au, new_ren_au)

        # Отправляем аудиофайл в группу
        audio_input_file = FSInputFile(new_ren_au)
        await bot.send_audio(chat_id=chat_admin, audio=audio_input_file, caption="Новая демка:\n\n",
                             reply_markup=admin_kb(user_id=user_id))

        await bot.delete_message(chat_id=message.chat.id, message_id=processing_message.message_id)
        await message.answer("Спасибо! Твоя демо-работа успешно отправлена администрации.",
                             reply_markup=menu_kb(user_id))

        # Удаляем файл после отправки
        os.remove(new_ren_au)
        await state.clear()
    else:
        await message.answer("Отправь свою демо-работу!")

# -----------------------------------------------------------------------------------------------------------------------


@demo_router.callback_query(F.data.startswith("accept_audio_file"))
async def accept_audio(callback_query: types.CallbackQuery):
    logging.info(f"Received callback data: {callback_query.data}")  # Логируем данные
    data_parts = callback_query.data.split("_")

    # Проверяем корректность данных
    if len(data_parts) < 4:  # Должно быть 4 части
        await callback_query.answer("Ошибка: неверные данные.")
        logging.error("Ошибка: недостаточно данных.")
        return

    user_id_str = data_parts[3]  # Изменяем индекс на 3

    # Проверяем, является ли последний элемент числом
    if not user_id_str.isdigit():
        await callback_query.answer("Ошибка: неверные данные.")
        logging.error(f"Ошибка: user_id не является числом: {user_id_str}")
        return

    user_id = int(user_id_str)  # user_id отправителя демо-работы
    admin_id = callback_query.from_user.id  # admin_id инициатора (кто нажал кнопку)

    await callback_query.answer("Демка принята.")

    try:
        # Получаем информацию о пользователе, используя user_id
        logging.info(f"Получаем информацию о пользователе с user_id: {user_id} в чате {callback_query.message.chat.id}")
        user_info = await bot.get_chat_member(chat_id=callback_query.message.chat.id, user_id=user_id)
        username = user_info.user.username if user_info.user.username else f"пользователь {user_id}"

        # Уведомляем администратора
        await bot.send_message(
            chat_admin,  # Отправляем сообщение инициатору
            f"Демка принята от @{username}!\nСвяжись с ним для дальнейших действий."
        )

        # Уведомляем пользователя о принятии демо
        await bot.send_message(user_id, "Твоя демо-работа принята!\nСвяжись с @gowebgoione.")

    except Exception as e:
        logging.error(f"Ошибка при получении информации о пользователе: {e}")
        await callback_query.answer("Ошибка: не удалось получить информацию о пользователе.")


@demo_router.callback_query(F.data.startswith("reject_audio_file"))
async def reject_audio(callback_query: types.CallbackQuery):
    await callback_query.answer()

    if callback_query.message.reply_to_message:
        await callback_query.message.reply_to_message.delete()

    await callback_query.message.answer("Демка отклонена.")
