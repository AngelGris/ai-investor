# AI Investor

`ai-investor` is a Python project that uses AI agents to analyze stocks.
This learning project focuses on building structured, typed AI agents that produce reliable outputs. **Should never be used as a tool for real investments.**

## Agents

### Opportunity Scout

**OpportunityScout** get a list of tickers to analyze and returns a list of candidates that a re worth
loking into. It uses search tools to gather information about the different companies.

_The Search engine tool uses a cache to keep previous results and avoid redundant API requests._

### Fundamental Scout

**FundamentalScout** recieves one of the companies from **OpportunityScoutt** and uses search engine tools to get the company's financial summary and recent news to generate a structured fundamental thesis, including bull/bear cases, confidence, and expected horizon.

### Risk Analyst

**RiskAnalyst** uses the report from **FundamentalScout** and does a risk analysis for the proposed company, retrieving valuable information like risk level, or stop loss.

### Decision Agent

**DecisionAgent** uses the reports from **FundamentalScout** and **RiskAnalyst** as input and generates a report indicating wheather the selected company is a good asset to invest in or not.

### Portfolio Allocation

With the data provided for the different selected companies, **PortfolioAllocation** puts it all together and generates
a report with companies to buy, and opportunities not to take, following some constrains.

---

## Features

- Structured AI agent with **Pydantic schemas**
- Typed outputs for predictable downstream processing
- Pre-commit hooks for code formatting and linting
- Extensible for future agents
- Runs pipelines asynchronously
- Protects tools that use API requests down to its allowed rate

---

## Project Structure

    ai-investor/
    ├── ai_agents/
    │   ├── decision_agent/
    │   │   ├── agent.py              # Main agent logic
    │   │   ├── schema.py             # Pydantic output schema
    │   │   └── prompt.py             # Prompt template
    │   ├── fundamental_scout/
    │   │   ├── agent.py
    │   │   ├── schema.py
    │   │   └── prompt.py
    │   ├── opportunity_scout/
    │   │   ├── agent.py
    │   │   ├── schema.py
    │   │   └── prompt.py
    │   ├── portfolio_allocation/
    │   │   ├── agent.py
    │   │   ├── schema.py
    │   │   └── prompt.py
    │   ├── risk_analyst/
    │   │   ├── agent.py
    │   │   ├── schema.py
    │   │   └── prompt.py
    │   └── tools/
    |       ├── rate_limiter.py       # Limits Brave search calls for async
    │       ├── brave_search.py       # Brave search engine tool
    │       └── cache.py              # Cache functions using Diskcache for persistance
    ├── .env                          # API keys (not committed)
    ├── .gitignore
    ├── main.py                       # Example entrypoint
    ├── pyproject.toml
    └── uv.lock

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone git@github.com:<USERNAME>/ai-investor.git
cd ai-investor
```

2. **Install dependencies using `uv`**

```bash
uv sync
```

3. **Set your OpenAI API key**

Create a .env file in the root folder:

```bash
OPENAI_API_KEY=sk-xxxxxx
BRAVE_API_KEY=xxxxxx
```

4. **Install pre-commit hooks**

```bash
pre-commit install
pre-commit run --all-files
```

## This ensures code is automatically formatted and checked before commits.

## Running the FundamentalScout Agent

You can test the agent using `main.py`:

```bash
uv run python main.py
```

It will:

- Load your .env API key
- Run the FundamentalScout agent
- Print a formatted JSON output with the analysis results

---

## Contribution Guidelines

- Use pre-commit hooks to ensure clean code
- Write Pydantic schemas for any new agent outputs
- Follow Python typing for functions
- Add tests for new functionality

---

## License

MIT License
