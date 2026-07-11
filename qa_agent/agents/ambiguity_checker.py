from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import AmbiguityCheck


def run_ambiguity_check(requirement: str, console) -> None:
    """Analyze a requirement for ambiguity and missing details before development starts."""

    console.print("[bold cyan]Checking for ambiguity...[/bold cyan]\n")

    prompt = f"""You are a senior QA engineer reviewing a requirement BEFORE development
starts, in a refinement/grooming session. Your job is to catch vague or incomplete
statements that would otherwise lead to bugs, missed edge cases, or rework later.

Be specific and concrete — point to exact phrases that are ambiguous, don't make
generic statements. If the requirement is genuinely clear and complete, say so honestly
rather than inventing issues.

Requirement:
{requirement}
"""

    try:
        result: AmbiguityCheck = ask_gemini_structured(prompt, AmbiguityCheck)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    console.print(f"[bold]Clarity:[/bold] {result.clarity_score}\n")

    console.print("[bold underline]Ambiguous Points[/bold underline]")
    if result.ambiguous_points:
        for item in result.ambiguous_points:
            console.print(f"  • {item}")
    else:
        console.print("  (none found)")
    console.print()

    console.print("[bold underline]Missing Details[/bold underline]")
    if result.missing_details:
        for item in result.missing_details:
            console.print(f"  • {item}")
    else:
        console.print("  (none found)")
    console.print()

    console.print("[bold underline]Clarifying Questions to Ask[/bold underline]")
    for item in result.clarifying_questions:
        console.print(f"  • {item}")
    console.print()

    console.print("[bold underline]Risky Assumptions if Left Unclarified[/bold underline]")
    for item in result.assumptions_if_unclarified:
        console.print(f"  • {item}")