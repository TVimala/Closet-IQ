"""Feedback agent placeholder."""


class FeedbackAgent:
    """Handles user feedback processing."""

    def __init__(self) -> None:
        self.name = "feedback_agent"

    def run(self, payload: dict | None = None) -> dict:
        return {"agent": self.name, "payload": payload or {}}
