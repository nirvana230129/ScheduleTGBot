from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Расписание на сегодня')],
                                     [KeyboardButton(text='Расписание на завтра')],
                                     [KeyboardButton(text='Расписание на другую дату')],
                                     [KeyboardButton(text='Найти преподавателя')]],
                           resize_keyboard=True, input_field_placeholder='0_o')
