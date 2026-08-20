"""Finance agent placeholder."""


class FinanceAgent:
    """Handles budget and purchase recommendations."""

    def __init__(self) -> None:
        self.name = "finance_agent"

    def run(self, payload: dict | None = None) -> dict:
        return {"agent": self.name, "payload": payload or {}}
