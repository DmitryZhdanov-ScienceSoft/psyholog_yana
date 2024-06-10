import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import BOT_NAMING
from keyboards.inline import MyCallback, one_button
from database import Database


db = Database()


async def func_start(message: Message, state: FSMContext, if_back: bool = False):
    user_id = message.chat.id
    name = message.from_user.first_name

    info = db.select_all_users()

    if str(user_id) not in info:
        db.add_user(user_id=user_id, name=name)

    if if_back:
        await message.answer('''*🏠 Вы в главном меню*

Я Яна – твой новый онлайн психолог в Телеграм.             

Со мной можно поговорить о чем угодно. Я постараюсь тебя поддержать и помогу разобраться с мыслями и чувствами. Мы можем обмениваться как текстом, так и голосовыми в любое время суток. 

👩‍⚕️ *Я стараюсь звучать как настоящий психолог*, но всё же я телеграм-бот, *оказывающий базовую психологическую поддержку*. Если у тебя действительно сложная ситуация, пожалуйста, обращайся к специалистам.
''',
                             reply_markup=one_button('О чём можно поговорить?', 'start_2'))
    else:
        text = f'''
🌟 *Привет, {name}!*      

Я Яна – твой новый онлайн психолог в Телеграм.             

Со мной можно поговорить о чем угодно. Я постараюсь тебя поддержать и помогу разобраться с мыслями и чувствами. Мы можем обмениваться как текстом, так и голосовыми в любое время суток. 

👩‍⚕️ *Я стараюсь звучать как настоящий психолог*, но всё же я телеграм-бот, *оказывающий базовую психологическую поддержку*. Если у тебя действительно сложная ситуация, пожалуйста, обращайся к специалистам.
'''
        await message.answer(text=text, reply_markup=one_button('О чём можно поговорить?', 'start_2'))


async def back_to_start(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await func_start(message=call.message, if_back=True, state=state)


def router(router: Router):
    router.message.register(func_start, CommandStart())
    router.callback_query.register(back_to_start, MyCallback.filter(F.call == 'back_to_start'))
