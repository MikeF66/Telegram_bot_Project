import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config import TOKEN
import sqlite3

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()


init_db()


@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Добрый день! Как вас зовут?\nНапишите фамилию и имя')
    await state.set_state(Form.name)


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько вам лет?\nВведите числовое значение')
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Из какой вы группы?\nУкажите название вашей группы')
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    student_data = await state.get_data()
    print(student_data)

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (student_data['name'], student_data['age'], student_data['grade']))
    conn.commit()

    # Получение списка студентов из группы
    cur.execute('''
    SELECT name, age FROM students WHERE grade = ?''', (student_data['grade'],))
    students = cur.fetchall()
    conn.close()

    # Формирование сообщения со списком студентов
    if students:
        students_message = 'Список студентов группы {}:\n'.format(student_data['grade'])
        for name, age in students:
            students_message += 'Имя: {}, Возраст: {}\n'.format(name, age)
    else:
        students_message = 'В группе {} пока нет студентов.'.format(student_data['grade'])

    await message.answer(students_message)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())