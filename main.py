import asyncio

from dotenv import load_dotenv

from ai_agents.fundamental_scout.agent import run_fundamental_scout


async def main():
    load_dotenv()

    company_name = "NVIDIA"

    output = await run_fundamental_scout(
        company_name=company_name,
    )

    print(output.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
