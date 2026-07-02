import random


def calculate_backoff(
    attempt: int,
    base_delay: float = 10.0,
    max_delay: float = 3600.0,
    jitter: bool = True,
) -> float:
    delay = min(base_delay * (2 ** attempt), max_delay)
    if jitter:
        delay = delay * (0.5 + random.random())
    return delay


def random_delay(min_seconds: int, max_seconds: int) -> float:
    return min_seconds + (random.random() * (max_seconds - min_seconds))
