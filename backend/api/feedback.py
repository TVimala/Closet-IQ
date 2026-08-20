"""Feedback-related routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("/health")
def feedback_health() -> dict[str, str]:
    return {"status": "feedback service ok"}
