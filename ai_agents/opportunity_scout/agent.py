from typing import List

from agents import Agent, Runner

from ai_agents.opportunity_scout.prompt import build_prompt
from ai_agents.opportunity_scout.schema import OpportunityScoutOutput
from ai_agents.tools.brave_search import cached_get_search_results


async def run_opportunity_scout(
    universe_name: str, ticker_list: List[str], max_candidates: int = 10
):
    prompt = build_prompt(
        universe_name=universe_name,
        ticker_list=ticker_list,
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
