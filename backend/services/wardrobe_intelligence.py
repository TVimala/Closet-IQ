from collections import defaultdict
from itertools import product


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
                style.lower()
            )

        for season in item.get("season", []):

            all_seasons.add(
                season.lower()
            )

        for occasion in item.get("occasion", []):

            all_occasions.add(
                occasion.lower()
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
        style.lower()
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
        occasion.lower()
        for occasion in item_a.get(
            "occasion",
            []
        )
    }

    occasions_b = {
        occasion.lower()
        for occasion in item_b.get(
            "occasion",
            []
        )
    }

    occasion_overlap = occasions_a.intersection(
        occasions_b
    )

    # --------------------------------------------------------
    # If both style and occasion have no relationship,
    # consider the combination weak.
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

            # Occasion overlap also helps

            accessory_occasions = {
                occasion.lower()
                for occasion in accessory.get(
                    "occasion",
                    []
                )
            }

            base_occasions = {
                occasion.lower()
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

    # Highest compatibility first

    selected_candidates.sort(
        key=lambda value: value[0],
        reverse=True
    )

    # --------------------------------------------------------
    # Keep only meaningful accessories.
    #
    # We do NOT force accessories into every outfit.
    # --------------------------------------------------------

    meaningful = [
        item
        for score, item
        in selected_candidates
        if score > 0
    ]

    if not meaningful:
        return [[]]

    accessory_options = [[]]

    # One accessory

    for accessory in meaningful:

        accessory_options.append(
            [accessory]
        )

    # Two accessories

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

                # Do not add two accessories
                # from the same subtype.

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

    # --------------------------------------------------------
    # FOOTWEAR IS REQUIRED
    # --------------------------------------------------------

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

        # ----------------------------------------------------
        # Add compatible outerwear
        # ----------------------------------------------------

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
#
# Example:
#
# top + jeans + shoes
#
# top + trousers + shoes + blazer
#
# top + skirt + shoes + bag
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

        # ----------------------------------------------------
        # Basic compatibility
        # ----------------------------------------------------

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
#
# Example:
#
# dress + shoes
# dress + shoes + jacket
#
# jumpsuit + shoes
# jumpsuit + shoes + blazer
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

        # ----------------------------------------------------
        # Mandatory footwear
        # ----------------------------------------------------

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

            # ------------------------------------------------
            # Optional outerwear
            # ------------------------------------------------

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
#
# Kurti is NOT treated as a complete outfit.
#
# Preferred:
#
# kurti + lower + footwear
#
# kurti + lower + dupatta + footwear
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

                # Base complete outfit

                outfits.append(
                    create_outfit(
                        base_items,
                        "kurti"
                    )
                )

                # ------------------------------------------------
                # Optional dupatta
                # ------------------------------------------------

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
#
# Saree + footwear
#
# Optional:
# saree + footwear + bag
# saree + footwear + ethnic accessory
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

            # ------------------------------------------------
            # Saree without accessory
            # ------------------------------------------------

            outfits.append(
                create_outfit(
                    base_items,
                    "saree"
                )
            )

            # ------------------------------------------------
            # Add compatible accessories
            # ------------------------------------------------

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

            # ------------------------------------------------
            # Add meaningful accessories
            # ------------------------------------------------

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
#
# This wrapper handles all traditional families.
# ============================================================

def generate_traditional_outfits(
    grouped_items
):

    outfits = []

    # --------------------------------------------------------
    # Kurti
    # --------------------------------------------------------

    outfits.extend(
        generate_kurti_outfits(
            grouped_items
        )
    )

    # --------------------------------------------------------
    # Saree
    # --------------------------------------------------------

    outfits.extend(
        generate_saree_outfits(
            grouped_items
        )
    )

    # --------------------------------------------------------
    # Lehenga / Anarkali /
    # Salwar Suit / Ethnic Set
    # --------------------------------------------------------

    outfits.extend(
        generate_special_traditional_outfits(
            grouped_items
        )
    )

    return outfits


# ============================================================
# GENERATE SWIMWEAR OUTFITS
#
# Only generated when swimwear actually exists.
#
# Example:
#
# swimsuit + footwear
# swimsuit + coverup + footwear
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

            # Optional cover-up

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
#
# This is mainly useful for beach/vacation wardrobes.
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

    # --------------------------------------------------------
    # upper + lower + cover-up + footwear
    # --------------------------------------------------------

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
#
# Prevents identical item combinations from appearing
# multiple times.
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
# IMPORTANT:
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
# MAIN DYNAMIC OUTFIT GENERATOR
# ============================================================

def generate_dynamic_outfits(
    wardrobe_intelligence
):

    grouped_items = wardrobe_intelligence[
        "grouped_items"
    ]

    all_outfits = []

    # ========================================================
    # FAMILY 1
    # WESTERN / UPPER + LOWER
    # ========================================================

    upper_lower_outfits = (
        generate_upper_lower_outfits(
            grouped_items
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
            grouped_items
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
            grouped_items
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
            grouped_items
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
            grouped_items
        )
    )

    all_outfits.extend(
        special_layer_outfits
    )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    all_outfits = (
        remove_duplicate_outfits(
            all_outfits
        )
    )

    # ========================================================
    # FINAL COMPLETENESS CHECK
    #
    # This is the safety net.
    # Even if a future generator creates something
    # incomplete, it will NOT reach the scoring stage.
    # ========================================================

    all_outfits = (
        validate_all_outfits(
            all_outfits
        )
    )

    return all_outfits