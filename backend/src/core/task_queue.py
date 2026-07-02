from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC
from typing import Any

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings


class TaskQueue(ABC):
    @abstractmethod
    async def enqueue(self, task_type: str, payload: dict[str, Any]) -> str:
        ...

    @abstractmethod
    async def get_status(self, task_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    async def cancel(self, task_id: str) -> bool:
        ...

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        ...


class APSchedulerQueue(TaskQueue):
    def __init__(self):
        jobstores = {"default": SQLAlchemyJobStore(url=settings.DATABASE_URL.replace("+aiosqlite", ""))}
        self._scheduler = AsyncIOScheduler(jobstores=jobstores)
        self._running = False

    async def enqueue(self, task_type: str, payload: dict[str, Any]) -> str:
        from datetime import datetime

        job = self._scheduler.add_job(
            func=payload.get("_func"),
            trigger="date",
            run_date=datetime.now(UTC),
            kwargs=payload,
        )
        return job.id

    async def get_status(self, task_id: str) -> dict[str, Any]:
        job = self._scheduler.get_job(task_id)
        if not job:
            return {"status": "not_found"}
        return {"status": "pending", "next_run": str(job.next_run_time)}

    async def cancel(self, task_id: str) -> bool:
        job = self._scheduler.get_job(task_id)
        if job:
            self._scheduler.remove_job(task_id)
            return True
        return False

    async def start(self) -> None:
        if not self._running:
            self._scheduler.start()
            self._running = True

    async def shutdown(self) -> None:
        if self._running:
            self._scheduler.shutdown(wait=False)
            self._running = False

    @property
    def scheduler(self) -> AsyncIOScheduler:
        return self._scheduler
