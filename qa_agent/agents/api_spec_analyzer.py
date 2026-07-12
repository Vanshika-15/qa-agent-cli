from qa_agent.core.ai_client import ask_gemini_structured
from qa_agent.core.schemas import APITestSuite
from qa_agent.core.file_utils import read_spec_file


def run_api_spec(spec_path: str, console) -> None:
    """Generate API test cases from an OpenAPI/Swagger spec file."""

    console.print(f"[bold cyan]Reading spec from {spec_path}...[/bold cyan]")

    try:
        spec_content = read_spec_file(spec_path)
    except ValueError as e:
        console.print(f"[bold red]✗ {e}[/bold red]")
        raise

    console.print("[bold cyan]Generating API test cases...[/bold cyan]\n")

    prompt = f"""You are a senior QA engineer specializing in API testing. Given the
following OpenAPI/Swagger specification, generate a thorough set of API test cases.

Cover, for each significant endpoint:
- Positive cases (valid request → expected success)
- Negative cases (invalid payloads, missing required fields, wrong types)
- Auth/permission cases (missing/invalid tokens, insufficient permissions)
- Boundary/validation cases (field length limits, invalid enums, etc.)

Ground every test case in the ACTUAL endpoints, methods, and schemas in the spec —
do not invent endpoints that aren't present.

API Spec:
{spec_content}
"""

    try:
        result: APITestSuite = ask_gemini_structured(prompt, APITestSuite)
    except ValueError as e:
        console.print(f"[bold red]✗ Configuration error:[/bold red] {e}")
        raise
    except Exception as e:
        console.print(f"[bold red]✗ Could not reach Gemini:[/bold red] {e}")
        console.print("[dim]Check your internet connection and API key in .env[/dim]")
        raise

    for tc in result.test_cases:
        console.print(f"[bold cyan]{tc.endpoint}[/bold cyan]  [dim](expect {tc.expected_status})[/dim]")
        console.print(f"  {tc.scenario}")
        if tc.notes:
            console.print(f"  [dim]→ {tc.notes}[/dim]")
        console.print()

    console.print("[bold underline]Risk Areas Worth Extra Attention[/bold underline]")
    for item in result.untested_risk_areas:
        console.print(f"  • {item}")