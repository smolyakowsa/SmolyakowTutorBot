import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tokens import bot_token
from texts import social_media, courses, info, price, booking, group_booking

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class Form(StatesGroup):
    waiting_for_date = State()
    waiting_for_confirmation = State()
    waiting_for_name = State()
    waiting_for_subject = State()

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Записаться на урок"),
            types.KeyboardButton(text="Групповые занятия")
        ],
        [
            types.KeyboardButton(text="Курсы"),
            types.KeyboardButton(text="Прайс-лист")
        ],
        [
            types.KeyboardButton(text="Соц. сети"),
            types.KeyboardButton(text="Информация")
        ],
        [
            types.KeyboardButton(text="Обратиться лично")
        ]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Выбери интересующий раздел:", reply_markup=keyboard)

@dp.message()
async def handle_text(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    selected_date = None
    selected_time = None

    if message.text == "Записаться на урок":
        await message.answer(booking)
    elif message.text == "Курсы":
        await message.answer(courses)
    elif message.text == "Групповые занятия":
        await message.answer(group_booking)
    elif message.text == "Прайс-лист":
        await message.answer(price)
    elif message.text == "Соц. сети":
        await message.answer(social_media, parse_mode='Markdown')
    elif message.text == "Информация":
        await message.answer(info)
    elif message.text == "Обратиться лично":
        await message.answer("Вы можете обратиться ко мне лично: [@smolyakow_tutor](https://t.me/smolyakow_tutor)",
                             parse_mode='Markdown')
    elif message.text == "Назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=keyboard)

if __name__ == "__main__":
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        print(f"An error occurred: {e}")
