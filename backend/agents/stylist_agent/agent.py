# ============================================================
# STYLIST AGENT
# ============================================================

from services.wardrobe_intelligence import (
    analyze_wardrobe,
    generate_dynamic_outfits
)

from .Scoring.diversity import (
    select_diverse_outfits,
    calculate_diversity_summary
)

from .Scoring.outfit_scorer import (
    score_outfits
)


# ============================================================
# MAIN STYLIST AGENT
# ============================================================

def run_stylist_agent(
    data,
    weather,
    learned_preferences=None
):

    print(
        "\n==================================="
    )

    print(
        "STYLIST AGENT STARTED"
    )

    print(
        "==================================="
    )

    print(
        f"\nRequested Occasion: "
        f"{data.occasion}"
    )


    # ========================================================
    # STEP 1
    # ANALYZE USER WARDROBE
    # ========================================================

    wardrobe_data = []

    for item in data.wardrobe:

        if hasattr(
            item,
            "model_dump"
        ):

            wardrobe_data.append(
                item.model_dump()
            )

        else:

            wardrobe_data.append(
                item
            )


    wardrobe_intelligence = (
        analyze_wardrobe(
            wardrobe_data
        )
    )


    print(
        f"\nTotal Available Wardrobe Items: "
        f"{wardrobe_intelligence['total_available_items']}"
    )


    # ========================================================
    # STEP 2
    # GENERATE DYNAMIC OUTFITS
    # ========================================================

    combinations = (
        generate_dynamic_outfits(
            wardrobe_intelligence
        )
    )


    print(
        f"\nTotal Dynamic Outfit Candidates: "
        f"{len(combinations)}"
    )


    # ========================================================
    # STEP 3 + STEP 4 + STEP 5
    # SCORE ALL OUTFITS
    # ========================================================

    scored_outfits = score_outfits(

        combinations,

        data.occasion,

        data.preferences,

        weather,

        learned_preferences
    )


    # ========================================================
    # STEP 10
    # RECOMMENDATION DIVERSITY
    # ========================================================

    diverse_outfits = (
        select_diverse_outfits(

            scored_outfits,

            limit=3,

            similarity_threshold=0.60
        )
    )


    # ========================================================
    # STEP 10
    # DIVERSITY SUMMARY
    # ========================================================

    diversity_summary = (
        calculate_diversity_summary(

            scored_outfits,

            diverse_outfits
        )
    )


    # ========================================================
    # DISPLAY FINAL RECOMMENDATIONS
    # ========================================================

    print(
        "\n==================================="
    )

    print(
        "TOP DIVERSE OUTFITS"
    )

    print(
        "==================================="
    )


    for index, outfit in enumerate(

        diverse_outfits,

        start=1

    ):

        print(
            f"\nRank #{index}"
        )


        print(
            f"Outfit Type: "
            f"{outfit['outfit_type']}"
        )


        print(
            "Items:"
        )


        for item in outfit["items"]:

            print(
                f" - {item.get('color', '')} "
                f"{item.get('category', '')} "
                f"({item.get('id', '')})"
            )


        print(
            f"Occasion Score: "
            f"{outfit['occasion_score']}/100"
        )


        print(
            f"Preference Score: "
            f"{outfit['preference_score']}/100"
        )


        print(
            f"Weather Score: "
            f"{outfit['weather_score']}/100"
        )

        print(
            f"Learned Preference Score: "
            f"{outfit.get('learned_preference_score', 50)}/100"
        )

        print(
            f"Final Score: "
            f"{outfit['final_score']}/100"
        )


        # ====================================================
        # STEP 9
        # RECOMMENDATION REASONS
        # ====================================================

        # if outfit.get("reasons"):

        #     print(
        #         "Reasons:"
        #     )

        #     for reason in outfit["reasons"]:

        #         print(
        #             f" - {reason}"
        #         )


    # ========================================================
    # IF FEWER THAN 3 UNIQUE OUTFITS EXIST
    # ========================================================

    if len(diverse_outfits) < 3:

        print(
            "\nNote: Only "
            f"{len(diverse_outfits)} genuinely "
            "different outfit(s) were available."
        )


    # ========================================================
    # RETURN API RESPONSE
    # ========================================================

    return {

        "status":
            "success",


        "requested_occasion":
            data.occasion,


        "weather":
            weather,


        # ====================================================
        # TEMPORAL PREFERENCE WEIGHTS
        # ====================================================

        "preference_weights": {

            "short_term":
                0.70,

            "long_term":
                0.30
        },


        # ====================================================
        # WARDROBE SUMMARY
        # ====================================================

        "wardrobe_summary": {

            "total_available_items":
                wardrobe_intelligence[
                    "total_available_items"
                ],

            "available_groups":
                wardrobe_intelligence[
                    "available_groups"
                ]
        },


        # ====================================================
        # ALL GENERATED CANDIDATES
        # ====================================================

        "total_combinations":
            len(scored_outfits),


        # ====================================================
        # STEP 10 DIVERSITY INFORMATION
        # ====================================================

        "diversity":
            diversity_summary,


        # ====================================================
        # FINAL RECOMMENDATIONS
        # ====================================================

        "outfits":
            diverse_outfits
    }