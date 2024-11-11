import time
import asyncio

import aiogram.exceptions
from aiogram.types import InputFile, FSInputFile, Message
from aiogram import Router, F, types
import logging
import os
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError, ID3NoHeaderError
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from routers_hendlers.main_menu.menu_kb import *
from routers_hendlers.demo_handler.demo_booking import *
from routers_hendlers.demo_handler.demo_kb import *
from booking.booking import *
from create_bot import bot, ALL_MEDIA_DIR
from database.db import *


demo_router = Router()


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

        audio_count = update_audio_count(user_id)

        if audio_count >= MAX_AUDIO_FILES:
            await message.answer(
                "Ты достиг максимального кол-ва демок, которые можно отправить!",
                reply_markup=menu_kb(message.from_user.id),
            )
            await state.clear()
            return

        user_audio_count[user_id] = audio_count + 1
        audio_file_id = message.audio.file_id

        # Скачиваем аудиофайл
        audio_file = await bot.get_file(audio_file_id)
        audio_path = os.path.join(
            ALL_MEDIA_DIR, f"{user_id}_{audio_count}_original.mp3"
        )
        await bot.download_file(audio_file.file_path, audio_path)

        # Отправляем интерактивное сообщение о процессе обработки
        processing_message = await message.answer(
            "Идет обработка твоего файла... Пожалуйста, подожди."
        )

        await asyncio.sleep(5)

        # Переименовываем файл в Unknown.mp3
        ren_au = os.path.join(ALL_MEDIA_DIR, "Unknown.mp3")
        os.rename(audio_path, ren_au)

        # Изменяем метаданные
        try:
            audio = MP3(ren_au, ID3=ID3)
            audio.delete()  # Удаляем все метаданные
            audio.save()
        except ID3NoHeaderError:
            pass  # Если метаданные отсутствуют, просто продолжаем

        # Проверяем, существует ли файл
        if not os.path.exists(ren_au):
            await message.answer(f"Файл не найден: {ren_au}")
            return

        for_admin_text = "Новая демка:\n\n"
        await asyncio.sleep(5)

        # Создаем FSInputFile с полным путем
        audio_input_file = FSInputFile(ren_au)

        # Отправляем аудиофайл
        await bot.send_audio(
            chat_id=-1002363283480,
            audio=audio_input_file,
            caption=for_admin_text,
            performer="Unknown",
            reply_markup=admin_kb(),
        )
        await bot.delete_message(
            chat_id=message.chat.id, message_id=processing_message.message_id
        )
        await message.answer(
            "Спасибо!\nТвоя демо-работа успешно отправлена администрации.",
            reply_markup=menu_kb(message.from_user.id),
        )

        # Удаляем файл после отправки
        os.remove(ren_au)  # Удаляем файл с полным путем
        await state.clear()

    else:
        await message.answer("Отправь свою демо-работу!")


# -----------------------------------------------------------------------------------------------------------------------


@demo_router.callback_query(F.data.startswith("accept_audio_file"))
async def accept_audio(callback_query: types.CallbackQuery):
    audio_file_id = callback_query.data.split("_")[1]
    await callback_query.answer("Демка принята.")

    await bot.send_message(
        callback_query.from_user.id,
        "Твоя демо-работа принята!\nСвяжись с @gowebgoione.",
    )


@demo_router.callback_query(F.data.startswith("reject_audio_file"))
async def reject_audio(callback_query: types.CallbackQuery):
    await callback_query.answer("Демка отклонена.")
