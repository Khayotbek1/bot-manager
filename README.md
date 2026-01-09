# Telegram Channel Manager Bot

Aiogram 3.x asosida yozilgan, **Telegram kanalni professional boshqarish** uchun mo‘ljallangan bot.  
Bot foydalanuvchilarni **majburiy ro‘yxatdan o‘tkazadi**, **kanalga kirish / chiqishni nazorat qiladi**,  
**statistika yuritadi** va **admin orqali broadcast xabarlar yuborish** imkonini beradi.

---

## 🚀 Asosiy imkoniyatlar

### 👤 Foydalanuvchilar uchun
- Kanalga **join request** orqali kirish
- Bot orqali majburiy **ro‘yxatdan o‘tish**
  - Telefon raqam
  - Ism
  - Viloyat
- Ro‘yxatdan o‘tmagan foydalanuvchi kanalga kira olmaydi

### 📊 Statistika
- Jami ro‘yxatdan o‘tganlar
- Jami chiqib ketganlar
- Bugungi:
  - qo‘shilganlar
  - chiqib ketganlar
- Oxirgi 7 kun
- Joriy oy statistikasi

### 📤 CSV eksport
- Bugungi foydalanuvchilar
- Sana oralig‘i bo‘yicha eksport
- Sana va vaqt **O‘zbekiston vaqti (Asia/Tashkent)** da
- CSV avtomatik o‘chiriladi (disk to‘lib ketmasligi uchun)

### 👨‍💼 Admin panel
- `/admin` orqali kirish
- Admin faqat **Telegram ID** orqali tekshiriladi
- Admin imkoniyatlari:
  - 📊 Statistika
  - 📤 Export
  - 📝 Post (broadcast)

### 📝 Broadcast (Post)
- Kontent **kanalga emas**
- Botdan ro‘yxatdan o‘tgan **barcha foydalanuvchilarga shaxsiy xabar** sifatida yuboriladi
- Qo‘llab-quvvatlanadi:
  - Text
  - Rasm
  - Video
  - Fayl
- Flood protection mavjud

---

## 🛠 Texnologiyalar

- Python 3.10+
- Aiogram 3.x
- SQLAlchemy (async)
- SQLite (default)
- FSM (Finite State Machine)
- python-dotenv

---

## 📁 Loyiha tuzilishi

```text
bot-manager/
│
├── bot.py
├── config.py
├── states.py
├── database.py
├── models.py
│
├── handlers/
│   ├── start.py
│   ├── registration.py
│   ├── join_request.py
│   └── admin.py
│
├── keyboards/
│   ├── reply.py
│   └── inline.py
│
├── utils/
│   ├── csv_export.py
│   └── statistics.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 👨‍💻 Dasturchi (Author)

**Ism:** Hayotbek  
**Familya:** Razzoqov

**Mutaxassislik:** Python Backend  
**Telegram:** https://t.me/Razzoqov7  

Agar loyiha bo‘yicha savollar, takliflar yoki hamkorlik bo‘lsa — bemalol bog‘lanishingiz mumkin.

