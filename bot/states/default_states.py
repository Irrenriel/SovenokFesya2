from aiogram.dispatcher.filters.state import StatesGroup, State


# /start
class start_states(StatesGroup):
    Q1 = State()


# ⚒Мастерская
class craft_states(StatesGroup):
    Q1 = State()
    Q2 = State()


# 🔥Битва
class battle_states(StatesGroup):
    menu = State()

    menu_pin = State()
    al_order = State()