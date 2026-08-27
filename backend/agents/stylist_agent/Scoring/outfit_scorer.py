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

from .learned_preferences import (
    calculate_learned_preference_score
)


# ============================================================
# SCORE ALL OUTFITS
# ============================================================

def score_outfits(
    combinations,
    occasion,
    preferences,
    weather,
    learned_preferences=None
):

    scored_outfits = []


    # ========================================================
    # SCORE EACH OUTFIT
    # ========================================================

    for outfit in combinations:


        # ----------------------------------------------------
        # STEP 3
        # OCCASION SCORE
        # ----------------------------------------------------

        occasion_score = (
            calculate_occasion_score(
                outfit,
                occasion
            )
        )


        # ----------------------------------------------------
        # STEP 4
        # USER PREFERENCE SCORE
        # ----------------------------------------------------

        preference_score = (
            calculate_preference_score(
                outfit,
                preferences
            )
        )


        # ----------------------------------------------------
        # STEP 5
        # WEATHER SCORE
        # ----------------------------------------------------

        weather_score = (
            calculate_weather_score(
                outfit,
                weather
            )
        )


        # ----------------------------------------------------
        # LEARNED PREFERENCE SCORE
        # ----------------------------------------------------

        learned_preference_score = (
            calculate_learned_preference_score(
                outfit,
                learned_preferences
            )
        )


        # ----------------------------------------------------
        # FINAL SCORE
        #
        # Occasion             = 45%
        # Explicit Preferences = 25%
        # Weather              = 20%
        # Learned Feedback     = 10%
        # ----------------------------------------------------

        final_score = (
            occasion_score * 0.45
            +
            preference_score * 0.25
            +
            weather_score * 0.20
            +
            learned_preference_score * 0.10
        )


        # ----------------------------------------------------
        # STORE SCORED OUTFIT
        # ----------------------------------------------------

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

            "learned_preference_score": round(
                learned_preference_score,
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


    # ========================================================
    # SORT HIGHEST SCORE FIRST
    # ========================================================

    scored_outfits.sort(
        key=lambda outfit: outfit["final_score"],
        reverse=True
    )


    # ========================================================
    # GENERATE REASONS
    # ========================================================

    for outfit in scored_outfits:

        outfit["reasons"] = (
            generate_outfit_reason(
                outfit,
                occasion,
                preferences,
                weather
            )
        )


    return scored_outfits