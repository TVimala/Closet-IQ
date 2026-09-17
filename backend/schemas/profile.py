from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfileCreate(BaseModel):
    user_id: str
    gender: Optional[str] = None
    birth_year: int

class UserPreferenceCreate(BaseModel):
    user_id: str

    styles: List[str] = []
    colors: List[str] = []
    fits: List[str] = []
    occasions: List[str] = []

    comfort_weight: int = Field(..., ge=1, le=5)

class UserPreferenceUpdate(BaseModel):
    styles: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    fits: Optional[List[str]] = None
    occasions: Optional[List[str]] = None
    comfort_weight: Optional[int] = Field(
        None,
        ge=1,
        le=5
    )
