from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date


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
# SINGLE OUTFIT REQUEST
# ============================================================

class OutfitRequest(BaseModel):

    user_id: str

    occasion: str

    latitude: float

    longitude: float


# ============================================================
# REGENERATION REQUEST
# ============================================================

class RegenerationRequest(BaseModel):

    user_id: str

    occasion: str

    latitude: float

    longitude: float

    previous_outfit: Dict[str, Any]

    # All outfits already shown during this regeneration chain.
    # Keep this optional so old clients that only send previous_outfit still work.
    previous_outfits: List[Dict[str, Any]] = Field(default_factory=list)

    regeneration_reason: Optional[str] = None


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

    style: List[str] = Field(
        default_factory=list
    )

    season: List[str] = Field(
        default_factory=list
    )

    occasion: List[str] = Field(
        default_factory=list
    )

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

    # ========================================================
    # REGENERATION
    # ========================================================
    #
    # These are optional so existing requests continue
    # working exactly as before.
    # ========================================================

    previous_outfit: Optional[Dict[str, Any]] = None

    # Complete regeneration history used to prevent A -> B -> A bouncing.
    previous_outfits: List[Dict[str, Any]] = Field(default_factory=list)

    regeneration_reason: Optional[str] = None


# ============================================================
# WEEKLY PLANNER — ONE DAY
# ============================================================

class WeeklyDayPlan(BaseModel):

    date: date

    occasion: str


# ============================================================
# WEEKLY OUTFIT REQUEST
# ============================================================

class WeeklyOutfitRequest(BaseModel):

    user_id: str

    start_date: date

    days: List[WeeklyDayPlan] = Field(
        min_length=1,
        max_length=7
    )

    latitude: float

    longitude: float