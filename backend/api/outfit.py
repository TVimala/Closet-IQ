from fastapi import APIRouter, HTTPException

from schemas.outfit_schema import (
    OutfitRequest,
    RegenerationRequest,
    WeeklyOutfitRequest,
)

from orchestrator.graph import (
    run_outfit_request,
    run_regeneration_request,
    run_weekly_outfit_request,
)


# ============================================================
# CREATE ROUTER
# ============================================================

router = APIRouter(
    prefix="/outfit",
    tags=["Outfit"]
)


# ============================================================
# SINGLE OUTFIT
#
# Previously built on MOCK_WARDROBE / MOCK_USER_PREFERENCES.
# Now routed through the Orchestrator, which pulls the real
# Wardrobe Agent + Profile Agent data for this user_id.
# ============================================================

@router.post("/generate")
def generate_outfit(
    request: OutfitRequest
):

    result = run_outfit_request(
        user_id=request.user_id,
        occasion=request.occasion,
        latitude=request.latitude,
        longitude=request.longitude,
    )

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


# ============================================================
# REGENERATION
# ============================================================

@router.post("/regenerate")
def regenerate_outfit(
    request: RegenerationRequest
):

    result = run_regeneration_request(
        user_id=request.user_id,
        occasion=request.occasion,
        latitude=request.latitude,
        longitude=request.longitude,
        previous_outfit=request.previous_outfit,
        regeneration_reason=request.regeneration_reason,
    )

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result


# ============================================================
# WEEKLY OUTFIT PLAN
#
# Previously built on MOCK_WARDROBE / MOCK_USER_PREFERENCES.
# Now routed through the Orchestrator.
# ============================================================

@router.post("/weekly")
def generate_weekly_outfits(
    request: WeeklyOutfitRequest
):

    result = run_weekly_outfit_request(
        user_id=request.user_id,
        start_date=request.start_date,
        days=[day.model_dump() for day in request.days],
        latitude=request.latitude,
        longitude=request.longitude,
    )

    if isinstance(result, dict) and result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result
