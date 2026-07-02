FROM --platform=$BUILDPLATFORM node:22-alpine AS frontend-builder

WORKDIR /frontend
COPY frontend/package.json frontend/.npmrc ./
RUN corepack enable && corepack prepare pnpm@latest --activate && pnpm install --config.onlyBuiltDependencies=esbuild
COPY frontend/ ./
RUN pnpm build


FROM --platform=$BUILDPLATFORM python:3.12-slim AS backend-builder

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

COPY backend/pyproject.toml backend/uv.lock ./
COPY backend/alembic.ini ./
COPY backend/alembic/ ./alembic/
COPY backend/src/ ./src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r tikdown && useradd -r -g tikdown -d /app tikdown

WORKDIR /app

COPY --from=backend-builder --chown=tikdown:tikdown /app/.venv /app/.venv
COPY --from=backend-builder --chown=tikdown:tikdown /app/src /app/src
COPY --from=backend-builder --chown=tikdown:tikdown /app/pyproject.toml /app/
COPY --from=backend-builder --chown=tikdown:tikdown /app/alembic.ini /app/
COPY --from=backend-builder --chown=tikdown:tikdown /app/alembic /app/alembic
COPY --from=frontend-builder --chown=tikdown:tikdown /frontend/dist /app/frontend/dist

RUN mkdir -p /app/data/media && chown -R tikdown:tikdown /app/data

USER tikdown

ENV PATH="/app/.venv/bin:$PATH"
ENV MEDIA_DIR=/app/data/media
ENV DATABASE_URL=sqlite+aiosqlite:////app/data/tikdown.db

EXPOSE 8000

VOLUME ["/app/data"]

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/system/health')"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
