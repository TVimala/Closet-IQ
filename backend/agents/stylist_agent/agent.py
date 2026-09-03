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

from .Scoring.color_compatibility import (
    filter_color_compatible_outfits
)


def run_stylist_agent(
    data,
    weather,
    learned_preferences=None
):
    print("\n===================================")
    print("STYLIST AGENT STARTED")
    print("===================================")
    print(f"\nRequested Occasion: {data.occasion}")

    # ========================================================
    # STEP 1
    # CONVERT WARDROBE TO DICTIONARIES
    # ========================================================

    wardrobe_data = []

    for item in data.wardrobe:

        if hasattr(item, "model_dump"):
            wardrobe_data.append(
                item.model_dump()
            )
        else:
            wardrobe_data.append(item)

    # ========================================================
    # STEP 2
    # WARDROBE INTELLIGENCE
    # ========================================================

    wardrobe_intelligence = analyze_wardrobe(
        wardrobe_data
    )

    print(
        f"\nTotal Available Wardrobe Items: "
        f"{wardrobe_intelligence['total_available_items']}"
    )

    # ========================================================
    # STEP 3
    # DYNAMIC OUTFIT GENERATION
    # ========================================================

    combinations = generate_dynamic_outfits(
        wardrobe_intelligence
    )

    print(
        f"\nTotal Dynamic Outfit Candidates: "
        f"{len(combinations)}"
    )

    # ========================================================
    # STEP 4
    # COLOR COMPATIBILITY
    # ========================================================

    color_compatible_outfits = (
        filter_color_compatible_outfits(
            combinations,
            minimum_score=45
        )
    )

    print(
        f"Color-Compatible Outfit Candidates: "
        f"{len(color_compatible_outfits)}"
    )

    removed_by_color = (
        len(combinations)
        - len(color_compatible_outfits)
    )

    print(
        f"Removed by Color Compatibility: "
        f"{removed_by_color}"
    )

    # ========================================================
    # SAFETY FALLBACK
    # ========================================================
    #
    # If color filtering unexpectedly removes every
    # candidate, keep the original dynamic candidates.
    #
    # This prevents the color engine from making the
    # entire stylist fail because of unusual colors.
    # ========================================================

    if not color_compatible_outfits:

        print(
            "\nWARNING: Color filtering removed "
            "all candidates."
        )

        print(
            "Falling back to original dynamic "
            "outfit candidates."
        )

        color_compatible_outfits = []

        for outfit in combinations:

            enriched_outfit = {
                **outfit,
                "color_compatibility_score": 50
            }

            color_compatible_outfits.append(
                enriched_outfit
            )

    # ========================================================
    # STEP 5
    # EXISTING SCORING
    # ========================================================

    scored_outfits = score_outfits(
        color_compatible_outfits,
        data.occasion,
        data.preferences,
        weather,
        learned_preferences
    )

    # ========================================================
    # STEP 6
    # DIVERSITY
    # ========================================================

    diverse_outfits = select_diverse_outfits(
        scored_outfits,
        limit=3,
        similarity_threshold=0.60
    )

    diversity_summary = calculate_diversity_summary(
        scored_outfits,
        diverse_outfits
    )

    # ========================================================
    # DISPLAY TOP OUTFITS
    # ========================================================

    print("\n===================================")
    print("TOP DIVERSE OUTFITS")
    print("===================================")

    for index, outfit in enumerate(
        diverse_outfits,
        start=1
    ):

        print(f"\nRank #{index}")

        print(
            f"Outfit Type: "
            f"{outfit['outfit_type']}"
        )

        print("Items:")

        for item in outfit["items"]:

            print(
                f" - {item.get('color', '')} "
                f"{item.get('category', '')} "
                f"({item.get('id', '')})"
            )

        print(
            f"Color Compatibility Score: "
            f"{outfit.get('color_compatibility_score', 0)}/100"
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

    if len(diverse_outfits) < 3:

        print(
            "\nNote: Only "
            f"{len(diverse_outfits)} genuinely "
            "different outfit(s) were available."
        )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {
        "status": "success",

        "requested_occasion": data.occasion,

        "weather": weather,

        "preference_weights": {
            "short_term": 0.70,
            "long_term": 0.30
        },

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

        "total_combinations":
            len(scored_outfits),

        "diversity":
            diversity_summary,

        "outfits":
            diverse_outfits
    }