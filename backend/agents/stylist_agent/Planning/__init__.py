# ============================================================
# WEEKLY OUTFIT PLANNER
# STEP 11
# ============================================================


# ============================================================
# GET ITEM IDS
# ============================================================

def get_item_ids(outfit):

    return {
        item.get("id")
        for item in outfit.get("items", [])
        if item.get("id")
    }


# ============================================================
# GET MAIN ITEM IDS
#
# Used to prevent excessive repetition of the same clothing
# items across the week.
# ============================================================

def get_main_item_ids(outfit):

    main_categories = {
        "upper_body",
        "lower_body",
        "one_piece",
        "traditional_main"
    }

    ids = set()

    for item in outfit.get("items", []):

        if item.get("wardrobe_group") in main_categories:

            item_id = item.get("id")

            if item_id:
                ids.add(item_id)

    return ids


# ============================================================
# EXACT OUTFIT MATCH
# ============================================================

def is_exact_repeat(
    candidate,
    selected_outfits
):

    candidate_ids = get_item_ids(candidate)

    for selected in selected_outfits:

        selected_ids = get_item_ids(selected)

        if candidate_ids == selected_ids:
            return True

    return False


# ============================================================
# OUTFIT SIMILARITY
#
# Jaccard similarity
# ============================================================

def calculate_similarity(
    outfit_a,
    outfit_b
):

    ids_a = get_item_ids(outfit_a)
    ids_b = get_item_ids(outfit_b)

    if not ids_a or not ids_b:
        return 0.0

    intersection = ids_a.intersection(ids_b)
    union = ids_a.union(ids_b)

    if not union:
        return 0.0

    return len(intersection) / len(union)


# ============================================================
# NEAR DUPLICATE CHECK
# ============================================================

def is_near_duplicate(
    candidate,
    selected_outfits,
    threshold=0.60
):

    for selected in selected_outfits:

        similarity = calculate_similarity(
            candidate,
            selected
        )

        if similarity >= threshold:
            return True

    return False


# ============================================================
# COUNT ITEM USAGE
# ============================================================

def calculate_item_usage(
    selected_outfits
):

    usage = {}

    for outfit in selected_outfits:

        for item in outfit.get("items", []):

            item_id = item.get("id")

            if not item_id:
                continue

            usage[item_id] = (
                usage.get(item_id, 0) + 1
            )

    return usage


# ============================================================
# CALCULATE REPETITION PENALTY
#
# Same item can still be reused.
# We simply discourage excessive repetition.
# ============================================================

def calculate_repetition_penalty(
    candidate,
    selected_outfits
):

    if not selected_outfits:
        return 0

    usage = calculate_item_usage(
        selected_outfits
    )

    penalty = 0

    for item in candidate.get("items", []):

        item_id = item.get("id")

        if not item_id:
            continue

        count = usage.get(
            item_id,
            0
        )

        # First use → no penalty
        #
        # Second use → small penalty
        #
        # Third use → stronger penalty
        #
        # Fourth+ → strong penalty

        if count == 1:

            penalty += 5

        elif count == 2:

            penalty += 10

        elif count >= 3:

            penalty += 20

    return min(
        penalty,
        50
    )


# ============================================================
# OUTFIT TYPE DIVERSITY PENALTY
# ============================================================

def calculate_type_penalty(
    candidate,
    selected_outfits
):

    if not selected_outfits:
        return 0

    candidate_type = candidate.get(
        "outfit_type"
    )

    same_type_count = sum(

        1
        for outfit in selected_outfits
        if outfit.get("outfit_type") == candidate_type

    )

    # Encourage different outfit structures
    if same_type_count == 0:
        return 0

    if same_type_count == 1:
        return 3

    if same_type_count == 2:
        return 7

    return 12


# ============================================================
# WEEKLY SELECTION SCORE
#
# Original outfit score is still the main factor.
# Weekly penalties only adjust it.
# ============================================================

def calculate_weekly_selection_score(
    candidate,
    selected_outfits
):

    original_score = candidate.get(
        "final_score",
        0
    )

    repetition_penalty = (
        calculate_repetition_penalty(
            candidate,
            selected_outfits
        )
    )

    type_penalty = (
        calculate_type_penalty(
            candidate,
            selected_outfits
        )
    )

    weekly_score = (
        original_score
        - repetition_penalty
        - type_penalty
    )

    return round(
        max(
            weekly_score,
            0
        ),
        2
    )


# ============================================================
# SELECT BEST OUTFIT FOR A DAY
# ============================================================

def select_outfit_for_day(
    scored_outfits,
    selected_outfits,
    similarity_threshold=0.60
):

    if not scored_outfits:
        return None

    # --------------------------------------------------------
    # First preference:
    # highest scoring outfit that is not a duplicate
    # --------------------------------------------------------

    for candidate in scored_outfits:

        if is_exact_repeat(
            candidate,
            selected_outfits
        ):
            continue

        if is_near_duplicate(
            candidate,
            selected_outfits,
            similarity_threshold
        ):
            continue

        return candidate

    # --------------------------------------------------------
    # Fallback
    #
    # If everything is too similar, choose the candidate
    # with the best weekly-adjusted score.
    # --------------------------------------------------------

    best_candidate = None
    best_score = -1

    for candidate in scored_outfits:

        if is_exact_repeat(
            candidate,
            selected_outfits
        ):
            continue

        weekly_score = (
            calculate_weekly_selection_score(
                candidate,
                selected_outfits
            )
        )

        if weekly_score > best_score:

            best_score = weekly_score
            best_candidate = candidate

    return best_candidate


# ============================================================
# BUILD WEEKLY PLAN
# ============================================================

def build_weekly_plan(
    daily_candidates,
    similarity_threshold=0.60
):

    weekly_plan = []

    selected_outfits = []

    # --------------------------------------------------------
    # daily_candidates format:
    #
    # [
    #   {
    #       "date": "...",
    #       "occasion": "...",
    #       "weather": {...},
    #       "outfits": [...]
    #   }
    # ]
    # --------------------------------------------------------

    for day in daily_candidates:

        date = day.get(
            "date"
        )

        occasion = day.get(
            "occasion"
        )

        weather = day.get(
            "weather",
            {}
        )

        candidates = day.get(
            "outfits",
            []
        )

        selected = select_outfit_for_day(

            candidates,

            selected_outfits,

            similarity_threshold
        )

        if selected is None:

            weekly_plan.append({

                "date": date,

                "occasion": occasion,

                "weather": weather,

                "outfit": None,

                "status": "no_suitable_outfit"

            })

            continue

        # ----------------------------------------------------
        # Calculate weekly-adjusted score
        # ----------------------------------------------------

        weekly_score = (
            calculate_weekly_selection_score(

                selected,

                selected_outfits
            )
        )

        selected_outfit = {
            **selected,

            "weekly_selection_score":
                weekly_score
        }

        # ----------------------------------------------------
        # Store
        # ----------------------------------------------------

        selected_outfits.append(
            selected_outfit
        )

        weekly_plan.append({

            "date": date,

            "occasion": occasion,

            "weather": weather,

            "outfit":
                selected_outfit,

            "status":
                "success"

        })

    return weekly_plan


# ============================================================
# WEEKLY SUMMARY
# ============================================================

def calculate_weekly_summary(
    weekly_plan
):

    successful_days = [

        day
        for day in weekly_plan
        if day.get("outfit") is not None

    ]

    all_outfit_ids = []

    outfit_types = set()

    for day in successful_days:

        outfit = day["outfit"]

        outfit_types.add(
            outfit.get(
                "outfit_type"
            )
        )

        all_outfit_ids.append(
            frozenset(
                get_item_ids(outfit)
            )
        )

    unique_outfits = len(
        set(all_outfit_ids)
    )

    average_score = 0

    if successful_days:

        average_score = round(

            sum(
                day["outfit"].get(
                    "final_score",
                    0
                )
                for day in successful_days
            )
            / len(successful_days),

            2
        )

    return {

        "planned_days":
            len(weekly_plan),

        "successful_days":
            len(successful_days),

        "unique_outfits":
            unique_outfits,

        "outfit_types_used":
            len(outfit_types),

        "average_original_score":
            average_score

    }