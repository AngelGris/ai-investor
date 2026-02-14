from pathlib import Path

import pandas as pd

SP500_CSV_PATH = Path("data/universe/sp500.csv")


def load_sp500_universe() -> pd.DataFrame:
    """
    Load the S&P 500 universe from CSV.

    Returns a pandas DataFrame with columns:
    - ticker
    - company
    - sector
    - sub_industry
    """
    if not SP500_CSV_PATH.exists():
        raise FileNotFoundError(
            f"S&P 500 universe file not found at {SP500_CSV_PATH}. "
            "Run scripts/fetch_sp500_universe.py first."
        )

    df = pd.read_csv(SP500_CSV_PATH)

    # Basic sanity checks
    required_columns = {"ticker", "company", "sector", "sub_industry"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in universe CSV: {missing}")

    # Normalize tickers (defensive)
    df["ticker"] = df["ticker"].str.strip().str.upper()

    return df


def load_sp500_tickers() -> list[str]:
    df = load_sp500_universe()
    return df["ticker"].tolist()
