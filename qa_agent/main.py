import typer
from rich.console import Console

from qa_agent.agents.test_case_generator import run_generate
from qa_agent.agents.pr_analyzer import run_analyze

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


if __name__ == "__main__":
    app()