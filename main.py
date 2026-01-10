import asyncio

from agents import custom_span, trace
from dotenv import load_dotenv

from ai_agents.decision_agent.agent import run_decision_agent
from ai_agents.fundamental_scout.agent import run_fundamental_scout
from ai_agents.opportunity_scout.agent import run_opportunity_scout
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
        with custom_span("opportunity-scout"):
            opportunity_results = await run_opportunity_scout(
                universe_name=universe_name,
                ticker_list=universe,
                max_candidates=3,
            )
            print("Opportunity Scout Results:\n", opportunity_results)

        pipelines = [
            run_company_pipeline(
                ticker=candidate.ticker,
                company_name=candidate.company_name,
            )
            for candidate in opportunity_results.candidates
        ]

        results = await asyncio.gather(*pipelines, return_exceptions=True)

    for res in results:
        print("\n==============================\n")
        print(f"Ticker: {res['ticker']}")
        print("Decision:")
        print(res["investment_decision"].model_dump_json(indent=2))


async def run_company_pipeline(ticker: str, company_name: str):
    with custom_span(f"pipeline-candidate-{ticker}"):
        with custom_span("fundamental-scout"):
            fundamental_analysis = await run_fundamental_scout(
                ticker=ticker,
                company_name=company_name,
            )
            print(
                f"Fundamental Analysis for {company_name} [{ticker}]:\n",
                fundamental_analysis,
            )

        with custom_span("risk-analyst"):
            risk_analysis = await run_risk_analyst(
                fundamental_analysis=fundamental_analysis,
            )
            print(f"Risk Analysis for {company_name} [{ticker}]:\n", risk_analysis)

        with custom_span("decision-agent"):
            decision_result = await run_decision_agent(
                fundamental_analysis=fundamental_analysis,
                risk_analysis=risk_analysis,
            )
            print(
                f"Investment Decision for {company_name} [{ticker}]:\n", decision_result
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
