from typing import List, Literal

from pydantic import BaseModel, Field


class PortfolioConstraints(BaseModel):
    max_positions: int = Field(
        ...,
        ge=1,
        le=50,
        description="Maximum number of positions allowed in the portfolio",
    )
    max_position_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description=(
            "Maximum percentage of the portfolio that can be allocated to a single position"
        ),
    )
    min_cash_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Minimum percentage of the portfolio to be held in cash",
    )


class AllocatedPosition(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol")
    allocation_pct: float = Field(
        ...,
        ge=0.0,
        le=20.0,
        description="The percentage of the portfolio allocated to this ticker",
    )
    risk_level: Literal["low", "medium", "high"] = Field(
        ...,
        description="The risk level associated with this position",
    )
    stop_loss_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Stop-loss percentage below entry price",
    )
    retionale: str = Field(
        ...,
        description="Short explanation for why this position is included and sized as such",
        max_length=500,
    )


class RejectedOpportunity(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol")
    reason: str = Field(
        ...,
        description="Reason why this opportunity was not included in the portfolio",
        max_length=300,
    )


class PortfolioSummary(BaseModel):
    total_positions: int = Field(
        ...,
        description="Total number of positions in the portfolio",
    )
    allocated_capital_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Total percentage of capital allocated",
    )
    cash_pct: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Percentage of capital held in cash",
    )
    risk_posture: Literal["conservative", "balanced", "aggressive"] = Field(
        ...,
        description="Overall risk posture of the portfolio",
    )


class PortfolioAllocation(BaseModel):
    portfolio_summary: PortfolioSummary = Field(
        ...,
        description="Summary of the overall portfolio allocation",
    )
    positions: List[AllocatedPosition] = Field(
        ...,
        description="List of individual position allocations",
        min_items=0,
    )
    rejected_opportunities: List[RejectedOpportunity] = Field(
        ...,
        description="List of opportunities that were considered but not included in the portfolio",
        min_items=0,
    )
    portfolio_risks: List[str] = Field(
        ...,
        description="List of identified key portfolio-level risks and concentrations",
        min_items=1,
        max_items=5,
    )
