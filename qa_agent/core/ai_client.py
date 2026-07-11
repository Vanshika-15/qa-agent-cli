import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_client():
    """Create (or reuse) a single Gemini client instance."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
        _client = genai.Client(api_key=api_key)
    return _client


def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    client = get_client()
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )
    return response.text


def ask_gemini_structured(prompt: str, schema):
    """
    Send a prompt to Gemini and get back a response matching the given
    Pydantic schema, instead of free-form text.
    """
    client = get_client()
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
        },
    )
    return response.parsed