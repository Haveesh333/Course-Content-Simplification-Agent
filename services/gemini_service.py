"""
gemini_service.py
Calls the Google Gemini REST API (generateContent) and returns the generated text.

This is a development/testing provider. Set AI_PROVIDER=gemini and supply
GEMINI_API_KEY in .env to use it. IBM Granite remains the primary project provider.
"""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Anchor load_dotenv() to backend/.env regardless of where uvicorn is launched from.
# __file__ is  …/backend/services/gemini_service.py  → parent.parent is  …/backend/
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

# ---------------------------------------------------------------------------
# Environment configuration — read lazily inside generate() so they always
# reflect the values actually loaded from .env, not an empty pre-load state.
# ---------------------------------------------------------------------------
_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


# ---------------------------------------------------------------------------
# Custom exception — carries the upstream HTTP status so the router can
# forward a meaningful status code instead of always returning 500.
# ---------------------------------------------------------------------------

class GeminiAPIError(Exception):
    """Raised when the Gemini API returns a non-200 response."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def generate(prompt: str) -> str:
    """
    Call the Google Gemini generateContent endpoint and return the text response.

    Parameters
    ----------
    prompt : str
        The complete prompt string (built by prompt_builder.build_prompt).

    Returns
    -------
    str
        The raw text content from the first candidate's first part.

    Raises
    ------
    RuntimeError
        If GEMINI_API_KEY is missing or the response shape is unexpected.
    GeminiAPIError
        If the Gemini API returns a non-200 HTTP status.
    """
    # Read at call-time so they are always resolved after .env is loaded.
    api_key = os.getenv("GEMINI_API_KEY", "")
    model_id = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to your backend/.env file before using the Gemini provider."
        )

    url = f"{_BASE_URL}/{model_id}:generateContent"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 2048,
            "temperature": 0.3,
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120.0,
        )

    if response.status_code != 200:
        # Extract a safe error message from the response body without
        # echoing the API key or any internal secrets.
        try:
            err_body = response.json()
            safe_message = (
                err_body.get("error", {}).get("message", "Unknown Gemini API error")
            )
        except Exception:
            safe_message = "Gemini API returned an unexpected error response."

        raise GeminiAPIError(
            status_code=response.status_code,
            message=f"Gemini API error [{response.status_code}]: {safe_message}",
        )

    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Unexpected response shape from Gemini: {result}"
        ) from exc
