from agents import Agent, Runner

from ai_agents.fundamental_scout.prompt import build_prompt
from ai_agents.fundamental_scout.schema import FundamentalScoutOutput
from ai_agents.tools.brave_search import (
    cached_get_company_overview,
    cached_get_latest_news,
)


async def run_fundamental_scout(ticker: str, company_name: str):
    prompt = build_prompt(ticker=ticker, company_name=company_name)
    agent = Agent(
        name="Fundamental Scout",
        model="gpt-5-mini",
        tools=[cached_get_company_overview, cached_get_latest_news],
        output_type=FundamentalScoutOutput,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
