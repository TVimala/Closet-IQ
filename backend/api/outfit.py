from fastapi import APIRouter

from schemas.outfit_schema import OutfitRequest
from services.outfit_service import process_outfit_request


# Create router
router = APIRouter(
    prefix="/outfit",
    tags=["Outfit"]
)


# Generate outfit
@router.post("/generate")
def generate_outfit(request: OutfitRequest):

    result = process_outfit_request(
        occasion=request.occasion,
        latitude=request.latitude,
        longitude=request.longitude
    )

    return result