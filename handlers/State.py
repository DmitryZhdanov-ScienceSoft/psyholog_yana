from aiogram.fsm.state import State, StatesGroup


class StepsForm(StatesGroup):
    text_request = State()
    name = State()
    age = State()
    descr = State()
