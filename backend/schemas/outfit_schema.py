from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ============================================================
# LONG-TERM USER PREFERENCES
# ============================================================

class LongTermPreferences(BaseModel):

    styles: List[str] = Field(
        default_factory=list
    )

    colors: List[str] = Field(
        default_factory=list
    )

    fits: List[str] = Field(
        default_factory=list
    )

    comfort_level: int = Field(
        default=3,
        ge=1,
        le=5
    )


# ============================================================
# SHORT-TERM / TODAY'S PREFERENCES
# ============================================================

class ShortTermPreferences(BaseModel):

    styles: List[str] = Field(
        default_factory=list
    )

    colors: List[str] = Field(
        default_factory=list
    )

    fits: List[str] = Field(
        default_factory=list
    )

    comfort_level: Optional[int] = Field(
        default=None,
        ge=1,
        le=5
    )

    avoid_styles: List[str] = Field(
        default_factory=list
    )

    avoid_colors: List[str] = Field(
        default_factory=list
    )

    occasion_note: Optional[str] = None

# ============================================================
# USER PREFERENCES
# ============================================================

class UserPreferences(BaseModel):
    long_term: LongTermPreferences = Field(
        default_factory=LongTermPreferences
    )

    short_term: ShortTermPreferences = Field(
        default_factory=ShortTermPreferences
    )


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