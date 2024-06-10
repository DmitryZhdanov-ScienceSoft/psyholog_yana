import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.inline import MyCallback, SELECT_MALE, one_button
from database import Database
from handlers.State import StepsForm

db = Database()


async def male(call: CallbackQuery):
    text = '''⚪️⚪️⚪️⚪️
Расскажи, пожалуйста, пару слов о себе 🙂'''

    await call.message.edit_text(
        text=text,
        reply_markup=SELECT_MALE
    )


async def select_male(call: CallbackQuery, callback_data: MyCallback, state: FSMContext):
    male_name = callback_data.call.split('_')[1]

    db.update_field(user_id=call.message.chat.id,
                    field='male',
                    value=male_name)

    await call.message.edit_text('''🟢⚪️⚪️⚪️
Как тебя зовут?''')

    await state.set_state(StepsForm.name)


async def get_name(message: Message, state: FSMContext):
    if message.text:
        name = message.text

        db.update_field(user_id=message.chat.id,
                        field='name',
                        value=name)

        await message.answer('''🟢🟢⚪️⚪️
Сколько тебе лет?''')

        await state.set_state(StepsForm.age)

    else:
        text = '⚠️ _Вы написали не текст и отправили мне что-то не то!_\n\n*Как тебя зовут?*'
        await message.answer(text=text)

        await state.set_state(StepsForm.name)


async def get_age(message: Message, state: FSMContext):
    if message.text:
        age = message.text

        db.update_field(user_id=message.chat.id,
                        field='age',
                        value=age)

        await message.answer('''🟢🟢🟢⚪️
Что еще важно о тебе знать? Напиши кратко, не более 300 символов.''',
                             reply_markup=one_button(
                                 'Заполню позже 🙂',
                                 'openai'
                             ))

        await state.set_state(StepsForm.descr)

    else:
        text = '⚠️ _Вы написали не текст и отправили мне что-то не то!_\n\n*Сколько тебе лет?*'
        await message.answer(text=text)

        await state.set_state(StepsForm.age)


async def get_descr(message: Message, state: FSMContext):
    if message.text:
        description = message.text

        db.update_field(user_id=message.chat.id,
                        field='description',
                        value=description)

        await message.answer(text='''🟢🟢🟢🟢
Большое спасибо за анкету! Теперь я больше о тебе знаю, и смогу лучше отвечать.''')

        await asyncio.sleep(2)

        await message.answer(text='Расскажи как у тебя дела, как проходит твой день? Пришли мне текст, кружок, или голосовое.')
        await state.set_state(StepsForm.text_request)

    else:
        text = '⚠️ _Вы написали не текст и отправили мне что-то не то!_\n\n*Что еще важно о тебе знать? Напиши кратко, не более 300 символов.*'
        await message.answer(text=text)

        await state.set_state(StepsForm.descr)


def router(rt: Router):
    rt.message.register(get_name, StepsForm.name)
    rt.message.register(get_age, StepsForm.age)
    rt.message.register(get_descr, StepsForm.descr)

    rt.callback_query.register(male, MyCallback.filter(F.call == 'opros'))

    rt.callback_query.register(select_male, MyCallback.filter(F.call.startswith('male_')))
