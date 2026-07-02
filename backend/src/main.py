from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from src.config import settings
from src.core.auth import is_setup_complete
from src.core.task_queue import APSchedulerQueue
from src.db.base import Base
from src.db.session import async_session_factory, engine

task_queue = APSchedulerQueue()
event_queue: asyncio.Queue[dict] = asyncio.Queue()

FRONTEND_DIST = os.environ.get("FRONTEND_DIST", "/app/frontend/dist")


def _mount_frontend(app: FastAPI) -> None:
    if not os.path.isdir(FRONTEND_DIST):
        return

    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend_assets")

    index_path = os.path.join(FRONTEND_DIST, "index.html")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("media/"):
            raise HTTPException(status_code=404)
        if os.path.isfile(index_path):
            return FileResponse(index_path)
        raise HTTPException(status_code=404)


def _create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await task_queue.start()
        yield
        await task_queue.shutdown()
        await engine.dispose()

    app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from src.api.routes import accounts, auth, cookies, events, monitor, videos

    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
    app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
    app.include_router(cookies.router, prefix="/api/cookies", tags=["cookies"])
    app.include_router(monitor.router, prefix="/api/monitor", tags=["monitor"])
    app.include_router(events.router, prefix="/api", tags=["events"])

    try:
        app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")
    except Exception:
        pass

    _mount_frontend(app)

    @app.get("/api/system/health")
    async def health():
        try:
            async with async_session_factory() as session:
                await session.execute(text("SELECT 1"))
        except Exception as e:
            return JSONResponse({"status": "unhealthy", "detail": str(e)}, status_code=500)

        return {
            "status": "healthy",
            "version": "0.1.0",
            "yt_dlp_pinned": settings.YT_DLP_VERSION_PINNED,
            "setup_complete": is_setup_complete(),
        }

    return app


app = _create_app()
