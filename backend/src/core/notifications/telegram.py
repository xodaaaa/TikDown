from __future__ import annotations

import json
from typing import Any

import httpx

from src.core.notifications.base import BaseNotifier, NotificationRegistry


@NotificationRegistry.register("telegram")
class TelegramNotifier(BaseNotifier):
    name = "telegram"

    def __init__(self, bot_token: str, chat_id: str):
        self._token = bot_token
        self._chat_id = chat_id

    async def send(self, event: dict[str, Any]) -> bool:
        event_type = event.get("type", "unknown")
        payload = event.get("payload", {})
        message = f"*TikDown* — {event_type}\n\n```json\n{json.dumps(payload, indent=2, default=str)}\n```"

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{self._token}/sendMessage",
                json={
                    "chat_id": self._chat_id,
                    "text": message[:4096],
                    "parse_mode": "Markdown",
                },
            )
            return resp.status_code == 200
