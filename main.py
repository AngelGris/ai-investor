import asyncio

from agents import custom_span, trace
from dotenv import load_dotenv

from ai_agents.decision_agent.agent import run_decision_agent
from ai_agents.fundamental_scout.agent import run_fundamental_scout
from ai_agents.opportunity_scout.agent import run_opportunity_scout
from ai_agents.portfolio_allocation.agent import run_portfolio_allocation
from ai_agents.risk_analyst.agent import run_risk_analyst


async def main():
    load_dotenv()

    universe_name = "NASDAQ-100"
    universe = [
        "AAPL",
        "MSFT",
        "NVDA",
        "AMZN",
        "META",
        "TSLA",
        "GOOGL",
        "AMD",
        "ASML",
        "INTC",
    ]

    with trace("ai-investor-session"):
        opportunity_results = await run_opportunity_scout(
            universe_name=universe_name,
            ticker_list=universe,
            max_candidates=3,
        )

        pipelines = [
            run_company_pipeline(
                ticker=candidate.ticker,
                company_name=candidate.company_name,
            )
            for candidate in opportunity_results.candidates
        ]

        pipeline_results = await asyncio.gather(*pipelines, return_exceptions=True)

        portfolio_allocation = await run_portfolio_allocation(
            risk_profiles=[result["risk_analysis"] for result in pipeline_results],
            investment_decisions=[
                result["investment_decision"] for result in pipeline_results
            ],
        )
        print("Final Portfolio Allocation:\n", portfolio_allocation)


async def run_company_pipeline(ticker: str, company_name: str):
    with custom_span(f"pipeline-candidate-{ticker}"):
        fundamental_analysis = await run_fundamental_scout(
            ticker=ticker,
            company_name=company_name,
        )

        risk_analysis = await run_risk_analyst(
            fundamental_analysis=fundamental_analysis,
        )

        decision_result = await run_decision_agent(
            fundamental_analysis=fundamental_analysis,
            risk_analysis=risk_analysis,
        )

    return {
        "ticker": ticker,
        "company_name": company_name,
        "fundamental_analysis": fundamental_analysis,
        "investment_decision": decision_result,
        "risk_analysis": risk_analysis,
    }


if __name__ == "__main__":
    asyncio.run(main())
