from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import CoverageGap
from qa_agent.core.file_utils import read_test_files


def run_coverage_gap(requirement: str, test_dir: str, console) -> None:
    """Compare a requirement against existing test files to find coverage gaps."""

    console.print(f"[bold cyan]Reading test files from {test_dir}...[/bold cyan]")

    try:
        existing_tests = read_test_files(test_dir)
    except ValueError as e:
        console.print(f"[bold red]✗ {e}[/bold red]")
        raise

    console.print("[bold cyan]Comparing against requirement...[/bold cyan]\n")

    prompt = f"""You are a senior QA engineer assessing test coverage. Compare the
requirement below against the existing test files. Identify what's already covered,
what's genuinely missing, and suggest specific new tests to close the gaps.

Do not suggest tests that are already effectively covered by the existing files,
even if worded differently.

Requirement:
{requirement}

Existing test files:
{existing_tests}
"""

    try:
        result: CoverageGap = ask_gemini_structured(prompt, CoverageGap)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    console.print(f"[bold]Coverage Estimate:[/bold] {result.coverage_estimate}\n")

    console.print("[bold underline]Already Covered[/bold underline]")
    for item in result.already_covered:
        console.print(f"  [green]✓[/green] {item}")
    console.print()

    console.print("[bold underline]Coverage Gaps[/bold underline]")
    for item in result.coverage_gaps:
        console.print(f"  [red]✗[/red] {item}")
    console.print()

    console.print("[bold underline]Suggested New Tests[/bold underline]")
    for item in result.suggested_new_tests:
        console.print(f"  • {item}")