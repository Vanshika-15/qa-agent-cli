from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import RegressionImpact
from qa_agent.core.git_utils import get_diff, get_changed_files
from qa_agent.core.dependency_scanner import find_dependents


def run_regression_impact(base: str, console) -> None:
    """Analyze git changes plus their dependents to assess real regression impact."""

    console.print("[bold cyan]Reading changed files...[/bold cyan]")
    changed_files = get_changed_files(base)
    diff_content = get_diff(base)

    console.print(f"[dim]{len(changed_files)} file(s) changed: {', '.join(changed_files)}[/dim]")
    console.print("[bold cyan]Scanning codebase for dependent files...[/bold cyan]")

    dependents = find_dependents(changed_files)

    dependents_summary_lines = []
    for changed, deps in dependents.items():
        if deps:
            dependents_summary_lines.append(f"{changed} is referenced by: {', '.join(deps)}")
        else:
            dependents_summary_lines.append(f"{changed} has no detected dependents in the scanned codebase")
    dependents_summary = "\n".join(dependents_summary_lines)

    console.print("[bold cyan]Analyzing regression impact...[/bold cyan]\n")

    prompt = f"""You are a senior QA engineer assessing regression risk for a code change.
You have two sources of information:

1. The actual code diff (what changed)
2. A dependency scan showing which other files in the project reference the changed files

Use BOTH to assess not just what changed, but what ELSE could break as a result —
this is the core of regression testing: catching ripple effects, not just the
obvious direct change.

Code diff:
{diff_content}

Dependency scan results:
{dependents_summary}
"""

    try:
        result: RegressionImpact = ask_gemini_structured(prompt, RegressionImpact)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    console.print(f"[bold]Summary:[/bold] {result.summary}\n")
    console.print(f"[bold]Regression Risk:[/bold] {result.risk_level}\n")

    console.print("[bold underline]Directly Changed Areas[/bold underline]")
    for item in result.directly_changed_areas:
        console.print(f"  • {item}")
    console.print()

    console.print("[bold underline]Downstream Impact (Ripple Effects)[/bold underline]")
    if result.downstream_impact:
        for item in result.downstream_impact:
            console.print(f"  [yellow]⚠[/yellow] {item}")
    else:
        console.print("  (none identified)")
    console.print()

    console.print("[bold underline]Recommended Regression Test Scope[/bold underline]")
    for item in result.regression_test_scope:
        console.print(f"  • {item}")