"""Wardrobe agent placeholder."""


class WardrobeAgent:
    """Handles wardrobe-related logic."""

    def __init__(self) -> None:
        self.name = "wardrobe_agent"

    def run(self, payload: dict | None = None) -> dict:
        return {"agent": self.name, "payload": payload or {}}
