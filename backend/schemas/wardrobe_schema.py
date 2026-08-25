from pydantic import BaseModel
from typing import Optional


class WardrobeItemUpdate(BaseModel):

    category: Optional[str] = None
    color: Optional[str] = None
    pattern: Optional[str] = None
    fit: Optional[str] = None
    style: Optional[str] = None
    occasion: Optional[str] = None
    season: Optional[str] = None
    condition: Optional[str] = None
    is_available: Optional[bool] = None