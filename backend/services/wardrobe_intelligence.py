from collections import defaultdict
from itertools import product
from math import ceil


# ============================================================
# CATEGORY GROUP DEFINITIONS
# ============================================================

CATEGORY_GROUPS = {

    # --------------------------------------------------------
    # UPPER BODY
    # --------------------------------------------------------

    "upper_body": {
        "top",
        "tshirt",
        "t_shirt",
        "shirt",
        "blouse",
        "crop_top",
        "tank_top",
        "polo",
        "sweater",
        "hoodie"
    },

    # --------------------------------------------------------
    # LOWER BODY
    # --------------------------------------------------------

    "lower_body": {
        "bottom",
        "jeans",
        "trousers",
        "pants",
        "shorts",
        "skirt",
        "joggers",
        "leggings"
    },

    # --------------------------------------------------------
    # ONE PIECE
    # --------------------------------------------------------

    "one_piece": {
        "dress",
        "jumpsuit",
        "romper",
        "co_ord_set"
    },

    # --------------------------------------------------------
    # OUTER LAYERS
    # --------------------------------------------------------

    "outer_layer": {
        "jacket",
        "blazer",
        "coat",
        "cardigan",
        "shrug"
    },

    # --------------------------------------------------------
    # TRADITIONAL / ETHNIC MAIN ITEMS
    # --------------------------------------------------------

    "traditional_main": {
        "saree",
        "kurti",
        "lehenga",
        "anarkali",
        "salwar_suit",
        "ethnic_set"
    },

    # --------------------------------------------------------
    # SWIMWEAR
    # --------------------------------------------------------

    "swimwear": {
        "bikini",
        "swimsuit",
        "swimwear"
    },

    # --------------------------------------------------------
    # SPECIAL LAYERS
    # --------------------------------------------------------

    "special_layer": {
        "cover_up",
        "beach_coverup",
        "kimono"
    },

    # --------------------------------------------------------
    # FOOTWEAR
    # --------------------------------------------------------

    "footwear": {
        "shoes",
        "sneakers",
        "heels",
        "sandals",
        "flats",
        "boots",
        "slippers",
        "loafers"
    },

    # --------------------------------------------------------
    # ACCESSORIES
    # --------------------------------------------------------

    "accessory": {
        "bag",
        "belt",
        "watch",
        "sunglasses",
        "dupatta",
        "scarf",
        "jewelry",
        "jewellery",
        "necklace",
        "earrings",
        "bracelet",
        "ring"
    }
}


# ============================================================
# ACCESSORY SUB-GROUPS
# ============================================================

ACCESSORY_CATEGORIES = {

    "bag": {
        "bag",
        "handbag",
        "tote",
        "clutch",
        "crossbody",
        "backpack"
    },

    "style_accessory": {
        "belt",
        "watch",
        "sunglasses"
    },

    "ethnic_accessory": {
        "dupatta",
        "scarf"
    },

    "jewelry": {
        "jewelry",
        "jewellery",
        "necklace",
        "earrings",
        "bracelet",
        "ring"
    }
}


# ============================================================
# COLOR FAMILIES
#
# This is intentionally rule-based.
# It does NOT map wardrobe IDs to each other.
# ============================================================

COLOR_FAMILIES = {

    "white": {
        "white",
        "ivory",
        "cream",
        "off_white",
        "off-white"
    },

    "black": {
        "black"
    },

    "grey": {
        "grey",
        "gray",
        "charcoal",
        "silver"
    },

    "blue": {
        "blue",
        "navy",
        "sky_blue",
        "sky-blue",
        "light_blue",
        "dark_blue",
        "royal_blue",
        "denim"
    },

    "green": {
        "green",
        "olive",
        "mint",
        "sage",
        "forest_green",
        "forest-green",
        "emerald"
    },

    "red": {
        "red",
        "maroon",
        "burgundy",
        "wine"
    },

    "pink": {
        "pink",
        "baby_pink",
        "baby-pink",
        "rose",
        "blush",
        "magenta"
    },

    "purple": {
        "purple",
        "lavender",
        "lilac",
        "violet"
    },

    "yellow": {
        "yellow",
        "mustard",
        "gold"
    },

    "orange": {
        "orange",
        "coral",
        "peach"
    },

    "brown": {
        "brown",
        "tan",
        "camel",
        "chocolate"
    },

    "beige": {
        "beige",
        "nude",
        "sand",
        "khaki"
    }
}


# ============================================================
# COLOR COMPATIBILITY
#
# Higher = better visual compatibility.
#
# This is a quality score, not a hard rule.
# Therefore unusual combinations are not automatically
# discarded.
# ============================================================

COLOR_COMPATIBILITY = {

    "white": {
        "white": 85,
        "black": 100,
        "grey": 95,
        "blue": 100,
        "green": 90,
        "red": 90,
        "pink": 95,
        "purple": 90,
        "yellow": 90,
        "orange": 90,
        "brown": 90,
        "beige": 95
    },

    "black": {
        "white": 100,
        "black": 80,
        "grey": 95,
        "blue": 90,
        "green": 85,
        "red": 90,
        "pink": 90,
        "purple": 90,
        "yellow": 90,
        "orange": 85,
        "brown": 85,
        "beige": 90
    },

    "grey": {
        "white": 95,
        "black": 95,
        "grey": 85,
        "blue": 95,
        "green": 90,
        "red": 85,
        "pink": 90,
        "purple": 90,
        "yellow": 90,
        "orange": 85,
        "brown": 85,
        "beige": 90
    },

    "blue": {
        "white": 100,
        "black": 90,
        "grey": 95,
        "blue": 80,
        "green": 75,
        "red": 70,
        "pink": 90,
        "purple": 85,
        "yellow": 85,
        "orange": 80,
        "brown": 90,
        "beige": 95
    },

    "green": {
        "white": 90,
        "black": 85,
        "grey": 90,
        "blue": 75,
        "green": 80,
        "red": 40,
        "pink": 80,
        "purple": 75,
        "yellow": 85,
        "orange": 75,
        "brown": 90,
        "beige": 90
    },

    "red": {
        "white": 90,
        "black": 90,
        "grey": 85,
        "blue": 70,
        "green": 40,
        "red": 75,
        "pink": 75,
        "purple": 70,
        "yellow": 70,
        "orange": 65,
        "brown": 75,
        "beige": 85
    },

    "pink": {
        "white": 95,
        "black": 90,
        "grey": 90,
        "blue": 90,
        "green": 80,
        "red": 75,
        "pink": 80,
        "purple": 90,
        "yellow": 85,
        "orange": 80,
        "brown": 85,
        "beige": 95
    },

    "purple": {
        "white": 90,
        "black": 90,
        "grey": 90,
        "blue": 85,
        "green": 75,
        "red": 70,
        "pink": 90,
        "purple": 80,
        "yellow": 75,
        "orange": 70,
        "brown": 80,
        "beige": 90
    },

    "yellow": {
        "white": 90,
        "black": 90,
        "grey": 90,
        "blue": 85,
        "green": 85,
        "red": 70,
        "pink": 85,
        "purple": 75,
        "yellow": 75,
        "orange": 70,
        "brown": 90,
        "beige": 90
    },

    "orange": {
        "white": 90,
        "black": 85,
        "grey": 85,
        "blue": 80,
        "green": 75,
        "red": 65,
        "pink": 80,
        "purple": 70,
        "yellow": 70,
        "orange": 75,
        "brown": 90,
        "beige": 90
    },

    "brown": {
        "white": 90,
        "black": 85,
        "grey": 85,
        "blue": 90,
        "green": 90,
        "red": 75,
        "pink": 85,
        "purple": 80,
        "yellow": 90,
        "orange": 90,
        "brown": 80,
        "beige": 95
    },

    "beige": {
        "white": 95,
        "black": 90,
        "grey": 90,
        "blue": 95,
        "green": 90,
        "red": 85,
        "pink": 95,
        "purple": 90,
        "yellow": 90,
        "orange": 90,
        "brown": 95,
        "beige": 85
    }
}


# ============================================================
# FIND GROUP FOR CATEGORY
# ============================================================

def get_category_group(category: str):

    if not category:
        return "other"

    category = category.lower().strip()

    for group_name, categories in CATEGORY_GROUPS.items():

        if category in categories:
            return group_name

    return "other"


# ============================================================
# FIND ACCESSORY TYPE
# ============================================================

def get_accessory_type(category: str):

    if not category:
        return "other"

    category = category.lower().strip()

    for accessory_type, categories in ACCESSORY_CATEGORIES.items():

        if category in categories:
            return accessory_type

    return "other"


# ============================================================
# NORMALIZE COLOR
# ============================================================

def normalize_color(color):

    if not color:
        return "unknown"

    normalized = (
        str(color)
        .lower()
        .strip()
        .replace(" ", "_")
    )

    for family, colors in COLOR_FAMILIES.items():

        if normalized in colors:
            return family

    return normalized


# ============================================================
# CALCULATE COLOR COMPATIBILITY BETWEEN TWO ITEMS
# ============================================================

def calculate_color_compatibility(
    item_a,
    item_b
):

    color_a = normalize_color(
        item_a.get("color")
    )

    color_b = normalize_color(
        item_b.get("color")
    )

    if (
        color_a == "unknown"
        or color_b == "unknown"
    ):
        return 70

    if color_a == color_b:

        return COLOR_COMPATIBILITY.get(
            color_a,
            {}
        ).get(
            color_b,
            80
        )

    score_a = COLOR_COMPATIBILITY.get(
        color_a,
        {}
    ).get(
        color_b
    )

    score_b = COLOR_COMPATIBILITY.get(
        color_b,
        {}
    ).get(
        color_a
    )

    if score_a is not None:
        return score_a

    if score_b is not None:
        return score_b

    # Unknown color relationship.
    # Do not reject it; give a neutral score.
    return 70


# ============================================================
# CALCULATE OUTFIT COLOR SCORE
# ============================================================

def calculate_outfit_color_score(
    items
):

    if len(items) < 2:
        return 100

    scores = []

    for first_index in range(
        len(items)
    ):

        for second_index in range(
            first_index + 1,
            len(items)
        ):

            score = (
                calculate_color_compatibility(
                    items[first_index],
                    items[second_index]
                )
            )

            scores.append(score)

    if not scores:
        return 100

    return round(
        sum(scores) / len(scores),
        2
    )


# ============================================================
# EXTRACT WEATHER INFORMATION
#
# Defensive helper because weather data can evolve.
# ============================================================

def extract_weather_values(weather):

    if not weather:
        return set()

    values = set()

    if isinstance(weather, str):

        values.add(
            weather.lower().strip()
        )

        return values

    if isinstance(weather, dict):

        relevant_keys = {
            "season",
            "weather",
            "condition",
            "conditions",
            "description",
            "temperature_category",
            "temperature",
            "temp"
        }

        for key, value in weather.items():

            key_lower = str(
                key
            ).lower()

            if key_lower not in relevant_keys:
                continue

            if isinstance(value, str):

                values.add(
                    value.lower().strip()
                )

            elif isinstance(value, (int, float)):

                values.add(
                    str(value)
                )

        return values

    return values


# ============================================================
# WEATHER RELEVANCE
#
# Returns:
#  1.0 = strong relevance
#  0.5 = unknown / neutral
#  0.0 = clearly mismatched
# ============================================================

def calculate_item_weather_relevance(
    item,
    weather
):

    if not weather:
        return 0.5

    item_seasons = {
        str(season).lower().strip()
        for season in item.get(
            "season",
            []
        )
    }

    weather_values = (
        extract_weather_values(
            weather
        )
    )

    if not item_seasons:
        return 0.5

    if not weather_values:
        return 0.5

    for season in item_seasons:

        if season in weather_values:
            return 1.0

    # General temperature/condition keywords

    joined_weather = " ".join(
        weather_values
    )

    cold_keywords = {
        "winter",
        "cold",
        "cool",
        "rain",
        "rainy",
        "monsoon"
    }

    hot_keywords = {
        "summer",
        "hot",
        "warm",
        "sunny"
    }

    if (
        any(
            keyword in joined_weather
            for keyword in cold_keywords
        )
        and "winter" in item_seasons
    ):
        return 1.0

    if (
        any(
            keyword in joined_weather
            for keyword in hot_keywords
        )
        and "summer" in item_seasons
    ):
        return 1.0

    return 0.5


# ============================================================
# OCCASION RELEVANCE
# ============================================================

def calculate_item_occasion_relevance(
    item,
    occasion
):

    if not occasion:
        return 0.5

    item_occasions = {
        str(value).lower().strip()
        for value in item.get(
            "occasion",
            []
        )
    }

    requested_occasion = (
        str(occasion)
        .lower()
        .strip()
    )

    if not item_occasions:
        return 0.5

    if requested_occasion in item_occasions:
        return 1.0

    # Useful general mappings

    occasion_groups = {

        "college": {
            "college",
            "casual",
            "everyday"
        },

        "casual": {
            "casual",
            "everyday",
            "college"
        },

        "party": {
            "party",
            "casual",
            "evening"
        },

        "formal": {
            "formal",
            "office",
            "business"
        },

        "office": {
            "office",
            "formal",
            "business"
        },

        "wedding": {
            "wedding",
            "festive",
            "traditional",
            "party"
        },

        "vacation": {
            "vacation",
            "travel",
            "beach",
            "casual"
        },

        "beach": {
            "beach",
            "vacation",
            "swimwear"
        }
    }

    related_occasions = occasion_groups.get(
        requested_occasion,
        set()
    )

    if item_occasions.intersection(
        related_occasions
    ):
        return 0.75

    return 0.0


# ============================================================
# SEASON RELEVANCE
# ============================================================

def calculate_item_season_relevance(
    item,
    season
):

    if not season:
        return 0.5

    item_seasons = {
        str(value).lower().strip()
        for value in item.get(
            "season",
            []
        )
    }

    requested_season = (
        str(season)
        .lower()
        .strip()
    )

    if not item_seasons:
        return 0.5

    if requested_season in item_seasons:
        return 1.0

    return 0.0


# ============================================================
# CALCULATE ITEM RELEVANCE SCORE
# ============================================================

def calculate_item_relevance_score(
    item,
    occasion=None,
    season=None,
    weather=None
):

    occasion_score = (
        calculate_item_occasion_relevance(
            item,
            occasion
        )
    )

    season_score = (
        calculate_item_season_relevance(
            item,
            season
        )
    )

    weather_score = (
        calculate_item_weather_relevance(
            item,
            weather
        )
    )

    # Occasion receives the strongest filtering influence.
    # Weather and season help refine the pool.
    relevance = (
        occasion_score * 0.50
        +
        season_score * 0.20
        +
        weather_score * 0.30
    )

    return round(
        relevance,
        3
    )


# ============================================================
# SELECT RELEVANT ITEMS
#
# IMPORTANT:
# This does NOT hardcode wardrobe IDs.
#
# It dynamically filters the user's actual wardrobe.
# ============================================================

def select_relevant_items(
    wardrobe_intelligence,
    occasion=None,
    season=None,
    weather=None
):

    grouped_items = (
        wardrobe_intelligence[
            "grouped_items"
        ]
    )

    relevant_grouped_items = (
        defaultdict(list)
    )

    for group_name, items in (
        grouped_items.items()
    ):

        for item in items:

            relevance_score = (
                calculate_item_relevance_score(
                    item,
                    occasion,
                    season,
                    weather
                )
            )

            enriched_item = {
                **item,
                "relevance_score":
                    relevance_score
            }

            # ------------------------------------------------
            # Keep strongly relevant items.
            #
            # Neutral items are also retained because some
            # wardrobe metadata may be incomplete.
            # ------------------------------------------------

            if relevance_score >= 0.50:

                relevant_grouped_items[
                    group_name
                ].append(
                    enriched_item
                )

    # --------------------------------------------------------
    # IMPORTANT FALLBACK
    #
    # If filtering becomes too aggressive because the wardrobe
    # contains sparse metadata, use the original available
    # wardrobe rather than returning zero outfits.
    # --------------------------------------------------------

    if not relevant_grouped_items:

        return grouped_items

    return dict(
        relevant_grouped_items
    )


# ============================================================
# ANALYZE COMPLETE WARDROBE
# ============================================================

def analyze_wardrobe(wardrobe):

    grouped_items = defaultdict(list)

    all_categories = set()
    all_styles = set()
    all_seasons = set()
    all_occasions = set()

    for item in wardrobe:

        # ----------------------------------------------------
        # Ignore unavailable items
        # ----------------------------------------------------

        if not item.get("is_available", True):
            continue

        category = (
            item.get("category", "unknown")
            .lower()
            .strip()
        )

        group = get_category_group(category)

        # ----------------------------------------------------
        # Enrich wardrobe item with intelligence metadata
        # ----------------------------------------------------

        enriched_item = {
            **item,
            "category": category,
            "wardrobe_group": group
        }

        # Add accessory subtype when applicable

        if group == "accessory":

            enriched_item[
                "accessory_type"
            ] = get_accessory_type(category)

        # ----------------------------------------------------
        # Store item inside its group
        # ----------------------------------------------------

        grouped_items[group].append(
            enriched_item
        )

        # ----------------------------------------------------
        # Learn wardrobe characteristics
        # ----------------------------------------------------

        all_categories.add(category)

        for style in item.get("style", []):

            all_styles.add(
                str(style).lower()
            )

        for season in item.get("season", []):

            all_seasons.add(
                str(season).lower()
            )

        for occasion in item.get("occasion", []):

            all_occasions.add(
                str(occasion).lower()
            )

    return {

        "grouped_items":
            dict(grouped_items),

        "available_groups":
            list(grouped_items.keys()),

        "available_categories":
            sorted(
                list(all_categories)
            ),

        "available_styles":
            sorted(
                list(all_styles)
            ),

        "available_seasons":
            sorted(
                list(all_seasons)
            ),

        "available_occasions":
            sorted(
                list(all_occasions)
            ),

        "total_available_items":
            sum(
                len(items)
                for items in grouped_items.values()
            )
    }


# ============================================================
# HELPER: GET GROUP ITEMS
# ============================================================

def get_group_items(
    grouped_items,
    group_name
):

    return grouped_items.get(
        group_name,
        []
    )


# ============================================================
# CREATE OUTFIT OBJECT
# ============================================================

def create_outfit(
    items,
    outfit_type
):

    return {

        "outfit_type":
            outfit_type,

        "items":
            items
    }


# ============================================================
# GET ITEM CATEGORIES
# ============================================================

def get_item_categories(items):

    return {
        item.get(
            "category",
            ""
        ).lower()
        for item in items
    }


# ============================================================
# GET ITEM STYLES
# ============================================================

def get_item_styles(item):

    return {
        str(style).lower()
        for style in item.get(
            "style",
            []
        )
    }


# ============================================================
# STYLE COMPATIBILITY
#
# Used mainly for optional accessories/layers.
# ============================================================

def calculate_style_overlap(
    item_a,
    item_b
):

    styles_a = get_item_styles(
        item_a
    )

    styles_b = get_item_styles(
        item_b
    )

    if not styles_a or not styles_b:
        return 0

    return len(
        styles_a.intersection(
            styles_b
        )
    )


# ============================================================
# CHECK BASIC ITEM COMPATIBILITY
# ============================================================

def are_items_compatible(
    item_a,
    item_b
):

    # --------------------------------------------------------
    # Style compatibility
    # --------------------------------------------------------

    style_overlap = calculate_style_overlap(
        item_a,
        item_b
    )

    # --------------------------------------------------------
    # Occasion compatibility
    # --------------------------------------------------------

    occasions_a = {
        str(occasion).lower()
        for occasion in item_a.get(
            "occasion",
            []
        )
    }

    occasions_b = {
        str(occasion).lower()
        for occasion in item_b.get(
            "occasion",
            []
        )
    }

    occasion_overlap = occasions_a.intersection(
        occasions_b
    )

    # --------------------------------------------------------
    # Color is intentionally NOT used as a hard rejection.
    #
    # Color is a quality signal and will be scored later.
    # --------------------------------------------------------

    if (
        style_overlap == 0
        and not occasion_overlap
    ):
        return False

    return True


# ============================================================
# SELECT COMPATIBLE ACCESSORIES
#
# Accessories are OPTIONAL.
# They are not blindly attached to every outfit.
# ============================================================

def select_compatible_accessories(
    base_items,
    accessory_items,
    max_accessories=2
):

    if not accessory_items:
        return [[]]

    selected_candidates = []

    for accessory in accessory_items:

        compatibility_score = 0

        for base_item in base_items:

            compatibility_score += (
                calculate_style_overlap(
                    accessory,
                    base_item
                )
            )

            accessory_occasions = {
                str(occasion).lower()
                for occasion in accessory.get(
                    "occasion",
                    []
                )
            }

            base_occasions = {
                str(occasion).lower()
                for occasion in base_item.get(
                    "occasion",
                    []
                )
            }

            if accessory_occasions.intersection(
                base_occasions
            ):
                compatibility_score += 1

        selected_candidates.append(
            (
                compatibility_score,
                accessory
            )
        )

    selected_candidates.sort(
        key=lambda value: value[0],
        reverse=True
    )

    meaningful = [
        item
        for score, item
        in selected_candidates
        if score > 0
    ]

    if not meaningful:
        return [[]]

    accessory_options = [[]]

    for accessory in meaningful:

        accessory_options.append(
            [accessory]
        )

    if max_accessories >= 2:

        for first_index in range(
            len(meaningful)
        ):

            for second_index in range(
                first_index + 1,
                len(meaningful)
            ):

                first = meaningful[
                    first_index
                ]

                second = meaningful[
                    second_index
                ]

                first_type = (
                    first.get(
                        "accessory_type"
                    )
                )

                second_type = (
                    second.get(
                        "accessory_type"
                    )
                )

                if (
                    first_type
                    == second_type
                ):
                    continue

                accessory_options.append(
                    [
                        first,
                        second
                    ]
                )

    return accessory_options


# ============================================================
# ADD OPTIONAL OUTERWEAR
#
# Outerwear is optional, but footwear remains mandatory.
# ============================================================

def generate_layer_variations(
    base_items,
    outerwear_items,
    footwear_items,
    outfit_type
):

    outfits = []

    for footwear in footwear_items:

        if not are_items_compatible(
            base_items[0],
            footwear
        ):
            continue

        outfit_items = (
            base_items
            + [footwear]
        )

        outfits.append(
            create_outfit(
                outfit_items,
                outfit_type
            )
        )

        for outerwear in outerwear_items:

            outerwear_compatible = all(
                are_items_compatible(
                    outerwear,
                    base_item
                )
                for base_item in base_items
            )

            if not outerwear_compatible:
                continue

            layered_items = (
                base_items
                + [
                    outerwear,
                    footwear
                ]
            )

            outfits.append(
                create_outfit(
                    layered_items,
                    outfit_type
                )
            )

    return outfits


# ============================================================
# GENERATE UPPER + LOWER OUTFITS
# ============================================================

def generate_upper_lower_outfits(
    grouped_items
):

    outfits = []

    upper_items = get_group_items(
        grouped_items,
        "upper_body"
    )

    lower_items = get_group_items(
        grouped_items,
        "lower_body"
    )

    outerwear_items = get_group_items(
        grouped_items,
        "outer_layer"
    )

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    if (
        not upper_items
        or not lower_items
        or not footwear_items
    ):
        return outfits

    for upper, lower in product(
        upper_items,
        lower_items
    ):

        if not are_items_compatible(
            upper,
            lower
        ):
            continue

        base_items = [
            upper,
            lower
        ]

        generated_outfits = (
            generate_layer_variations(
                base_items,
                outerwear_items,
                footwear_items,
                "upper_lower"
            )
        )

        outfits.extend(
            generated_outfits
        )

    return outfits


# ============================================================
# GENERATE ONE-PIECE OUTFITS
# ============================================================

def generate_one_piece_outfits(
    grouped_items
):

    outfits = []

    one_piece_items = get_group_items(
        grouped_items,
        "one_piece"
    )

    outerwear_items = get_group_items(
        grouped_items,
        "outer_layer"
    )

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    if not footwear_items:
        return outfits

    for one_piece in one_piece_items:

        for footwear in footwear_items:

            if not are_items_compatible(
                one_piece,
                footwear
            ):
                continue

            base_items = [
                one_piece,
                footwear
            ]

            outfits.append(
                create_outfit(
                    base_items,
                    "one_piece"
                )
            )

            for outerwear in outerwear_items:

                if not are_items_compatible(
                    one_piece,
                    outerwear
                ):
                    continue

                outfits.append(
                    create_outfit(
                        base_items
                        + [outerwear],
                        "one_piece"
                    )
                )

    return outfits


# ============================================================
# GENERATE KURTI OUTFITS
# ============================================================

def generate_kurti_outfits(
    grouped_items
):

    outfits = []

    kurti_items = []

    for item in get_group_items(
        grouped_items,
        "traditional_main"
    ):

        if item.get("category") == "kurti":
            kurti_items.append(item)

    lower_items = get_group_items(
        grouped_items,
        "lower_body"
    )

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    accessory_items = get_group_items(
        grouped_items,
        "accessory"
    )

    dupatta_items = [
        item
        for item in accessory_items
        if item.get(
            "accessory_type"
        ) == "ethnic_accessory"
        and item.get(
            "category"
        ) == "dupatta"
    ]

    if (
        not kurti_items
        or not lower_items
        or not footwear_items
    ):
        return outfits

    for kurti in kurti_items:

        for lower in lower_items:

            if not are_items_compatible(
                kurti,
                lower
            ):
                continue

            for footwear in footwear_items:

                if not are_items_compatible(
                    kurti,
                    footwear
                ):
                    continue

                base_items = [
                    kurti,
                    lower,
                    footwear
                ]

                outfits.append(
                    create_outfit(
                        base_items,
                        "kurti"
                    )
                )

                for dupatta in dupatta_items:

                    if not are_items_compatible(
                        kurti,
                        dupatta
                    ):
                        continue

                    outfits.append(
                        create_outfit(
                            base_items
                            + [dupatta],
                            "kurti"
                        )
                    )

    return outfits


# ============================================================
# GENERATE SAREE OUTFITS
# ============================================================

def generate_saree_outfits(
    grouped_items
):

    outfits = []

    sarees = [
        item
        for item in get_group_items(
            grouped_items,
            "traditional_main"
        )
        if item.get(
            "category"
        ) == "saree"
    ]

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    accessory_items = get_group_items(
        grouped_items,
        "accessory"
    )

    if (
        not sarees
        or not footwear_items
    ):
        return outfits

    for saree in sarees:

        for footwear in footwear_items:

            if not are_items_compatible(
                saree,
                footwear
            ):
                continue

            base_items = [
                saree,
                footwear
            ]

            outfits.append(
                create_outfit(
                    base_items,
                    "saree"
                )
            )

            accessory_options = (
                select_compatible_accessories(
                    base_items,
                    accessory_items,
                    max_accessories=2
                )
            )

            for accessories in accessory_options:

                if not accessories:
                    continue

                outfits.append(
                    create_outfit(
                        base_items
                        + accessories,
                        "saree"
                    )
                )

    return outfits


# ============================================================
# GENERATE LEHENGA / ETHNIC SET OUTFITS
# ============================================================

def generate_special_traditional_outfits(
    grouped_items
):

    outfits = []

    traditional_items = [
        item
        for item in get_group_items(
            grouped_items,
            "traditional_main"
        )
        if item.get("category")
        in {
            "lehenga",
            "anarkali",
            "salwar_suit",
            "ethnic_set"
        }
    ]

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    accessory_items = get_group_items(
        grouped_items,
        "accessory"
    )

    if (
        not traditional_items
        or not footwear_items
    ):
        return outfits

    for traditional_item in traditional_items:

        for footwear in footwear_items:

            if not are_items_compatible(
                traditional_item,
                footwear
            ):
                continue

            base_items = [
                traditional_item,
                footwear
            ]

            outfits.append(
                create_outfit(
                    base_items,
                    "traditional"
                )
            )

            accessory_options = (
                select_compatible_accessories(
                    base_items,
                    accessory_items,
                    max_accessories=2
                )
            )

            for accessories in accessory_options:

                if not accessories:
                    continue

                outfits.append(
                    create_outfit(
                        base_items
                        + accessories,
                        "traditional"
                    )
                )

    return outfits


# ============================================================
# GENERATE TRADITIONAL OUTFITS
# ============================================================

def generate_traditional_outfits(
    grouped_items
):

    outfits = []

    outfits.extend(
        generate_kurti_outfits(
            grouped_items
        )
    )

    outfits.extend(
        generate_saree_outfits(
            grouped_items
        )
    )

    outfits.extend(
        generate_special_traditional_outfits(
            grouped_items
        )
    )

    return outfits


# ============================================================
# GENERATE SWIMWEAR OUTFITS
# ============================================================

def generate_swimwear_outfits(
    grouped_items
):

    outfits = []

    swimwear_items = get_group_items(
        grouped_items,
        "swimwear"
    )

    special_layers = get_group_items(
        grouped_items,
        "special_layer"
    )

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    if (
        not swimwear_items
        or not footwear_items
    ):
        return outfits

    for swimwear in swimwear_items:

        for footwear in footwear_items:

            if not are_items_compatible(
                swimwear,
                footwear
            ):
                continue

            base_items = [
                swimwear,
                footwear
            ]

            outfits.append(
                create_outfit(
                    base_items,
                    "swimwear"
                )
            )

            for layer in special_layers:

                if not are_items_compatible(
                    swimwear,
                    layer
                ):
                    continue

                outfits.append(
                    create_outfit(
                        base_items
                        + [layer],
                        "swimwear"
                    )
                )

    return outfits


# ============================================================
# GENERATE SPECIAL LAYER OUTFITS
# ============================================================

def generate_special_layer_outfits(
    grouped_items
):

    outfits = []

    upper_items = get_group_items(
        grouped_items,
        "upper_body"
    )

    lower_items = get_group_items(
        grouped_items,
        "lower_body"
    )

    special_layers = get_group_items(
        grouped_items,
        "special_layer"
    )

    footwear_items = get_group_items(
        grouped_items,
        "footwear"
    )

    if (
        not special_layers
        or not footwear_items
    ):
        return outfits

    if upper_items and lower_items:

        for upper, lower in product(
            upper_items,
            lower_items
        ):

            if not are_items_compatible(
                upper,
                lower
            ):
                continue

            for layer in special_layers:

                if not are_items_compatible(
                    upper,
                    layer
                ):
                    continue

                for footwear in footwear_items:

                    base_items = [
                        upper,
                        lower,
                        layer,
                        footwear
                    ]

                    outfits.append(
                        create_outfit(
                            base_items,
                            "special_layer"
                        )
                    )

    return outfits


# ============================================================
# REMOVE DUPLICATE OUTFITS
# ============================================================

def remove_duplicate_outfits(
    outfits
):

    unique_outfits = []
    seen = set()

    for outfit in outfits:

        item_ids = tuple(
            sorted(
                item.get(
                    "id"
                )
                for item in outfit.get(
                    "items",
                    []
                )
                if item.get("id") is not None
            )
        )

        key = (
            outfit.get(
                "outfit_type"
            ),
            item_ids
        )

        if key in seen:
            continue

        seen.add(key)

        unique_outfits.append(
            outfit
        )

    return unique_outfits


# ============================================================
# VALIDATE OUTFIT COMPLETENESS
#
# Every generated outfit MUST contain footwear.
# ============================================================

def validate_outfit(
    outfit
):

    items = outfit.get(
        "items",
        []
    )

    if not items:
        return False

    categories = get_item_categories(
        items
    )

    outfit_type = outfit.get(
        "outfit_type"
    )

    # --------------------------------------------------------
    # FOOTWEAR IS ALWAYS REQUIRED
    # --------------------------------------------------------

    if not (
        categories.intersection(
            CATEGORY_GROUPS["footwear"]
        )
    ):
        return False

    # --------------------------------------------------------
    # ONE CATEGORY CANNOT APPEAR TWICE
    #
    # Exception: accessories can contain multiple categories.
    # --------------------------------------------------------

    structural_categories = []

    for item in items:

        group = get_category_group(
            item.get("category")
        )

        if group not in {
            "accessory",
            "footwear"
        }:

            structural_categories.append(
                group
            )

    if len(structural_categories) != len(
        set(structural_categories)
    ):
        return False

    # --------------------------------------------------------
    # UPPER + LOWER
    # --------------------------------------------------------

    if outfit_type == "upper_lower":

        has_upper = bool(
            categories.intersection(
                CATEGORY_GROUPS["upper_body"]
            )
        )

        has_lower = bool(
            categories.intersection(
                CATEGORY_GROUPS["lower_body"]
            )
        )

        return (
            has_upper
            and has_lower
        )

    # --------------------------------------------------------
    # ONE PIECE
    # --------------------------------------------------------

    if outfit_type == "one_piece":

        return bool(
            categories.intersection(
                CATEGORY_GROUPS["one_piece"]
            )
        )

    # --------------------------------------------------------
    # KURTI
    # --------------------------------------------------------

    if outfit_type == "kurti":

        return (
            "kurti" in categories
            and bool(
                categories.intersection(
                    CATEGORY_GROUPS[
                        "lower_body"
                    ]
                )
            )
        )

    # --------------------------------------------------------
    # SAREE
    # --------------------------------------------------------

    if outfit_type == "saree":

        return "saree" in categories

    # --------------------------------------------------------
    # TRADITIONAL
    # --------------------------------------------------------

    if outfit_type == "traditional":

        return bool(
            categories.intersection(
                CATEGORY_GROUPS[
                    "traditional_main"
                ]
            )
        )

    # --------------------------------------------------------
    # SWIMWEAR
    # --------------------------------------------------------

    if outfit_type == "swimwear":

        return bool(
            categories.intersection(
                CATEGORY_GROUPS[
                    "swimwear"
                ]
            )
        )

    # --------------------------------------------------------
    # SPECIAL LAYER
    # --------------------------------------------------------

    if outfit_type == "special_layer":

        return (
            bool(
                categories.intersection(
                    CATEGORY_GROUPS[
                        "upper_body"
                    ]
                )
            )
            and bool(
                categories.intersection(
                    CATEGORY_GROUPS[
                        "lower_body"
                    ]
                )
            )
            and bool(
                categories.intersection(
                    CATEGORY_GROUPS[
                        "special_layer"
                    ]
                )
            )
        )

    return False


# ============================================================
# FINAL OUTFIT VALIDATION
# ============================================================

def validate_all_outfits(
    outfits
):

    return [
        outfit
        for outfit in outfits
        if validate_outfit(
            outfit
        )
    ]


# ============================================================
# FILTER LOW QUALITY COLOR COMBINATIONS
#
# Color is used AFTER structural generation.
#
# We keep the threshold moderate so unusual but valid outfits
# are not unnecessarily removed.
# ============================================================

def filter_color_compatible_outfits(
    outfits,
    minimum_color_score=55
):

    filtered_outfits = []

    for outfit in outfits:

        color_score = (
            calculate_outfit_color_score(
                outfit.get(
                    "items",
                    []
                )
            )
        )

        enriched_outfit = {
            **outfit,
            "color_compatibility_score":
                color_score
        }

        if color_score >= minimum_color_score:

            filtered_outfits.append(
                enriched_outfit
            )

    return filtered_outfits


# ============================================================
# MAIN DYNAMIC OUTFIT GENERATOR
#
# New flow:
#
# Wardrobe
#    ↓
# Relevant item selection
#    ↓
# Dynamic outfit families
#    ↓
# Structural validation
#    ↓
# Color compatibility
#    ↓
# Duplicate removal
#    ↓
# Candidate pool
# ============================================================

def generate_dynamic_outfits(
    wardrobe_intelligence,
    occasion=None,
    season=None,
    weather=None
):

    # ========================================================
    # STEP A
    # RELEVANT ITEM SELECTION
    # ========================================================

    relevant_grouped_items = (
        select_relevant_items(
            wardrobe_intelligence,
            occasion=occasion,
            season=season,
            weather=weather
        )
    )

    all_outfits = []

    # ========================================================
    # FAMILY 1
    # WESTERN / UPPER + LOWER
    # ========================================================

    upper_lower_outfits = (
        generate_upper_lower_outfits(
            relevant_grouped_items
        )
    )

    all_outfits.extend(
        upper_lower_outfits
    )

    # ========================================================
    # FAMILY 2
    # ONE PIECE
    # ========================================================

    one_piece_outfits = (
        generate_one_piece_outfits(
            relevant_grouped_items
        )
    )

    all_outfits.extend(
        one_piece_outfits
    )

    # ========================================================
    # FAMILY 3
    # TRADITIONAL / ETHNIC
    # ========================================================

    traditional_outfits = (
        generate_traditional_outfits(
            relevant_grouped_items
        )
    )

    all_outfits.extend(
        traditional_outfits
    )

    # ========================================================
    # FAMILY 4
    # SWIMWEAR
    # ========================================================

    swimwear_outfits = (
        generate_swimwear_outfits(
            relevant_grouped_items
        )
    )

    all_outfits.extend(
        swimwear_outfits
    )

    # ========================================================
    # FAMILY 5
    # SPECIAL LAYERS
    # ========================================================

    special_layer_outfits = (
        generate_special_layer_outfits(
            relevant_grouped_items
        )
    )

    all_outfits.extend(
        special_layer_outfits
    )

    # ========================================================
    # STRUCTURAL VALIDATION
    # ========================================================

    all_outfits = (
        validate_all_outfits(
            all_outfits
        )
    )

    # ========================================================
    # COLOR COMPATIBILITY
    # ========================================================

    all_outfits = (
        filter_color_compatible_outfits(
            all_outfits
        )
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    all_outfits = (
        remove_duplicate_outfits(
            all_outfits
        )
    )

    return all_outfits