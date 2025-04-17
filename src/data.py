import sqlite3
from sqlite3 import Error
# data/task_repository.py
import httpx
from utils import get_current_day_num

class TaskRepository:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def add_task(self, user_id: int, task_text: str, day: int = None) -> int:
        if day is None:
            day = get_current_day_num()
        payload = {
            "user_id": user_id,
            "text": task_text,
            "day": day
        }
        resp = await self.client.post(f"{self.base_url}/tasks", json=payload)
        resp.raise_for_status()
        return resp.json()["id"]

    async def delete_task(self, user_id: int, task_text: str) -> bool:
        return False

    async def get_all_user_tasks(self, user_id: int, day: int = None) -> list[str]:
        if day is None:
            day = get_current_day_num()
        resp = await self.client.get(f"{self.base_url}/tasks", params={"user_id": user_id, "day": day})
        resp.raise_for_status()
        return [task["text"] for task in resp.json()]

    async def get_old_user_tasks(self, user_id: int, day: int = None) -> list[str]:
        if day is None:
            day = get_current_day_num()
        resp = await self.client.get(f"{self.base_url}/tasks/old", params={"user_id": user_id, "day": day})
        resp.raise_for_status()
        return [task["text"] for task in resp.json()]


todolist = [
    "Сделать домашнее задание по виртуализации",
    "Погулять с собакой"
]
