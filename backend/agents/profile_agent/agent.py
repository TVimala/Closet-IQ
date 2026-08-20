"""Profile agent placeholder."""


class ProfileAgent:
    """Handles user profile context."""

    def __init__(self) -> None:
        self.name = "profile_agent"

    def run(self, payload: dict | None = None) -> dict:
        return {"agent": self.name, "payload": payload or {}}
