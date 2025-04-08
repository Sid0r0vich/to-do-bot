from aiogram import types, F, Router, flags
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import kb
import text
from states import State
from data import TaskRepository
from utils import get_current_day_num

task_repo = TaskRepository('../tasks.db')
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
    tasks = list(task_repo.get_all_user_tasks(clbck.from_user.id, get_current_day_num()))
    await clbck.message.answer("\n".join(map(lambda str: "▶️ " + str, tasks)) if len(tasks) != 0 else "Текущих задач нет", reply_markup=kb.exit_kb)

@router.callback_query(F.data == "get_old_tasks")
async def get_old_tasks_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.get_todolist)
    await clbck.message.edit_text("Получить невыполненные задачи")
    tasks = list(task_repo.get_old_user_tasks(clbck.from_user.id, get_current_day_num()))
    await clbck.message.answer("\n".join(map(lambda str: "❌ " + str, tasks)) if len(tasks) != 0 else "Все задачи выполнены", reply_markup=kb.exit_kb)

@router.callback_query(F.data == "add_task")
async def add_task_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.waiting_for_task)
    await clbck.message.edit_text("Добавить задачу")
    await clbck.message.answer("Введите текст задачи:", reply_markup=kb.exit_kb)

@router.message(State.waiting_for_task)
async def waiting_task_handler(message: Message, state: FSMContext):
    task_id = task_repo.add_task(message.from_user.id, message.text, get_current_day_num())

    await message.answer("Задача добавлена: " + message.text, reply_markup=kb.exit_kb)
    await state.clear()

@router.callback_query(F.data == "delete_task")
async def delete_task_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.waiting_for_deleting_task)
    await clbck.message.edit_text("Удалить задачу")
    await clbck.message.answer("Введите текст задачи:", reply_markup=kb.exit_kb)

@router.message(State.waiting_for_deleting_task)
async def waiting_for_deleting_task_handler(message: Message, state: FSMContext):
    isDeleted = task_repo.delete_task(message.from_user.id, message.text)
    await message.answer("Задача удалена: " + message.text if isDeleted else "Задача не найдена", reply_markup=kb.exit_kb)
    await state.clear()