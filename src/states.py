from aiogram.fsm.state import State, StatesGroup

class LinkInput(StatesGroup):
    waiting_for_link = State()
    waiting_for_confirmation = State()