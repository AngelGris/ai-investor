# from aiolimiter import AsyncLimiter

# brave_limiter = AsyncLimiter(max_rate=1, time_period=1)  # 1 requests per second in average

import asyncio
import time


class RateLimiter:
    def __init__(self, min_interval_seconds: float):
        self.min_interval = min_interval_seconds
        self._lock = asyncio.Lock()
        self._last_called = 0.0

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_called
            if elapsed < self.min_interval:
                await asyncio.sleep(self.min_interval - elapsed)
            self._last_called = time.monotonic()


brave_limiter = RateLimiter(min_interval_seconds=1.5)  # 1 request per 1.5 seconds
