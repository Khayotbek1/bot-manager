from aiogram.fsm.state import State, StatesGroup


# ================= USER REGISTRATION =================

class RegisterState(StatesGroup):
    phone = State()
    first_name = State()
    region = State()


# ================= ADMIN POST (BROADCAST) =================

class AdminPostState(StatesGroup):
    waiting_content = State()
