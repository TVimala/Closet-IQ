# ============================================================
# OUTFIT HISTORY
# STEP 12
# ============================================================

from datetime import datetime


# ============================================================
# TEMPORARY IN-MEMORY STORAGE
#
# Later this will be replaced by a database.
# ============================================================

OUTFIT_HISTORY = []


# ============================================================
# GET ITEM IDS
# ============================================================

def get_item_ids(
    items
):

    if not items:

        return []

    item_ids = []

    for item in items:

        if isinstance(
            item,
            dict
        ):

            item_id = item.get(
                "id"
            )

        else:

            item_id = getattr(
                item,
                "id",
                None
            )

        if item_id:

            item_ids.append(
                item_id
            )

    return item_ids


# ============================================================
# CREATE OUTFIT HISTORY RECORD
# ============================================================

def create_outfit_history_record(
    user_id,
    outfit_id,
    items,
    occasion=None,
    date_worn=None,
    source="app_generated"
):

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    if date_worn is None:

        date_worn = (
            datetime.now()
            .date()
            .isoformat()
        )


    # --------------------------------------------------------
    # EXTRACT ITEM IDS
    # --------------------------------------------------------

    item_ids = get_item_ids(
        items
    )


    # --------------------------------------------------------
    # CREATE RECORD
    # --------------------------------------------------------

    history_record = {

        "history_id":
            f"H{len(OUTFIT_HISTORY) + 1:04d}",

        "user_id":
            user_id,

        "outfit_id":
            outfit_id,

        "item_ids":
            item_ids,

        "occasion":
            occasion,

        "date_worn":
            date_worn,

        "source":
            source,

        "created_at":
            datetime.now().isoformat()
    }


    return history_record


# ============================================================
# CHECK DUPLICATE HISTORY RECORD
#
# Prevent accidental multiple clicks on
# "I Wore It" from creating duplicates.
# ============================================================

def history_record_exists(
    user_id,
    outfit_id,
    date_worn
):

    for record in OUTFIT_HISTORY:

        if (

            record["user_id"] == user_id

            and

            record["outfit_id"] == outfit_id

            and

            record["date_worn"] == date_worn

        ):

            return True

    return False


# ============================================================
# RECORD OUTFIT AS WORN
# ============================================================

def record_outfit_worn(
    user_id,
    outfit_id,
    items,
    occasion=None,
    date_worn=None,
    source="app_generated"
):

    # --------------------------------------------------------
    # CREATE RECORD FIRST
    # --------------------------------------------------------

    record = create_outfit_history_record(

        user_id=user_id,

        outfit_id=outfit_id,

        items=items,

        occasion=occasion,

        date_worn=date_worn,

        source=source
    )


    # --------------------------------------------------------
    # PREVENT DUPLICATE
    # --------------------------------------------------------

    exists = history_record_exists(

        user_id=record["user_id"],

        outfit_id=record["outfit_id"],

        date_worn=record["date_worn"]
    )


    if exists:

        return {

            "status":
                "already_recorded",

            "message":
                "This outfit is already recorded "
                "as worn for this date.",

            "record":
                None
        }


    # --------------------------------------------------------
    # SAVE RECORD
    # --------------------------------------------------------

    OUTFIT_HISTORY.append(
        record
    )


    return {

        "status":
            "recorded",

        "message":
            "Outfit successfully recorded "
            "in outfit history.",

        "record":
            record
    }


# ============================================================
# GET USER OUTFIT HISTORY
# ============================================================

def get_user_outfit_history(
    user_id
):

    return [

        record

        for record in OUTFIT_HISTORY

        if record["user_id"] == user_id
    ]


# ============================================================
# GET RECENT OUTFIT HISTORY
# ============================================================

def get_recent_outfits(
    user_id,
    limit=10
):

    history = get_user_outfit_history(
        user_id
    )


    history.sort(

        key=lambda record:
        record["date_worn"],

        reverse=True
    )


    return history[:limit]


# ============================================================
# GET RECENTLY WORN ITEM IDS
# ============================================================

def get_recently_worn_item_ids(
    user_id,
    limit=10
):

    recent_outfits = get_recent_outfits(

        user_id=user_id,

        limit=limit
    )


    item_ids = set()


    for outfit in recent_outfits:

        for item_id in outfit[
            "item_ids"
        ]:

            item_ids.add(
                item_id
            )


    return sorted(
        list(item_ids)
    )


# ============================================================
# GET ITEM WEAR COUNT
#
# Returns None if the user has no outfit history.
#
# This preserves the difference between:
#
# UNKNOWN
# vs
# KNOWN ZERO
# ============================================================

def get_item_wear_count(
    user_id,
    item_id
):

    user_history = get_user_outfit_history(
        user_id
    )


    # No history exists at all
    # → Unknown, not zero

    if not user_history:

        return None


    wear_count = 0


    for record in user_history:

        if item_id in record["item_ids"]:

            wear_count += 1


    return wear_count