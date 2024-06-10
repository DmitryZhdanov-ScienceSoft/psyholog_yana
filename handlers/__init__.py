from . import (
    start,
    openai,
    buy,
    text_messages,
    opros,
    info
)
from aiogram import Dispatcher, Router


def register_routers(rt: Router):
    start.router(rt)
    info.router(rt)
    opros.router(rt)
    text_messages.router(rt)
    buy.router(rt)

    openai.router(rt)
