# ============================================================
# FEEDBACK AGENT
# DATA MODELS
# STEP 11
# ============================================================

from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# SUPPORTED FEEDBACK TYPES
# ============================================================

FEEDBACK_TYPES = {
    "like",
    "wore_it",
    "rating",
    "regenerate",
    "skip"
}


# ============================================================
# SUPPORTED REGENERATION REASONS
# ============================================================

REGENERATION_REASONS = {
    "too_formal",
    "too_casual",
    "dont_like_colors",
    "dont_like_combination",
    "not_comfortable",
    "dont_like_fit",
    "already_wore_similar",
    "dont_like_individual_item",
    "other",
    "skipped"
}


# ============================================================
# FEEDBACK REQUEST
#
# This is the standardized input received
# from the user or frontend.
# ============================================================

class FeedbackRequest(BaseModel):

    user_id: str

    outfit_id: str

    feedback_type: str

    reason: Optional[str] = None

    rating: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )

    comment: Optional[str] = None


# ============================================================
# NORMALIZED FEEDBACK EVENT
#
# This is what the Feedback Agent returns
# after validation and processing.
# ============================================================

class FeedbackEvent(BaseModel):

    user_id: str

    outfit_id: str

    feedback_type: str

    reason: Optional[str] = None

    rating: Optional[int] = None

    comment: Optional[str] = None

    timestamp: str

    status: str = "recorded"