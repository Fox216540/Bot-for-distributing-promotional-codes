from aiogram.dispatcher.filters.state import State, StatesGroup

class Mailing(StatesGroup):
    message = State()

class Promo(StatesGroup):
    message = State()

class Channels(StatesGroup):
    channel = State()