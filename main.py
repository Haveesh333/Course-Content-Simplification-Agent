"""
main.py
FastAPI application entry point for CourseEase AI.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.simplify import router as simplify_router

app = FastAPI(
    title="CourseEase AI",
    description="Course Content Simplification Agent",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simplify_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # run from backend/
