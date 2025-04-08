from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="📝 Список дел на сегодня", callback_data="get_todolist"),
     InlineKeyboardButton(text="⏱️ Список невыполненных задач", callback_data="get_old_tasks")],
    [InlineKeyboardButton(text="📤 Добавить задачу", callback_data="add_task"),
     InlineKeyboardButton(text="🗑 Удалить задачу", callback_data="delete_task")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
#iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
