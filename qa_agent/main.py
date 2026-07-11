import typer
from rich.console import Console
from rich.markdown import Markdown

from qa_agent.core.ai_client import ask_gemini, ask_gemini_structured
from qa_agent.core.schemas import QAAnalysis
from qa_agent.core.git_utils import get_diff

app = typer.Typer()
console = Console()


@app.command()
def hello(name: str = "QA Engineer"):
    """Say hello to someone by name."""
    print(f"Hello, {name}! Welcome to QA Agent CLI.")


@app.command()
def generate(requirement: str):
    """Generate test cases from a requirement description."""
    console.print("[bold cyan]Generating test cases...[/bold cyan]")

    prompt = f"""You are a senior QA engineer. Given the following requirement,
generate a well-structured list of test cases. Include positive, negative,
and edge cases. Format as a numbered markdown list with clear titles.

Requirement: {requirement}
"""

    result = ask_gemini(prompt)
    console.print(Markdown(result))


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
):
    """Analyze a PR description, requirement, or git diff and produce a structured QA report."""

    if from_git:
        console.print("[bold cyan]Reading git diff...[/bold cyan]")
        description = get_diff(base)
    elif not description:
        console.print("[bold red]Error:[/bold red] Provide a description, or use --from-git.")
        raise typer.Exit(code=1)

    console.print("[bold cyan]Analyzing...[/bold cyan]\n")

    prompt = f"""You are a senior QA engineer reviewing a pull request or requirement
description before it goes to testing. Analyze it carefully and identify concrete,
specific risks — avoid generic or obvious statements.

If this looks like a raw git diff (code changes), infer the functional impact
from the code itself, not just literal file names.

PR/Requirement description or diff:
{description}
"""

    result: QAAnalysis = ask_gemini_structured(prompt, QAAnalysis)

    console.print(f"[bold]Summary:[/bold] {result.summary}\n")
    console.print(f"[bold]Risk Level:[/bold] {result.risk_level}\n")

    console.print("[bold underline]What to Verify[/bold underline]")
    for item in result.what_to_verify:
        console.print(f"  • {item}")
    console.print()

    console.print("[bold underline]APIs / Services Changed[/bold underline]")
    if result.apis_changed:
        for item in result.apis_changed:
            console.print(f"  • {item}")
    else:
        console.print("  (none identified)")
    console.print()

    console.print("[bold underline]Regression Risk Areas[/bold underline]")
    for item in result.regression_risk_areas:
        console.print(f"  • {item}")
    console.print()

    console.print("[bold underline]Smoke Tests to Run[/bold underline]")
    for item in result.smoke_tests:
        console.print(f"  • {item}")


if __name__ == "__main__":
    app()