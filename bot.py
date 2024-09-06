from aiogram import types, Bot, executor
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import markup

import classes

import db

bot = Bot(token="")#TOKEN бота
# Диспетчер
dp = Dispatcher(bot,storage=MemoryStorage())



def check_sub_channel(chat_member):
    if chat_member.status != 'left':
        return True
    else:
        return False

@dp.message_handler(commands=['start'])
async def number(message: types.Message):
    print(message.chat.id)
    text = '''🥺 Привет, это официальный бот по промокодам StandChillow, чтобы получить промокод, тебе нужно нажать на кнопку, и подписаться на все каналы, далее ты сможешь получить промокод, а также, промокоды ты сможешь получать каждые 24 часа!\n
ПРЕДУПРЕЖДЕНИЕ❗️❗️❗️
ЕСЛИ БОТ, В КОТОРОМ ВЫ НАЖИМАЕТЕ СТАРТ ПРОСИТ ВАС ПОДЕЛИТЬСЯ СВОИМ  НОМЕРОМ ТЕЛЕФОНА, НИ В КОЕМ СЛУЧАЕ НЕ СКИДЫВАЙТЕ ЕМУ❗️ У ВАС УКРАДУТ АККАУНТ❗️❗️❗\n
WARNING❗️❗️❗️
IF THE BOT IN WHICH YOU PRESS START ASKS YOU TO SHARE YOUR PHONE NUMBER, DO NOT TELL IT ❗️ OR YOUR ACCOUNT WILL BE STOLE❗️❗️❗️\n
👇 Жми на кнопку и открывай доступ к промокодам на StandChillow'''
    photo = "photo.jpg"
    with open(photo, 'rb') as phot:
        await bot.send_photo(message.chat.id,photo=phot,caption=text,reply_markup=markup.markup1())

@dp.message_handler(commands=['mailing'])
async def number(message: types.Message):

    if message.from_user.id != 6324881718:
        await message.answer('Вы не админ')
        return
    await message.answer('Напишите текст для рассылки')
    await classes.Mailing.message.set()

@dp.message_handler(state=classes.Mailing.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    text = await state.get_data()
    for user in db.users():
        try:
            await bot.send_message(user[0],text['message'])
        except:
            pass
    await message.answer('Рассылка сделана')
    await state.finish()
@dp.message_handler(commands=['promo'])
async def number(message: types.Message):

    if message.chat.id != 6324881718:
        await message.answer('Вы не админ')
        return
    await message.answer('Напишите промокод')
    await classes.Promo.message.set()

@dp.message_handler(state=classes.Promo.message)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    text = await state.get_data()
    db.change(text['message'])
    await message.answer('Вы поменяли промокод')
    await state.finish()

@dp.message_handler(commands=['channel'])
async def number(message: types.Message):

    if message.from_user.id != 6324881718:
        await message.answer('Вы не админ')
        return
    await message.answer('Напишите каналы через пробел \n\nПример:https://t.me/...')
    await classes.Channels.channel.set()

@dp.message_handler(state=classes.Channels.channel)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(channel=message.text)
    text = await state.get_data()
    db.add_channel(text['channel'])
    await message.answer('Каналы изменены')
    await state.finish()

@dp.callback_query_handler(text='yes')
async def next_menu(callback: types.CallbackQuery):
    for i in markup.markup2()[1]:
        if not check_sub_channel(await bot.get_chat_member(chat_id=i[0].replace('https://t.me/','@'), user_id=callback.message.chat.id)):
            await callback.message.answer('Пожалуйста, подпишитесь на каналы')
            return
    db.add_user(callback.message.chat.id)
    await callback.message.answer(f'Спасибо что выполнили все задания!❤️\nВаш промокод: {db.text()}\n\nОставайтесь с нами и получайте ежедневно промокоды!🥳')
    await callback.message.delete()
@dp.callback_query_handler(text='next2')
async def next_menu(callback: types.CallbackQuery):
    for i in markup.markup2()[1]:
        id = i[0]
        if i[1] != None:
            id = i[1]
        else:
            id = id.replace('https://t.me/', '@')
        if not check_sub_channel(await bot.get_chat_member(chat_id=id, user_id=callback.message.chat.id)):
            await callback.message.answer('Пожалуйста, подпишитесь на каналы')
            return
    await callback.message.delete()
    photo = "photo.jpg"
    with open(photo, 'rb') as phot:
        await bot.send_photo(callback.message.chat.id,phot,'👇 Осталось немного, подпишись на эти каналы:',reply_markup=markup.markup3()[0])
@dp.callback_query_handler(text='next1')
async def number(callback: types.CallbackQuery):
    await callback.message.delete()
    photo = "photo.jpg"
    with open(photo, 'rb') as phot:
        await bot.send_photo(callback.message.chat.id,photo=phot,caption='👇 Чтобы получить промокод, тебе необходимо подписаться на всех:',reply_markup=markup.markup2()[0])


executor.start_polling(dp,skip_updates=True)