from handlers import register_routers
from aiogram import Router, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.updation import updation2


def setup(dp: Dispatcher):
    main_router = Router()
    register_routers(main_router)

    dp.include_router(main_router)


def schedule():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(updation2, trigger='cron', hour=0, minute=0)
    scheduler.start()
