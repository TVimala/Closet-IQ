"""Feedback-related routes.

Previously a placeholder ("feedback service ok" health check
only, and not even wired into main.py). Now exposes the actual
Feedback Agent flow (validation -> persistence -> outfit
history / wardrobe usage update -> learned preferences) through
the Orchestrator.
"""

from fastapi import APIRouter, HTTPException

from schemas.feedback_schema import SubmitFeedbackRequest

from orchestrator.graph import run_feedback_request

from agents.feedback_agent.outfit_history import get_user_outfit_history
from agents.feedback_agent.feedback_store import get_user_feedback_events
from agents.feedback_agent.agent import run_feedback_agent


router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("/health")
def feedback_health() -> dict:
    return {"status": "feedback service ok"}


# ============================================================
# SUBMIT FEEDBACK
#
# Handles: like, wore_it, rating, regenerate, skip
# (validated against the existing FEEDBACK_TYPES set).
# ============================================================

@router.post("/")
def submit_feedback(request: SubmitFeedbackRequest):

    result = run_feedback_request(
        user_id=request.user_id,
        outfit_id=request.outfit_id,
        feedback_type=request.feedback_type,
        reason=request.reason,
        rating=request.rating,
        comment=request.comment,
        items=request.items,
        occasion=request.occasion,
    )

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


# ============================================================
# OUTFIT HISTORY
# ============================================================

@router.get("/history/{user_id}")
def get_outfit_history(user_id: str):

    history = get_user_outfit_history(user_id)

    return {
        "success": True,
        "user_id": user_id,
        "count": len(history),
        "history": history,
    }


# ============================================================
# LEARNED PREFERENCES
# ============================================================

@router.get("/learned-preferences/{user_id}")
def get_learned_preferences(user_id: str):

    events = get_user_feedback_events(user_id)

    if not events:
        return {
            "success": True,
            "user_id": user_id,
            "message": "No feedback recorded yet.",
            "learned_preferences": None,
        }

    result = run_feedback_agent(events)

    return {
        "success": True,
        "user_id": user_id,
        "learned_preferences": result.get("learned_preferences"),
    }
