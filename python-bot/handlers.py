from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import re
from datetime import datetime

import kb
import text
from states import State
from data import TaskRepository

task_repo = TaskRepository("http://localhost:8080")
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
    await state.update_data(task_text=message.text)
    await message.answer(
        f"📌 Задача: <b>{message.text}</b>\n\n" +
        text.ask_notification,
        reply_markup=kb.notification_kb,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "skip_notification")
async def skip_notification_handler(clbck: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_text = user_data.get("task_text")

    await task_repo.add_task(clbck.from_user.id, task_text)
    await clbck.message.answer(f"Задача добавлена: {task_text}", reply_markup=kb.exit_kb)
    await state.clear()


@router.callback_query(F.data == "add_notification")
async def add_notification_handler(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(State.waiting_for_date)
    await clbck.message.answer(text.enter_date, reply_markup=kb.exit_kb)


@router.message(State.waiting_for_date)
async def waiting_for_date_handler(message: Message, state: FSMContext):
    if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", message.text):
        await message.answer(text.invalid_date_format, reply_markup=kb.exit_kb)
        return

    await state.update_data(notification_date=message.text)
    await state.set_state(State.waiting_for_time)
    await message.answer(text.enter_time, reply_markup=kb.exit_kb)


@router.message(State.waiting_for_time)
async def waiting_for_time_handler(message: Message, state: FSMContext):
    if not re.match(r"^\d{2}:\d{2}$", message.text):
        await message.answer(text.invalid_time_format, reply_markup=kb.exit_kb)
        return

    user_data = await state.get_data()
    task_text = user_data.get("task_text")
    date_str = user_data.get("notification_date")

    try:
        notification_datetime = datetime.strptime(f"{date_str} {message.text}", "%d.%m.%Y %H:%M")
        await state.update_data(notification_time=message.text, notification_datetime=notification_datetime)

        await state.set_state(State.waiting_for_confirmation)
        confirmation_message = f"Задача: {task_text}\nУведомление: {date_str} в {message.text}\n\nПодтвердите создание задачи:"
        await message.answer(confirmation_message, reply_markup=kb.confirm_kb)
    except ValueError:
        await message.answer("Введена некорректная дата или время. Пожалуйста, попробуйте снова.",
                             reply_markup=kb.exit_kb)
        await state.set_state(State.waiting_for_date)
        await message.answer(text.enter_date)


@router.callback_query(F.data == "confirm_notification")
async def confirm_notification_handler(clbck: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_text = user_data.get("task_text")
    notification_date = user_data.get("notification_date")
    notification_time = user_data.get("notification_time")
    notification_datetime = user_data.get("notification_datetime")

    await task_repo.add_task(clbck.from_user.id, task_text, notify_at=notification_datetime)

    await clbck.message.answer(
        text.notification_scheduled.format(
            task=task_text,
            date=notification_date,
            time=notification_time
        ),
        reply_markup=kb.exit_kb
    )
    await state.clear()


@router.callback_query(F.data == "cancel_notification")
async def cancel_notification_handler(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Создание задачи с уведомлением отменено.", reply_markup=kb.exit_kb)
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
