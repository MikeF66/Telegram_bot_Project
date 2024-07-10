import asyncio
import random
import re   # импорт из модуля `re` (регулярные выражения) для поиска соответствия определенному шаблону
            # в строке `message.text`
import requests
from gtts import gTTS
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from deep_translator import GoogleTranslator
from config import (TOKEN, WEATHER_API_KEY)
from translate import translate # импорт функции переводчика на русский из файла translate.py

bot = Bot(token=TOKEN)
dp = Dispatcher()


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

# @dp.message(Command('start'))
# async def start(message: Message):
#     await message.answer(f'Привет, {message.from_user.full_name}! Я - бот, который знает прогноз погоды')
def get_weather(city: str, api_key: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# @dp.message(F.text == 'Что такое ИИ?')
# async def ai(message: Message):
#     await message.answer('Искусственный интеллект (ИИ) — это область компьютерной науки, которая занимается '
#                          'созданием систем, способных выполнять задачи, требующие человеческого интеллекта. '
#                          'Такие системы могут включать в себя способность к обучению, распознаванию речи, '
#                          'визуальному восприятию, принятию решений и переводу языков. Основной целью ИИ '
#                          'является создание машин, которые могут выполнять задачи, требующие человеческого разума.')

@dp.message(Command('city'))
async def handle_city_command(message: Message):
    match = re.match(r"/city\s+(.+)", message.text, re.IGNORECASE)
        # re.match(pattern, string, flags=0)  более подробно смотри в уроке
        # - функция `re.match` ищет соответствие шаблону только в начале строки.
        # - `pattern`: Шаблон регулярного выражения - r"/city\s+(.+)"
        # - `string`: Строка, в которой происходит поиск - message.text
        # - `flags`: Дополнительные флаги для изменения поведения поиска - `re.IGNORECASE` для игнорирования регистра)
    if match:
        city_name = match.group(1).strip()
        weather_data = get_weather(city_name, WEATHER_API_KEY)
        if weather_data:
            weather_en = weather_data['weather'][0]['description']
            weather = translate(weather_en)
            temperature = weather_data['main']['temp']
            pressure = weather_data['main']['pressure']
            humidity = weather_data['main']['humidity']
            await message.answer(f"Погода в городе {city_name}:\n{weather}\nТемпература: {temperature}°C\nДавление: {pressure} гПа\nВлажность: {humidity}%")
        else:
            await message.answer("Не удалось получить данные о погоде. Проверьте правильность названия города.")


@dp.message(Command('en'))
async def handle_translate_command(message: Message):
    match = re.match(r"/en\s+(.+)", message.text, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
        translator = GoogleTranslator(source='auto', target='en')
        translated_text = translator.translate(text)
        tts = gTTS(text=translated_text, lang='en-us')
        tts.save('en_trans.ogg')
        await message.answer(translated_text)
        audio = FSInputFile('en_trans.ogg')
        await bot.send_audio(message.chat.id, audio)
        os.remove('en_trans.ogg')
    else:
        await message.answer("Не удалось получить текст для перевода.")

@dp.message(Command('ru'))
async def handle_translate_command(message: Message):
    match = re.match(r"/ru\s+(.+)", message.text, re.IGNORECASE)
    if match:
        text = match.group(1).strip()
        translator = GoogleTranslator(source='auto', target='ru')
        translated_text = translator.translate(text)
        tts = gTTS(text=translated_text, lang='ru')
        tts.save('en_trans.ogg')
        await message.answer(translated_text)
        audio = FSInputFile('en_trans.ogg')
        await bot.send_audio(message.chat.id, audio)
        os.remove('en_trans.ogg')
    else:
        await message.answer("Не удалось получить текст для перевода.")

@dp.message(Command('photo', prefix='$'))
async def got_photo(message: Message):
    list = ['Классная фотка!', 'Скинь еще.', 'Не отправляй мне всякую ерунду!']
    answer = random.choice(list)
    await message.answer(answer)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я - бот, который знает прогноз погоды')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
