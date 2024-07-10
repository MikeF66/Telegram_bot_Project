import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, CAT_API_KEY
from translate import translate, translate_to_en

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_cat_breed():
    url = 'https://api.thecatapi.com/v1/breeds'
    headers = {'x-api-key': CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def cat_image_by_breed(breed_id):
    url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
    headers = {'x-api-key': CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']

def get_breed_info(breed_name):
    breeds = get_cat_breed()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Напиши породу кошки, и я пришлю информацию о ней и фотографию.')

@dp.message()
async def send_cat_info(message: Message):
    breed_name_ru = message.text
    breed_name = translate_to_en(breed_name_ru)
    breed_info = get_breed_info(breed_name)
    if breed_info:
        cat_image_url = cat_image_by_breed(breed_info['id'])
        cat_name = translate(breed_info['name'])
        cat_description = translate(breed_info['description'])
        info = (f"Порода: {cat_name}\n"
                f"Описание: {cat_description}\n"
                f"Продолжительность жизни: {breed_info['life_span']} лет")
        await message.answer_photo(photo=cat_image_url, caption=info)
    else:
        await message.answer('Порода не найдена')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())