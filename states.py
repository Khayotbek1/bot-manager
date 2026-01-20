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
    panel = State()            # Admin panel (boshlanish)
    export = State()           # Export bo‘limi

    statistics_menu = State()  # Statistika asosiy menyu
    channel_list = State()     # Kanallar ro‘yxati
    channel_detail = State()   # Bitta kanal statistikasi
