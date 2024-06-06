import asyncio
import logging

from aiogram import Bot
from peewee import PostgresqlDatabase, SqliteDatabase

from bot.handlers import get_handlers_router
from bot.middlewares import register_middlewares
from brok import broker, redis_source, scheduler

from data import config
from loader import dp, bot

if config.DB_USER and config.DB_PASSWORD and config.DB_HOST and config.DB_PORT and config.DB_NAME:
    database = PostgresqlDatabase(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                                  host=config.DB_HOST, port=config.DB_PORT)
else:
    database = SqliteDatabase(f'{config.DIR}/database.sqlite3')


# Taskiq calls this function when starting the worker.
@dp.startup()
async def setup_taskiq(bot: Bot, *_args, **_kwargs):
    # Here we check if it's a clien-side,
    # Because otherwise you're going to
    # create infinite loop of startup events.
    if not broker.is_worker_process:
        logging.info("Setting up broker taskiq")
        await scheduler.startup()


# Taskiq calls this function when shutting down the worker.
@dp.shutdown()
async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
    if not broker.is_worker_process:
        logging.info("Shutting down broker taskiq")
        await scheduler.shutdown()


# Запуск бота
async def main():
    dp.include_router(get_handlers_router())
    register_middlewares(dp)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
