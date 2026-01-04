import asyncio

from agents import trace
from dotenv import load_dotenv

from ai_agents.decision_agent.agent import run_decision_agent
from ai_agents.fundamental_scout.agent import run_fundamental_scout


async def main():
    load_dotenv()

    company_name = "NVIDIA"

    with trace("ai-investor-session"):
        fundamental_analysis = await run_fundamental_scout(
            company_name=company_name,
        )

        decision_result = await run_decision_agent(
            fundamental_analysis=fundamental_analysis,
        )
        decision_result_json = decision_result.model_dump_json(indent=2)

        print(decision_result_json)


if __name__ == "__main__":
    asyncio.run(main())
