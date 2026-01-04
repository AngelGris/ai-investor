from typing import List, Literal

from pydantic import BaseModel, Field


class RiskProfile(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol.")
    risk_level: Literal["low", "medium", "high"] = Field(
        ...,
        description="Overall risk level associated with the investment.",
    )
    confidence_in_assessment: Literal["low", "medium", "high"] = Field(
        ...,
        description="Confidence level in the risk assessment provided.",
    )
    max_position_pct: float = Field(
        ...,
        ge=0,
        le=100,
        description="Maximum position size as percentage of total portfolio.",
    )
    max_loss_pct: float = Field(
        ...,
        ge=0.1,
        le=5,
        description="Maximum acceptable loss as percentage of position size.",
    )
    stop_loss_pct: float = Field(
        ...,
        ge=1,
        le=40,
        description="Recommended stop-loss level as percentage of entry price.",
    )
    primary_risks: List[str] = Field(
        ...,
        min_items=2,
        max_items=6,
        description="Key factors that could cause capital loss.",
    )
    risk_mitigations: List[str] = Field(
        ...,
        min_items=1,
        max_items=4,
        description="Actions or constraints that reduce risk exposure.",
    )
    worst_case_scenarios: str = Field(
        ...,
        description="Plausible worst-case outcome and impact.",
    )
