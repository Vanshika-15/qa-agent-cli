from rich.markdown import Markdown

from qa_agent.core.ai_client import ask_gemini


def run_generate(requirement: str, console) -> None:
    """Generate test cases from a requirement description and print them."""
    console.print("[bold cyan]Generating test cases...[/bold cyan]")

    prompt = f"""You are a senior QA engineer. Given the following requirement,
generate a well-structured list of test cases. Include positive, negative,
and edge cases. Format as a numbered markdown list with clear titles.

Requirement: {requirement}
"""

    try:
        result = ask_gemini(prompt)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    console.print(Markdown(result))