import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, EXCHANGE_RATES_API_KEY
import requests
import sqlite3
import random
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

button_register = KeyboardButton(text='Регистрация в телеграм-боте')
button_exchange_rates = KeyboardButton(text='Курс валют')
button_tips = KeyboardButton(text='Советы по экономии')
button_finances = KeyboardButton(text='Личные финансы')

keyboard = ReplyKeyboardMarkup(keyboard=[
    [button_register, button_exchange_rates],
    [button_tips, button_finances]
], resize_keyboard=True)

conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    name TEXT,
    category1 TEXT,
    category2 TEXT,
    category3 TEXT,
    expenses1 REAL,
    expenses2 REAL,
    expenses3 REAL)
''')
conn.commit()
class FinancesForm(StatesGroup):
    category1 = State()
    category2 = State()
    category3 = State()
    expenses1 = State()
    expenses2 = State()
    expenses3 = State()

@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await state.update_data(my_name=message.from_user.first_name)
    await message.answer(f'Привет, {message.from_user.first_name}! Я твой личный финансовый '
                         f'помошник. Выбери одну из опций в меню', reply_markup=keyboard)

@dp.message(F.text =='Регистрация в телеграм-боте')
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cursor.fetchone()
    if user:
        await message.answer('Вы уже зарегистрированы!')
    else:
        cursor.execute('''
        INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer('Вы успешно зарегистрировались!')

@dp.message(F.text == 'Курс валют')
async def exchange_rates(message: Message):
    url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATES_API_KEY}/latest/USD'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer('Не удалось получить данные о курсе валют!')
            return
        usd_to_rub = data['conversion_rates']['RUB']
        usd_to_eur = data['conversion_rates']['EUR']
        euro_to_rub = usd_to_rub / usd_to_eur
        print(f'usd_to_eur = {usd_to_eur}')
        await message.answer(f'1 USD - {usd_to_rub:.2f} RUB\n'
                             f'1 EUR - {euro_to_rub:.2f} RUB')
    except:
        await message.answer('Произошла ошибка')

@dp.message(F.text == 'Советы по экономии')
async def exchange_rates(message: Message):
    tips = [
    'Планируйте свои доходы и расходы. Записывайте все траты и анализируйте их в конце месяца. Это поможет лучше понять, куда уходят деньги и где можно сэкономить.',
    'Определите краткосрочные и долгосрочные цели, такие как покупка жилья, отпуск или образование детей. Это поможет сосредоточиться на экономии и избегать необдуманных расходов.',
    'Создавайте списки покупок перед походом в магазин и придерживайтесь их. Это поможет избежать импульсивных покупок.',
    'Следите за распродажами, акциями и скидками. Многие магазины предлагают выгодные предложения, которыми можно воспользоваться.',
    'Сократите расходы на развлечения: Вместо дорогих кинотеатров и ресторанов, выбирайте более бюджетные варианты отдыха, такие как пикники, прогулки или просмотр фильмов дома.',
    'Готовьте еду дома: Питание вне дома может сильно ударить по бюджету. Готовьте еду дома и берите с собой обеды на работу. Это не только экономит деньги, но и позволяет контролировать качество и калорийность пищи.',
    'Используйте общественный транспорт: Если у вас есть возможность, пользуйтесь общественным транспортом вместо личного автомобиля. Это поможет сократить расходы на топливо, парковку и обслуживание машины.',
    'Сравнивайте цены: Перед крупными покупками сравнивайте цены в разных магазинах и выбирайте наиболее выгодные предложения. Интернет-магазины часто предлагают более низкие цены, чем офлайн.',
    'Энергосбережение: Сократите расходы на коммунальные услуги, используя энергосберегающие лампы, отключая электроприборы, если они не используются, и уменьшая температуру отопления на ночь.',
    'Откажитесь от ненужных подписок: Проверьте свои подписки на различные сервисы и откажитесь от тех, которыми вы не пользуетесь или которые не приносят вам реальной пользы.'
]
    tip = random.choice(tips)
    await message.answer(tip)

@dp.message(F.text == 'Личные финансы')
async def finances(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply('Введите наименование первой категории расходов')

@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.reply('Введите расходы для первой категории')

@dp.message(FinancesForm.expenses1)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.reply('Введите наименование второй категории расходов')

@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply('Введите расходы для второй категории')

@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.reply('Введите наименование третьей категории расходов')

@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply('Введите расходы для третьей категории')

@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
    data = await state.get_data()
    telegram_id = message.from_user.id
    cursor.execute('''UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, 
    expenses3 = ? WHERE telegram_id = ?''', (data['category1'], data['expenses1'], data['category2'],
                                             data['expenses2'], data['category3'], float(message.text), telegram_id))
    conn.commit()
    await state.clear()
    await message.answer('Категории и расходы сохранены')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())