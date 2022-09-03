from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


#кнопки для админа
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton("/Удалить")
button_stop = KeyboardButton("/stop")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
					.add(button_load).add(button_delete).add(button_stop)