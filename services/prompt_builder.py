"""
prompt_builder.py
Constructs a level-appropriate prompt for IBM Granite that instructs the model
to return all five output sections as a single valid JSON object.
"""

_LEVEL_DESCRIPTIONS: dict[str, str] = {
    "beginner": (
        "Use very simple, everyday language. Write short sentences. "
        "Rely on real-life analogies to explain concepts. Avoid all jargon; "
        "if a technical word is unavoidable, immediately explain it in plain terms."
    ),
    "intermediate": (
        "Use moderate detail. When domain-specific terms are introduced, "
        "briefly explain each one in parentheses. Aim for balanced depth — "
        "thorough enough to be useful, concise enough to remain accessible."
    ),
    "advanced": (
        "Use precise technical language and assume the reader has strong "
        "subject-matter knowledge. Provide full depth and nuance. "
        "You do not need to simplify terminology."
    ),
}


def build_prompt(text: str, level: str) -> str:
    """
    Build a structured prompt for IBM Granite.

    Parameters
    ----------
    text : str
        The raw course content to be processed.
    level : str
        One of "beginner", "intermediate", or "advanced".

    Returns
    -------
    str
        A complete prompt string ready to be sent to the Granite model.
    """
    level_key = level.lower().strip()
    if level_key not in _LEVEL_DESCRIPTIONS:
        raise ValueError(
            f"Invalid level '{level}'. Must be one of: beginner, intermediate, advanced."
        )

    level_description = _LEVEL_DESCRIPTIONS[level_key]

    prompt = f"""You are a course content simplification assistant. Your job is to help students understand academic material by processing course content and producing structured educational output at the appropriate complexity level.

DIFFICULTY LEVEL: {level_key.upper()}
LEVEL INSTRUCTIONS: {level_description}

TASK:
Analyse the course content provided at the end of this prompt and produce ALL of the following:
1. A clear, well-structured simplified explanation of the main topic.
2. A list of the most important key points (aim for 4–6 bullet points).
3. A list of difficult or domain-specific terms with a plain-language meaning for each.
4. Two or more concrete, relatable examples that illustrate the core concepts.
5. Exactly 5 multiple-choice quiz questions, each with exactly 4 options labelled A, B, C, D and a single correct answer.

OUTPUT FORMAT — CRITICAL INSTRUCTIONS:
- Respond with a SINGLE valid JSON object and nothing else.
- Do NOT wrap the JSON in markdown code fences (no ```json or ```).
- Do NOT add any explanation, preamble, or commentary outside the JSON object.
- The JSON must match this exact schema:

{{
  "simplified_explanation": "<string: clear explanation of the content at the chosen difficulty level>",
  "key_points": [
    "<string: key point 1>",
    "<string: key point 2>"
  ],
  "difficult_terms": [
    {{"term": "<string: term>", "meaning": "<string: plain-language meaning>"}}
  ],
  "examples": [
    "<string: example 1>",
    "<string: example 2>"
  ],
  "quiz": [
    {{
      "question": "<string: question text>",
      "options": ["A. <option>", "B. <option>", "C. <option>", "D. <option>"],
      "answer": "<single capital letter: A, B, C, or D>"
    }}
  ]
}}

QUIZ REQUIREMENTS:
- The quiz array must contain EXACTLY 5 question objects.
- Each question must have EXACTLY 4 options in the "options" array, prefixed A. B. C. D.
- The "answer" field must be a single capital letter (A, B, C, or D) matching the correct option.
- Questions should test genuine understanding of the course content, not trivial recall.

---
COURSE CONTENT:
{text.strip()}
---

Remember: output ONLY the JSON object. No markdown, no extra text."""

    return prompt
