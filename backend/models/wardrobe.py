"""Wardrobe model."""

from dataclasses import dataclass, field


@dataclass
class WardrobeItem:
    id: str
    name: str
    category: str
    color: str | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class Wardrobe:
    user_id: str
    items: list[WardrobeItem] = field(default_factory=list)
