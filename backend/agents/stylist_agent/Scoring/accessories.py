# ============================================================
# ACCESSORY HANDLING
# OPTIONAL ACCESSORY SELECTION
# ============================================================

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
# NORMALIZE TEXT
# ============================================================

def normalize_text(value):

    if value is None:
        return ""

    return str(value).lower().strip()


# ============================================================
# NORMALIZE MULTI-VALUE FIELD
# ============================================================

def normalize_values(value):

    if value is None:
        return set()

    if isinstance(value, list):

        values = set()

        for item in value:

            text = normalize_text(item)

            if text:
                values.add(text)

        return values

    text = normalize_text(value)

    if not text:
        return set()

    text = text.replace("/", ",")

    return {
        item.strip()
        for item in text.split(",")
        if item.strip()
    }


# ============================================================
# CHECK WHETHER ITEM IS AN ACCESSORY
# ============================================================

def is_accessory_item(item):

    category = normalize_text(
        item.get("category", "")
    )

    wardrobe_group = normalize_text(
        item.get("wardrobe_group", "")
    )

    item_type = normalize_text(
        item.get("type", "")
    )

    return (
        category in ACCESSORY_CATEGORIES
        or wardrobe_group == "accessory"
        or item_type in ACCESSORY_CATEGORIES
    )


# ============================================================
# GET ACCESSORIES FROM WARDROBE
# ============================================================

def get_available_accessories(wardrobe):

    accessories = []

    for item in wardrobe:

        # ----------------------------------------------------
        # Respect wardrobe availability
        # ----------------------------------------------------

        if item.get("is_available") is False:
            continue

        # ----------------------------------------------------
        # Only accessory items
        # ----------------------------------------------------

        if not is_accessory_item(item):
            continue

        accessories.append(item)

    return accessories


# ============================================================
# GET OUTFIT ITEMS
# ============================================================

def get_outfit_items(outfit):

    items = outfit.get(
        "items",
        []
    )

    if not isinstance(items, list):
        return []

    return items


# ============================================================
# GET OUTFIT ITEM IDS
# ============================================================
#
# Used to prevent adding an accessory that is already
# present in the outfit.
# ============================================================

def get_outfit_item_ids(outfit):

    item_ids = set()

    for item in get_outfit_items(outfit):

        item_id = item.get("id")

        if item_id is not None:

            item_ids.add(
                str(item_id)
            )

    return item_ids


def count_outfit_accessories(outfit):

    count = 0

    for item in get_outfit_items(outfit):

        if is_accessory_item(item):
            count += 1

    return count


# ============================================================
# GET OUTFIT TEXT FEATURES
# ============================================================

def get_outfit_features(outfit):

    items = get_outfit_items(outfit)

    colors = set()
    styles = set()
    occasions = set()
    categories = set()

    for item in items:

        # ----------------------------------------------------
        # COLOR
        # ----------------------------------------------------

        color_values = normalize_values(
            item.get("color", "")
        )

        colors.update(
            color_values
        )

        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        style_values = normalize_values(
            item.get("style", "")
        )

        styles.update(
            style_values
        )

        # ----------------------------------------------------
        # OCCASION
        # ----------------------------------------------------

        occasion_values = normalize_values(
            item.get("occasion", "")
        )

        occasions.update(
            occasion_values
        )

        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        category = normalize_text(
            item.get("category", "")
        )

        if category:

            categories.add(
                category
            )

    return {
        "colors": colors,
        "styles": styles,
        "occasions": occasions,
        "categories": categories
    }


# ============================================================
# ACCESSORY USEFULNESS
# ============================================================

def calculate_accessory_need(
    outfit,
    requested_occasion
):

    features = get_outfit_features(
        outfit
    )

    categories = features["categories"]
    styles = features["styles"]

    occasion = normalize_text(
        requested_occasion
    )

    score = 0

    # --------------------------------------------------------
    # OCCASION
    # --------------------------------------------------------

    if occasion in {
        "party",
        "wedding",
        "festive",
        "celebration",
        "date",
        "event"
    }:

        score += 35

    elif occasion in {
        "formal",
        "office",
        "business",
        "interview"
    }:

        score += 15

    elif occasion in {
        "college",
        "casual",
        "everyday"
    }:

        score += 5

    # --------------------------------------------------------
    # OUTFIT TYPE
    # --------------------------------------------------------

    if (
        "dress" in categories
        or "skirt" in categories
    ):

        score += 20

    if (
        "saree" in categories
        or "lehenga" in categories
        or "ethnic_set" in categories
        or "kurti" in categories
    ):

        score += 30

    if (
        "blazer" in categories
        or "jacket" in categories
        or "coat" in categories
    ):

        score += 15

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    if (
        "elegant" in styles
        or "romantic" in styles
        or "feminine" in styles
        or "bold" in styles
    ):

        score += 15

    # --------------------------------------------------------
    # KEEP CASUAL OUTFITS SIMPLE
    # --------------------------------------------------------

    if (
        occasion in {
            "college",
            "casual",
            "everyday"
        }
        and
        not (
            "dress" in categories
            or "skirt" in categories
            or "saree" in categories
            or "lehenga" in categories
            or "ethnic_set" in categories
        )
    ):

        score = min(
            score,
            20
        )

    return min(
        score,
        100
    )


# ============================================================
# ACCESSORY COLOR COMPATIBILITY
# ============================================================

def calculate_accessory_color_score(
    accessory,
    outfit
):

    accessory_colors = normalize_values(
        accessory.get("color", "")
    )

    outfit_colors = (
        get_outfit_features(outfit)["colors"]
    )

    if not accessory_colors:

        return 60

    if not outfit_colors:

        return 60

    # --------------------------------------------------------
    # Direct color match
    # --------------------------------------------------------

    if accessory_colors.intersection(
        outfit_colors
    ):

        return 90

    # --------------------------------------------------------
    # Neutral accessories
    # --------------------------------------------------------

    neutral_colors = {
        "black",
        "white",
        "cream",
        "beige",
        "brown",
        "gold",
        "silver",
        "navy"
    }

    if accessory_colors.intersection(
        neutral_colors
    ):

        return 80

    # --------------------------------------------------------
    # Unknown / unusual combinations
    # --------------------------------------------------------

    return 50


# ============================================================
# ACCESSORY STYLE COMPATIBILITY
# ============================================================

def calculate_accessory_style_score(
    accessory,
    outfit
):

    accessory_styles = normalize_values(
        accessory.get("style", "")
    )

    outfit_styles = (
        get_outfit_features(outfit)["styles"]
    )

    if not accessory_styles:

        return 65

    if not outfit_styles:

        return 65

    # --------------------------------------------------------
    # Direct style match
    # --------------------------------------------------------

    if accessory_styles.intersection(
        outfit_styles
    ):

        return 95

    compatible_style_pairs = {

        "minimal": {
            "classic",
            "elegant",
            "casual"
        },

        "classic": {
            "minimal",
            "formal",
            "elegant"
        },

        "elegant": {
            "minimal",
            "classic",
            "feminine",
            "romantic"
        },

        "feminine": {
            "elegant",
            "romantic"
        },

        "romantic": {
            "feminine",
            "elegant"
        },

        "bold": {
            "party",
            "elegant"
        },

        "casual": {
            "minimal",
            "comfortable",
            "classic"
        }
    }

    for outfit_style in outfit_styles:

        compatible_styles = (
            compatible_style_pairs.get(
                outfit_style,
                set()
            )
        )

        if accessory_styles.intersection(
            compatible_styles
        ):

            return 80

    return 60


# ============================================================
# ACCESSORY OCCASION COMPATIBILITY
# ============================================================

def calculate_accessory_occasion_score(
    accessory,
    requested_occasion
):

    accessory_occasions = normalize_values(
        accessory.get("occasion", "")
    )

    requested_occasion = normalize_text(
        requested_occasion
    )

    if not accessory_occasions:

        return 65

    # --------------------------------------------------------
    # Exact occasion
    # --------------------------------------------------------

    if requested_occasion in accessory_occasions:

        return 95

    # --------------------------------------------------------
    # Casual compatibility
    # --------------------------------------------------------

    if requested_occasion in {
        "college",
        "casual",
        "everyday"
    }:

        if "casual" in accessory_occasions:

            return 85

    # --------------------------------------------------------
    # Party / event compatibility
    # --------------------------------------------------------

    if requested_occasion in {
        "party",
        "wedding",
        "festive",
        "event"
    }:

        if (
            "party" in accessory_occasions
            or
            "elegant" in accessory_occasions
        ):

            return 85

    return 60


# ============================================================
# SCORE ACCESSORY
# ============================================================

def calculate_accessory_score(
    accessory,
    outfit,
    requested_occasion
):

    color_score = (
        calculate_accessory_color_score(
            accessory,
            outfit
        )
    )

    style_score = (
        calculate_accessory_style_score(
            accessory,
            outfit
        )
    )

    occasion_score = (
        calculate_accessory_occasion_score(
            accessory,
            requested_occasion
        )
    )

    final_score = (
        color_score * 0.35
        +
        style_score * 0.35
        +
        occasion_score * 0.30
    )

    return round(
        final_score,
        2
    )


# ============================================================
# SELECT BEST ACCESSORY
# ============================================================

def select_optional_accessory(
    outfit,
    wardrobe,
    requested_occasion
):

    accessories = get_available_accessories(
        wardrobe
    )

    if not accessories:

        return None

    # --------------------------------------------------------
    # Find items already present in the outfit
    # --------------------------------------------------------

    existing_item_ids = (
        get_outfit_item_ids(
            outfit
        )
    )

    # --------------------------------------------------------
    # Decide whether accessory is useful
    # --------------------------------------------------------

    accessory_need = (
        calculate_accessory_need(
            outfit,
            requested_occasion
        )
    )

    if count_outfit_accessories(outfit) >= 2:

        return None
    
    if accessory_need < 25:

        return None

    best_accessory = None
    best_score = 0

    for accessory in accessories:

        accessory_id = accessory.get(
            "id"
        )

        # ----------------------------------------------------
        # CRITICAL DUPLICATE PROTECTION
        # ----------------------------------------------------

        if (
            accessory_id is not None
            and
            str(accessory_id)
            in existing_item_ids
        ):

            continue

        score = (
            calculate_accessory_score(
                accessory,
                outfit,
                requested_occasion
            )
        )

        if score > best_score:

            best_score = score

            best_accessory = accessory

    # --------------------------------------------------------
    # No new accessory available
    # --------------------------------------------------------

    if (
        best_accessory is None
        or
        best_score < 75
    ):

        return None

    return {
        "item": best_accessory,
        "score": best_score,
        "need_score": accessory_need
    }


# ============================================================
# APPLY OPTIONAL ACCESSORY
# ============================================================

def add_optional_accessory(
    outfit,
    wardrobe,
    requested_occasion
):

    result = {
        **outfit
    }

    # --------------------------------------------------------
    # Copy items so original outfit is not modified
    # --------------------------------------------------------

    result["items"] = list(
        outfit.get(
            "items",
            []
        )
    )

    selected_accessory = (
        select_optional_accessory(
            outfit,
            wardrobe,
            requested_occasion
        )
    )

    # --------------------------------------------------------
    # No accessory required
    # --------------------------------------------------------

    if selected_accessory is None:

        result["accessory_added"] = False

        result["accessory_score"] = 0

        result["accessory_need_score"] = (
            calculate_accessory_need(
                outfit,
                requested_occasion
            )
        )

        return result

    # --------------------------------------------------------
    # Add ONLY ONE accessory
    # --------------------------------------------------------

    accessory = (
        selected_accessory["item"]
    )

    # --------------------------------------------------------
    # FINAL SAFETY CHECK
    # --------------------------------------------------------

    existing_item_ids = (
        get_outfit_item_ids(
            result
        )
    )

    accessory_id = accessory.get(
        "id"
    )

    if (
        accessory_id is not None
        and
        str(accessory_id)
        in existing_item_ids
    ):

        result["accessory_added"] = False

        result["accessory_score"] = 0

        result["accessory_need_score"] = (
            selected_accessory["need_score"]
        )

        return result

    # --------------------------------------------------------
    # Add accessory
    # --------------------------------------------------------

    result["items"].append(
        accessory
    )

    result["accessory_added"] = True

    result["accessory_score"] = (
        selected_accessory["score"]
    )

    result["accessory_need_score"] = (
        selected_accessory["need_score"]
    )

    return result