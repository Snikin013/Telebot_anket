from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb


ID = [628333023]

class FSMAdmin(StatesGroup):
	photo = State()
	name = State()
	description = State()
	price = State()


#check moredators
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
	global ID
	if message.from_user.id not in ID:
		ID.append(message.from_user.id)
	await bot.send_message(message.from_user.id, 'Хозяяииин ' + str(ID), reply_markup=admin_kb.button_case_admin)
	await message.delete()


#Начало диалога загрузки нового пункта меню
#@dp.message_handler(command='Загрузить', state=None)
async def cm_start(message: types.Message):
	if message.from_user.id in ID:
		await FSMAdmin.photo.set()
		await message.reply('Загрузи фото')


#first answer
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
	if message.from_user.id in ID:
		async with state.proxy() as data:
			data['photo'] = message.photo[0].file_id
		await FSMAdmin.next()
		await message.reply('Теперь введи название')

#second answer
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
	if message.from_user.id in ID:
		async with state.proxy() as data:
			data['name'] = message.text
		await FSMAdmin.next()
		await message.reply('Теперь введи описание')

#third answer
#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
	if message.from_user.id in ID:
		async with state.proxy() as data:
			data['description'] = message.text
		await FSMAdmin.next()
		await message.reply('Теперь введи цену')

#@dp.message_handler(state=FSMAdmin.description)
async def load_price(message: types.Message, state: FSMContext):
	if message.from_user.id in ID:
		async with state.proxy() as data:
			data['price'] = float(message.text)

		await sqlite_db.sql_add_command(state)
		await state.finish()


#do cancel
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('Ok')



############################################################################################################################################

async def deactivate_my_bot(message: types.Message):
	if message.from_user.id in ID:
		await bot.send_message(message.from_user.id, 'Выключаюсь ')
		await exit()
		



def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
	dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin)
	dp.register_message_handler(load_name, state=FSMAdmin.name)
	dp.register_message_handler(load_description, state=FSMAdmin.description)
	dp.register_message_handler(load_price, state=FSMAdmin.price)
	dp.register_message_handler(cancel_handler, state='*', commands='отмена')
	dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
	dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
	dp.register_message_handler(deactivate_my_bot, commands=['stop'])






