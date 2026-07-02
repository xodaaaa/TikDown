from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseNotifier(ABC):
    name: str = "base"

    @abstractmethod
    async def send(self, event: dict[str, Any]) -> bool:
        ...


class NotificationRegistry:
    _notifiers: dict[str, type[BaseNotifier]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(notifier_cls: type[BaseNotifier]):
            cls._notifiers[name] = notifier_cls
            return notifier_cls
        return decorator

    @classmethod
    def get(cls, name: str) -> type[BaseNotifier] | None:
        return cls._notifiers.get(name)

    @classmethod
    def list(cls) -> list[str]:
        return list(cls._notifiers.keys())
