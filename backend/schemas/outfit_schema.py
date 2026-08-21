from pydantic import BaseModel
from typing import List


class OutfitRequest(BaseModel):
    occasion: str


class WardrobeItem(BaseModel):
    id: str
    name: str
    category: str
    color: str
    style: List[str]
    fit: str | None = None
    available: bool


class StylistInput(BaseModel):
    occasion: str
    wardrobe: List[WardrobeItem]