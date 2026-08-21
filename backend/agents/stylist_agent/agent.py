from schemas.outfit_schema import StylistInput


# ============================================================
# STEP 3: OCCASION + STYLE SCORING RULES
# ============================================================

OCCASION_STYLE_SCORES = {

    "college": {
        "casual": 10,
        "comfortable": 10,
        "minimal": 8,
        "classic": 6,
        "formal": 2
    },

    "office": {
        "formal": 10,
        "classic": 10,
        "minimal": 8,
        "casual": 4,
        "comfortable": 2
    },

    "party": {
        "trendy": 10,
        "maximal": 10,
        "formal": 8,
        "casual": 3
    },

    "casual": {
        "casual": 10,
        "comfortable": 10,
        "minimal": 6,
        "classic": 5
    },

    "date": {
        "classic": 10,
        "minimal": 8,
        "trendy": 8,
        "formal": 6,
        "casual": 4
    },

    "travel": {
        "comfortable": 10,
        "casual": 10,
        "minimal": 6
    }
}


# ============================================================
# STEP 2: GENERATE VALID OUTFIT COMBINATIONS
# ============================================================

def generate_outfit_combinations(wardrobe):

    # --------------------------------------------------------
    # 1. Keep only available and usable wardrobe items
    # --------------------------------------------------------

    valid_items = [
        item for item in wardrobe
        if item.is_available
        and item.condition.lower() not in ["damaged", "unusable"]
    ]

    # --------------------------------------------------------
    # 2. Separate clothes by category
    # --------------------------------------------------------

    tops = [
        item for item in valid_items
        if item.category.lower() == "top"
    ]

    bottoms = [
        item for item in valid_items
        if item.category.lower() == "bottom"
    ]

    shoes = [
        item for item in valid_items
        if item.category.lower() == "shoes"
    ]

    print(f"\nAvailable Tops: {len(tops)}")
    print(f"Available Bottoms: {len(bottoms)}")
    print(f"Available Shoes: {len(shoes)}")

    combinations = []

    # --------------------------------------------------------
    # 3. Create every possible outfit combination
    # --------------------------------------------------------

    for top in tops:
        for bottom in bottoms:
            for shoe in shoes:

                outfit = {
                    "top": {
                        "id": top.id,
                        "name": top.color + " " + top.category,
                        "category": top.category,
                        "color": top.color,
                        "style": top.style,
                        "occasion": top.occasion
                    },

                    "bottom": {
                        "id": bottom.id,
                        "name": bottom.color + " " + bottom.category,
                        "category": bottom.category,
                        "color": bottom.color,
                        "style": bottom.style,
                        "occasion": bottom.occasion
                    },

                    "shoes": {
                        "id": shoe.id,
                        "name": shoe.color + " " + shoe.category,
                        "category": shoe.category,
                        "color": shoe.color,
                        "style": shoe.style,
                        "occasion": shoe.occasion
                    }
                }

                combinations.append(outfit)

    return combinations


# ============================================================
# STEP 3A: SCORE ONE ITEM FOR THE REQUESTED OCCASION
# ============================================================

def calculate_item_occasion_score(item, requested_occasion):

    requested_occasion = requested_occasion.lower()

    # =====================================
    # 1. OCCASION SCORE - Maximum 60 points
    # =====================================

    occasion_score = 0

    item_occasions = [
        occasion.lower()
        for occasion in item["occasion"]
    ]

    if requested_occasion in item_occasions:
        occasion_score = 60


    # =====================================
    # 2. STYLE SCORE - Maximum 40 points
    # =====================================

    style_score = 0

    style_rules = OCCASION_STYLE_SCORES.get(
        requested_occasion,
        {}
    )

    matched_style_points = []

    for style in item["style"]:

        points = style_rules.get(
            style.lower(),
            0
        )

        if points > 0:
            matched_style_points.append(points)


    # Average the matched style scores
    if matched_style_points:

        average_style_points = (
            sum(matched_style_points)
            / len(matched_style_points)
        )

        # Maximum possible raw style score is 10
        style_score = (
            average_style_points / 10
        ) * 40


    # =====================================
    # 3. FINAL ITEM SCORE
    # =====================================

    final_score = occasion_score + style_score

    return round(final_score, 2)


# ============================================================
# STEP 3B: CALCULATE TOTAL OUTFIT SCORE
# ============================================================

def calculate_occasion_score(outfit, occasion):

    top_score = calculate_item_occasion_score(
        outfit["top"],
        occasion
    )

    bottom_score = calculate_item_occasion_score(
        outfit["bottom"],
        occasion
    )

    shoe_score = calculate_item_occasion_score(
        outfit["shoes"],
        occasion
    )

    # Average of all three items
    final_score = (
        top_score
        + bottom_score
        + shoe_score
    ) / 3

    return round(final_score, 2)


# ============================================================
# STEP 3C: SCORE AND SORT ALL OUTFITS
# ============================================================

def score_outfits_by_occasion(combinations, occasion):

    scored_outfits = []

    for outfit in combinations:

        score = calculate_occasion_score(
            outfit,
            occasion
        )

        # Add score to this outfit
        outfit["occasion_score"] = score

        scored_outfits.append(outfit)

    # Sort highest score first
    scored_outfits.sort(
        key=lambda outfit: outfit["occasion_score"],
        reverse=True
    )

    return scored_outfits


# ============================================================
# MAIN STYLIST AGENT
# ============================================================

def run_stylist_agent(data: StylistInput):

    print("\n===================================")
    print("STYLIST AGENT STARTED")
    print("===================================")

    print(f"\nRequested Occasion: {data.occasion}")

    # --------------------------------------------------------
    # STEP 2
    # Generate all valid outfit combinations
    # --------------------------------------------------------

    combinations = generate_outfit_combinations(
        data.wardrobe
    )

    print(
        f"\nTotal Outfit Combinations Generated: "
        f"{len(combinations)}"
    )

    # --------------------------------------------------------
    # STEP 3
    # Score outfits based on occasion
    # --------------------------------------------------------

    scored_outfits = score_outfits_by_occasion(
        combinations,
        data.occasion
    )

    # --------------------------------------------------------
    # Display Top 3 in terminal
    # --------------------------------------------------------

    print("\n===================================")
    print("TOP 3 OUTFITS")
    print("===================================")

    for index, outfit in enumerate(
        scored_outfits[:3],
        start=1
    ):

        print(f"\nRank #{index}")

        print(
            f"Top: "
            f"{outfit['top']['name']}"
        )

        print(
            f"Bottom: "
            f"{outfit['bottom']['name']}"
        )

        print(
            f"Shoes: "
            f"{outfit['shoes']['name']}"
        )

        print(
            f"Occasion Score: "
            f"{outfit['occasion_score']}"
        )

    # --------------------------------------------------------
    # Return result to API
    # --------------------------------------------------------

    return {
        "status": "success",
        "requested_occasion": data.occasion,
        "total_combinations": len(scored_outfits),
        "outfits": scored_outfits
    }