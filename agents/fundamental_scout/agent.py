from openai import OpenAI

from .prompt import build_prompt
from .schema import FundamentalScoutOutput


def run_fundamental_scout(
    company_name: str,
    financial_summary: str,
    recent_news: str,
) -> FundamentalScoutOutput:
    client = OpenAI()

    prompt = build_prompt(
        company_name=company_name,
        financial_summary=financial_summary,
        recent_news=recent_news,
    )

    response = client.responses.parse(
        model="gpt-5",
        input=prompt,
        text_format=FundamentalScoutOutput,
    )

    return response.output_parsed
