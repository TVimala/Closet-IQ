"""Stylist agent placeholder."""


class StylistAgent:
    """Handles outfit recommendations and styling."""

    def __init__(self) -> None:
        self.name = "stylist_agent"

    def run(self, payload: dict | None = None) -> dict:
        return {"agent": self.name, "payload": payload or {}}


