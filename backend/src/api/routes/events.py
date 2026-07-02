from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from src.main import event_queue

router = APIRouter()


@router.get("/events")
async def event_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            try:
                event = await asyncio.wait_for(event_queue.get(), timeout=30.0)
                yield {"event": event.get("type", "message"), "data": json.dumps(event, default=str)}
            except TimeoutError:
                yield {"event": "ping", "data": "{}"}

    return EventSourceResponse(event_generator())
