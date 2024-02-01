import asyncio
from aiogram import Bot, Dispatcher, types
from config import token, TOKEN
from aiogram.filters import Command
import tink
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
import keyboards
from aiogram import F
bot = Bot(token)
# Диспетчер
dp = Dispatcher()
storage = MemoryStorage()


class New1(StatesGroup):
    name = State()


@dp.message(Command("start"))
async def st(message: types.Message, state: FSMContext):
    await message.answer("Бот запущен",reply_markup=keyboards.keyboard)
    await message.answer(f'Подождите,пока прогрузятся все данные')
    await asyncio.sleep(0.5)
    data = open('2.txt')
    m = message.chat.id
    for i in data:
        i = i.split(' ')

        await bot.send_message(chat_id=m, text=f'тикер: {i[1]} название фирмы: {i[2]}\n', disable_notification=False)
        await asyncio.sleep(0.3)
    await message.answer(f'Напишите в чат интересующий тикер')
    await state.set_state(New1.name)


@dp.message(New1.name)
async def st(call: types.Message, state: FSMContext):
    await state.set_state(New1.name)
    await state.update_data(name=call.text)
    data1 = await state.get_data()
    d = data1['name']
    await call.answer(f'Данные по акции\n{tink.tnk(d)}')
    await state.clear()

@dp.message(F.text.lower() == "заново 🔁")
async def add_item(message: types.Message, state: FSMContext):
    await message.answer("Бот запущен", reply_markup=keyboards.keyboard)
    await message.answer(f'Напишите в чат интересующий тикер')
    await state.set_state(New1.name)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    print("База данных успешно подключена")
