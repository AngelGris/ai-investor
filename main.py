from dotenv import load_dotenv

from agents.fundamental_scout.agent import run_fundamental_scout


def main():
    load_dotenv()

    output = run_fundamental_scout(
        company_name="NVIDIA",
        financial_summary="""
NVIDIA designs GPUs and AI accelerators.
Revenue growth driven by data centers and AI workloads.
High margins but customer concentration risk.
""",
        recent_news="""
NVIDIA announced new AI chips targeting inference workloads.
Major cloud providers increased long-term partnerships.
""",
    )

    print(output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
