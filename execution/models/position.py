from pydantic import BaseModel, Field


class Position(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    quantity: int = Field(
        ..., gt=0, description="Number of shares held in the position"
    )
    avg_price: float = Field(
        ..., gt=0.0, description="Volume-weighted average entry price"
    )
    stop_loss_pct: float = Field(
        ..., ge=0.0, le=100.0, description="Stop-loss percentage below average price"
    )
    unrealized_pnl: float = Field(
        ..., description="Current unrealized PnL in currency units"
    )
