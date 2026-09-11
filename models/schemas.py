from typing import List

from pydantic import BaseModel


class DifficultTerm(BaseModel):
    term: str
    meaning: str


class QuizQuestion(BaseModel):
    question: str
    options: List[str]  # exactly 4 items: ["A. ...", "B. ...", "C. ...", "D. ..."]
    answer: str  # single letter: "A", "B", "C", or "D"


class SimplifyResponse(BaseModel):
    simplified_explanation: str
    key_points: List[str]
    difficult_terms: List[DifficultTerm]
    examples: List[str]
    quiz: List[QuizQuestion]
