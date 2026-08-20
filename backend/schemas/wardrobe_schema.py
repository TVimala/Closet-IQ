"""Wardrobe request/response schemas."""

from pydantic import BaseModel


class WardrobeItemCreate(BaseModel):
    name: str
    category: str
    color: str | None = None
    tags: list[str] | None = None


class WardrobeItemRead(BaseModel):
    id: str
    name: str
    category: str
    color: str | None = None
    tags: list[str] = []
