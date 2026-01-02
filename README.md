# AI Investor

`ai-investor` is a Python project that uses AI agents to analyze stocks based on **fundamental information**.
This learning project focuses on building structured, typed AI agents that produce reliable outputs.

The first agent implemented is **FundamentalScout**, which takes a company's financial summary and recent news to generate a structured fundamental thesis, including bull/bear cases, confidence, and expected horizon.

---

## Features

- Structured AI agent with **Pydantic schemas**
- Typed outputs for predictable downstream processing
- Pre-commit hooks for code formatting and linting
- Ready for future agents (technical analysis, risk evaluation, etc.)

---

## Project Structure

    ai-investor/
    ├── agents/
    │   └── fundamental_scout/
    │       ├── agent.py        # Main agent logic
    │       ├── schema.py       # Pydantic output schema
    │       └── prompt.py       # Prompt template
    ├── .env                    # API keys (not committed)
    ├── .gitignore
    ├── main.py                 # Example entrypoint
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
- Print a formatted JSON output with the company's thesis

Example output:

```bash
{
  "company_name": "NVIDIA",
  "thesis": "NVIDIA's growth is driven by AI workloads...",
  "bull_case": ["Strong AI chip demand", "High margins in data centers"],
  "bear_case": ["Customer concentration risk", "Supply chain constraints"],
  "confidence": 0.85,
  "horizon": "medium"
}
```

---

## Contribution Guidelines

- Use pre-commit hooks to ensure clean code
- Write Pydantic schemas for any new agent outputs
- Follow Python typing for functions
- Add tests for new functionality

---

## License

MIT License
