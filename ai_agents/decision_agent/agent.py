from agents import Agent, Runner

from ai_agents.decision_agent.prompt import build_prompt
from ai_agents.decision_agent.schema import InvestmentDecisionOutput


async def run_decision_agent(fundamental_analysis: str, risk_analysis: str):
    prompt = build_prompt(
        fundamental_analysis=fundamental_analysis,
        risk_analysis=risk_analysis,
    )
    agent = Agent(
        name="Decision Agent",
        model="gpt-5-mini",
        tools=[],
        output_type=InvestmentDecisionOutput,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
