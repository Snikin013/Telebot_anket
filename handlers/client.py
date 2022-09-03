from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import client_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db


class FSMclient(StatesGroup):
	photo = State()
	name = State()
	description = State()
	price = State()


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
	try:
		await bot.send_message(message.from_user.id, 

			"<b>{} {}</b>, Приветствуем Вас!,\nНужна помощь? "
			.format(message.from_user.first_name, message.from_user.last_name if message.from_user.last_name != None else '') +
            f"\n/start вернуться в начало\n/list заполнить анкету\n/contact связаться с менеджером\n/continue продолжить" +
            f"\n/help список команд"

            , reply_markup=client_kb.kb_client, parse_mode='html')

		await message.delete()
	except:
		await message.reply('Общение с ботом через ЛС, напиши сюда\nhttps://t.me/TheWeatherrBot')


async def time_of_work(message: types.Message):
	await bot.send_message(message.from_user.id, 'Не работаем')


async def dislocation(message: types.Message):
	await bot.send_message(message.from_user.id, 'РФ')




##############################
async def new_client(message: types.Message):

	await bot.send_message(message.from_user.id, 
						   '''
						   <b>Заполните пожалуйста анкету. Заполнение анкеты будет проходить поэтапно.</b>
						   ''', 
						   reply_markup=client_kb.kb_client, parse_mode='html') #? reply_markup  выяснить что означает параметр и что можно передать
	await message.delete()


#Начало диалога загрузки
async def list_first_step(message: types.Message):
	await FSMclient.photo.set()
	await message.reply('Загрузи фото')


# Введите данные для анкеты:\n1)Имя и Телелефонный номер\n2)Пол\n3)Возраст\n4)Срок и сумма Просрочки\n" \
            # f"5)Время для связи\n6)Промокод


#first answer
#@dp.message_handler(content_types=['photo'], state=FSMclient.photo)
async def load_client_photo(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['photo'] = message.photo[0].file_id
	await FSMclient.next()
	await message.reply('Теперь введи Имя Фамилию Отчество в указанном порядке.')

#second answer
async def name_of_client(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text
	await FSMclient.next()
	await message.reply('Теперь выбери свой пол: \n/Male - мужской \n /Female - женский \n/Regect - воздержусь от ответа')

#third answer
async def choose_sex(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['sex'] = message.text[1:]
	await FSMclient.next()
	await message.reply('Теперь введите контактный номер телефона в виде +7 999 999 99 99')


async def mobile_number(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		# if 
		data['mob_number'] = message.text

	await sqlite_db.sql_add_command(state)
	await state.finish()
	await message.reply('Ваша анкета отправлена!\nОжидайте, наш специалист свяжется с Вами в ближайшее время.')


#do cancel
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler_cl(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('Ok')
################
 

def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help'])
	dp.register_message_handler(time_of_work, commands=['Режим_работы'])
	dp.register_message_handler(dislocation, commands=['Расположение'])

	dp.register_message_handler(list_first_step, commands=['list', 'Анкета'], state=None)
	dp.register_message_handler(load_client_photo, content_types=['photo'], state=FSMclient)
	dp.register_message_handler(name_of_client, state=FSMclient.name)
	dp.register_message_handler(choose_sex, state=FSMclient.description)
	dp.register_message_handler(mobile_number, state=FSMclient.price)
	dp.register_message_handler(cancel_handler_cl, state='*', commands='Отмена')
	dp.register_message_handler(cancel_handler_cl, Text(equals='Отмена', ignore_case=True), state='*')


