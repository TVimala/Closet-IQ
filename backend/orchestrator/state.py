"""State management for orchestrator workflows."""

from dataclasses import dataclass, field


@dataclass
class OrchestratorState:
    """Placeholder state container."""

    current_step: str = "idle"
    context: dict[str, object] = field(default_factory=dict)
