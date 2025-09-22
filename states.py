from aiogram.fsm.state import State, StatesGroup


class AddAdStates(StatesGroup):
    waiting_for_content = State()
    waiting_for_photo_caption = State()
