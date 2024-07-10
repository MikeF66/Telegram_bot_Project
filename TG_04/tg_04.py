import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from deep_translator import GoogleTranslator
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.update_data(my_name=message.from_user.first_name)
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=await kb.builder_keyboard())

@dp.message(F.text == "Привет")
async def hello(message: Message, state: FSMContext):
    await state.update_data(my_name=message.from_user.first_name)
    await message.answer(f'Привет, {message.from_user.first_name}!')

@dp.message(F.text == "Пока")
async def bye(message: Message, state: FSMContext):
    await state.update_data(my_name=message.from_user.first_name)
    await message.answer(f'До свидания, {message.from_user.first_name}!') #reply_markup=kb.reply_keyboard)

@dp.message(Command('link'))
async def link(message: Message):
    await message.answer(f'Доступны следующие ссылки:', reply_markup=kb.inline_keyboard)

@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer(f'Доступны опции', reply_markup=kb.inline_key_board)

@dp.callback_query(F.data == 'show_more')
async def show_more(callback: CallbackQuery):
    await callback.answer('Опции подгружаются')
    await callback.message.edit_text('Доступны следующие опции', reply_markup=kb.in_line_keyboard)

@dp.callback_query(F.data == 'option1')
async def show_more(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    my_name = user_data.get('my_name', 'пользователь')
    await callback.answer('🕦')
    await callback.message.answer(f'{my_name}, это текст опции № 1')

@dp.callback_query(F.data == 'option2')
async def show_more(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    my_name = user_data.get('my_name', 'пользователь')
    await callback.answer('🕦')
    await callback.message.answer(f'{my_name}, это текст опции № 2')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Список команд, которые умеет выполнять этот бот, вы можете открыть в меню.'
                         '\n\nОн умеет выполнять следующие команды:\n '
                         '/start  - приветствие\n '
                         '/help  - список команд \n '
                         '/city и название города  - узнать погоду в этом городе \n'
                         '/en и текст - перевод текста на английский язык \n'
                         '/ru и текст на любом языке - перевод текста на русский \n'
                         '$photo  - можно отправить мне свое фото')


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())