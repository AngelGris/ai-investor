from typing import List, Literal

from pydantic import BaseModel, Field


class FundamentalScoutOutput(BaseModel):
    company_name: str = Field(
        ..., description="The name of the company being analyzed."
    )
    ticker: str = Field(..., description="The stock ticker symbol.")
    thesis: str = Field(
        ..., description="Concise fundamental thesis (3 to 5 sentences)."
    )
    bull_case: List[str] = Field(
        ..., description="Key factors that could drive upside."
    )
    bear_case: List[str] = Field(..., description="Key risks or downside factors.")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence level in the thesis (0 to 1)."
    )
    horizon: Literal["short", "medium", "long"] = Field(
        ..., description="Expected time horizon of the thesis."
    )
