# ============================================================
# COLOR COMPATIBILITY
# STEP 6 - DYNAMIC COLOR COMPATIBILITY
# ============================================================

"""
Dynamic color compatibility engine.

IMPORTANT:
- No wardrobe IDs are hardcoded.
- No specific outfit combinations are hardcoded.
- Works with any user's wardrobe.
- New colors can be handled through color families.
- Unknown colors are handled safely instead of crashing.
"""


# ============================================================
# COLOR FAMILIES
# ============================================================

COLOR_FAMILIES = {
    "white": "neutral",
    "off_white": "neutral",
    "ivory": "neutral",
    "cream": "neutral",
    "beige": "neutral",
    "gray": "neutral",
    "grey": "neutral",
    "black": "neutral",

    "blue": "blue",
    "light_blue": "blue",
    "sky_blue": "blue",
    "navy": "blue",
    "royal_blue": "blue",

    "pink": "pink",
    "pastel_pink": "pink",
    "rose": "pink",
    "blush": "pink",

    "red": "red",
    "maroon": "red",
    "burgundy": "red",

    "green": "green",
    "emerald": "green",
    "olive": "green",
    "mint": "green",

    "yellow": "yellow",
    "mustard": "yellow",

    "brown": "brown",
    "tan": "brown",
    "camel": "brown",

    "purple": "purple",
    "lavender": "purple",
    "violet": "purple",

    "orange": "orange",
    "coral": "orange",

    "gold": "metallic",
    "silver": "metallic",
    "bronze": "metallic",

    # Used for patterns / multi-color items.
    "floral": "multicolor",
    "multicolor": "multicolor",
    "printed": "multicolor",
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_color(color):
    """
    Normalize a wardrobe color into a known color family.

    This function is intentionally tolerant because different
    users may store colors differently.
    """

    if color is None:
        return "unknown"

    color = str(color).strip().lower()

    if not color:
        return "unknown"

    color = color.replace("-", "_")
    color = color.replace(" ", "_")

    return COLOR_FAMILIES.get(color, "unknown")


# ============================================================
# BASE COLOR COMPATIBILITY
# ============================================================

# Scores represent visual compatibility between color families.
#
# These are general fashion color relationships, NOT wardrobe-
# specific combinations.
#
# The engine remains dynamic because it evaluates the actual
# colors present in the user's wardrobe.

BASE_COLOR_SCORES = {

    # --------------------------------------------------------
    # NEUTRALS
    # --------------------------------------------------------

    ("neutral", "neutral"): 95,

    ("neutral", "blue"): 92,
    ("neutral", "pink"): 92,
    ("neutral", "red"): 88,
    ("neutral", "green"): 90,
    ("neutral", "yellow"): 88,
    ("neutral", "brown"): 94,
    ("neutral", "purple"): 90,
    ("neutral", "orange"): 88,
    ("neutral", "metallic"): 92,

    # --------------------------------------------------------
    # BLUE
    # --------------------------------------------------------

    ("blue", "blue"): 82,
    ("blue", "pink"): 88,
    ("blue", "red"): 72,
    ("blue", "green"): 76,
    ("blue", "yellow"): 84,
    ("blue", "brown"): 88,
    ("blue", "purple"): 82,
    ("blue", "orange"): 78,
    ("blue", "metallic"): 88,

    # --------------------------------------------------------
    # PINK
    # --------------------------------------------------------

    ("pink", "pink"): 84,
    ("pink", "red"): 78,
    ("pink", "green"): 74,
    ("pink", "yellow"): 84,
    ("pink", "brown"): 86,
    ("pink", "purple"): 88,
    ("pink", "orange"): 76,
    ("pink", "metallic"): 90,

    # --------------------------------------------------------
    # RED
    # --------------------------------------------------------

    ("red", "red"): 72,
    ("red", "green"): 38,
    ("red", "yellow"): 62,
    ("red", "brown"): 70,
    ("red", "purple"): 68,
    ("red", "orange"): 58,
    ("red", "metallic"): 84,

    # --------------------------------------------------------
    # GREEN
    # --------------------------------------------------------

    ("green", "green"): 78,
    ("green", "yellow"): 82,
    ("green", "brown"): 88,
    ("green", "purple"): 70,
    ("green", "orange"): 76,
    ("green", "metallic"): 84,

    # --------------------------------------------------------
    # YELLOW
    # --------------------------------------------------------

    ("yellow", "yellow"): 76,
    ("yellow", "brown"): 90,
    ("yellow", "purple"): 78,
    ("yellow", "orange"): 72,
    ("yellow", "metallic"): 82,

    # --------------------------------------------------------
    # BROWN
    # --------------------------------------------------------

    ("brown", "brown"): 82,
    ("brown", "purple"): 76,
    ("brown", "orange"): 82,
    ("brown", "metallic"): 86,

    # --------------------------------------------------------
    # PURPLE
    # --------------------------------------------------------

    ("purple", "purple"): 80,
    ("purple", "orange"): 68,
    ("purple", "metallic"): 88,

    # --------------------------------------------------------
    # ORANGE
    # --------------------------------------------------------

    ("orange", "orange"): 72,
    ("orange", "metallic"): 82,

    # --------------------------------------------------------
    # METALLIC
    # --------------------------------------------------------

    ("metallic", "metallic"): 82,

    # --------------------------------------------------------
    # MULTICOLOR
    # --------------------------------------------------------

    # Multicolor / floral items are intentionally flexible.
    ("multicolor", "neutral"): 90,
    ("multicolor", "blue"): 78,
    ("multicolor", "pink"): 78,
    ("multicolor", "red"): 68,
    ("multicolor", "green"): 72,
    ("multicolor", "yellow"): 72,
    ("multicolor", "brown"): 82,
    ("multicolor", "purple"): 76,
    ("multicolor", "orange"): 70,
    ("multicolor", "metallic"): 78,

    ("multicolor", "multicolor"): 55,
}


# ============================================================
# COLOR PAIR SCORE
# ============================================================

def calculate_color_pair_score(color_a, color_b):
    """
    Calculate compatibility between two colors.

    Returns:
        int: score from 0 to 100
    """

    family_a = normalize_color(color_a)
    family_b = normalize_color(color_b)

    if family_a == "unknown" or family_b == "unknown":
        # Unknown colors should not automatically destroy
        # an otherwise valid outfit.
        return 70

    if family_a == family_b:
        pair = (family_a, family_b)

        if pair in BASE_COLOR_SCORES:
            return BASE_COLOR_SCORES[pair]

    pair = (family_a, family_b)

    if pair in BASE_COLOR_SCORES:
        return BASE_COLOR_SCORES[pair]

    reverse_pair = (family_b, family_a)

    if reverse_pair in BASE_COLOR_SCORES:
        return BASE_COLOR_SCORES[reverse_pair]

    # Safe fallback for color combinations that are not
    # explicitly represented.
    return 65


# ============================================================
# ITEM COLOR SCORE
# ============================================================

def calculate_item_color_score(item_a, item_b):
    """
    Calculate color compatibility between two wardrobe items.
    """

    if not item_a or not item_b:
        return 70

    return calculate_color_pair_score(
        item_a.get("color"),
        item_b.get("color")
    )


# ============================================================
# MAIN OUTFIT COLOR SCORE
# ============================================================

def calculate_outfit_color_score(outfit):
    """
    Calculate the overall color compatibility of an outfit.

    Important design decision:
    Accessories are NOT allowed to dominate the outfit's
    primary color score.

    Primary clothing + footwear are evaluated first.
    Accessories provide only a small influence.

    Returns:
        int: 0-100
    """

    items = outfit.get("items", [])

    if len(items) <= 1:
        return 100

    primary_items = []
    accessory_items = []

    accessory_categories = {
        "bag",
        "belt",
        "watch",
        "sunglasses",
        "scarf",
        "dupatta",
        "accessory",
    }

    for item in items:
        category = str(
            item.get("category", "")
        ).strip().lower()

        if category in accessory_categories:
            accessory_items.append(item)
        else:
            primary_items.append(item)

    # --------------------------------------------------------
    # PRIMARY COLOR RELATIONSHIPS
    # --------------------------------------------------------

    pair_scores = []

    for i in range(len(primary_items)):
        for j in range(i + 1, len(primary_items)):
            score = calculate_item_color_score(
                primary_items[i],
                primary_items[j]
            )
            pair_scores.append(score)

    if pair_scores:
        primary_score = sum(pair_scores) / len(pair_scores)
    else:
        primary_score = 100

    # --------------------------------------------------------
    # ACCESSORY INFLUENCE
    # --------------------------------------------------------

    accessory_scores = []

    if primary_items and accessory_items:

        for accessory in accessory_items:

            best_score = 0

            for primary in primary_items:

                score = calculate_item_color_score(
                    accessory,
                    primary
                )

                best_score = max(
                    best_score,
                    score
                )

            accessory_scores.append(best_score)

    if accessory_scores:

        accessory_score = (
            sum(accessory_scores)
            / len(accessory_scores)
        )

        # Accessories influence the final result,
        # but much less than the main clothing.
        final_score = (
            primary_score * 0.85
            + accessory_score * 0.15
        )

    else:
        final_score = primary_score

    return round(
        max(0, min(100, final_score))
    )


# ============================================================
# COLOR COMPATIBILITY CHECK
# ============================================================

def is_color_compatible(
    outfit,
    minimum_score=45
):
    """
    Determine whether an outfit passes the basic
    color compatibility threshold.

    The threshold is deliberately moderate so that the
    system does not eliminate creative combinations.
    """

    score = calculate_outfit_color_score(outfit)

    return score >= minimum_score


# ============================================================
# FILTER OUTFITS
# ============================================================

def filter_color_compatible_outfits(
    outfits,
    minimum_score=45
):
    """
    Filter dynamically generated outfits based on
    color compatibility.

    No wardrobe IDs or combinations are hardcoded.
    """

    compatible_outfits = []

    for outfit in outfits:

        color_score = calculate_outfit_color_score(
            outfit
        )

        if color_score >= minimum_score:

            enriched_outfit = {
                **outfit,
                "color_compatibility_score": color_score
            }

            compatible_outfits.append(
                enriched_outfit
            )

    return compatible_outfits