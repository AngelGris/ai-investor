from agents import Agent, Runner

from ai_agents.decision_agent.prompt import build_prompt
from ai_agents.decision_agent.schema import InvestmentDecisionOutput


async def run_decision_agent(
    ticker: str, fundamental_analysis: str, risk_analysis: str, portfolio: dict
) -> InvestmentDecisionOutput:
    positions = []
    for pos in portfolio.positions.values():
        positions.append(
            f"- {pos.ticker}: {pos.quantity} shares at avg price {pos.avg_price}."
        )

    prompt = build_prompt(
        ticker=ticker,
        fundamental_analysis=fundamental_analysis,
        risk_analysis=risk_analysis,
        cash=portfolio.cash,
        positions_summary=portfolio.positions,
    )
    agent = Agent(
        name="Decision Agent",
        model="gpt-5-mini",
        tools=[],
        output_type=InvestmentDecisionOutput,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
