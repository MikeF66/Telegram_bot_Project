# Задание 1: Создание простого меню с кнопками
# При отправке команды /start бот будет показывать меню с кнопками "Привет" и "Пока".
# При нажатии на кнопку "Привет" бот должен отвечать "Привет, {имя пользователя}!", а при
# нажатии на кнопку "Пока" бот должен отвечать "До свидания, {имя пользователя}!".

# Задание 2: Кнопки с URL-ссылками
# При отправке команды /links бот будет показывать инлайн-кнопки с URL-ссылками.
# Создайте три кнопки с ссылками на новости/музыку/видео


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# rekey = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Привет')],
#     [KeyboardButton(text='Пока')]
# ], resize_keyboard=True)
#
# reply_keyboard = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Привет'), KeyboardButton(text='Пока')]
# ], resize_keyboard=True)

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Новости', url="https://dzen.ru/news")],
    [InlineKeyboardButton(text='Музыка', url="https://top-radio.ru/web/dorozhnoe")],
    [InlineKeyboardButton(text='Видео', url="https://youtu.be/CPrNzB3lJ1g")]
])

key_list = ['Привет', 'Пока', '/link', '/dynamic']
async def builder_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in key_list:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)

inline_key_board = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать больше', callback_data="show_more")]])

in_line_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Опция 1', callback_data="option1")],
    [InlineKeyboardButton(text='Опция 2', callback_data="option2")]
])