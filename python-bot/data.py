import httpx
from datetime import datetime, timedelta
from utils import get_current_day_num


class TaskRepository:
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = httpx.AsyncClient()

    async def add_task(self, user_id: int, task_text: str, day: int = None, notify_at: datetime = None) -> int:
        if day is None:
            day = get_current_day_num()
        
        payload = {
            "user_id": user_id,
            "text": task_text,
            "day": day
        }

        notify_at = notify_at + timedelta(minutes=1)
        
        if notify_at:
            payload["notify_at"] = notify_at.isoformat() + "Z"
            payload["has_notification"] = True
            
        resp = await self.client.post(f"{self.base_url}/tasks", json=payload)
        resp.raise_for_status()
        return resp.json()["id"]

    async def delete_task(self, user_id: int, task_text: str) -> bool:
        # TODO
        return False

    async def get_all_user_tasks(self, user_id: int, day: int = None) -> list[str]:
        if day is None:
            day = get_current_day_num()
        resp = await self.client.get(f"{self.base_url}/tasks", params={"user_id": user_id, "day": day})
        resp.raise_for_status()
        tasks = []
        for task in resp.json():
            task_text = task["text"]
            if task.get("has_notification", False) and "notify_at" in task:
                notify_time = datetime.fromisoformat(task["notify_at"].replace('Z', '+00:00'))
                formatted_time = notify_time.strftime("%d.%m.%Y %H:%M")
                task_text = f"{task_text} 🔔 {formatted_time}"
            tasks.append(task_text)
        return tasks

    async def get_old_user_tasks(self, user_id: int, day: int = None) -> list[str]:
        # TODO
        return []
    
    async def get_pending_notifications(self) -> list[dict]:
        try:
            resp = await self.client.get(f"{self.base_url}/notifications/pending")
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Ошибка при получении ожидающих уведомлений: {e}")
            return []
    
    async def mark_notification_sent(self, task_id: int) -> bool:
        try:
            resp = await self.client.post(f"{self.base_url}/notifications/{task_id}/mark-sent")
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"Ошибка при отметке уведомления как отправленного: {e}")
            return False