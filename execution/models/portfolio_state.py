from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field

from execution.models.position import Position
from execution.models.trade import Trade


class PortfolioState(BaseModel):
    timestamp: datetime = Field(..., description="Last update time (UTC)")
    cash: float = Field(..., ge=0.0, description="Available uninvested cash")
    positions: Dict[str, Position] = Field(
        default_factory=dict,
        description="Current positions in the portfolio, keyed by ticker symbol",
    )
    trades: List[Trade] = Field(
        default_factory=list, description="List of executed trades"
    )
    realized_pnl: float = Field(
        ..., description="Total realized profit and loss from closed positions"
    )
    total_commissions: float = Field(
        ..., description="Total commissions paid on executed trades"
    )
