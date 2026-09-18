"""Request routing for orchestrator tasks.

Replaces the previous placeholder Router class. The router only
classifies which agent(s) a request needs to go to. It performs
NO business logic itself.
"""

from enum import Enum


class RequestType(str, Enum):

    WARDROBE_REQUEST = "WARDROBE_REQUEST"
    PROFILE_REQUEST = "PROFILE_REQUEST"
    OUTFIT_REQUEST = "OUTFIT_REQUEST"
    WEEKLY_OUTFIT_REQUEST = "WEEKLY_OUTFIT_REQUEST"
    REGENERATION_REQUEST = "REGENERATION_REQUEST"
    FEEDBACK_REQUEST = "FEEDBACK_REQUEST"
    PURCHASE_ANALYSIS_REQUEST = "PURCHASE_ANALYSIS_REQUEST"
    PURCHASE_DECISION_REQUEST = "PURCHASE_DECISION_REQUEST"
    NOTIFICATION_REQUEST = "NOTIFICATION_REQUEST"


# ============================================================
# WHICH AGENTS EACH REQUEST TYPE NEEDS
#
# Informational map only - the Orchestrator's graph.py is what
# actually calls the agents. This exists so the routing decision
# is visible/testable in one place.
# ============================================================

REQUEST_AGENT_MAP = {

    RequestType.WARDROBE_REQUEST: ["wardrobe_agent"],

    RequestType.PROFILE_REQUEST: ["profile_agent"],

    RequestType.OUTFIT_REQUEST: [
        "profile_agent", "wardrobe_agent", "weather_service", "stylist_agent"
    ],

    RequestType.WEEKLY_OUTFIT_REQUEST: [
        "profile_agent", "wardrobe_agent", "weather_service",
        "stylist_agent.weekly_planner"
    ],

    RequestType.REGENERATION_REQUEST: [
        "profile_agent", "wardrobe_agent", "weather_service", "stylist_agent"
    ],

    RequestType.FEEDBACK_REQUEST: ["feedback_agent"],

    RequestType.PURCHASE_ANALYSIS_REQUEST: [
        "wardrobe_agent", "finance_agent"
    ],

    RequestType.PURCHASE_DECISION_REQUEST: [
        "finance_agent", "wardrobe_agent"
    ],

    RequestType.NOTIFICATION_REQUEST: [
        "finance_agent", "feedback_agent", "notification_agent"
    ],
}


class Router:
    """Determines which RequestType a raw request corresponds to.

    Kept intentionally simple: the API layer already knows which
    endpoint was hit (e.g. POST /outfit/generate vs POST
    /outfit/regenerate), so in practice callers usually pass the
    RequestType directly. classify() is provided for the cases
    described in the spec (e.g. free-text routing) but is not
    required for the API endpoints below.
    """

    def __init__(self) -> None:
        self.routes: dict[str, str] = {}

    def add_route(self, key: str, value: str) -> None:
        self.routes[key] = value

    @staticmethod
    def agents_for(request_type: "RequestType") -> list:
        return REQUEST_AGENT_MAP.get(request_type, [])

    @staticmethod
    def classify(text: str) -> "RequestType":
        """Very small keyword-based classifier for free-text requests.

        Not used by the structured API endpoints (they already know
        their RequestType), but implements the "User asks ... ->
        ROUTE" behaviour described in the spec for completeness.
        """

        if not text:
            return RequestType.OUTFIT_REQUEST

        lowered = text.lower()

        if "regenerate" in lowered:
            return RequestType.REGENERATION_REQUEST

        if "7 day" in lowered or "week" in lowered:
            return RequestType.WEEKLY_OUTFIT_REQUEST

        if "wore" in lowered or "didn't wear" in lowered or "feedback" in lowered:
            return RequestType.FEEDBACK_REQUEST

        if "afford" in lowered or "buy" in lowered or "purchase" in lowered:
            return RequestType.PURCHASE_ANALYSIS_REQUEST

        if "wardrobe" in lowered or "closet" in lowered:
            return RequestType.WARDROBE_REQUEST

        if "profile" in lowered or "preference" in lowered:
            return RequestType.PROFILE_REQUEST

        if "notification" in lowered or "budget reminder" in lowered:
            return RequestType.NOTIFICATION_REQUEST

        return RequestType.OUTFIT_REQUEST
