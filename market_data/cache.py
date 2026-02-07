import sqlite3
from datetime import datetime, timezone


class PriceCache:
    def __init__(self, conn: sqlite3.Connection, ttl_seconds: float):
        self.conn = conn
        self.ttl = ttl_seconds
        self._store: dict[str, tuple[float, float]] = {}

    def get(self, ticker: str) -> float | None:
        ticker = ticker.upper()
        row = self.conn.execute(
            "SELECT price, timestamp FROM market_prices WHERE ticker = ?", (ticker,)
        ).fetchone()

        if row is None:
            return None

        price, timestamp = row
        timestamp = datetime.fromisoformat(timestamp)
        age = (datetime.now(timezone.utc) - timestamp).total_seconds()
        if age > self.ttl:
            self.conn.execute(
                "DELETE FROM market_prices WHERE ticker = ?",
                (ticker,),
            )
            self.conn.commit()
            return None

        return price

    def set(self, ticker: str, price: float):
        ticker = ticker.upper()

        self.conn.execute(
            """
            INSERT INTO market_prices (ticker, price, timestamp)
            VALUES (?, ?, ?)
            ON CONFLICT(ticker) DO UPDATE SET
                price = excluded.price,
                timestamp = excluded.timestamp
            """,
            (
                ticker,
                price,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.conn.commit()
