from unittest.mock import AsyncMock

import pytest

from src.core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError


class TestCircuitBreaker:
    @pytest.mark.asyncio
    async def test_passes_when_closed(self):
        cb = CircuitBreaker("test-1")
        mock_fn = AsyncMock(return_value="success")
        result = await cb.call(mock_fn)
        assert result == "success"
        assert not cb.is_open

    @pytest.mark.asyncio
    async def test_opens_after_failures(self):
        on_open = AsyncMock()
        cb = CircuitBreaker("test-2", max_failures=3, on_open=on_open)
        mock_fn = AsyncMock(side_effect=Exception("fail"))

        for _ in range(3):
            with pytest.raises(Exception):
                await cb.call(mock_fn)

        assert cb.is_open
        on_open.assert_called_once_with("test-2")

    @pytest.mark.asyncio
    async def test_raises_when_open(self):
        cb = CircuitBreaker("test-3", max_failures=1)
        mock_fn = AsyncMock(side_effect=Exception("fail"))

        with pytest.raises(Exception):
            await cb.call(mock_fn)

        assert cb.is_open
        with pytest.raises(CircuitBreakerOpenError):
            await cb.call(AsyncMock())

    @pytest.mark.asyncio
    async def test_resets_on_success(self):
        cb = CircuitBreaker("test-4", max_failures=2)
        mock_fn = AsyncMock(side_effect=Exception("fail"))
        for _ in range(1):
            with pytest.raises(Exception):
                await cb.call(mock_fn)

        assert cb.failure_count == 1
        mock_fn.side_effect = None
        mock_fn.return_value = "ok"
        await cb.call(mock_fn)
        assert cb.failure_count == 0
