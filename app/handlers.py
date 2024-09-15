from aiogram import types, Router
from aiogram.filters import CommandStart

import app.keyboards as kbs

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=kbs.main)
