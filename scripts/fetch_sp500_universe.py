#!/usr/bin/env python3

from pathlib import Path

import pandas as pd
import requests

WIKIPEDIA_SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
OUTPUT_PATH = Path("data/universe/sp500.csv")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def main():
    print("Fetching S&P 500 constituents from Wikipedia...")

    response = requests.get(WIKIPEDIA_SP500_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    # Parse tables from HTML content
    tables = pd.read_html(response.text)
    sp500_table = tables[0]

    # Normalize column names
    sp500_table = sp500_table.rename(
        columns={
            "Symbol": "ticker",
            "Security": "company",
            "GICS Sector": "sector",
            "GICS Sub-Industry": "sub_industry",
        }
    )

    # Clean ticker symbols (BRK.B -> BRK-B)
    sp500_table["ticker"] = (
        sp500_table["ticker"].str.strip().str.replace(".", "-", regex=False)
    )

    # Keep relevant columns only
    sp500_table = sp500_table[["ticker", "company", "sector", "sub_industry"]]

    # Sort for deterministic output
    sp500_table = sp500_table.sort_values("ticker").reset_index(drop=True)

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save CSV
    sp500_table.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {len(sp500_table)} tickers to {OUTPUT_PATH.resolve()}")
    print("\nPreview:")
    print(sp500_table.head(10))


if __name__ == "__main__":
    main()
