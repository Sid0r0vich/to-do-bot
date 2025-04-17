from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import kb
import text
from states import State
from data import TaskRepository  # <-- этот теперь асинхронный
from utils import get_current_day_num

task_repo = TaskRepository("http://localhost:8080")  # URL Go-сервера
router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(Command("menu"))
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "get_todolist")
async def get_todolist_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.get_todolist)
    await clbck.message.edit_text("Список дел на сегодня")
    tasks = await task_repo.get_all_user_tasks(clbck.from_user.id)

    if tasks:
        formatted = "\n".join(f"▶️ {t}" for t in tasks)
    else:
        formatted = "Текущих задач нет"
    await clbck.message.answer(formatted, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "get_old_tasks")
async def get_old_tasks_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.get_todolist)
    await clbck.message.edit_text("Получить невыполненные задачи")
    tasks = await task_repo.get_old_user_tasks(clbck.from_user.id)

    if tasks:
        formatted = "\n".join(f"❌ {t}" for t in tasks)
    else:
        formatted = "Все задачи выполнены"
    await clbck.message.answer(formatted, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "add_task")
async def add_task_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.waiting_for_task)
    await clbck.message.edit_text("Добавить задачу")
    await clbck.message.answer("Введите текст задачи:", reply_markup=kb.exit_kb)


@router.message(State.waiting_for_task)
async def waiting_task_handler(message: Message, state: FSMContext):
    await task_repo.add_task(message.from_user.id, message.text)
    await message.answer(f"Задача добавлена: {message.text}", reply_markup=kb.exit_kb)
    await state.clear()


@router.callback_query(F.data == "delete_task")
async def delete_task_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.waiting_for_deleting_task)
    await clbck.message.edit_text("Удалить задачу")
    await clbck.message.answer("Введите текст задачи:", reply_markup=kb.exit_kb)


@router.message(State.waiting_for_deleting_task)
async def waiting_for_deleting_task_handler(message: Message, state: FSMContext):
    is_deleted = await task_repo.delete_task(message.from_user.id, message.text)
    if is_deleted:
        await message.answer(f"Задача удалена: {message.text}", reply_markup=kb.exit_kb)
    else:
        await message.answer("Задача не найдена", reply_markup=kb.exit_kb)
    await state.clear()
