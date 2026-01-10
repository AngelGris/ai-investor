def build_prompt(fundamental_analysis, risk_analysis) -> list[dict[str, str]]:
    system_prompt = """
You are an investment decision agent.

Your task is to evaluate a company based solely on the provided
FundamentalAnalysis data.

Rules:
- Do NOT use external knowledge.
- Do NOT request tools.
- Base your judgment only on the given information.
- Be decisive, but acknowledge uncertainty.
- Optimize for a short-term aggressive investor profile.
- Prefer clarity over verbosity.
"""
    user_prompt = f"""
Given the following FundamentalAnalysis and RiskAnalysis, produce an InvestmentDecision.

FundamentalAnalysis:
{fundamental_analysis}

RiskAnalysis:
{risk_analysis}
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
