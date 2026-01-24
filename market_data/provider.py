import os
from datetime import datetime, timezone

import httpx

from market_data.cache import PriceCache
from market_data.models import MarketQuote
from market_data.rate_limiter import RateLimiter


class MarketDataProvider:
    BASE_URL = os.getenv("ALPHA_VANTAGE_BASE_URL", "https://www.alphavantage.co/query")

    def __init__(self):
        self._api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self._api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is not set.")
        min_interval = float(os.getenv("ALPHA_VANTAGE_MIN_INTERVAL", "12.0"))
        self._limiter = RateLimiter(min_interval)
        self._cache = PriceCache(ttl_seconds=3600)  # Cache for 1 hour
        self._client = httpx.AsyncClient(timeout=10.0)

    async def get_market_quote(self, ticker: str) -> MarketQuote:
        ticker = ticker.upper()

        # Cache check
        cached_price = self._cache.get(ticker)
        if cached_price is not None:
            return MarketQuote(
                ticker=ticker,
                price=cached_price,
                timestamp=datetime.now(timezone.utc),
            )

        # Rate limiting
        await self._limiter.acquire()

        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self._api_key,
        }

        response = await self._client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        quote = data.get("Global Quote", {})
        if not quote or "05. price" not in quote:
            raise ValueError(f"No market data found for ticker {ticker}: {data}")

        price = float(quote["05. price"])

        # Cache result
        self._cache.set(ticker, price)

        return MarketQuote(
            ticker=ticker,
            price=price,
            timestamp=datetime.now(timezone.utc),
        )

    async def close(self):
        await self._client.aclose()
