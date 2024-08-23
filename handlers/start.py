from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,
)
from aiogram.fsm.context import FSMContext

from create_bot import bot
from db_handler.db_class import Database

db = Database()
start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    orders = await db.orders()

    if orders:
        global kb
        for order in orders:
            keyboard = [
                [
                    InlineKeyboardButton(text=f'Заказ {order[0]}', callback_data=f'select_order_{order[0]}')
                ]
            ]
            kb = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await message.answer("Здравствуйте! Выберите диалог:", reply_markup=kb)
    else:
        await message.answer("Нет доступных заказов.")


@start_router.callback_query(lambda callback: callback.data.startswith('select_order_'))
async def select_order(callback_query: CallbackQuery):
    order_id = callback_query.data.split('_')[2]

    status = await db.status(order_id)

    if status and status[0] == 'Ожидание':
        global start_dialog
        keyboard = [
            [
                InlineKeyboardButton(text="Начать диалог", callback_data=f'start_dialog_{order_id}')
            ]
        ]
        start_dialog = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await bot.send_message(callback_query.from_user.id, "Необходимо начать диалог по этому заказу.",
                               reply_markup=start_dialog)
    else:
        await bot.send_message(callback_query.from_user.id, "Заказ уже активен.")


@start_router.callback_query(lambda callback: callback.data.startswith('start_dialog_'))
async def start_dialog(callback_query: CallbackQuery):
    order_id = callback_query.data.split('_')[2]

    participants = await db.participants(order_id=order_id)

    if participants:
        customer_id, executor_id = participants

        try:
            await bot.send_message(executor_id, "Диалог начат")
            await db.change(order_id)
            await bot.send_message(callback_query.from_user.id, "Диалог успешно начат.")
        except Exception as e:
            await bot.send_message(callback_query.from_user.id,
                                   "Пользователь ранее не писал сообщения боту. Ожидайте.")
    else:
        await bot.send_message(callback_query.from_user.id, "Ошибка: участники не найдены.")
