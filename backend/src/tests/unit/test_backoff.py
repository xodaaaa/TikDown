import pytest

from src.core.backoff import calculate_backoff, random_delay


class TestBackoff:
    def test_base_case_no_retries(self):
        delay = calculate_backoff(0, jitter=False)
        assert delay == 10.0

    def test_exponential_growth(self):
        d0 = calculate_backoff(0, jitter=False)
        d1 = calculate_backoff(1, jitter=False)
        d2 = calculate_backoff(2, jitter=False)
        assert d1 == pytest.approx(d0 * 2)
        assert d2 == pytest.approx(d0 * 4)

    def test_max_delay_cap(self):
        delay = calculate_backoff(20, base_delay=10, max_delay=3600, jitter=False)
        assert delay == 3600.0

    def test_jitter_adds_variation(self):
        delays = [calculate_backoff(2, jitter=True) for _ in range(10)]
        assert len(set(delays)) > 1

    def test_random_delay_within_range(self):
        for _ in range(100):
            delay = random_delay(5, 30)
            assert 5 <= delay <= 30
