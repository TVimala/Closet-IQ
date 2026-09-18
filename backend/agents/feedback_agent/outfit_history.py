# ============================================================
# OUTFIT HISTORY
# STEP 12
#
# NOTE:
# Originally this module stored outfit history in an in-memory
# Python list (OUTFIT_HISTORY = []), explicitly marked as
# temporary ("Later this will be replaced by a database.").
#
# It is now backed by the OutfitHistoryDB table (see
# database/models.py) so history survives server restarts and
# is visible to the Notification scheduler.
#
# All function names and signatures below are preserved exactly
# as before so existing callers (Feedback Agent, Orchestrator)
# do not need to change.
# ============================================================

from datetime import datetime

from database.connection import SessionLocal
from database.models import OutfitHistoryDB


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
                str(item_id)
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
    # CREATE RECORD (in-memory representation, not yet saved)
    # --------------------------------------------------------

    db = SessionLocal()

    try:
        count = db.query(OutfitHistoryDB).count()
    finally:
        db.close()

    history_record = {

        "history_id":
            f"H{count + 1:04d}",

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

    db = SessionLocal()

    try:

        existing = db.query(OutfitHistoryDB).filter(
            OutfitHistoryDB.user_id == user_id,
            OutfitHistoryDB.outfit_id == str(outfit_id),
            OutfitHistoryDB.date_worn == date_worn
        ).first()

        return existing is not None

    finally:
        db.close()


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
    # SAVE RECORD TO DATABASE
    # --------------------------------------------------------

    db = SessionLocal()

    try:

        db_record = OutfitHistoryDB(
            history_id=record["history_id"],
            user_id=record["user_id"],
            outfit_id=str(record["outfit_id"]),
            item_ids=record["item_ids"],
            occasion=record["occasion"],
            date_worn=record["date_worn"],
            source=record["source"]
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        record["history_id"] = db_record.history_id

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


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

    db = SessionLocal()

    try:

        records = db.query(OutfitHistoryDB).filter(
            OutfitHistoryDB.user_id == user_id
        ).all()

        return [
            {
                "history_id": record.history_id,
                "user_id": record.user_id,
                "outfit_id": record.outfit_id,
                "item_ids": record.item_ids or [],
                "occasion": record.occasion,
                "date_worn": (
                    record.date_worn.isoformat()
                    if hasattr(record.date_worn, "isoformat")
                    else record.date_worn
                ),
                "source": record.source,
                "created_at": (
                    record.created_at.isoformat()
                    if record.created_at
                    else None
                )
            }
            for record in records
        ]

    finally:
        db.close()


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

        if str(item_id) in record["item_ids"]:

            wear_count += 1


    return wear_count


# ============================================================
# OUTFIT GENERATED / WORN TODAY HELPERS
#
# New helpers (additive) used by the Notification Agent flow
# to check "was an outfit generated today" / "has the user
# marked anything worn today" without duplicating DB logic
# inside the Orchestrator or the scheduler.
# ============================================================

def has_outfit_worn_today(user_id, today=None):

    if today is None:
        today = datetime.now().date()

    history = get_user_outfit_history(user_id)

    for record in history:
        if (
            str(record["date_worn"]) == str(today)
            and record["source"] == "confirmed_worn"
        ):
            return True

    return False


def log_outfit_generated(user_id, outfit_id, items, occasion=None):
    """
    Records that an outfit was generated today (source=
    "generated_only"). This is separate from record_outfit_worn
    (source="confirmed_worn"), which is only written when the
    user explicitly says they wore it. The distinction is what
    lets the Notification Agent tell the difference between
    "generated" and "worn" per the project spec.
    """

    today = datetime.now().date().isoformat()

    db = SessionLocal()

    try:
        count = db.query(OutfitHistoryDB).count()

        record = OutfitHistoryDB(
            history_id=f"H{count + 1:04d}",
            user_id=user_id,
            outfit_id=str(outfit_id),
            item_ids=get_item_ids(items),
            occasion=occasion,
            date_worn=today,
            source="generated_only"
        )

        db.add(record)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


def has_outfit_generated_today(user_id, today=None):

    if today is None:
        today = datetime.now().date()

    history = get_user_outfit_history(user_id)

    for record in history:
        if str(record["date_worn"]) == str(today):
            return True

    return False
