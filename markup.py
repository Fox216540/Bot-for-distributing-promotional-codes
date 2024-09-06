from aiogram.types import KeyboardButton, InlineKeyboardMarkup
import  db
def markup1():
    markup = InlineKeyboardMarkup()
    buttons = [
        KeyboardButton(text="➕Получить промокод",callback_data='next1'),
    ]
    markup.add(*buttons)
    return markup
def markup2():
    sub = InlineKeyboardMarkup()

    buttons = []
    for channel in db.channels()[:3]:
        buttons.append(KeyboardButton(text="ПОДПИСАТЬСЯ",url = channel[0]))
    buttons.append(KeyboardButton(text="☑️ Проверить подписку", callback_data='next2'))
    sub.add(*buttons)
    return sub,db.channels()[:3]
def markup3():
    sub = InlineKeyboardMarkup()
    buttons = []
    for channel in db.channels()[3:]:
        buttons.append(KeyboardButton(text="ПОДПИСАТЬСЯ",url = channel[0]))
    buttons.append(KeyboardButton(text="✅Подписался, получить промокод!", callback_data='yes'))
    sub.add(*buttons)
    return sub,db.channels()[3:]