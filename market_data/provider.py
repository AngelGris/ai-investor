import os
from datetime import datetime, timezone
from typing import List

import httpx

from market_data.cache import PriceCache
from market_data.models import MarketQuote
from market_data.rate_limiter import RateLimiter
from persistence.database import get_connection


class MarketDataProvider:
    def __init__(self, provider: str = "alpha_vantage"):
        self._provider = provider.lower()

        if provider == "alpha_vantage":
            self._base_url = os.getenv(
                "ALPHA_VANTAGE_BASE_URL", "https://www.alphavantage.co/query"
            )
            self._api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            min_interval = float(os.getenv("ALPHA_VANTAGE_MIN_INTERVAL", "12.0"))
            self._get_quote_function = self._get_alpha_vantage_quote
        else:
            self._base_url = os.getenv(
                "TWELVE_DATA_BASE_URL", "https://api.twelvedata.com/quote"
            )
            self._api_key = os.getenv("TWELVE_DATA_API_KEY")
            min_interval = 1

        if not self._api_key:
            raise ValueError("Market data provider API key is not set.")
        self._limiter = RateLimiter(min_interval)
        self._cache = PriceCache(
            conn=get_connection(), ttl_seconds=3600 * 12
        )  # Cache for 12 hours
        self._client = httpx.AsyncClient(timeout=10.0)

    async def _get_alpha_vantage_quote(self, ticker: str) -> MarketQuote:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self._api_key,
        }
        response = await self._client.get(self._base_url, params=params)
        response.raise_for_status()
        data = response.json()

        quote = data.get("Global Quote", {})
        if not quote or "05. price" not in quote:
            raise ValueError(f"No market data found for ticker {ticker}: {data}")

        price = float(quote["05. price"])
        return MarketQuote(
            ticker=ticker,
            price=price,
            timestamp=datetime.now(timezone.utc),
            source="alpha_vantage",
        )

    async def _get_twelve_data_quotes(self, tickers: List[str]) -> List[MarketQuote]:
        params = {
            "symbol": ",".join(tickers),
            "apikey": self._api_key,
        }
        response = await self._client.get(self._base_url, params=params)
        response.raise_for_status()
        data = response.json()

        quotes = {}
        now = datetime.now(timezone.utc)
        for ticker in tickers:
            payload = data.get(ticker)

            if not payload or "price" not in payload:
                raise ValueError(f"No market data found for ticker {ticker}: {data}")

            quotes[ticker] = MarketQuote(
                ticker=ticker,
                price=float(payload["price"]),
                timestamp=now,
                source="twelve_data",
            )
        return quotes

    async def get_market_quotes(self, tickers: List[str]) -> List[MarketQuote]:
        quotes = {}
        for ticker in tickers:
            ticker = ticker.upper()

            # Cache check
            cached_price = self._cache.get(ticker)
            if cached_price is not None:
                quotes[ticker] = MarketQuote(
                    ticker=ticker,
                    price=cached_price,
                    timestamp=datetime.now(timezone.utc),
                )
                continue

            # Rate limiting
            await self._limiter.acquire()

            # Alpha Vantage get one ticker at a time
            if self._provider == "alpha_vantage":
                quote = await self._get_alpha_vantage_quote(ticker)

                # Cache result
                self._cache.set(ticker, quote.price)

                quotes[ticker] = quote

        if self._provider == "twelve_data":
            quotes = await self._get_twelve_data_quotes(tickers)
            for quote in quotes.values():
                if isinstance(quote, Exception):
                    continue
                # Cache result
                self._cache.set(quote.ticker, quote.price)
        return quotes

    async def close(self):
        await self._client.aclose()
