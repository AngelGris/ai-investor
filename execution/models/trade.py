from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID


@dataclass(frozen=True)
class Trade:
    trade_id: UUID
    portfolio_id: UUID
    executed_at: datetime

    ticker: str
    side: str  # "BUY" | "SELL"

    quantity: float
    price: float
    commission: float

    strategy: Optional[str] = None
    reason: Optional[str] = None
    metadata: Optional[Dict] = None
    notes: Optional[str] = None

    @property
    def notional(self) -> float:
        return self.quantity * self.price
