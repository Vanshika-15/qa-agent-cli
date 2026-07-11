from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import BugReport


def run_bug_report(description: str, console) -> None:
    """Turn a rough bug description into a properly structured bug report."""

    console.print("[bold cyan]Structuring bug report...[/bold cyan]\n")

    prompt = f"""You are a senior QA engineer turning a rough, informal bug description
into a properly structured bug report suitable for a ticket. Make reasonable, clearly
labeled inferences where the description is incomplete, but don't invent specific
technical details that weren't implied.

Rough description:
{description}
"""

    try:
        result: BugReport = ask_gemini_structured(prompt, BugReport)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    console.print(f"[bold]Title:[/bold] {result.title}")
    console.print(f"[bold]Severity:[/bold] {result.severity}\n")

    console.print("[bold underline]Steps to Reproduce[/bold underline]")
    for i, step in enumerate(result.steps_to_reproduce, start=1):
        console.print(f"  {i}. {step}")
    console.print()

    console.print(f"[bold underline]Expected Result[/bold underline]\n  {result.expected_result}\n")
    console.print(f"[bold underline]Actual Result[/bold underline]\n  {result.actual_result}\n")

    console.print("[bold underline]Environment to Capture[/bold underline]")
    for item in result.environment_notes:
        console.print(f"  • {item}")
    console.print()

    console.print(f"[bold underline]Possible Root Cause[/bold underline]\n  {result.possible_root_cause}")