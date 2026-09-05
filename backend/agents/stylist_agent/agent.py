# ============================================================
# STYLIST AGENT
# ============================================================

from services.wardrobe_intelligence import (
    analyze_wardrobe,
    generate_dynamic_outfits
)

from .Scoring.diversity import (
    select_diverse_outfits,
    calculate_diversity_summary,
    calculate_combined_similarity
)

from .Scoring.outfit_scorer import (
    score_outfits
)

from .Scoring.color_compatibility import (
    filter_color_compatible_outfits
)


# ============================================================
# ACCESSORY CATEGORIES
# ============================================================

ACCESSORY_CATEGORIES = {
    "accessory",
    "belt",
    "watch",
    "sunglasses",
    "scarf",
    "dupatta",
    "jewelry",
    "necklace",
    "earrings",
    "bracelet",
    "ring",
    "hat",
    "cap",
}


# ============================================================
# COUNT ACCESSORIES IN OUTFIT
# ============================================================

def count_outfit_accessories(outfit):

    count = 0

    for item in outfit.get(
        "items",
        []
    ):

        category = str(
            item.get(
                "category",
                ""
            )
        ).lower().strip()

        wardrobe_group = str(
            item.get(
                "wardrobe_group",
                ""
            )
        ).lower().strip()

        item_type = str(
            item.get(
                "type",
                ""
            )
        ).lower().strip()

        if (
            category in ACCESSORY_CATEGORIES
            or wardrobe_group == "accessory"
            or item_type in ACCESSORY_CATEGORIES
        ):

            count += 1

    return count


# ============================================================
# GET OUTFIT ITEM IDS
# ============================================================

def get_outfit_item_ids(outfit):

    return {
        item.get("id")
        for item in outfit.get(
            "items",
            []
        )
        if item.get("id")
    }


# ============================================================
# CHECK EXACT PREVIOUS OUTFIT
# ============================================================

def is_same_outfit(
    candidate,
    previous_outfit
):

    if not previous_outfit:

        return False

    candidate_ids = (
        get_outfit_item_ids(
            candidate
        )
    )

    previous_ids = (
        get_outfit_item_ids(
            previous_outfit
        )
    )

    return (
        candidate_ids == previous_ids
        and
        bool(candidate_ids)
    )


# ============================================================
# CHECK GENUINE DIFFERENCE
# ============================================================

def is_genuinely_different(
    candidate,
    previous_outfit,
    similarity_threshold=0.60
):

    if not previous_outfit:

        return True

    similarity = (
        calculate_combined_similarity(
            candidate,
            previous_outfit
        )
    )

    return (
        similarity < similarity_threshold
    )


# ============================================================
# FILTER REGENERATION CANDIDATES
# ============================================================

def filter_regeneration_candidates(
    scored_outfits,
    previous_outfit,
    similarity_threshold=0.60
):

    if not previous_outfit:

        return scored_outfits

    regenerated_candidates = []

    exact_removed = 0
    similar_removed = 0

    for outfit in scored_outfits:

        # ----------------------------------------------------
        # REMOVE EXACT PREVIOUS OUTFIT
        # ----------------------------------------------------

        if is_same_outfit(
            outfit,
            previous_outfit
        ):

            exact_removed += 1

            continue

        # ----------------------------------------------------
        # REMOVE NEAR-DUPLICATE OUTFITS
        # ----------------------------------------------------

        if not is_genuinely_different(
            outfit,
            previous_outfit,
            similarity_threshold
        ):

            similar_removed += 1

            continue

        regenerated_candidates.append(
            outfit
        )

    print(
        "\n==================================="
    )

    print(
        "REGENERATION FILTER"
    )

    print(
        "==================================="
    )

    print(
        f"Original Scored Candidates: "
        f"{len(scored_outfits)}"
    )

    print(
        f"Exact Previous Outfit Removed: "
        f"{exact_removed}"
    )

    print(
        f"Near-Duplicate Outfits Removed: "
        f"{similar_removed}"
    )

    print(
        f"Genuinely Different Candidates: "
        f"{len(regenerated_candidates)}"
    )

    return regenerated_candidates


# ============================================================
# MAIN STYLIST AGENT
# ============================================================

def run_stylist_agent(
    data,
    weather,
    learned_preferences=None,
    weekly_mode=False
):

    print("\n===================================")

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
    # REGENERATION MODE
    # ========================================================

    regeneration_mode = (
        data.previous_outfit is not None
    )


    if regeneration_mode:

        print(
            "Mode: REGENERATION"
        )

        print(
            f"Regeneration Reason: "
            f"{data.regeneration_reason}"
        )

    elif weekly_mode:

        print(
            "Mode: WEEKLY PLANNING "
            "(FULL SCORED OUTFIT POOL)"
        )

    else:

        print(
            "Mode: SINGLE OUTFIT "
            "(TOP 5)"
        )


    # ========================================================
    # STEP 1
    # CONVERT WARDROBE TO DICTIONARIES
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


    # ========================================================
    # STEP 2
    # WARDROBE INTELLIGENCE
    # ========================================================

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
    # STEP 3
    # DYNAMIC OUTFIT GENERATION
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
        -
        len(color_compatible_outfits)
    )

    print(
        f"Removed by Color Compatibility: "
        f"{removed_by_color}"
    )


    # ========================================================
    # SAFETY FALLBACK
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

                "color_compatibility_score":
                    50
            }

            color_compatible_outfits.append(
                enriched_outfit
            )


    # ========================================================
    # STEP 5
    # SCORE ALL CANDIDATES
    # ========================================================

    scored_outfits = score_outfits(

        color_compatible_outfits,

        data.occasion,

        data.preferences,

        weather,

        learned_preferences,

        wardrobe_data
    )

    print(
        f"\nTotal Fully Scored Outfits: "
        f"{len(scored_outfits)}"
    )


    # ========================================================
    # ACCESSORY SUMMARY
    # ========================================================

    accessories_added = sum(

        1

        for outfit in scored_outfits

        if outfit.get(
            "accessory_added",
            False
        )
    )

    outfits_with_accessories = sum(

        1

        for outfit in scored_outfits

        if count_outfit_accessories(
            outfit
        ) > 0
    )

    print(
        f"Outfits With Accessories: "
        f"{outfits_with_accessories}/"
        f"{len(scored_outfits)}"
    )

    print(
        f"Optional Accessories Newly Added: "
        f"{accessories_added}/"
        f"{len(scored_outfits)}"
    )


    # ========================================================
    # STEP 6
    # REGENERATION MODE
    # ========================================================

    if regeneration_mode:

        regenerated_candidates = (
            filter_regeneration_candidates(

                scored_outfits,

                data.previous_outfit,

                similarity_threshold=0.60
            )
        )


        # ====================================================
        # NO DIFFERENT OUTFIT
        # ====================================================

        if not regenerated_candidates:

            print(
                "\n==================================="
            )

            print(
                "REGENERATION FAILED"
            )

            print(
                "==================================="
            )

            print(
                "No genuinely different outfit "
                "is available."
            )

            return {

                "status":
                    "no_regeneration_available",

                "requested_occasion":
                    data.occasion,

                "weather":
                    weather,

                "regeneration_reason":
                    data.regeneration_reason,

                "previous_outfit":
                    data.previous_outfit,

                "outfits":
                    [],

                "total_combinations":
                    len(scored_outfits)
            }


        # ====================================================
        # BEST REGENERATED OUTFIT
        # ====================================================

        regenerated_outfit = (
            regenerated_candidates[0]
        )

        print(
            "\n==================================="
        )

        print(
            "REGENERATED OUTFIT"
        )

        print(
            "==================================="
        )

        print(
            f"Reason: "
            f"{data.regeneration_reason}"
        )

        print(
            f"Outfit Type: "
            f"{regenerated_outfit['outfit_type']}"
        )

        print("Items:")

        for item in regenerated_outfit["items"]:

            print(
                f" - {item.get('color', '')} "
                f"{item.get('category', '')} "
                f"({item.get('id', '')})"
            )

        print(
            f"Accessories Present: "
            f"{count_outfit_accessories(regenerated_outfit)}"
        )

        print(
            f"Additional Accessory Added: "
            f"{regenerated_outfit.get('accessory_added', False)}"
        )

        if regenerated_outfit.get(
            "accessory_added",
            False
        ):

            print(
                f"Accessory Score: "
                f"{regenerated_outfit.get('accessory_score', 0)}/100"
            )

        print(
            f"Final Score: "
            f"{regenerated_outfit['final_score']}"
        )


        return {

            "status":
                "success",

            "requested_occasion":
                data.occasion,

            "weather":
                weather,

            "regeneration":
                True,

            "regeneration_reason":
                data.regeneration_reason,

            "previous_outfit":
                data.previous_outfit,

            "total_combinations":
                len(scored_outfits),

            "regenerated_candidates":
                len(regenerated_candidates),

            "outfits":
                [
                    regenerated_outfit
                ]
        }


    # ========================================================
    # STEP 7
    # WEEKLY MODE
    # ========================================================

    if weekly_mode:

        print(
            "\nWeekly Mode Active"
        )

        print(
            "Returning FULL scored outfit pool "
            "to weekly planner."
        )

        return {

            "status":
                "success",

            "requested_occasion":
                data.occasion,

            "weather":
                weather,

            "preference_weights": {

                "short_term":
                    0.70,

                "long_term":
                    0.30
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

            "scored_outfits":
                scored_outfits,

            "outfits":
                scored_outfits,

            "diversity":
                None
        }


    # ========================================================
    # STEP 8
    # NORMAL SINGLE-OUTFIT MODE
    # ========================================================

    diverse_outfits = (
        select_diverse_outfits(

            scored_outfits,

            limit=5,

            similarity_threshold=0.60
        )
    )

    diversity_summary = (
        calculate_diversity_summary(

            scored_outfits,

            diverse_outfits
        )
    )


    # ========================================================
    # DISPLAY TOP OUTFITS
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

        # ----------------------------------------------------
        # ACCESSORY INFORMATION
        # ----------------------------------------------------

        accessory_count = (
            count_outfit_accessories(
                outfit
            )
        )

        print(
            f"Accessories Present: "
            f"{accessory_count}/2"
        )

        # print(
        #     f"Additional Accessory Added: "
        #     f"{outfit.get('accessory_added', False)}"
        # )

        if outfit.get(
            "accessory_added",
            False
        ):

            print(
                f"Accessory Score: "
                f"{outfit.get('accessory_score', 0)}/100"
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


    if len(diverse_outfits) < 5:

        print(
            "\nNote: Only "
            f"{len(diverse_outfits)} genuinely "
            "different outfit(s) were available."
        )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "status":
            "success",

        "requested_occasion":
            data.occasion,

        "weather":
            weather,

        "preference_weights": {

            "short_term":
                0.70,

            "long_term":
                0.30
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