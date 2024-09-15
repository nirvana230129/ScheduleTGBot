import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

with open('token.txt', 'r') as file:
    TOKEN = file.read()


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('\n\n===START' + '=' * 163)
    asyncio.run(main())
