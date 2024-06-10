from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.markdown import link

from keyboards.inline import MyCallback, one_button


async def start_2(call: CallbackQuery):
    text = '''Мы можем поговорить практически о чем угодно! 

Моя главная цель – дать тебе *поддержку и добрый совет*, когда они наиболее необходимы. Быстро и в любое время!'''

    await call.message.answer_photo(
        photo=FSInputFile('system_files/start_2.jpg'),
        caption=text,
        reply_markup=one_button('Это безопасно?', 'start_3')
    )


async def start_3(call: CallbackQuery):
    link_url = link(title='Политику конфиденциальности',
                    url='https://annabot.craft.me/0S55JuO0P1Rjqi')

    text = f'''🔒 Твои данные защищены, и не передаются третьим лицам. Мой разработчик написал короткую и понятную {link_url}. Продолжая, ты соглашаешься с ней.        

💾 Я храню только 100 последних сообщений нашей переписки, чтобы лучше помнить контекст нашего общения и генерировать отчеты для тебя.'''

    await call.message.answer(text=text,
                              reply_markup=one_button('Хорошо', 'start_4'))


async def start_4(call: CallbackQuery):
    await call.message.answer(
        text='Мы почти закончили – жми Далее 🌟',
        reply_markup=one_button('Далее', 'opros')
    )


def router(rt: Router):
    rt.callback_query.register(start_2, MyCallback.filter(F.call == 'start_2'))
    rt.callback_query.register(start_3, MyCallback.filter(F.call == 'start_3'))
    rt.callback_query.register(start_4, MyCallback.filter(F.call == 'start_4'))
