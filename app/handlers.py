from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from datetime import datetime, timedelta

import app.keyboards as kbs
from schedule import Schedule

router = Router()


class Register(StatesGroup):
    date = State()
    teacher_name = State()


# schedule = Schedule("data/schedule.ics")
schedule = Schedule("data/schedule.txt")


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=kbs.main)


@router.message(F.text.lower().strip().in_(['расписание на сегодня']))
async def schedule_for_today(message: types.Message):
    date = datetime.today().date()
    intro = f'Расписание на сегодня ({date.strftime("%A, %d %B")}):\n'
    await message.answer(intro + (''.join(str(event) for event in schedule.get_schedule_by_date(date)) or "Пар нет!"))


@router.message(F.text.lower().strip().in_(['расписание на завтра']))
async def schedule_for_tomorrow(message: types.Message):
    date = datetime.today().date() + timedelta(days=1)
    intro = f'Расписание на завтра ({date.strftime("%A, %d %B")}):\n'
    await message.answer(intro + (''.join(str(event) for event in schedule.get_schedule_by_date(date)) or "Пар нет!"))


@router.message(F.text.lower().strip().in_(['расписание на другую дату']))
async def schedule_by_date(message: types.Message, state: FSMContext):
    await state.set_state(Register.date)
    await message.answer(text='Введите дату в формате dd.mm')


@router.message(Register.date)
async def register_date(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()

    date = datetime.strptime(f"{data['date']}.{datetime.today().year}", "%d.%m.%Y").date()
    intro = f'Расписание на {date.strftime("%A, %d %B")}:\n'
    await message.answer(intro + (''.join(str(event) for event in schedule.get_schedule_by_date(date)) or "Пар нет!"))

    await state.clear()

@router.message(F.text.lower().strip().in_(['найти преподавателя']))
async def search_for_teacher(message: types.Message, state: FSMContext):
    await state.set_state(Register.teacher_name)
    await message.answer(text='Введите префикс ФИО преподавателя')


@router.message(Register.teacher_name)
async def register_teacher_name(message: types.Message, state: FSMContext):
    await state.update_data(teacher_name=message.text)
    data = await state.get_data()
    teacher_name = data['teacher_name']
    await state.clear()

    teacher = schedule.get_teacher(teacher_name)
    if teacher is None:
        await message.answer(f'Преподаватель "{teacher_name}" не найден')
    else:
        if teacher.photo is not None:
            photo = FSInputFile(teacher.photo)
            await message.answer_photo(photo, caption=str(teacher))
        else:
            await message.answer(text=str(teacher))
