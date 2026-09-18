from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SubmitFeedbackRequest(BaseModel):

    user_id: str

    outfit_id: str

    feedback_type: str

    reason: Optional[str] = None

    rating: Optional[int] = None

    comment: Optional[str] = None

    # ------------------------------------------------------
    # Only needed when feedback_type == "wore_it": the actual
    # outfit items being marked as worn (each needs at least
    # an "id"), and optionally which occasion they were worn
    # for. Generated outfits aren't persisted anywhere, so the
    # caller (frontend) passes back what it already has.
    # ------------------------------------------------------

    items: Optional[List[Dict[str, Any]]] = None

    occasion: Optional[str] = None
