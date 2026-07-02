from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "TikDown"
    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"

    DATABASE_URL: str = "sqlite+aiosqlite:///./data/tikdown.db"

    FERNET_KEY: str = ""

    ADMIN_PASSWORD_HASH: str = ""

    MONITOR_INTERVAL_MINUTES: int = 60
    MAX_CONCURRENT_DOWNLOADS: int = 2
    MAX_RETRIES_PER_VIDEO: int = 3
    MAX_CONSECUTIVE_FAILURES: int = 5
    MIN_DELAY_SECONDS: int = 5
    MAX_DELAY_SECONDS: int = 30

    ENABLE_EXTERNAL_NOTIFICATIONS: bool = False
    TELEGRAM_BOT_TOKEN: str | None = None
    TELEGRAM_CHAT_ID: str | None = None
    DISCORD_WEBHOOK_URL: str | None = None
    GENERIC_WEBHOOK_URL: str | None = None
    GENERIC_WEBHOOK_SECRET: str | None = None
    GENERIC_WEBHOOK_TIMEOUT: int = 10

    MEDIA_DIR: str = "./data/media"

    YT_DLP_VERSION_PINNED: str = "2026.6.9"
    YT_DLP_CHECK_UPDATES: bool = True
    YT_DLP_UPDATE_CHECK_INTERVAL_HOURS: int = 168

    PROFILE_REFRESH_INTERVAL_HOURS: int = 48

    COOKIE_VALIDATION_INTERVAL_HOURS: int = 24

    ALLOWED_ORIGINS: str = "http://localhost:5173"


settings = Settings()
