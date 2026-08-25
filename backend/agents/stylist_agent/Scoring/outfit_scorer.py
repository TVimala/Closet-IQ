# ============================================================
# OUTFIT SCORER
# STEPS 3 + 4 + 5
# ============================================================
from ..Reason.reasons import generate_outfit_reason
from .occasion import (
    calculate_occasion_score
)

from .preferences import (
    calculate_preference_score
)

from .weather import (
    calculate_weather_score
)


# ============================================================
# SCORE ALL OUTFITS
# ============================================================

def score_outfits(
    combinations,
    occasion,
    preferences,
    weather
):

    scored_outfits = []

    for outfit in combinations:

        # ----------------------------------------------------
        # STEP 3
        # OCCASION
        # ----------------------------------------------------

        occasion_score = (
            calculate_occasion_score(
                outfit,
                occasion
            )
        )

        # ----------------------------------------------------
        # STEP 4
        # PREFERENCES
        #
        # Short-term = 70%
        # Long-term  = 30%
        # ----------------------------------------------------

        preference_score = (
            calculate_preference_score(
                outfit,
                preferences
            )
        )

        # ----------------------------------------------------
        # STEP 5
        # WEATHER
        # ----------------------------------------------------

        weather_score = (
            calculate_weather_score(
                outfit,
                weather
            )
        )

        # ----------------------------------------------------
        # FINAL SCORE
        #
        # Occasion   = 50%
        # Preference = 30%
        # Weather    = 20%
        # ----------------------------------------------------

        final_score = (

            occasion_score * 0.50

            +

            preference_score * 0.30

            +

            weather_score * 0.20
        )

        scored_outfit = {
            **outfit,

            "occasion_score": round(
                occasion_score,
                2
            ),

            "preference_score": round(
                preference_score,
                2
            ),

            "weather_score": round(
                weather_score,
                2
            ),

            "final_score": round(
                final_score,
                2
            )
        }

        scored_outfits.append(
            scored_outfit
        )

    # --------------------------------------------------------
    # HIGHEST SCORE FIRST
    # --------------------------------------------------------

    scored_outfits.sort(
        key=lambda outfit:
        outfit["final_score"],
        reverse=True
    )

    for outfit in scored_outfits:

        outfit["reasons"] = generate_outfit_reason(
            outfit,
            occasion,
            preferences,
            weather
        )
    return scored_outfits