from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    call: str


BACK_TO_START = {'inline_keyboard': [
    [
        {'text': '🏠 В меню', 'callback_data': MyCallback(call='back_to_start').pack()},
    ],
]}

MENU = {'inline_keyboard': [
    [
        {'text': 'Психолог', 'callback_data': MyCallback(call='openai').pack()},
    ],
    [
        {'text': '💵 Купить подписку', 'callback_data': MyCallback(call='buy2s').pack()},
    ],
]}

MENU_TARIFS = {'inline_keyboard': [
    [
        {'text': '💰 199₽ - 1 месяц', 'callback_data': MyCallback(call='buyss_199').pack()},
    ],
    [
        {'text': '🔥 1199₽ - 1 год', 'callback_data': MyCallback(call='buyss_1199').pack()},
    ],
    [
        {'text': '♾️ 9999₽ - Навсегда', 'callback_data': MyCallback(call='buyss_9999').pack()},
    ],
    [
        {'text': '🏠 В меню', 'callback_data': MyCallback(call='back_to_start').pack()},
    ],
]}


def payment(callback):
    return {'inline_keyboard': [
        [
            {'text': '💸 Купить', 'callback_data': MyCallback(call=f'buy_{callback}').pack()},
        ],
        [
            {'text': '🔙 Назад', 'callback_data': MyCallback(call='buy2_subscribe').pack()},
        ],
    ]}


def one_button(name, callback):
    return {'inline_keyboard': [
        [
            {'text': name, 'callback_data': MyCallback(call=callback).pack()},
        ],
    ]}


SELECT_MALE = {'inline_keyboard': [
    [
        {'text': 'Я женщина', 'callback_data': MyCallback(call='male_Женщина').pack()},
        {'text': 'Я мужчина', 'callback_data': MyCallback(call='male_Мужчина').pack()},
    ],
    [
        {'text': 'Пропустить', 'callback_data': MyCallback(call='openai').pack()},
    ],
]}

INFO_MENU = {'inline_keyboard': [
    [
        {'text': 'Изменить анкету', 'callback_data': MyCallback(call='opros').pack()},
        {'text': 'Отменить', 'callback_data': MyCallback(call='openai').pack()},
    ],
]}

BUY_MENU = {'inline_keyboard': [
    [
        {'text': '1 месяц - 990₽', 'callback_data': MyCallback(call='buy_1 месяц_990').pack()},
    ],
    [
        {'text': '3 месяца - 2500₽', 'callback_data': MyCallback(call='buy_3 месяца_2500').pack()},
    ],
    [
        {'text': '6 месяцев - 4500₽', 'callback_data': MyCallback(call='buy_6 месяцев_4500').pack()},
    ],
    [
        {'text': 'Скрыть', 'callback_data': MyCallback(call='delete').pack()},
    ],
]}


def upload_payment(name):
    bth1 = InlineKeyboardButton(text='💳 ЮMoney', callback_data=MyCallback(call=f'yoo_{name}').pack())
    bth2 = InlineKeyboardButton(text='🪙 CryptoPay', callback_data=MyCallback(call=f'crypto_{name}').pack())

    markup = InlineKeyboardMarkup(inline_keyboard=[[bth1], [bth2]])

    return markup


def payload_markup(url, call):
    bth1 = InlineKeyboardButton(text='💸 Оплатить',
                                      url=url)
    bth2 = InlineKeyboardButton(text='💵 Оплатить в приложении',
                                      web_app=WebAppInfo(url=url))
    bth3 = InlineKeyboardButton(text='✅ Оплачено',
                                      callback_data=MyCallback(call=call).pack())

    markup = InlineKeyboardMarkup(inline_keyboard=[[bth1], [bth2], [bth3]])

    return markup


def pay(url, id, name, price):
    bth1 = InlineKeyboardButton(text='💵 Оплатить', url=url)
    bth2 = InlineKeyboardButton(text='✅ Оплатил', callback_data=MyCallback(call=f"chent_{id}_{name}").pack())

    markup = InlineKeyboardMarkup(inline_keyboard=[[bth1], [bth2]])

    return markup
