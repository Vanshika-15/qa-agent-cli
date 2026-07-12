import typer
from rich.console import Console

from qa_agent.agents.test_case_generator import run_generate
from qa_agent.agents.pr_analyzer import run_analyze
from qa_agent.agents.ambiguity_checker import run_ambiguity_check
from qa_agent.agents.bug_reporter import run_bug_report
from qa_agent.agents.prioritizer import run_prioritize
from qa_agent.agents.coverage_checker import run_coverage_gap
from qa_agent.agents.api_spec_analyzer import run_api_spec

app = typer.Typer()
console = Console()


@app.command()
def hello(name: str = "QA Engineer"):
    """Say hello to someone by name."""
    print(f"Hello, {name}! Welcome to QA Agent CLI.")


@app.command()
def generate(requirement: str):
    """Generate test cases from a requirement description."""
    try:
        run_generate(requirement, console)
    except Exception:
        raise typer.Exit(code=1)


@app.command()
def analyze(
    description: str = typer.Argument(
        None, help="A PR description or requirement to analyze."
    ),
    from_git: bool = typer.Option(
        False, "--from-git", help="Pull the description automatically from your git diff."
    ),
    base: str = typer.Option(
        None, "--base", help="Branch to diff against (e.g. main). Omit to diff uncommitted changes."
    ),
    save: str = typer.Option(
        None, "--save", help="Save the report to a markdown file (provide a filename, e.g. report.md)."
    ),
):
    """Analyze a PR description, requirement, or git diff and produce a structured QA report."""
    try:
        run_analyze(description, from_git, base, save, console)
    except Exception:
        raise typer.Exit(code=1)

@app.command()
def ambiguity_check(requirement: str):
    """Check a requirement for ambiguity and missing details before development starts."""
    try:
        run_ambiguity_check(requirement, console)
    except Exception:
        raise typer.Exit(code=1)


@app.command()
def bug_report(description: str):
    """Turn a rough bug description into a properly structured bug report."""
    try:
        run_bug_report(description, console)
    except Exception:
        raise typer.Exit(code=1)


@app.command()
def prioritize(
    test_cases: str = typer.Argument(..., help="Test cases to prioritize (paste a list, comma or newline separated)."),
    context: str = typer.Option(None, "--context", help="Optional context, e.g. 'only 2 hours before release'."),
):
    """Rank test cases by priority when there isn't time to run everything."""
    try:
        run_prioritize(test_cases, context, console)
    except Exception:
        raise typer.Exit(code=1)


@app.command()
def coverage_gap(
    requirement: str = typer.Argument(..., help="The requirement to check coverage for."),
    test_dir: str = typer.Option("tests", "--test-dir", help="Directory containing existing test files."),
):
    """Compare a requirement against your existing test suite to find gaps."""
    try:
        run_coverage_gap(requirement, test_dir, console)
    except Exception:
        raise typer.Exit(code=1)

@app.command()
def api_spec(
    spec_path: str = typer.Argument(..., help="Path to an OpenAPI/Swagger spec file (JSON or YAML)."),
):
    """Generate API test cases from an OpenAPI/Swagger spec file."""
    try:
        run_api_spec(spec_path, console)
    except Exception:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()