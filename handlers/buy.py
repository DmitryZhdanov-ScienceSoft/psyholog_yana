import asyncio
import requests

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile, LabeledPrice, PreCheckoutQuery
from aiogram.utils.markdown import link
from crypto_pay_api_sdk import cryptopay
from yoomoney import Quickpay, Client

from config import BOT_NAMING, CRYPTO_TOKEN, YOOMONEY_TOKEN, RECEIVER
from database import Database
from keyboards.inline import MyCallback, BUY_MENU, BACK_TO_START, upload_payment, payload_markup, pay

db = Database()
Crypto = cryptopay.Crypto(token=CRYPTO_TOKEN)

sroki = {
    '1 месяц': 30,
    '3 месяца': 90,
    '6 месяцев': 180
}

timetosleep = {
    30: 2592000,
    90: 7776000,
    180: 15552000
}


async def main_menu(message: Message, bot: Bot):
    await bot.send_chat_action(message.chat.id, 'typing')

    text = '''
`Доступ к Яна Premium`

⏳ `До 2 часов общения в день   `  
🗯 `Голосовые ответы   `  
🌐 `Онлайн 24/7, днем и ночью    ` 
😎 `Самая продвинутая нейросеть `    
    
😊 `Максимальная поддержка, качественные и подробные ответы`
💸 `Тариф на 1 месяц дешевле 1 сессии у человека-психолога`
'''

    await message.answer_photo(photo=FSInputFile(f'system_files/premium.jpg'),
                               caption=text, reply_markup=BUY_MENU)


async def buy(call: CallbackQuery, callback_data: MyCallback):
    name_of_subscribe = callback_data.call.split('_')[1]
    price = callback_data.call.split('_')[2]

    srok = sroki[name_of_subscribe]

    text = f'''
К оплате: 
*{price} рублей 🇷🇺 картой.*   

Срок действия: *{srok} дней*. 
Доступно вопросов и ответов: *100 в день* = 2 часа общения каждый день.        
    
💳 Выберите *ЮMoney*, если хотите *оплатить картой*.
🪙 Если хотите *оплатить криптовалютой*, то нажмите *СryptoPay*.'''

    await call.message.answer(text=text,
                              reply_markup=upload_payment(f'{name_of_subscribe}_{price}'))


async def pay_yoomoney(call: CallbackQuery, callback_data: MyCallback):
    await call.message.delete()

    price = int(callback_data.call.split('_')[2])
    name = callback_data.call.split('_')[1]

    user_id = call.message.chat.id
    order_id = db.select_order_id(user_id=user_id) + 1
    db.update_order_id(user_id=user_id, order_id=order_id)

    callbk = f'oplata_{name}_{price}_{order_id}'

    quickpay = Quickpay(
        receiver=RECEIVER,
        quickpay_form="shop",
        targets=f"{BOT_NAMING} | Оплата тарифа на {name}",
        paymentType="SB",
        sum=price,
        label=callbk
    )

    text = f'''Ваш заказ: *{BOT_NAMING} |  Оплата тарифа на {name}*

Статус: Создан
🔐 Цена: *{price}₽*

_‼️После оплаты нажмите на кнопку_ *✅ Оплачено* _для проверки_'''

    await call.message.answer(text=text,
                                    reply_markup=payload_markup(url=quickpay.redirected_url,
                                                                call=callbk))


async def successful_payment(call: CallbackQuery, bot: Bot, callback_data: MyCallback):
    callback = callback_data.call

    if callback.startswith('oplata_'):
        callback_data = callback.split('_')

        name = callback_data[1]

        client = Client(YOOMONEY_TOKEN)

        history = client.operation_history(label=callback)

        if not history.operations:
            text = '''К сожалению, оплата не поступила

Попробуйте снова или обратитесь в поддержку, если вы уже оплатили, а данное окно остается'''

            await call.answer(text,
                              show_alert=True)
        else:
            await call.message.delete()
            user_id = call.message.chat.id

            text = '💵 Ваш платеж успешно зачислен!\n\n⌛️ *Подождите, вам начисляется тариф...*'

            msg = await call.message.answer(text)

            await bot.send_chat_action(call.message.chat.id, 'typing')

            db.update_buying_usage(user_id, 100, 1)

            text = f'''
🚀 *Ура! Ваша подписка уже ждет вас на аккаунте!*
'''

            srok = sroki[name]
            time_to_sleep = timetosleep[srok]

            await msg.edit_text(text,
                                reply_markup=BACK_TO_START)

            await asyncio.sleep(time_to_sleep)

            db.update_buying_usage(user_id, 20, 0)

            await call.message.answer('''🪫 *Упс, срок действия вашего тарифа подошел к концу*

💳 Купите доступ к тарифу, чтобы пользоваться ботом без ограничений!''',
                                      reply_markup=BUY_MENU)


async def cryptopay(call: CallbackQuery, callback_data: MyCallback):
    await call.message.delete()

    callback = callback_data.call

    crypto_name = 'tether'

    price = int(callback.split('_')[2])
    name = callback.split('_')[1]

    data = float(requests.get(f'https://api.coingecko.com/api/v3/coins/{crypto_name}').json()['market_data']['current_price']['rub'])

    price2 = float(price) / data

    text = f'''
💸 *Вы оплачиваете тариф Premium на {name}*

Сумма к оплате: *{price2}USDT* ≈ {price}₽

_Для совершения оплаты перейдите по ссылке ниже_
'''

    user_id = call.message.chat.id

    order_id = db.select_order_id(user_id=user_id) + 1
    db.update_order_id(user_id=user_id, order_id=order_id)

    payload = Crypto.createInvoice(asset="USDT", amount=str(price2),
                               params={
                                    "paid_bth_url": f"https://t.me/{BOT_NAMING}/"
                               })

    url_pay = payload['result']['pay_url']
    id = payload['result']['invoice_id']

    await call.message.answer(text=text, reply_markup=pay(url_pay, id, name, price))


async def check_pay(call: CallbackQuery, callback_data: MyCallback, bot: Bot):
    order_id = callback_data.call.split('_')[1]

    invoice = Crypto.getInvoices(params={'id': order_id})

    status = invoice['result']['items'][0]['status']

    if status == 'active':
        text = '''К сожалению, оплата не поступила

Попробуйте снова или обратитесь в поддержку, если вы уже оплатили, а данное окно остается'''

        await call.answer(text,
                          show_alert=True)

    else:
        name = callback_data.call.split('_')[2]

        message = call.message

        user_id = message.chat.id

        text = '💵 Ваш платеж успешно зачислен!\n\n⌛️ *Подождите, вам начисляется пакет...*'

        msg = await message.answer(text)

        await bot.send_chat_action(message.chat.id, 'typing')

        db.update_buying_usage(user_id, 100, 1)

        text = f'''
🚀 *Ура! Ваша подписка уже ждет вас на аккаунте!*
        '''

        srok = sroki[name]
        time_to_sleep = timetosleep[srok]

        await msg.edit_text(text,
                            reply_markup=BACK_TO_START)

        await asyncio.sleep(time_to_sleep)

        db.update_buying_usage(user_id, 20, 0)

        await call.message.answer('''🪫 *Упс, срок действия вашего тарифа подошел к концу*

💳 Купите доступ к тарифу, чтобы пользоваться ботом без ограничений!''',
                                  reply_markup=BUY_MENU)


async def delete(call: CallbackQuery):
    await call.message.delete()


def router(rt: Router):
    rt.message.register(main_menu, F.text == '/pay')

    rt.callback_query.register(buy, MyCallback.filter(F.call.startswith('buy_')))

    rt.callback_query.register(pay_yoomoney, MyCallback.filter(F.call.startswith('yoo_')))

    rt.callback_query.register(cryptopay, MyCallback.filter(F.call.startswith('crypto_')))
    rt.callback_query.register(check_pay, MyCallback.filter(F.call.startswith('chent_')))

    rt.callback_query.register(successful_payment, MyCallback.filter(F.call.startswith('oplata_')))

    rt.callback_query.register(delete, MyCallback.filter(F.call == 'delete'))
