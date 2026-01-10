from aiolimiter import AsyncLimiter

brave_limiter = AsyncLimiter(max_rate=1, time_period=1)  # 1 requests per second
