# ============================================================
# OCCASION SCORING
# ============================================================


OCCASION_STYLE_SCORES = {

    "college": {
        "casual": 10,
        "comfortable": 10,
        "minimal": 8,
        "classic": 6,
        "trendy": 7,
        "formal": 3
    },

    "office": {
        "formal": 10,
        "classic": 10,
        "minimal": 8,
        "elegant": 7,
        "casual": 4,
        "comfortable": 3
    },

    "party": {
        "trendy": 10,
        "bold": 10,
        "maximal": 10,
        "elegant": 8,
        "formal": 8,
        "playful": 7,
        "casual": 3
    },

    "casual": {
        "casual": 10,
        "comfortable": 10,
        "minimal": 7,
        "classic": 6,
        "cozy": 7
    },

    "date": {
        "romantic": 10,
        "elegant": 9,
        "feminine": 9,
        "classic": 8,
        "minimal": 7,
        "trendy": 8,
        "casual": 5
    },

    "travel": {
        "comfortable": 10,
        "casual": 10,
        "vacation": 9,
        "minimal": 7,
        "boho": 7,
        "trendy": 6
    },

    "vacation": {
        "vacation": 10,
        "boho": 9,
        "casual": 8,
        "comfortable": 8,
        "playful": 8,
        "trendy": 7
    },

    "beach": {
        "vacation": 10,
        "boho": 9,
        "comfortable": 8,
        "casual": 8,
        "playful": 7
    },

    "brunch": {
        "casual": 9,
        "minimal": 9,
        "feminine": 8,
        "playful": 8,
        "trendy": 7,
        "comfortable": 7
    },

    "dinner": {
        "elegant": 10,
        "classic": 9,
        "romantic": 8,
        "formal": 8,
        "minimal": 7
    },

    "family_event": {
        "comfortable": 9,
        "traditional": 9,
        "ethnic": 9,
        "casual": 7,
        "classic": 7
    },

    "festive": {
        "traditional": 10,
        "ethnic": 10,
        "elegant": 8,
        "bold": 7,
        "feminine": 7
    },

    "formal": {
        "formal": 10,
        "classic": 9,
        "elegant": 8,
        "minimal": 7
    },

    "wedding": {
        "traditional": 10,
        "ethnic": 10,
        "elegant": 9,
        "feminine": 8,
        "bold": 7
    }
}


# ============================================================
# GET OUTFIT ITEMS
# ============================================================

def get_outfit_items(outfit):

    return outfit.get(
        "items",
        []
    )


# ============================================================
# ITEM OCCASION SCORE
# MAXIMUM = 100
# ============================================================

def calculate_item_occasion_score(
    item,
    requested_occasion
):

    requested_occasion = (
        requested_occasion
        .lower()
        .strip()
    )

    # --------------------------------------------------------
    # DIRECT OCCASION MATCH
    # MAXIMUM = 60
    # --------------------------------------------------------

    occasion_score = 0

    item_occasions = [
        occasion.lower()
        for occasion in item.get(
            "occasion",
            []
        )
    ]

    if requested_occasion in item_occasions:

        occasion_score = 60

    # --------------------------------------------------------
    # STYLE SUITABILITY
    # MAXIMUM = 40
    # --------------------------------------------------------

    style_score = 0

    style_rules = OCCASION_STYLE_SCORES.get(
        requested_occasion,
        {}
    )

    matched_style_points = []

    for style in item.get(
        "style",
        []
    ):

        points = style_rules.get(
            style.lower(),
            0
        )

        if points > 0:

            matched_style_points.append(
                points
            )

    if matched_style_points:

        average_style_points = (
            sum(matched_style_points)
            / len(matched_style_points)
        )

        style_score = (
            average_style_points / 10
        ) * 40

    return round(
        min(
            occasion_score + style_score,
            100
        ),
        2
    )


# ============================================================
# COMPLETE OUTFIT OCCASION SCORE
# ============================================================

def calculate_occasion_score(
    outfit,
    occasion
):

    outfit_items = get_outfit_items(
        outfit
    )

    if not outfit_items:

        return 0

    scores = []

    for item in outfit_items:

        scores.append(
            calculate_item_occasion_score(
                item,
                occasion
            )
        )

    return round(
        sum(scores) / len(scores),
        2
    )