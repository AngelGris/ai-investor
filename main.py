import asyncio

from agents import trace
from dotenv import load_dotenv

from ai_agents.decision_agent.agent import run_decision_agent
from ai_agents.fundamental_scout.agent import run_fundamental_scout
from ai_agents.risk_analyst.agent import run_risk_analyst


async def main():
    load_dotenv()

    company_name = "NVIDIA"

    with trace("ai-investor-session"):
        fundamental_analysis = await run_fundamental_scout(
            company_name=company_name,
        )
        print("Fundamental Analysis:\n", fundamental_analysis)

        decision_result = await run_decision_agent(
            fundamental_analysis=fundamental_analysis,
        )
        print("Investment Decision:\n", decision_result)

        risk_analysis = await run_risk_analyst(
            fundamental_analysis=fundamental_analysis,
            investment_decision=decision_result,
        )
        print("Risk Analysis:\n", risk_analysis)


if __name__ == "__main__":
    asyncio.run(main())
