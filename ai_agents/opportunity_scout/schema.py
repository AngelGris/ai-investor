from typing import List, Literal

from pydantic import BaseModel, Field


class OpportunityCandidate(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol.")
    company_name: str = Field(..., description="The full name of the company.")
    sector: str = Field(..., description="The sector in which the company operates.")
    priority: Literal["low", "medium", "high"] = Field(
        ..., description="Relative priority for deeper analysis."
    )
    why_now: str = Field(
        ...,
        max_length=500,
        description="Concise explanation of why this company deserves attention now.",
    )
    key_catalysts: List[str] = Field(
        ...,
        min_items=1,
        max_items=5,
        description="Events or themes that could drive near-term attention or volatility.",
    )
    confidence: Literal["low", "medium", "high"] = Field(
        ..., description="Confidence in the signal, not in the investment outcome."
    )


class OpportunityScoutOutput(BaseModel):
    universe_name: str = Field(
        ..., description="Name of the investment universe or sector analyzed."
    )
    universe_size: int = Field(
        ..., ge=1, description="Total number of companies scanned."
    )
    selected_count: int = Field(
        ..., ge=0, description="Number of candidates selected for deeper analysis."
    )
    candidates: List[OpportunityCandidate] = Field(
        ...,
        min_items=0,
        max_items=15,
        description="Ranked shortlist of companies worth deeper analysis.",
    )
    summary: str = Field(
        ...,
        max_length=800,
        description="High-level summary of why these opportunities were selected.",
    )
