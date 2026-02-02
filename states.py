from aiogram.fsm.state import State, StatesGroup


# ================= USER REGISTRATION =================

class RegisterState(StatesGroup):
    phone = State()
    first_name = State()
    region = State()
    channel = State()


# ================= ADMIN POST (BROADCAST) =================

class AdminPostState(StatesGroup):
    waiting_content = State()


# ================= ADMIN FSM =================

class AdminSection(StatesGroup):
    panel = State()
    export = State()

    statistics_menu = State()
    channel_list = State()
    channel_detail = State()
