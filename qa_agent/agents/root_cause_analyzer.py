from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import RootCauseAnalysis
from qa_agent.core.code_search import find_relevant_code


def run_root_cause(error_text: str, console) -> None:
    """Analyze an error/stack trace/bug description and hypothesize root causes."""

    console.print("[bold cyan]Scanning codebase for relevant files...[/bold cyan]")
    relevant_code = find_relevant_code(error_text)

    console.print("[bold cyan]Analyzing root cause...[/bold cyan]\n")

    prompt = f"""You are a senior QA/debugging engineer investigating a bug, error, or
test failure. Use the error information AND any relevant code provided below to
hypothesize the most likely root cause(s). Be specific and grounded — if the code
doesn't give you enough to be confident, say so honestly (Low confidence) rather
than guessing generically.

Error / failure description:
{error_text}

Relevant code found in the project:
{relevant_code}
"""

    try:
        result: RootCauseAnalysis = ask_gemini_structured(prompt, RootCauseAnalysis)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    console.print(f"[bold]Confidence:[/bold] {result.confidence}\n")

    console.print("[bold underline]Likely Causes[/bold underline]")
    for i, item in enumerate(result.likely_causes, start=1):
        console.print(f"  {i}. {item}")
    console.print()

    console.print("[bold underline]Affected Code Areas[/bold underline]")
    for item in result.affected_code_areas:
        console.print(f"  • {item}")
    console.print()

    console.print("[bold underline]Debugging Steps[/bold underline]")
    for item in result.debugging_steps:
        console.print(f"  • {item}")
    console.print()

    console.print("[bold underline]Test Gaps This Reveals[/bold underline]")
    if result.related_test_gaps:
        for item in result.related_test_gaps:
            console.print(f"  • {item}")
    else:
        console.print("  (none identified)")