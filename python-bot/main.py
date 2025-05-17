import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import text
from data import TaskRepository
from handlers import router
import config

task_repo = TaskRepository("http://go-backend:8080")


async def check_notifications(bot: Bot):
    while True:
        try:
            pending_notifications = await task_repo.get_pending_notifications()

            for notification in pending_notifications:
                user_id = notification.get("user_id")
                task_text = notification.get("text")
                task_id = notification.get("id")

                if user_id and task_text and task_id:
                    notification_message = text.task_notification.format(task=task_text)
                    await bot.send_message(user_id, notification_message)

                    await task_repo.mark_notification_sent(task_id)

                    logging.info(f"Отправлено уведомление пользователю {user_id} о задаче: {task_text}")

        except Exception as e:
            logging.error(f"Ошибка при проверке уведомлений: {e}")

        await asyncio.sleep(30)


async def main():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    asyncio.create_task(check_notifications(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
