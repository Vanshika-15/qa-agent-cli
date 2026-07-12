# QA Agent CLI

AI-powered command-line assistant for QA Engineers — automates requirement analysis, test case generation, regression risk assessment, and root-cause investigation using LLMs (Gemini, with pluggable support for other providers).

Unlike a generic AI chatbot, QA Agent CLI grounds its analysis in **your actual project**: it reads real git diffs, scans your codebase for dependent files, compares against your existing test suite, and pulls real code into error diagnosis — instead of generating generic, one-size-fits-all output.

## Why this exists

Manually analyzing requirements, writing test cases, assessing regression risk, and investigating bugs are repetitive tasks that eat into a QA engineer's time. QA Agent CLI automates the first draft of each of these, so you spend your time on judgment calls instead of blank-page work.

## Features

| Command | What it does |
|---|---|
| `generate` | Generate test cases (positive/negative/edge) from a requirement |
| `analyze` | Structured QA risk report from a requirement, PR description, **or live git diff** |
| `ambiguity-check` | Flags vague/missing requirement details *before* development starts |
| `bug-report` | Turns a rough bug description into a properly structured ticket |
| `prioritize` | Ranks test cases by risk (P0/P1/P2) when time is limited |
| `coverage-gap` | Compares a requirement against your **existing test files** to find real gaps |
| `api-spec` | Generates API test cases grounded in a real OpenAPI/Swagger spec |
| `regression-impact` | Scans your codebase for files that depend on what changed, for real ripple-effect analysis |
| `root-cause` | Investigates an error/stack trace using the **actual referenced code** from your project |

## What makes this different from asking ChatGPT

Most "AI test case generators" are a single prompt wrapped in a UI. This tool instead:
- Reads live `git diff` output directly — no copy-pasting code changes
- Scans your actual codebase to find which files depend on what changed (`regression-impact`)
- Reads your real test files to find genuine coverage gaps, not duplicate suggestions (`coverage-gap`)
- Pulls the actual source code referenced in a stack trace into the analysis (`root-cause`)
- Returns **structured, typed data** (via Pydantic schemas), not free-form text — so output is consistent and exportable

## Installation

Requires Python 3.12+ (tested on 3.14).

```bash
git clone https://github.com/YOUR-USERNAME/qa-agent-cli.git
cd qa-agent-cli
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Setup

Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey), then:

```bash
cp .env.example .env
# edit .env and add your key:
# GEMINI_API_KEY=your_key_here
```

## Usage

```bash
# Generate test cases from a requirement
python3 -m qa_agent.main generate "User should be able to reset password via email"

# Analyze your current uncommitted changes for QA risk
python3 -m qa_agent.main analyze --from-git

# Save the analysis as a shareable report
python3 -m qa_agent.main analyze --from-git --save report.md

# Catch ambiguous requirements before dev starts
python3 -m qa_agent.main ambiguity-check "Users can upload a profile picture"

# Structure a rough bug report
python3 -m qa_agent.main bug-report "checkout button sometimes does nothing"

# Prioritize tests under time pressure
python3 -m qa_agent.main prioritize "login, checkout, footer text, password reset" --context "2 hours before release"

# Find real coverage gaps against your existing tests
python3 -m qa_agent.main coverage-gap "login with account lockout after 5 attempts" --test-dir tests

# Generate API tests from a real spec
python3 -m qa_agent.main api-spec examples/sample_api_spec.json

# Full regression impact analysis (diff + dependency graph)
python3 -m qa_agent.main regression-impact

# Investigate an error using real project code
python3 -m qa_agent.main root-cause "ModuleNotFoundError: No module named 'qa_agent.core.git_utils'"
```

See `python3 -m qa_agent.main --help` for the full command list, and `<command> --help` for options.

## Example output

See [`examples/sample_report.md`](examples/sample_report.md) for a real generated analysis report.

## Tech stack

- **Python 3.12+**
- **Typer** — CLI framework
- **Rich** — terminal formatting
- **Pydantic** — structured, validated AI output
- **Google Gemini API** (`google-genai`) — LLM backend
- **python-dotenv** — configuration

## Architecture
qa_agent/
├── main.py              # CLI command wiring (thin layer)
├── agents/               # One file per AI agent — the actual QA logic
│   ├── test_case_generator.py
│   ├── pr_analyzer.py
│   ├── ambiguity_checker.py
│   ├── bug_reporter.py
│   ├── prioritizer.py
│   ├── coverage_checker.py
│   ├── api_spec_analyzer.py
│   ├── regression_analyzer.py
│   └── root_cause_analyzer.py
└── core/                 # Shared infrastructure
├── ai_client.py       # Gemini API wrapper
├── schemas.py          # Pydantic output schemas
├── git_utils.py        # Git diff/changed-files helpers
├── file_utils.py        # Test/spec file reading
├── dependency_scanner.py # Codebase dependency detection
└── code_search.py        # Error-to-code matching


New agents follow a consistent pattern: define a Pydantic schema → write a prompt → wire a CLI command. This makes the codebase easy to extend with new agents.

## Roadmap

- [ ] Local run history / project memory
- [ ] Support for additional LLM providers (Claude, OpenAI)
- [ ] Direct URL fetching for OpenAPI specs
- [ ] Generate runnable automation code (Playwright/pytest) from test cases
- [ ] CI/CD integration (pre-commit / PR bot mode)

## License

MIT