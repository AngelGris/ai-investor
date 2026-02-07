def build_prompt(
    ticker: str,
    fundamental_analysis: str,
    risk_analysis: str,
    cash: float,
    positions_summary: str,
) -> list[dict[str, str]]:
    system_prompt = """
You are a portfolio-aware investment decision agent.

Your role is to decide what ACTION to take for a specific stock
given both:
- the company analysis provided
- the current portfolio state

You do NOT decide position sizes.
You do NOT override risk limits.
You do NOT simulate trades.
You do NOT fetch new information.

Your responsibility is to recommend ONE clear portfolio action:
- initiate: open a new position
- add: increase an existing position
- hold: keep the position unchanged
- reduce: decrease exposure
- exit: fully close the position
- avoid: do not open a position

Your decision must explicitly consider:
- whether the stock is already held
- existing exposure to the company or sector
- portfolio concentration and diversification
- current capital usage and opportunity cost

Guiding principles:
- Decisions are about CHANGES, not static opinions
- Existing positions require justification to add or exit
- Avoid redundant exposure unless conviction is high
- Capital preservation is more important than idea quantity
- Doing nothing (hold / avoid) is a valid and often correct decision

When information is mixed or uncertain, prefer HOLD or AVOID
over aggressive actions.

Your output must strictly follow the InvestmentDecisionOutput schema.
"""
    user_prompt = f"""
You are evaluating the following stock in the context of an existing portfolio.

Ticker:
{ticker}

Company analysis:
{fundamental_analysis}

Risk assessment:
{risk_analysis}

Current portfolio state (summary):
- Available cash: {cash}
- Current positions:
{positions_summary}

Based ONLY on the information above:

- Decide the most appropriate portfolio action for this stock
- Explicitly consider whether the stock is already held
- Explain how the current portfolio influenced your decision
- Do NOT suggest position sizes or allocation percentages
- Do NOT repeat the analysis verbatim

Return a single InvestmentDecisionOutput.

"""

    return [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]
