from typing import List

from agents import Agent, Runner

from ai_agents.opportunity_scout.prompt import build_prompt
from ai_agents.opportunity_scout.schema import OpportunityScoutOutput
from ai_agents.tools.brave_search import cached_get_search_results


async def run_opportunity_scout(
    ticker_list: List[str],
    portfolio_tickers: List[str],
    portfolio_value: float,
    cash_available: float,
    max_candidates: int = 10,
):
    prompt = build_prompt(
        ticker_list=ticker_list,
        portfolio_tickers=portfolio_tickers,
        portfolio_value=portfolio_value,
        cash_avilable=cash_available,
        max_candidates=max_candidates,
    )
    agent = Agent(
        name="Opportunity Scout",
        model="gpt-5-mini",
        tools=[cached_get_search_results],
        output_type=OpportunityScoutOutput,
    )

    result = await Runner.run(agent, prompt)

    return result.final_output
