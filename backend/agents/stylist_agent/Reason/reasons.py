# ============================================================
# RECOMMENDATION REASONS
# STEP 9
# ============================================================


# ============================================================
# HELPER: NORMALIZE TEXT
# ============================================================

def normalize_list(values):

    if not values:
        return []

    return [
        str(value).lower().strip()
        for value in values
    ]


# ============================================================
# HELPER: GET OUTFIT STYLES
# ============================================================

def get_outfit_styles(items):

    styles = set()

    for item in items:

        for style in item.get(
            "style",
            []
        ):

            styles.add(
                str(style).lower().strip()
            )

    return styles


# ============================================================
# HELPER: GET OUTFIT COLORS
# ============================================================

def get_outfit_colors(items):

    colors = set()

    for item in items:

        color = item.get(
            "color"
        )

        if color:

            colors.add(
                str(color).lower().strip()
            )

    return colors


# ============================================================
# HELPER: GET ITEM DESCRIPTION
# ============================================================

def describe_item(item):

    color = item.get(
        "color",
        ""
    )

    category = item.get(
        "category",
        "item"
    )

    if color:

        return f"{color} {category}"

    return category


# ============================================================
# HELPER: FIND PREFERRED STYLE MATCHES
# ============================================================

def get_preferred_style_matches(
    items,
    preferences
):

    matches = set()

    short_term = getattr(
        preferences,
        "short_term",
        None
    )

    long_term = getattr(
        preferences,
        "long_term",
        None
    )

    short_styles = normalize_list(
        getattr(
            short_term,
            "styles",
            []
        )
        if short_term
        else []
    )

    long_styles = normalize_list(
        getattr(
            long_term,
            "styles",
            []
        )
        if long_term
        else []
    )

    preferred_styles = set(
        short_styles + long_styles
    )

    outfit_styles = get_outfit_styles(
        items
    )

    matches = outfit_styles.intersection(
        preferred_styles
    )

    return matches


# ============================================================
# HELPER: FIND PREFERRED COLOR MATCHES
# ============================================================

def get_preferred_color_matches(
    items,
    preferences
):

    short_term = getattr(
        preferences,
        "short_term",
        None
    )

    long_term = getattr(
        preferences,
        "long_term",
        None
    )

    short_colors = normalize_list(
        getattr(
            short_term,
            "colors",
            []
        )
        if short_term
        else []
    )

    long_colors = normalize_list(
        getattr(
            long_term,
            "colors",
            []
        )
        if long_term
        else []
    )

    preferred_colors = set(
        short_colors + long_colors
    )

    outfit_colors = get_outfit_colors(
        items
    )

    return outfit_colors.intersection(
        preferred_colors
    )


# ============================================================
# HELPER: CHECK FOOTWEAR
# ============================================================

def has_footwear(items):

    footwear_categories = {
        "shoes",
        "sneakers",
        "heels",
        "sandals",
        "flats",
        "boots",
        "slippers",
        "loafers"
    }

    return any(

        item.get(
            "wardrobe_group"
        ) == "footwear"

        or

        item.get(
            "category"
        ) in footwear_categories

        for item in items
    )


# ============================================================
# HELPER: GET SHORT-TERM MATCHES
# ============================================================

def get_short_term_matches(
    items,
    preferences
):

    short_term = getattr(
        preferences,
        "short_term",
        None
    )

    if not short_term:
        return set(), set()

    short_styles = set(
        normalize_list(
            getattr(
                short_term,
                "styles",
                []
            )
        )
    )

    short_colors = set(
        normalize_list(
            getattr(
                short_term,
                "colors",
                []
            )
        )
    )

    outfit_styles = get_outfit_styles(
        items
    )

    outfit_colors = get_outfit_colors(
        items
    )

    style_matches = (
        outfit_styles.intersection(
            short_styles
        )
    )

    color_matches = (
        outfit_colors.intersection(
            short_colors
        )
    )

    return (
        style_matches,
        color_matches
    )


# ============================================================
# GENERATE HUMAN-READABLE REASONS
# ============================================================

def generate_outfit_reason(
    outfit,
    occasion,
    preferences,
    weather
):

    reasons = []

    occasion_score = outfit.get(
        "occasion_score",
        0
    )

    preference_score = outfit.get(
        "preference_score",
        0
    )

    weather_score = outfit.get(
        "weather_score",
        0
    )

    final_score = outfit.get(
        "final_score",
        0
    )

    items = outfit.get(
        "items",
        []
    )

    # ========================================================
    # 1. OCCASION REASON
    # ========================================================

    if occasion_score >= 90:

        reasons.append(
            f"Excellent match for {occasion}."
        )

    elif occasion_score >= 75:

        reasons.append(
            f"Well suited for {occasion}."
        )

    elif occasion_score >= 60:

        reasons.append(
            f"Reasonably suitable for {occasion}."
        )

    # ========================================================
    # 2. IDENTIFY ACTUAL PREFERENCE MATCHES
    # ========================================================

    style_matches = (
        get_preferred_style_matches(
            items,
            preferences
        )
    )

    color_matches = (
        get_preferred_color_matches(
            items,
            preferences
        )
    )

    # ========================================================
    # 3. SHORT-TERM PREFERENCE
    # PRIORITY OVER LONG-TERM
    # ========================================================

    (
        short_style_matches,
        short_color_matches
    ) = get_short_term_matches(
        items,
        preferences
    )

    if short_style_matches:

        style_text = ", ".join(
            sorted(short_style_matches)
        )

        reasons.append(
            f"The outfit matches your current "
            f"{style_text} style preference."
        )

    elif style_matches:

        style_text = ", ".join(
            sorted(style_matches)
        )

        reasons.append(
            f"The outfit fits your preferred "
            f"{style_text} style."
        )

    # ========================================================
    # 4. COLOR PREFERENCE
    # ========================================================

    if short_color_matches:

        color_text = ", ".join(
            sorted(short_color_matches)
        )

        reasons.append(
            f"It uses your currently preferred "
            f"{color_text} color."
        )

    elif color_matches:

        color_text = ", ".join(
            sorted(color_matches)
        )

        reasons.append(
            f"It includes your preferred "
            f"{color_text} color."
        )

    # ========================================================
    # 5. SPECIFIC ITEM HIGHLIGHT
    # ========================================================

    if items:

        highlighted_item = None

        # Prefer an item matching short-term style
        for item in items:

            item_styles = set(
                normalize_list(
                    item.get(
                        "style",
                        []
                    )
                )
            )

            if item_styles.intersection(
                short_style_matches
            ):

                highlighted_item = item
                break

        # Otherwise find short-term color match
        if highlighted_item is None:

            for item in items:

                color = item.get(
                    "color"
                )

                if (
                    color
                    and color.lower()
                    in short_color_matches
                ):

                    highlighted_item = item
                    break

        if highlighted_item:

            item_description = describe_item(
                highlighted_item
            )

            reasons.append(
                f"The {item_description} "
                f"helps give the look its character."
            )

    # ========================================================
    # 6. WEATHER
    # ========================================================

    if weather_score >= 90:

        reasons.append(
            "All pieces are well suited to today's weather."
        )

    elif weather_score >= 70:

        reasons.append(
            "Most pieces are suitable for today's weather."
        )

    # ========================================================
    # 7. FOOTWEAR
    # ========================================================

    if has_footwear(items):

        reasons.append(
            "Footwear completes the look."
        )

    # ========================================================
    # 8. PREFERENCE SCORE
    # ONLY ADD IF THERE IS NO SPECIFIC
    # PREFERENCE REASON
    # ========================================================

    if (
        preference_score >= 80
        and not style_matches
        and not color_matches
    ):

        reasons.append(
            "The overall combination strongly "
            "matches your preferences."
        )

    # ========================================================
    # 9. FINAL SCORE
    # ========================================================

    if final_score >= 85:

        reasons.append(
            "It has a very strong overall recommendation score."
        )

    elif (
        final_score >= 75
        and len(reasons) < 3
    ):

        reasons.append(
            "It has a strong overall recommendation score."
        )

    # ========================================================
    # 10. REMOVE DUPLICATE REASONS
    # ========================================================

    unique_reasons = []

    seen = set()

    for reason in reasons:

        normalized_reason = (
            reason.lower().strip()
        )

        if normalized_reason not in seen:

            seen.add(
                normalized_reason
            )

            unique_reasons.append(
                reason
            )

    # ========================================================
    # 11. LIMIT REASONS
    # ========================================================

    # We don't want a huge explanation.
    #
    # Maximum = 5 useful reasons

    unique_reasons = unique_reasons[:5]

    # ========================================================
    # 12. FALLBACK
    # ========================================================

    if not unique_reasons:

        unique_reasons.append(
            "This outfit achieved a good overall "
            "score across the available wardrobe factors."
        )

    return unique_reasons