from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Анкета')
b4 = KeyboardButton('/Отмена')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).add(b3).add(b4)

'''
kb_client.add(b1).row(b1,b2).insert(b4)

row - добавляет в строку все
insert - добавляяет в строку если есть место

ReplyKeyboardMarkup(one_time_keyboard=True) - для сворачивания клавиатуры


from aiogram.types import ReplyKeyboardRemove

bot.send_message(message.from_user.id, '', reply_markup=ReplyKeyboardRemove())
для удаления калвиатуры совсем в clients в хендлер добавляем реплай
и удаляем здесь one_time_keyboard=True

'''