from typing import List

from agents import Agent, Runner

from ai_agents.decision_agent.schema import InvestmentDecisionOutput
from ai_agents.portfolio_allocation.prompt import build_prompt
from ai_agents.portfolio_allocation.schema import (
    PortfolioAllocation,
    PortfolioConstraints,
)
from ai_agents.risk_analyst.schema import RiskProfile


async def run_portfolio_allocation(
    risk_profiles: List[RiskProfile],
    investment_decisions: List[InvestmentDecisionOutput],
):
    constraints = PortfolioConstraints(
        max_positions=5,
        max_position_pct=30.0,
        min_cash_pct=0.0,
    )

    prompt = build_prompt(
        constraints=constraints,
        risk_analysis=risk_profiles,
        investment_decisions=investment_decisions,
    )

    agent = Agent(
        name="Portfolio Allocation",
        model="gpt-5-mini",
        tools=[],
        output_type=PortfolioAllocation,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
