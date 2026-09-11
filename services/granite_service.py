"""
granite_service.py
Authenticates with IBM IAM and calls the watsonx.ai text generation endpoint.
"""

import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Anchor to backend/.env regardless of the working directory uvicorn is launched from.
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

# ---------------------------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------------------------
_API_KEY = os.getenv("WATSONX_API_KEY", "")
_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
_MODEL_ID = os.getenv("WATSONX_MODEL_ID", "ibm/granite-4-h-small")
_WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

_IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
_GENERATION_PATH = "/ml/v1/text/generation?version=2023-05-29"

# ---------------------------------------------------------------------------
# IAM token cache  (module-level, lives for the process lifetime)
# ---------------------------------------------------------------------------
_cached_token: str = ""
_token_expiry: float = 0.0  # Unix timestamp after which the token is stale


async def _get_iam_token() -> str:
    """Return a valid IAM Bearer token, refreshing when within 60 s of expiry."""
    global _cached_token, _token_expiry

    if not _API_KEY:
        raise RuntimeError(
            "WATSONX_API_KEY is not set. "
            "Add it to your .env file or environment before starting the server."
        )

    # Return cached token if it is still fresh.
    if _cached_token and time.time() < _token_expiry:
        return _cached_token

    async with httpx.AsyncClient() as client:
        response = await client.post(
            _IAM_TOKEN_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": _API_KEY,
            },
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"IAM token request failed [{response.status_code}]: {response.text}"
        )

    token_data = response.json()
    _cached_token = token_data["access_token"]
    # expires_in is in seconds; keep a 60-second safety buffer.
    _token_expiry = time.time() + token_data.get("expires_in", 3600) - 60
    return _cached_token


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def generate(prompt: str) -> str:
    """Call the IBM Granite model and return the generated text string."""
    if not _PROJECT_ID:
        raise RuntimeError(
            "WATSONX_PROJECT_ID is not set. "
            "Add it to your .env file or environment before starting the server."
        )

    token = await _get_iam_token()

    payload = {
        "model_id": _MODEL_ID,
        "input": prompt,
        "parameters": {
            "max_new_tokens": 1500,
            "temperature": 0.3,
        },
        "project_id": _PROJECT_ID,
    }

    url = f"{_WATSONX_URL.rstrip('/')}{_GENERATION_PATH}"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120.0,
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"watsonx.ai generation request failed [{response.status_code}]: "
            f"{response.text}"
        )

    result = response.json()
    try:
        return result["results"][0]["generated_text"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(
            f"Unexpected response shape from watsonx.ai: {result}"
        ) from exc
