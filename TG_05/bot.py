import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, CAT_API_KEY, CALENDAR_API_KEY
from translate import translate

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_holidays(country, year):
    url = f'https://calendarific.com/api/v2/holidays?&api_key={CALENDAR_API_KEY}&country={country}&year={year}'
    response = requests.get(url)
    return response.json()

def get_list(country, year):
    error = ''
    holidays = get_holidays(country, year)
    holiday_list = []
    if 'response' in holidays and 'holidays' in holidays['response']:
        for holiday in holidays['response']['holidays']:
            name = translate(holiday['name'])
            date = translate(holiday['date']['iso'])
            description = translate(holiday['description'])
            holiday = f'Праздник: {name}\nДата: {date}\nОписание: {description}\n\n'
            holiday_list.append(holiday)
    else:
        error = "Нет доступных данных о праздниках."
    return holiday_list, error

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Введи страну и год, а я напишу '
                         f'все праздники в этой стране в этом году.')

@dp.message()
async def handle_message(message: types.Message):
    try:
        country, year = message.text.split(',') # Разделяем введенный текст по запятой
        country = country.strip() # Удаляем лишние пробелы в начале и конце строк
        year = year.strip()
        holiday_list, error = get_list(country, year)  # Исправлено на правильную функцию
        if holiday_list:
            for holiday in holiday_list:
                await message.answer(holiday)
        else:
            await message.answer(error)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())