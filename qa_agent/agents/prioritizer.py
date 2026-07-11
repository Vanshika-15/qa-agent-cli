from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import PrioritizationResult


def run_prioritize(test_cases: str, context: str, console) -> None:
    """Rank a list of test cases by risk/priority."""

    console.print("[bold cyan]Prioritizing test cases...[/bold cyan]\n")

    context_line = f"\nAdditional context (e.g. time constraints, release notes): {context}\n" if context else ""

    prompt = f"""You are a senior QA lead deciding what to test when there isn't time
to run everything. Given the following test cases, assign each a priority:
- P0: must run, high risk of critical failure or business impact if skipped
- P1: should run if time allows
- P2: nice to have, low risk if skipped

Be decisive and realistic — not everything can be P0.
{context_line}
Test cases:
{test_cases}
"""

    try:
        result: PrioritizationResult = ask_gemini_structured(prompt, PrioritizationResult)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    priority_colors = {"P0": "bold red", "P1": "bold yellow", "P2": "dim"}

    for item in result.prioritized_tests:
        color = priority_colors.get(item.priority, "white")
        console.print(f"[{color}]{item.priority}[/{color}]  {item.test_case}")
        console.print(f"      [dim]→ {item.reasoning}[/dim]")

    console.print("\n[bold underline]If Time is Very Limited, Run At Minimum[/bold underline]")
    for item in result.recommended_minimum:
        console.print(f"  • {item}")