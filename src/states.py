from aiogram.fsm.state import StatesGroup, State


class State(StatesGroup):
    get_todolist = State()
    waiting_for_task = State()
    waiting_for_deleting_task = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_confirmation = State()
