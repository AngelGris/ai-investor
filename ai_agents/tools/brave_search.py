import json
import os

import httpx
from agents import function_tool

from ai_agents.tools.brave_rate_limiter import brave_limiter
from ai_agents.tools.cache import cached_function_tool


async def brave_search(
    query: str, limit: int = 5, result_filter: list[str] = None
) -> list[dict]:
    """
    Perform a Brave Search query and return top results.

    Args:
        query (str): Search query string
        limit (int): Number of results to return

    Returns:
        List of dicts with 'title', 'url', 'descrition', 'page_age'
    """
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

    HEADERS = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": BRAVE_API_KEY,
    }

    if result_filter is None:
        result_filter = ["web"]

    params = {
        "q": query,
        "count": limit,
        "result_filter": ",".join(result_filter),
    }

    print(f"Brave Search Query: {query}", flush=True)
    async with brave_limiter:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                BRAVE_SEARCH_URL,
                headers=HEADERS,
                params=params,
            )
    response.raise_for_status()
    data = response.json()

    results = []

    for filter in result_filter:
        filter_results = data.get(filter, {}).get("results", [])
        for item in filter_results:
            results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "description": item.get("description"),
                    "page_age": item.get("page_age"),
                }
            )
    return results


@function_tool
async def get_company_overview(company_name: str) -> str:
    """
    Get a short company overview from Brave Search results.
    """
    query = f"{company_name} company overview financials business model"
    results = await brave_search(query, limit=3)

    return json.dumps(results, indent=2)


@function_tool
async def get_latest_news(company_name: str) -> str:
    """
    Get recent news headlines about the company.
    """
    query = f"{company_name} latest news"
    results = await brave_search(query, limit=10)

    return json.dumps(results, indent=2)


@function_tool
async def get_seach_results(query: str, limit: int = 20) -> str:
    """
    Get search results for a given query.
    """
    results = await brave_search(query, limit=limit)

    return json.dumps(results, indent=2)


cached_get_company_overview = cached_function_tool(
    tool=get_company_overview, ttl=12 * 3600
)  # Cache for 12 hours
cached_get_latest_news = cached_function_tool(
    tool=get_latest_news, ttl=1 * 3600
)  # Cache for 1 hour
cached_get_search_results = cached_function_tool(
    tool=get_seach_results, ttl=6 * 3600
)  # Cache for 6 hours
