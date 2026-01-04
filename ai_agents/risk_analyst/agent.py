from agents import Agent, Runner

from ai_agents.risk_analyst.prompt import build_prompt
from ai_agents.risk_analyst.schema import RiskProfile


async def run_risk_analyst(fundamental_analysis: str, investment_decision: str):
    prompt = build_prompt(
        fundamental_analysis=fundamental_analysis,
        investment_decision=investment_decision,
    )
    agent = Agent(
        name="Risk Analyst",
        model="gpt-5-mini",
        tools=[],
        output_type=RiskProfile,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
