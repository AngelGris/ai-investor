from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class InvestmentDecisionOutput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol.")
    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Overall investment attractiveness score (0-100).",
    )
    action: Literal["initiate", "add", "hold", "reduce", "exit", "avoid"] = Field(
        ...,
        description="Recommended portfolio action for this ticker.",
    )
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
    portfolio_context_notes: Optional[str] = Field(
        None,
        description=(
            "Optional notes explaining how the current portfolio influenced "
            "this decision (e.g., existing exposure, diversification, drawdowns)."
        ),
    )
