from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.config import settings

_ph = PasswordHasher()


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(password: str, hash_str: str) -> bool:
    try:
        return _ph.verify(hash_str, password)
    except VerifyMismatchError:
        return False


def is_setup_complete() -> bool:
    return bool(settings.ADMIN_PASSWORD_HASH)


def setup_admin_password(password: str) -> str:
    return hash_password(password)


def verify_admin_password(password: str) -> bool:
    if not settings.ADMIN_PASSWORD_HASH:
        return False
    return verify_password(password, settings.ADMIN_PASSWORD_HASH)
