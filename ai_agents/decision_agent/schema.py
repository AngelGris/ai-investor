from typing import List, Literal

from pydantic import BaseModel, Field


class InvestmentDecisionOutput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol.")
    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall investment attractiveness score (0-100).",
    )
    recommendation: Literal["buy", "watch", "avoid"]
    conviction: Literal["high", "medium", "low"]
    time_horizon: Literal["short_term", "medium_term", "long_term"]
    key_strengths: List[str] = Field(
        ...,
        description="List of key strengths supporting the investment decision.",
    )
    key_risks: List[str] = Field(
        ...,
        description="List of key risks or uncertainties associated with the investment decision.",
    )
    thesis: str = Field(
        ...,
        description="A concise investment thesis summarizing the rationale behind the decision.",
    )
