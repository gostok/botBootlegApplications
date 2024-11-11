import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import os

from decouple import config

TOKEN = "6302423087:AAEMMjincW-Gm4YeKEnXhiD7x9dSIRphBMk"


ALL_MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_audio")


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
