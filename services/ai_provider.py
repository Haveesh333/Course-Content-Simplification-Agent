"""
ai_provider.py
Single entry-point for AI text generation.

Reads the AI_PROVIDER environment variable and routes generate() calls to the
appropriate backend service:

  AI_PROVIDER=granite  (default) → granite_service  (IBM watsonx.ai — primary)
  AI_PROVIDER=gemini              → gemini_service   (Google Gemini — dev/testing)

No other module needs to import granite_service or gemini_service directly;
they all import `generate` from here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Anchor to backend/.env regardless of the working directory uvicorn is launched from.
# __file__ is  …/backend/services/ai_provider.py  → parent.parent is  …/backend/
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

_PROVIDER = os.getenv("AI_PROVIDER", "granite").strip().lower()

if _PROVIDER == "gemini":
    from services.gemini_service import generate as generate  # noqa: F401
elif _PROVIDER == "granite":
    from services.granite_service import generate as generate  # noqa: F401
else:
    raise RuntimeError(
        f"Unknown AI_PROVIDER '{_PROVIDER}'. "
        "Set AI_PROVIDER to 'granite' (default) or 'gemini' in your .env file."
    )
