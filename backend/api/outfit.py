from fastapi import APIRouter
from schemas.outfit_schema import OutfitRequest
from services.outfit_service import process_outfit_request


router = APIRouter(
    prefix="/outfit",
    tags=["Outfit"]
)


@router.post("/generate")
def generate_outfit(request: OutfitRequest):

    result = process_outfit_request(request.occasion)

    return result