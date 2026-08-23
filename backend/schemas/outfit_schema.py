from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ============================================================
# USER PREFERENCES
# ============================================================

class UserPreferences(BaseModel):
    styles: List[str] = []
    colors: List[str] = []
    fits: List[str] = []
    comfort_level: int = 3


# ============================================================
# OUTFIT REQUEST
# ============================================================

class OutfitRequest(BaseModel):
    occasion: str
    latitude: float
    longitude: float


# ============================================================
# WARDROBE ITEM
# ============================================================

class WardrobeItem(BaseModel):
    id: str
    user_id: str

    image_url: Optional[str] = None

    category: str
    color: Optional[str] = None
    pattern: Optional[str] = None
    fit: Optional[str] = None

    style: List[str] = []
    season: List[str] = []
    occasion: List[str] = []

    condition: str
    is_available: bool = True

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    usage_count: int = 0
    last_worn_at: Optional[datetime] = None

    embedding: Optional[List[float]] = None


# ============================================================
# DATA SENT TO STYLIST AGENT
# ============================================================

class StylistInput(BaseModel):
    occasion: str
    wardrobe: List[WardrobeItem]
    preferences: UserPreferences