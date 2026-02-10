from agents import Agent, Runner

from ai_agents.risk_analyst.prompt import build_prompt
from ai_agents.risk_analyst.schema import RiskProfile


async def run_risk_analyst(
    fundamental_analysis: str, portfolio_value: float
) -> RiskProfile:
    prompt = build_prompt(
        fundamental_analysis=fundamental_analysis,
        portfolio_value=portfolio_value,
    )
    agent = Agent(
        name="Risk Analyst",
        model="gpt-5-mini",
        tools=[],
        output_type=RiskProfile,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
