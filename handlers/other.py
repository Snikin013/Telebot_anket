from aiogram import types, Dispatcher
from create_bot import dp
import json, string


ID = [628333023]

# @dp.message_handler()
async def echo_send(message: types.Message):

	# if message.text == 'Выключись' and message.from_user.id in ID:
	# 	await message.reply('Выключаюсь')
	# 	await exit()

	if {i.lower().translate(str.maketrans('', '', string.punctuation))  for i in message.text.split(' ')}\
		.intersection(set(json.load(open('cenz.json')))) != set():
		
		await message.reply('Маты запрещены, будь паенькой')
		await message.delete()




def register_handlers_other(dp: Dispatcher):
	dp.register_message_handler(echo_send)