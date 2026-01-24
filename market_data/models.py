from datetime import datetime

from pydantic import BaseModel


class MarketQuote(BaseModel):
    ticker: str
    price: float
    timestamp: datetime
    source: str = "alpha_vantage"
