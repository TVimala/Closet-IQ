from pydantic import BaseModel
from typing import List, Optional


class OutfitRequest(BaseModel):
    occasion: str


class WardrobeItem(BaseModel):
    id: str
    name: str
    category: str
    color: str
    style: List[str]
    fit: Optional[str] = None
    available: bool


class StylistInput(BaseModel):
    occasion: str
    wardrobe: List[WardrobeItem]


class OutfitCombination(BaseModel):
    top: WardrobeItem
    bottom: WardrobeItem
    shoes: WardrobeItem