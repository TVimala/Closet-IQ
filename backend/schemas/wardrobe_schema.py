from pydantic import BaseModel
from typing import Optional, List


class WardrobeItemUpdate(BaseModel):

    category: Optional[str] = None
    color: Optional[str] = None
    pattern: Optional[str] = None
    fit: Optional[str] = None

    styles: Optional[List[str]] = None
    occasions: Optional[List[str]] = None
    seasons: Optional[List[str]] = None

    condition: Optional[str] = None
    is_available: Optional[bool] = None