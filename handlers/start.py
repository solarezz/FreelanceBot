from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from db_handler.db_class import DatabaseManager

dsn = 'dbname=postgres user=postgres password=020722 host=localhost'
db = DatabaseManager()
start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    db.add_user(tgID=message.chat.id, username=message.from_user.username)
    await message.answer('Вы успешно зарегистрированы!')
    db.users()
