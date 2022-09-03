from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('1231540472:AAFp-vIk2TuJt_OEJWUfqHTaxbsxsNj1UgU')
dp = Dispatcher(bot, storage=storage)