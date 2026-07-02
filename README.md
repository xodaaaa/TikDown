# TikDown

TikTok video monitoring and downloading platform. Monitor TikTok accounts, auto-detect and download new videos, playback integrated, dark mode support, and optional external notifications (Telegram, Discord, generic webhooks).

## Features

- **Account Monitoring** — Add TikTok accounts and auto-detect new videos
- **Auto Download** — Downloads new videos automatically with yt-dlp
- **Built-in Gallery** — Browse and play downloaded videos
- **Cookie Manager** — Upload `cookies.txt` or `cookies.json` from "Get cookies.txt LOCALLY" browser extension
- **Real-time Activity Feed** — Server-Sent Events (SSE) for live updates
- **Profile Stats** — Shows avatar, followers, likes, video count per monitored account
- **Deduplication** — Smart cross-account deduplication by `tiktok_id`
- **External Notifications** — Optional Telegram, Discord, and generic webhook notifications
- **Anti-blocking** — Exponential backoff, jitter, circuit breaker per account
- **Dark Mode** — Fully supported

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy (async), yt-dlp, APScheduler |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, TanStack Query v5 |
| Database | SQLite (aiosqlite) |
| Encryption | Fernet (cookie encryption at rest) |
| Auth | Single-user, argon2 password, httpOnly session cookie |
| Deployment | Docker (multi-arch: amd64 + arm64) |

## Quick Start

### Docker (recommended)

```bash
# Clone the repo
git clone https://github.com/xodaaaa/TikDown.git
cd TikDown

# Copy and edit environment
cp .env.example .env

# Start
docker compose up -d
```

Open `http://localhost:8000`

### Local Development

**Backend:**

```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload --port 8000
```

**Frontend (requires Node.js + pnpm):**

```bash
cd frontend
pnpm install
pnpm dev
```

Open `http://localhost:5173`

## Configuration

Copy `.env.example` to `.env` and configure:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Application secret key |
| `FERNET_KEY` | Encryption key for cookies (leave empty to auto-generate) |
| `ADMIN_PASSWORD_HASH` | Leave empty, use the setup page on first run |
| `MONITOR_INTERVAL_MINUTES` | Check interval for accounts (default: 60) |
| `MAX_CONCURRENT_DOWNLOADS` | Max simultaneous downloads (default: 2) |

## Getting TikTok Cookies

1. Install "Get cookies.txt LOCALLY" browser extension
2. Log in to tiktok.com
3. Export cookies (TXT or JSON format)
4. Upload via Settings > Cookies Manager in TikDown

## Project Structure

```
TikDown/
├── backend/              # Python/FastAPI backend
│   ├── src/
│   │   ├── api/routes/   # REST + SSE endpoints
│   │   ├── core/         # DownloadEngine, crypto, auth, backoff, notifications
│   │   ├── db/models/    # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic (monitor)
│   └── alembic/          # Database migrations
├── frontend/             # React/TypeScript frontend
│   └── src/
│       ├── pages/        # Dashboard, Users, Gallery, Settings
│       ├── components/   # Sidebar, Badge, ProgressBar
│       └── services/     # API client, TanStack Query hooks
├── Dockerfile            # Multi-arch Docker build
└── docker-compose.yml
```
