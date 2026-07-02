from __future__ import annotations

import asyncio
from typing import Any

from src.config import settings
from src.core.notifications.base import BaseNotifier
from src.core.notifications.discord import DiscordNotifier
from src.core.notifications.generic_webhook import GenericWebhookNotifier
from src.core.notifications.telegram import TelegramNotifier


class NotificationService:
    def __init__(self):
        self._notifiers: list[BaseNotifier] = []
        self._enabled = settings.ENABLE_EXTERNAL_NOTIFICATIONS
        if self._enabled:
            self._init_notifiers()

    def _init_notifiers(self) -> None:
        if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
            self._notifiers.append(
                TelegramNotifier(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID)
            )
        if settings.DISCORD_WEBHOOK_URL:
            self._notifiers.append(DiscordNotifier(settings.DISCORD_WEBHOOK_URL))
        if settings.GENERIC_WEBHOOK_URL:
            self._notifiers.append(
                GenericWebhookNotifier(
                    settings.GENERIC_WEBHOOK_URL,
                    settings.GENERIC_WEBHOOK_SECRET,
                    settings.GENERIC_WEBHOOK_TIMEOUT,
                )
            )

    async def dispatch(self, event_type: str, payload: dict[str, Any]) -> None:
        if not self._enabled or not self._notifiers:
            return

        event = {"type": event_type, "payload": payload}
        tasks = [notifier.send(event) for notifier in self._notifiers]
        await asyncio.gather(*tasks, return_exceptions=True)


_notification_service: NotificationService | None = None


def get_notification_service() -> NotificationService:
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
