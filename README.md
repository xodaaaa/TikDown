# TikDown — Plataforma de Monitorizacion y Descarga de Videos de TikTok

> **Proyecto personal** para monitorizar cuentas de TikTok, detectar automaticamente nuevos videos, descargarlos de forma robusta y gestionarlos con una interfaz web moderna y amigable. Desplegable en Docker (amd64 + arm64).

**Estado actual**: Completamente funcional con todas las caracteristicas de la especificacion tecnica.

---

## Caracteristicas Principales

### Core
- **Monitorizacion automatica** de multiples cuentas de TikTok
- **Deteccion inteligente** de nuevos videos con deduplicacion cross-account (`tiktok_id` UNIQUE)
- **Descargas robustas** con `yt-dlp` (como libreria Python)
  - Backoff exponencial + jitter
  - Circuit breaker por cuenta
  - Separacion chequeo liviano vs descarga pesada
  - Soporte completo de cookies (TXT Netscape + JSON)
- **Refresco periodico de perfiles** (avatar, seguidores, likes, numero de videos)
- **Reintentos inteligentes** de descargas fallidas

### Seguridad y Cookies
- Subida de cookies directamente desde la web (`CookiesManager.tsx`)
- Soporte completo para **.txt (Netscape)** y **.json** generados por la extension **"Get cookies.txt LOCALLY"**
- Validacion completa + prueba real con yt-dlp
- Cifrado en reposo con **Fernet** (clave fuera de la base de datos)
- Autenticacion simple de un solo usuario con cookie `httpOnly` + Argon2

### Notificaciones (totalmente opcionales)
- **Telegram**
- **Discord**
- **Webhook generico** con firma HMAC-SHA256 (preparado para automatizaciones futuras con n8n, Make, etc.)
- Integrado con todos los eventos importantes del sistema

### Interfaz Web Moderna
- **Dashboard** en tiempo real con Activity Feed via **SSE**
- **Gestion de cuentas** con avatar, estadisticas y acciones optimistas
- **Galeria** responsiva con filtros, paginacion y reproductor integrado
- **Settings** completo:
  - Preferencias de monitorizacion
  - Cookies Manager (drag & drop TXT/JSON + test)
  - Configuracion de notificaciones externas
- Modo oscuro nativo (Tailwind v4)
- Totalmente responsive (desktop + movil)

### Infraestructura
- **Docker multi-arquitectura** (amd64 + arm64) -- funciona en Raspberry Pi
- Volumenes persistentes para SQLite + archivos de video
- Healthcheck integrado
- Usuario no-root en el contenedor final
- Opcional: Caddy como reverse proxy con TLS automatico

---

## Stack Tecnologico

### Backend (Python)
- **FastAPI** + Uvicorn (async)
- **SQLAlchemy 2.0** (modo async) + **aiosqlite**
- **Alembic** (migraciones con `render_as_batch=True`)
- **APScheduler** (tareas en background + jobstore SQLite)
- **yt-dlp** (como libreria)
- **cryptography** (Fernet)
- **pydantic-settings** + **structlog**
- **pytest** + fixtures HTTP

### Frontend (TypeScript)
- **React 19** + **Vite** (Rolldown)
- **Tailwind CSS v4** (configuracion CSS-first)
- **TanStack Query v5**
- **React Router**
- **Zustand** (estado ligero)
- **SSE nativo** con reconexion automatica

### Infra
- Docker + docker-compose
- Multi-stage build optimizado
- ffmpeg incluido para posibles procesamientos futuros

---

## Estructura del Proyecto

```
TikDown/
├── backend/                     # Python/FastAPI backend
│   ├── src/
│   │   ├── main.py              # EntryPoint + lifespan + CORS + Health
│   │   ├── config.py            # pydantic-settings
│   │   ├── db/
│   │   │   ├── base.py          # SQLAlchemy declarative base
│   │   │   ├── session.py       # async session factory
│   │   │   └── models/          # account, video, cookie, event, setting
│   │   ├── schemas/             # Pydantic (separados de modelos DB)
│   │   ├── api/routes/          # auth, accounts, videos, cookies, monitor, events (SSE)
│   │   ├── core/
│   │   │   ├── download_engine.py   # Wrapper yt-dlp (nunca curl/aria2c)
│   │   │   ├── task_queue.py        # Interfaz TaskQueue + APScheduler
│   │   │   ├── crypto.py            # Fernet encrypt/decrypt
│   │   │   ├── auth.py              # argon2 + sesion httpOnly
│   │   │   ├── backoff.py           # Exponencial + jitter
│   │   │   ├── circuit_breaker.py
│   │   │   └── notifications/       # base, telegram, discord, generic_webhook, service
│   │   └── services/
│   │       └── monitor.py       # Orquestacion completa + deduplicacion + refresh perfil
│   ├── alembic/
│   │   ├── env.py               # render_as_batch=True (crítico para SQLite)
│   │   └── versions/
│   └── tests/                   # 20 tests unitarios (todos pasan)
│       └── unit/                # backoff, circuit_breaker, crypto, cookies
│
├── frontend/                    # React/TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard/       # DashboardCards, MonitorPanel, ActivityFeed (SSE)
│   │   │   ├── Users/           # UsersTable (avatar + stats), AddUserModal
│   │   │   ├── Gallery/         # VideoGrid, VideoCard, VideoModal (reproductor + retry)
│   │   │   ├── Settings/        # MonitorSettingsForm, CookiesManager (TXT+JSON), NotificationsSettings
│   │   │   └── LoginPage.tsx
│   │   ├── hooks/
│   │   │   ├── useEventSource.ts    # SSE nativo con reconexion automatica
│   │   │   └── useAppStore.ts       # Zustand (theme)
│   │   ├── services/
│   │   │   ├── api.ts               # Cliente fetch completo
│   │   │   └── queries.ts           # TanStack Query keys + hooks
│   │   └── types/
│   │       └── index.ts             # Interfaces compartidas
│   └── index.html
│
├── Dockerfile                    # Multi-stage + multi-arch
├── docker-compose.yml
├── Caddyfile                     # (opcional, para HTTPS externo)
├── .env.example
```

---

## Inicio Rapido

### Docker (recomendado)

```bash
git clone https://github.com/xodaaaa/TikDown.git
cd TikDown
cp .env.example .env
docker compose up -d --build
```

Abre **http://localhost:8000**. La primera vez te pedira crear la contrasena de administrador.

### Desarrollo Local

**Backend:**

```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload --port 8000
```

**Frontend (requiere Node.js + pnpm):**

```bash
cd frontend
pnpm install
pnpm dev
```

Abre **http://localhost:5173**. El proxy de Vite redirige `/api` al backend en `localhost:8000`.

---

## Configuracion

Copia `.env.example` a `.env` y configura:

| Variable | Descripcion | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de la aplicacion | *obligatorio* |
| `FERNET_KEY` | Clave de cifrado para cookies (dejar vacio para autogenerar) | |
| `ADMIN_PASSWORD_HASH` | Hash de contrasena (dejar vacio, se configura via web) | |
| `MONITOR_INTERVAL_MINUTES` | Intervalo de chequeo entre cuentas | `60` |
| `MAX_CONCURRENT_DOWNLOADS` | Descargas simultaneas maximas | `2` |
| `MAX_CONSECUTIVE_FAILURES` | Fallos consecutivos antes de pausar cuenta | `5` |
| `ENABLE_EXTERNAL_NOTIFICATIONS` | Activar notificaciones externas | `false` |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | |
| `TELEGRAM_CHAT_ID` | Chat ID de Telegram | |
| `DISCORD_WEBHOOK_URL` | URL del webhook de Discord | |
| `GENERIC_WEBHOOK_URL` | URL del webhook generico | |
| `GENERIC_WEBHOOK_SECRET` | Secreto HMAC para webhook generico | |
| `ALLOWED_ORIGINS` | Origenes CORS permitidos | `http://localhost:5173` |

---

## Configuracion Inicial Recomendada

1. **Crear contrasena** de administrador (primera ejecucion)
2. **Agregar cuentas** de TikTok en la seccion Users
3. **Subir cookies** (Settings > Cookies Manager)
   - Instala la extension **Get cookies.txt LOCALLY**
   - Inicia sesion en tiktok.com
   - Exporta en formato **TXT** (recomendado) o **JSON**
   - Subelo por drag & drop
   - Verifica con el boton "Test"
4. **Configurar notificaciones** (opcional, en Settings > Notifications)
5. **Iniciar monitor** desde el Dashboard

---

## Obtencion de Cookies de TikTok

1. Instala la extension de navegador **"Get cookies.txt LOCALLY"** (disponible para Chrome, Edge, Brave, Firefox)
2. Inicia sesion normalmente en `tiktok.com`
3. Con la pestana de TikTok activa, abre la extension y exporta las cookies
4. Sube el archivo `.txt` o `.json` directamente desde la interfaz web (Settings > Cookies Manager)
5. La aplicacion valida automaticamente:
   - Formato correcto del archivo
   - Presencia de `sessionid` (obligatoria)
   - Prueba real de autenticacion contra TikTok

---

## Testing

```bash
# Backend unit tests
cd backend
uv run pytest src/tests/unit/ -v

# Lint
uv run ruff check src/
```

Resultado actual: **20 tests pasados, lint limpio**.

---

## Roadmap / Proximas Mejoras

- Backup automatico programado + retencion de videos
- Motor de reglas/acciones automaticas sobre webhooks
- Soporte opcional de proxies
- Exportacion masiva de videos
- Estadisticas avanzadas y graficos

---

## Licencia

Proyecto personal. Uso libre bajo tu propia responsabilidad.

---

*Desarrollado siguiendo las mejores practicas de robustez, seguridad y mantenibilidad para scraping de TikTok en 2026.*

*Ultima actualizacion: Julio 2026*
