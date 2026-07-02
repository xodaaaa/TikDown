from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

import httpx

from src.core.notifications.base import BaseNotifier, NotificationRegistry


@NotificationRegistry.register("generic_webhook")
class GenericWebhookNotifier(BaseNotifier):
    name = "generic_webhook"

    def __init__(self, url: str, secret: str | None = None, timeout: int = 10):
        self.url = url
        self.secret = secret.encode() if secret else None
        self.timeout = timeout

    async def send(self, event: dict[str, Any]) -> bool:
        payload = json.dumps(event, default=str)
        headers = {"Content-Type": "application/json"}
        if self.secret:
            signature = hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()
            headers["X-Signature-256"] = f"sha256={signature}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(self.url, content=payload, headers=headers)
            return 200 <= resp.status_code < 300
