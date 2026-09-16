from fastapi import APIRouter

from schemas.outfit_schema import (
    OutfitRequest,
    WeeklyOutfitRequest,
    UserPreferences,
    WardrobeItem
)

from services.outfit_service import (
    process_outfit_request,
    MOCK_WARDROBE,
    MOCK_USER_PREFERENCES
)

from agents.stylist_agent.Planning.weekly_planner import (
    generate_weekly_plan
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
# ============================================================

@router.post("/generate")
def generate_outfit(
    request: OutfitRequest
):

    result = process_outfit_request(
        occasion=request.occasion,
        latitude=request.latitude,
        longitude=request.longitude
    )

    return result


# ============================================================
# WEEKLY OUTFIT PLAN
# ============================================================

@router.post("/weekly")
def generate_weekly_outfits(
    request: WeeklyOutfitRequest
):

    # --------------------------------------------------------
    # CONVERT MOCK WARDROBE DICTIONARIES TO PYDANTIC OBJECTS
    # --------------------------------------------------------

    wardrobe = [

        WardrobeItem(**item)

        for item in MOCK_WARDROBE
    ]


    # --------------------------------------------------------
    # CREATE USER PREFERENCES
    # --------------------------------------------------------

    preferences = UserPreferences(
        **MOCK_USER_PREFERENCES
    )


    # --------------------------------------------------------
    # GENERATE 7-DAY PLAN
    # --------------------------------------------------------

    result = generate_weekly_plan(
        request=request,
        wardrobe=wardrobe,
        preferences=preferences
    )


    return result