import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from db_handler.db_class import DatabaseManager

DATABASE_URL = 'dbname=users user=postgres password=020722 host=localhost'
db = DatabaseManager()


async def main():
    db.connect()
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
