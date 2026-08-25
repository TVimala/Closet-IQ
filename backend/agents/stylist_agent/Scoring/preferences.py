# ============================================================
# PREFERENCE SCORING
# STEP 4
#
# SHORT TERM = 70%
# LONG TERM  = 30%
# ============================================================


# ============================================================
# NORMALIZE TEXT LIST
# ============================================================

def normalize_list(values):

    if not values:

        return []

    return [
        value.lower().strip()
        for value in values
    ]


# ============================================================
# TEMPORAL PREFERENCE SCORE
# MAXIMUM = 100
# ============================================================

def calculate_temporal_preference_score(
    outfit,
    preferences
):

    long_term = preferences.long_term
    short_term = preferences.short_term

    # --------------------------------------------------------
    # LONG TERM
    # --------------------------------------------------------

    long_term_score = (
        calculate_single_preference_score(
            outfit,
            long_term,
            include_avoid=False
        )
    )

    # --------------------------------------------------------
    # SHORT TERM
    # --------------------------------------------------------

    short_term_score = (
        calculate_single_preference_score(
            outfit,
            short_term,
            include_avoid=True
        )
    )

    # --------------------------------------------------------
    # TEMPORAL WEIGHT
    #
    # Short-term preferences represent
    # what the user wants NOW.
    #
    # Therefore they receive more weight.
    # --------------------------------------------------------

    final_score = (

        long_term_score * 0.30

        +

        short_term_score * 0.70
    )

    return round(
        min(final_score, 100),
        2
    )


# ============================================================
# SINGLE PREFERENCE SCORE
# MAXIMUM = 100
#
# STYLE    = 40
# COLOR    = 30
# FIT      = 20
# COMFORT  = 10
# ============================================================

def calculate_single_preference_score(
    outfit,
    preference,
    include_avoid=False
):

    items = outfit.get(
        "items",
        []
    )

    if not items:

        return 0

    style_score = calculate_style_score(
        items,
        preference.styles
    )

    color_score = calculate_color_score(
        items,
        preference.colors
    )

    fit_score = calculate_fit_score(
        items,
        preference.fits
    )

    comfort_score = calculate_comfort_score(
        items,
        preference.comfort_level
    )

    score = (
        style_score
        +
        color_score
        +
        fit_score
        +
        comfort_score
    )

    # --------------------------------------------------------
    # SHORT-TERM AVOID RULES
    # --------------------------------------------------------

    if include_avoid:

        avoid_penalty = calculate_avoid_penalty(
            items,
            preference
        )

        score -= avoid_penalty

    return round(
        max(
            min(score, 100),
            0
        ),
        2
    )


# ============================================================
# STYLE SCORE
# MAXIMUM = 40
# ============================================================

def calculate_style_score(
    items,
    preferred_styles
):

    preferred_styles = normalize_list(
        preferred_styles
    )

    if not preferred_styles:

        return 20

    matched = 0

    for item in items:

        item_styles = normalize_list(
            item.get(
                "style",
                []
            )
        )

        if any(
            style in preferred_styles
            for style in item_styles
        ):

            matched += 1

    return round(
        (
            matched / len(items)
        ) * 40,
        2
    )


# ============================================================
# COLOR SCORE
# MAXIMUM = 30
# ============================================================

def calculate_color_score(
    items,
    preferred_colors
):

    preferred_colors = normalize_list(
        preferred_colors
    )

    if not preferred_colors:

        return 15

    matched = 0

    for item in items:

        color = item.get(
            "color"
        )

        if (
            color
            and color.lower()
            in preferred_colors
        ):

            matched += 1

    return round(
        (
            matched / len(items)
        ) * 30,
        2
    )


# ============================================================
# FIT SCORE
# MAXIMUM = 20
# ============================================================

def calculate_fit_score(
    items,
    preferred_fits
):

    preferred_fits = normalize_list(
        preferred_fits
    )

    if not preferred_fits:

        return 10

    relevant_items = [
        item
        for item in items
        if item.get("fit")
    ]

    if not relevant_items:

        return 10

    matched = 0

    for item in relevant_items:

        fit = item.get(
            "fit"
        ).lower()

        if fit in preferred_fits:

            matched += 1

    return round(
        (
            matched
            / len(relevant_items)
        ) * 20,
        2
    )


# ============================================================
# COMFORT SCORE
# MAXIMUM = 10
# ============================================================

def calculate_comfort_score(
    items,
    comfort_level
):

    if comfort_level is None:

        return 5

    comfort_level = max(
        1,
        min(
            comfort_level,
            5
        )
    )

    comfort_styles = {
        "comfortable",
        "casual",
        "cozy"
    }

    comfort_fits = {
        "relaxed",
        "oversized",
        "loose"
    }

    relevant_items = [
        item
        for item in items
        if item.get("style")
        or item.get("fit")
    ]

    if not relevant_items:

        return 5

    matched = 0

    for item in relevant_items:

        styles = normalize_list(
            item.get(
                "style",
                []
            )
        )

        style_match = any(
            style in comfort_styles
            for style in styles
        )

        fit = item.get(
            "fit"
        )

        fit_match = (
            fit
            and fit.lower()
            in comfort_fits
        )

        if style_match or fit_match:

            matched += 1

    base_score = (
        matched
        / len(relevant_items)
    ) * 10

    importance_multiplier = (
        comfort_level / 5
    )

    return round(
        base_score
        * importance_multiplier,
        2
    )


# ============================================================
# SHORT-TERM AVOID PENALTY
# ============================================================

def calculate_avoid_penalty(
    items,
    short_term
):

    penalty = 0

    avoid_styles = set(
        normalize_list(
            short_term.avoid_styles
        )
    )

    avoid_colors = set(
        normalize_list(
            short_term.avoid_colors
        )
    )

    for item in items:

        item_styles = set(
            normalize_list(
                item.get(
                    "style",
                    []
                )
            )
        )

        item_color = item.get(
            "color"
        )

        # ----------------------------------------------------
        # AVOID STYLE
        # ----------------------------------------------------

        if avoid_styles.intersection(
            item_styles
        ):

            penalty += 25

        # ----------------------------------------------------
        # AVOID COLOR
        # ----------------------------------------------------

        if (
            item_color
            and item_color.lower()
            in avoid_colors
        ):

            penalty += 20

    return min(
        penalty,
        100
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def calculate_preference_score(
    outfit,
    preferences
):

    return calculate_temporal_preference_score(
        outfit,
        preferences
    )