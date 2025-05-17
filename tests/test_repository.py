import pytest
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../python-bot')))
from data import TaskRepository
from datetime import datetime, timedelta
import pytest
import httpx
from httpx import Response, Request
from datetime import datetime, timedelta, UTC

@pytest.mark.asyncio
async def test_add_and_get_task_mocked():

    def mock_send(request: Request):
        if request.url.path == "/tasks" and request.method == "POST":
            return Response(200, json={"id": 1})

        elif request.url.path == "/tasks" and request.method == "GET":
            params = dict(request.url.params)
            if params.get("user_id") == "12345" and params.get("day"):
                return Response(200, json=[
                    {"id": 1, "text": "Test task from pytest", "notify_at": "2025-05-17T10:00:00Z"}
                ])

        return Response(404)


    transport = httpx.MockTransport(mock_send)
    client = httpx.AsyncClient(transport=transport, base_url="http://localhost:8080")

    repo = TaskRepository("http://localhost:8080")
    repo.client = client

    task_text = "Test task from pytest"
    user_id = 12345
    notify_time = datetime.now(UTC) + timedelta(minutes=5)

    task_id = await repo.add_task(user_id, task_text, notify_at=notify_time)
    assert task_id == 1

    tasks = await repo.get_all_user_tasks(user_id)
    assert any(task_text in str(t) for t in tasks)

    await client.aclose()
