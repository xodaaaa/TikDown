from cryptography.fernet import Fernet

from src.config import settings


def _get_fernet() -> Fernet:
    key = settings.FERNET_KEY
    if not key:
        key = Fernet.generate_key().decode()
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
