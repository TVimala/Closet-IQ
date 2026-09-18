"""State management for orchestrator workflows.

Replaces the previous placeholder OrchestratorState dataclass.
Only fields that existing agents/services actually need are
included (per project instructions: do not blindly add every
possible field).
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class OrchestratorState:

    # ------------------------------------------------------
    # REQUEST IDENTITY
    # ------------------------------------------------------

    user_id: Optional[str] = None
    request_type: Optional[str] = None
    status: str = "idle"
    error: Optional[str] = None

    # ------------------------------------------------------
    # OUTFIT REQUEST INPUTS
    # ------------------------------------------------------

    occasion: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # ------------------------------------------------------
    # DATA GATHERED FROM AGENTS
    # ------------------------------------------------------

    preferences: Optional[dict] = None
    wardrobe: list = field(default_factory=list)
    weather: Optional[dict] = None
    learned_preferences: Optional[dict] = None

    # ------------------------------------------------------
    # OUTFIT RESULTS
    # ------------------------------------------------------

    generated_outfit: Optional[dict] = None
    selected_outfit: Optional[dict] = None
    previous_outfit: Optional[dict] = None
    regeneration_reason: Optional[str] = None

    # ------------------------------------------------------
    # FEEDBACK
    # ------------------------------------------------------

    feedback: Optional[dict] = None

    # ------------------------------------------------------
    # FINANCE
    # ------------------------------------------------------

    monthly_budget: Optional[float] = None
    shopping_spend: Optional[float] = None
    purchase_request: Optional[dict] = None
    purchase_analysis: Optional[dict] = None

    # ------------------------------------------------------
    # NOTIFICATIONS
    # ------------------------------------------------------

    notification_results: list = field(default_factory=list)

    # ------------------------------------------------------
    # FREEFORM CONTEXT (escape hatch, kept from the original
    # placeholder so nothing that referenced .context breaks)
    # ------------------------------------------------------

    context: dict = field(default_factory=dict)
