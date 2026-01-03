import os
from time import sleep

import requests
from agents import function_tool


def brave_search(query: str, limit: int = 5) -> list[dict]:
    """
    Perform a Brave Search query and return top results.

    Args:
        query (str): Search query string
        limit (int): Number of results to return

    Returns:
        List of dicts with 'title', 'url', 'snippet'
    """
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

    HEADERS = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": BRAVE_API_KEY,
    }

    params = {"q": query, "count": limit}  # number of results

    sleep(1)  # To respect rate limits
    print(f"Brave Search Query: {query}")
    response = requests.get(BRAVE_SEARCH_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("webPages", {}).get("value", []):
        results.append(
            {
                "title": item.get("name"),
                "url": item.get("url"),
                "snippet": item.get("snippet"),
            }
        )

    return results


@function_tool
def get_company_overview(company_name: str) -> str:
    """
    Get a short company overview from Brave Search results.
    """
    query = f"{company_name} company overview financials business model"
    results = brave_search(query, limit=3)

    # Combine snippets
    overview_text = " ".join([r["snippet"] for r in results])
    return overview_text


@function_tool
def get_latest_news(company_name: str) -> str:
    """
    Get recent news headlines about the company.
    """
    query = f"{company_name} latest news"
    results = brave_search(query, limit=5)

    news_text = "\n".join([f"{r['title']}: {r['snippet']}" for r in results])
    return news_text
