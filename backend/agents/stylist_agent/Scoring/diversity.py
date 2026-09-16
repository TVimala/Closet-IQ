# ============================================================
# RECOMMENDATION DIVERSITY
# ============================================================


# ============================================================
# CATEGORY DEFINITIONS
# ============================================================

FOOTWEAR_CATEGORIES = {
    "shoes",
    "sneakers",
    "heels",
    "sandals",
    "flats",
    "boots",
    "slippers",
    "loafers"
}


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
    "cap"
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
# GET ITEM IDS
# ============================================================

def get_outfit_item_ids(outfit):

    items = get_outfit_items(
        outfit
    )

    return {
        item.get("id")
        for item in items
        if item.get("id")
    }


# ============================================================
# GET MAIN CLOTHING ITEMS
#
# Footwear is intentionally excluded.
#
# This prevents:
#
# Red dress + beige shoes
# Red dress + red shoes
#
# from being treated as completely different outfits.
# ============================================================

def get_main_clothing_ids(outfit):

    items = get_outfit_items(
        outfit
    )

    main_ids = set()

    for item in items:

        category = (
            item.get(
                "category",
                ""
            )
            .lower()
            .strip()
        )

        wardrobe_group = (
            item.get(
                "wardrobe_group",
                ""
            )
            .lower()
            .strip()
        )

        # Ignore footwear and accessories
        if (
            category in FOOTWEAR_CATEGORIES
            or wardrobe_group == "footwear"
            or category in ACCESSORY_CATEGORIES
            or wardrobe_group == "accessory"
        ):
            continue

        if item.get("id"):

            main_ids.add(
                item["id"]
            )

    return main_ids


# ============================================================
# GET STRUCTURAL OUTFIT SIGNATURE
#
# This represents the actual outfit construction.
#
# Examples:
#
# dress + shoes
# jumpsuit + shoes
# top + jeans + shoes
# kurti + flats
#
# Footwear is ignored because footwear alone should not
# create a completely new recommendation.
# ============================================================

def get_outfit_structure(outfit):

    items = get_outfit_items(
        outfit
    )

    structure = []

    for item in items:

        category = (
            item.get(
                "category",
                ""
            )
            .lower()
            .strip()
        )

        wardrobe_group = (
            item.get(
                "wardrobe_group",
                ""
            )
            .lower()
            .strip()
        )

        if (
            category in FOOTWEAR_CATEGORIES
            or wardrobe_group == "footwear"
            or category in ACCESSORY_CATEGORIES
            or wardrobe_group == "accessory"
        ):
            continue

        structure.append(
            (
                wardrobe_group,
                category
            )
        )

    return tuple(
        sorted(structure)
    )


# ============================================================
# CALCULATE ITEM-LEVEL JACCARD SIMILARITY
#
# 1.0 = exactly same items
# 0.0 = completely different items
# ============================================================

def calculate_outfit_similarity(
    outfit_a,
    outfit_b
):

    ids_a = get_outfit_item_ids(
        outfit_a
    )

    ids_b = get_outfit_item_ids(
        outfit_b
    )

    if not ids_a or not ids_b:

        return 0.0

    intersection = (
        ids_a.intersection(
            ids_b
        )
    )

    union = (
        ids_a.union(
            ids_b
        )
    )

    if not union:

        return 0.0

    similarity = (
        len(intersection)
        /
        len(union)
    )

    return round(
        similarity,
        2
    )


# ============================================================
# MAIN CLOTHING SIMILARITY
#
# This is more important than footwear similarity.
#
# Example:
#
# Red dress + beige shoes
# Red dress + red shoes
#
# Main similarity = 1.0
#
# Therefore they are considered near duplicates.
# ============================================================

def calculate_main_clothing_similarity(
    outfit_a,
    outfit_b
):

    ids_a = get_main_clothing_ids(
        outfit_a
    )

    ids_b = get_main_clothing_ids(
        outfit_b
    )

    if not ids_a or not ids_b:

        return 0.0

    intersection = (
        ids_a.intersection(
            ids_b
        )
    )

    union = (
        ids_a.union(
            ids_b
        )
    )

    if not union:

        return 0.0

    similarity = (
        len(intersection)
        /
        len(union)
    )

    return round(
        similarity,
        2
    )


# ============================================================
# STRUCTURE SIMILARITY
# ============================================================

def calculate_structure_similarity(
    outfit_a,
    outfit_b
):

    structure_a = get_outfit_structure(
        outfit_a
    )

    structure_b = get_outfit_structure(
        outfit_b
    )

    if not structure_a or not structure_b:

        return 0.0

    if structure_a == structure_b:

        return 1.0

    set_a = set(
        structure_a
    )

    set_b = set(
        structure_b
    )

    intersection = (
        set_a.intersection(
            set_b
        )
    )

    union = (
        set_a.union(
            set_b
        )
    )

    if not union:

        return 0.0

    return round(
        len(intersection)
        /
        len(union),
        2
    )


# ============================================================
# COMBINED DIVERSITY SIMILARITY
#
# Main clothing is weighted most heavily.
#
# Main clothing     = 70%
# Structure         = 20%
# Complete items    = 10%
#
# This means changing only shoes will not make an outfit
# sufficiently different.
# ============================================================

def calculate_combined_similarity(
    outfit_a,
    outfit_b
):

    main_similarity = (
        calculate_main_clothing_similarity(
            outfit_a,
            outfit_b
        )
    )

    structure_similarity = (
        calculate_structure_similarity(
            outfit_a,
            outfit_b
        )
    )

    item_similarity = (
        calculate_outfit_similarity(
            outfit_a,
            outfit_b
        )
    )

    combined_similarity = (

        main_similarity * 0.70

        +

        structure_similarity * 0.20

        +

        item_similarity * 0.10

    )

    return round(
        combined_similarity,
        2
    )


# ============================================================
# CHECK WHETHER OUTFIT IS TOO SIMILAR
# ============================================================

def is_near_duplicate(
    candidate,
    selected_outfits,
    similarity_threshold=0.60
):

    for selected in selected_outfits:

        similarity = (
            calculate_combined_similarity(
                candidate,
                selected
            )
        )

        if similarity >= similarity_threshold:

            return True

    return False


# ============================================================
# SELECT DIVERSE OUTFITS
#
# Highest-scoring outfit is always considered first.
#
# Later outfits are accepted only if they are sufficiently
# different from ALL already-selected outfits.
# ============================================================

def select_diverse_outfits(
    scored_outfits,
    limit=5,
    similarity_threshold=0.60
):

    if not scored_outfits:

        return []


    selected_outfits = []


    for outfit in scored_outfits:

        # ----------------------------------------------------
        # FIRST OUTFIT
        # ----------------------------------------------------

        if not selected_outfits:

            selected_outfits.append(
                outfit
            )

            continue


        # ----------------------------------------------------
        # CHECK AGAINST SELECTED OUTFITS
        # ----------------------------------------------------

        duplicate = (
            is_near_duplicate(

                outfit,

                selected_outfits,

                similarity_threshold
            )
        )


        if duplicate:

            continue


        # ----------------------------------------------------
        # ACCEPT GENUINELY DIFFERENT OUTFIT
        # ----------------------------------------------------

        selected_outfits.append(
            outfit
        )


        # ----------------------------------------------------
        # STOP AT REQUESTED LIMIT
        # ----------------------------------------------------

        if (
            len(selected_outfits)
            >= limit
        ):

            break


    return selected_outfits


# ============================================================
# DIVERSITY SUMMARY
# ============================================================

def calculate_diversity_summary(
    scored_outfits,
    selected_outfits
):

    total_candidates = len(
        scored_outfits
    )

    selected_count = len(
        selected_outfits
    )

    filtered_count = (
        total_candidates
        -
        selected_count
    )

    return {

        "total_candidates":
            total_candidates,

        "selected_count":
            selected_count,

        "filtered_near_duplicates":
            filtered_count,

        "unique_outfits":
            selected_count,

        "diversity_target":
            min(
                5,
                total_candidates
            )
    }