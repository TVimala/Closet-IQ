# ============================================================
# WEEKLY OUTFIT PLANNER
# ============================================================

from typing import List

from schemas.outfit_schema import (
    WeeklyOutfitRequest,
    UserPreferences,
    WardrobeItem,
    StylistInput
)

from services.weather_service import (
    get_weekly_weather
)

from agents.stylist_agent.agent import (
    run_stylist_agent
)


# ============================================================
# GET OUTFIT ITEM IDS
# ============================================================

def get_outfit_item_ids(outfit):

    return {
        item.get("id")
        for item in outfit.get("items", [])
        if item.get("id")
    }


# ============================================================
# CHECK WHETHER OUTFIT WAS ALREADY USED
# ============================================================

def is_repeated_outfit(
    candidate,
    selected_outfits
):

    candidate_ids = get_outfit_item_ids(
        candidate
    )

    for selected in selected_outfits:

        selected_ids = get_outfit_item_ids(
            selected
        )

        # Same complete outfit
        if candidate_ids == selected_ids:

            return True

    return False


# ============================================================
# SELECT BEST NON-REPEATED OUTFIT
# ============================================================

def select_weekly_outfit(
    outfits,
    selected_outfits
):

    for outfit in outfits:

        if not is_repeated_outfit(
            outfit,
            selected_outfits
        ):

            return outfit

    return None


# ============================================================
# FIND WEATHER FOR REQUESTED DATE
# ============================================================

def get_weather_for_date(
    weekly_weather,
    requested_date
):

    requested_date = str(
        requested_date
    )

    for weather in weekly_weather:

        if weather.get("date") == requested_date:

            return weather

    return None


# ============================================================
# WEEKLY PLANNER
# ============================================================

def generate_weekly_plan(
    request: WeeklyOutfitRequest,
    wardrobe: List[WardrobeItem],
    preferences: UserPreferences
):

    print(
        "\n==================================="
    )

    print(
        "WEEKLY OUTFIT PLANNER STARTED"
    )

    print(
        "==================================="
    )

    print(
        f"\nStart Date: {request.start_date}"
    )

    print(
        f"Days Requested: {len(request.days)}"
    )


    # ========================================================
    # STEP 1
    # GET 7-DAY WEATHER USING LATITUDE + LONGITUDE
    # ========================================================

    weekly_weather = get_weekly_weather(
        request.latitude,
        request.longitude
    )


    print(
        f"\nWeather Forecast Received: "
        f"{len(weekly_weather)} days"
    )


    # ========================================================
    # DEBUG — SHOW FORECAST DATES
    # ========================================================

    print(
        "\nAvailable Weather Dates:"
    )

    for weather in weekly_weather:

        print(
            f"  {weather.get('date')}"
        )


    # ========================================================
    # STEP 2
    # STORE FINAL WEEKLY OUTFITS
    # ========================================================

    weekly_outfits = []

    selected_outfits = []


    # ========================================================
    # STEP 3
    # PROCESS EACH REQUESTED DAY
    # ========================================================

    for index, day in enumerate(
        request.days,
        start=1
    ):

        print(
            "\n-----------------------------------"
        )

        print(
            f"PLANNING DAY {index}"
        )

        print(
            f"Date: {day.date}"
        )

        print(
            f"Occasion: {day.occasion}"
        )


        # ====================================================
        # STEP 3A
        # FIND WEATHER USING ACTUAL DATE
        # ====================================================

        requested_date = str(
            day.date
        )

        day_weather = get_weather_for_date(
            weekly_weather,
            requested_date
        )


        # ====================================================
        # WEATHER NOT AVAILABLE
        # ====================================================

        if day_weather is None:

            print(
                f"No weather data available "
                f"for {requested_date}"
            )

            weekly_outfits.append({

                "day":
                    index,

                "date":
                    requested_date,

                "occasion":
                    day.occasion,

                "weather":
                    None,

                "outfit":
                    None,

                "status":
                    "weather_unavailable"
            })

            continue


        # ====================================================
        # DISPLAY WEATHER
        # ====================================================

        print(
            f"Temperature: "
            f"{day_weather['temperature_min']} - "
            f"{day_weather['temperature_max']}°C"
        )

        print(
            f"Condition: "
            f"{day_weather['condition']}"
        )

        print(
            f"Recommended Season: "
            f"{day_weather['recommended_season']}"
        )


        # ====================================================
        # STEP 3B
        # CREATE STYLIST INPUT
        # ====================================================

        stylist_input = StylistInput(

            occasion=
                day.occasion,

            wardrobe=
                wardrobe,

            preferences=
                preferences
        )


        # ====================================================
        # STEP 3C
        # RUN EXISTING STYLIST AGENT
        # ====================================================

        stylist_result = run_stylist_agent(

            stylist_input,

            day_weather
        )


        # ====================================================
        # STEP 3D
        # GET CANDIDATE OUTFITS
        # ====================================================

        candidate_outfits = (
            stylist_result.get(
                "outfits",
                []
            )
        )


        print(
            f"Candidate Outfits: "
            f"{len(candidate_outfits)}"
        )


        # ====================================================
        # STEP 3E
        # SELECT NON-REPEATED OUTFIT
        # ====================================================

        selected_outfit = (
            select_weekly_outfit(

                candidate_outfits,

                selected_outfits
            )
        )


        # ====================================================
        # NO UNIQUE OUTFIT
        # ====================================================

        if selected_outfit is None:

            print(
                "No unique outfit available "
                "for this day."
            )

            weekly_outfits.append({

                "day":
                    index,

                "date":
                    requested_date,

                "occasion":
                    day.occasion,

                "weather":
                    day_weather,

                "outfit":
                    None,

                "status":
                    "no_unique_outfit_available"
            })

            continue


        # ====================================================
        # STEP 3F
        # SAVE SELECTED OUTFIT
        # ====================================================

        selected_outfits.append(
            selected_outfit
        )


        weekly_outfits.append({

            "day":
                index,

            "date":
                requested_date,

            "occasion":
                day.occasion,

            "weather":
                day_weather,

            "outfit":
                selected_outfit,

            "status":
                "success"
        })


        print(
            "\nSelected Outfit:"
        )

        print(
            f"Type: "
            f"{selected_outfit.get('outfit_type')}"
        )

        print(
            f"Final Score: "
            f"{selected_outfit.get('final_score')}"
        )


    # ========================================================
    # STEP 4
    # FINAL SUMMARY
    # ========================================================

    successful_days = sum(

        1

        for day in weekly_outfits

        if day["outfit"] is not None
    )


    print(
        "\n==================================="
    )

    print(
        "WEEKLY PLANNER COMPLETED"
    )

    print(
        "==================================="
    )

    print(
        f"Successful Days: "
        f"{successful_days}/{len(request.days)}"
    )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "status":
            "success",

        "start_date":
            str(request.start_date),

        "total_days":
            len(request.days),

        "planned_days":
            successful_days,

        "weekly_plan":
            weekly_outfits
    }