import os
from pathlib import Path

from cryptography.fernet import Fernet

from src.config import settings

_FERNET_KEY_FILE = os.path.join(settings.MEDIA_DIR, "..", "fernet.key")


def _get_or_create_fernet_key() -> str:
    key = settings.FERNET_KEY
    if key:
        return key

    try:
        key_path = Path(_FERNET_KEY_FILE).resolve()
        if key_path.exists():
            return key_path.read_text().strip()
    except Exception:
        pass

    key = Fernet.generate_key().decode()
    try:
        key_path = Path(_FERNET_KEY_FILE).resolve()
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_text(key)
    except Exception:
        pass

    return key


def _get_fernet() -> Fernet:
    key = _get_or_create_fernet_key()
    try:
        return Fernet(key.encode() if isinstance(key, str) else key)
    except Exception:
        key = Fernet.generate_key().decode()
        return Fernet(key.encode())


_fernet: Fernet | None = None


def get_fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = _get_fernet()
    return _fernet


def encrypt_cookies(data: str) -> str:
    f = get_fernet()
    return f.encrypt(data.encode()).decode()


def decrypt_cookies(encrypted_data: str) -> str:
    f = get_fernet()
    return f.decrypt(encrypted_data.encode()).decode()
