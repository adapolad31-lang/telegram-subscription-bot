import os
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

GROUP_ID = int(os.getenv("GROUP_ID"))

users = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💳 Ödəniş et və qoşul", callback_data="pay")
    )

    text = """
🔥 PREMIUM QAPALI QRUP 🔥

📌 Qrup haqqında:

• Gündəlik siqnallar  
• Canlı analiz  
• Təlim dəstəyi  

💰 40 AZN / 30 gün

📜 Qaydalar və Şərtlər:

1️⃣ Ödəniş geri qaytarılmır  
2️⃣ Link paylaşmaq qadağandır  
3️⃣ Müddət bitdikdə avtomatik çıxarılacaqsınız  

Qoşulmaq üçün düyməyə klik edin 👇
"""

    await message.answer(text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "pay")
async def fake_payment(callback_query: types.CallbackQuery):

    user_id = callback_query.from_user.id
    expiry = datetime.now() + timedelta(days=30)

    users[user_id] = expiry

    invite_link = await bot.create_chat_invite_link(
        chat_id=GROUP_ID,
        member_limit=1
    )

    await bot.send_message(
        user_id,
        f"✅ Ödəniş təsdiqləndi!\n\nBu linklə qrupa qoşulun:\n{invite_link.invite_link}"
    )

async def check_expired():
    while True:
        now = datetime.now()
        for user_id, expiry in list(users.items()):
            if now > expiry:
                try:
                    await bot.ban_chat_member(GROUP_ID, user_id)
                    await bot.unban_chat_member(GROUP_ID, user_id)
                except:
                    pass
                del users[user_id]
        await asyncio.sleep(86400)

async def on_startup(dp):
    asyncio.create_task(check_expired())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
