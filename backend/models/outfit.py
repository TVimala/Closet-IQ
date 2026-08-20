"""Outfit model."""

from dataclasses import dataclass, field


@dataclass
class Outfit:
    id: str
    user_id: str
    items: list[str] = field(default_factory=list)
    occasion: str | None = None
