import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import INFO_MENU
from database import Database

db = Database()


async def info_user(message: Message):
    info = db.select_personal_info(user_id=message.chat.id)

    text = f'''
*Ваша информация:*
Имя: {info[1]}
Пол: {info[0]}
Возраст: {info[2]}
Доп.информация: {info[3]}  
'''
    await message.answer(text=text)

    await asyncio.sleep(1)
    await message.answer(text='Нажмите на кнопку, чтобы редактировать анкету 🙂',
                         reply_markup=INFO_MENU)


def router(rt: Router):
    rt.message.register(info_user, F.text == '/info')
