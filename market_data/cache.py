import time


class PriceCache:
    def __init__(self, ttl_seconds: float):
        self.ttl = ttl_seconds
        self._store: dict[str, tuple[float, float]] = {}

    def get(self, ticker: str) -> float | None:
        entry = self._store.get(ticker)
        if not entry:
            return None

        price, timestamp = entry
        if time.time() - timestamp > self.ttl:
            self._store.ticker(ticker, None)
            return None

        return price

    def set(self, ticker: str, price: float):
        self._store[ticker] = (price, time.time())
