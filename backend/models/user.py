"""User model."""

from dataclasses import dataclass, field


@dataclass
class User:
    id: str
    email: str
    name: str
    preferences: dict[str, object] = field(default_factory=dict)
