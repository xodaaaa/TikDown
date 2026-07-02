from __future__ import annotations

import json
from typing import Any

import httpx

from src.core.notifications.base import BaseNotifier, NotificationRegistry


@NotificationRegistry.register("discord")
class DiscordNotifier(BaseNotifier):
    name = "discord"

    def __init__(self, webhook_url: str):
        self._url = webhook_url

    async def send(self, event: dict[str, Any]) -> bool:
        event_type = event.get("type", "unknown")
        payload = event.get("payload", {})

        embed = {
            "title": f"TikDown — {event_type}",
            "description": f"```json\n{json.dumps(payload, indent=2, default=str)[:4000]}\n```",
            "color": 0xFF69B4,
            "timestamp": event.get("timestamp", ""),
        }

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                self._url,
                json={"embeds": [embed]},
            )
            return 200 <= resp.status_code < 300
