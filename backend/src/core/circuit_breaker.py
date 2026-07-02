from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from src.config import settings


class CircuitBreaker:
    def __init__(
        self,
        account_id: str,
        max_failures: int | None = None,
        on_open: Callable[[str], Awaitable[None]] | None = None,
    ):
        self.account_id = account_id
        self.max_failures = max_failures or settings.MAX_CONSECUTIVE_FAILURES
        self.failure_count = 0
        self.is_open = False
        self.on_open = on_open

    def record_success(self) -> None:
        self.failure_count = 0
        self.is_open = False

    def record_failure(self) -> None:
        self.failure_count += 1
        if self.failure_count >= self.max_failures:
            self.is_open = True

    async def call(self, fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
        if self.is_open:
            raise CircuitBreakerOpenError(self.account_id, self.failure_count)
        try:
            result = await fn(*args, **kwargs)
            self.record_success()
            return result
        except Exception:
            self.record_failure()
            if self.is_open and self.on_open:
                await self.on_open(self.account_id)
            raise


class CircuitBreakerOpenError(Exception):
    def __init__(self, account_id: str, failures: int):
        self.account_id = account_id
        self.failures = failures
        super().__init__(f"Circuit breaker open for account {account_id} after {failures} failures")
