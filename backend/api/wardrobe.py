"""Wardrobe-related routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/wardrobe", tags=["wardrobe"])


@router.get("/health")
def wardrobe_health() -> dict[str, str]:
    return {"status": "wardrobe service ok"}
