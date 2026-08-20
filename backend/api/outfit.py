"""Outfit-related routes."""

from fastapi import APIRouter

router = APIRouter(prefix="/outfit", tags=["outfit"])


@router.get("/health")
def outfit_health() -> dict[str, str]:
    return {"status": "outfit service ok"}
