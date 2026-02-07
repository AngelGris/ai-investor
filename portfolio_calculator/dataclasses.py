from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PositionMetrics:
    ticker: str
    quantity: int
    avg_price: float
    market_price: float
    market_value: float
    unrealized_pnl: float
    allocation_pct: float


@dataclass(frozen=True)
class PortfolioMetrics:
    total_value: float
    cash: float
    cash_allocation_pct: float
    unrealized_pnl: float
    realized_pnl: float
    total_commissions: float
    positions: Dict[str, PositionMetrics]
