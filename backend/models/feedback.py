"""Feedback model."""

from dataclasses import dataclass


@dataclass
class Feedback:
    id: str
    user_id: str
    outfit_id: str | None = None
    rating: int | None = None
    comment: str | None = None
