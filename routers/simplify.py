"""
simplify.py
FastAPI router exposing GET /health and POST /simplify.
"""

import json
import re
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from models.schemas import SimplifyResponse
from services.ai_provider import generate
from services.gemini_service import GeminiAPIError
from services.document_parser import extract_text
from services.prompt_builder import build_prompt

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    """Liveness check — returns {"status": "ok"}."""
    return {"status": "ok"}


@router.post("/simplify", response_model=SimplifyResponse)
async def simplify(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    level: str = Form(...),
) -> SimplifyResponse:
    """
    Accept course content (uploaded file or pasted text) plus a difficulty level,
    call the configured AI provider (IBM Granite by default), parse the JSON
    response, and return a SimplifyResponse.
    """
    # 1. Validate that at least one input source was provided.
    if file is None and not text:
        raise HTTPException(
            status_code=422,
            detail="Provide either a file or text input.",
        )

    # 2. Extract raw text from the uploaded file, or use the form text directly.
    if file is not None:
        file_bytes = await file.read()
        try:
            raw_text = extract_text(file_bytes, file.filename or "upload")
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
    else:
        raw_text = text  # type: ignore[assignment]

    # 3-7. Build prompt → call AI provider → parse JSON → return response.
    try:
        prompt = build_prompt(raw_text, level)
        generated_text = await generate(prompt)
        # Strip markdown code fences that some models wrap around JSON output
        # (e.g. ```json … ``` or ``` … ```) before attempting to parse.
        clean_text = re.sub(r"^```[a-zA-Z]*\s*", "", generated_text.strip())
        clean_text = re.sub(r"\s*```$", "", clean_text)
        parsed = json.loads(clean_text.strip())
        return SimplifyResponse(**parsed)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"JSON parse error: {e}")
    except GeminiAPIError as e:
        # Forward the upstream HTTP status code and its safe message.
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
