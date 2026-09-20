# ============================================================
# FEEDBACK STORE
#
# Persists validated feedback events and reconstructs the
# corresponding outfit from the existing outfit_id/item IDs
# when feedback is loaded for learning.
#
# No database schema change is required.
# ============================================================

from datetime import datetime, timezone

from database.connection import SessionLocal
from database.models import FeedbackRecordDB, WardrobeItem, OutfitHistoryDB

# ============================================================
# EXTRACT ITEM IDS FROM OUTFIT ID
# Example: "13-17-5-9" -> ["13", "17", "5", "9"]
# ============================================================

def _extract_item_ids_from_outfit_id(outfit_id):
    if outfit_id is None:
        return []

    return [
        part.strip()
        for part in str(outfit_id).split("-")
        if part.strip()
    ]


# ============================================================
# GET OUTFIT OCCASION FROM EXISTING OUTFIT HISTORY
# ============================================================

def _get_outfit_occasion(db, user_id, outfit_id):
    history_record = (
        db.query(OutfitHistoryDB)
        .filter(
            OutfitHistoryDB.user_id == user_id,
            OutfitHistoryDB.outfit_id == str(outfit_id)
        )
        .order_by(OutfitHistoryDB.created_at.desc())
        .first()
    )

    if not history_record:
        return None

    return history_record.occasion


# ============================================================
# RECONSTRUCT OUTFIT FOR FEEDBACK LEARNING
# ============================================================

def _reconstruct_outfit(db, user_id, outfit_id):

    item_ids = _extract_item_ids_from_outfit_id(
        outfit_id
    )

    if not item_ids:
        return None

    # outfit_id contains integer wardrobe item IDs
    try:
        integer_item_ids = [
            int(item_id)
            for item_id in item_ids
        ]
    except ValueError:
        return None

    # Fetch only the required items belonging to this user
    wardrobe_records = (
        db.query(WardrobeItem)
        .filter(
            WardrobeItem.user_id == user_id,
            WardrobeItem.id.in_(integer_item_ids)
        )
        .all()
    )

    wardrobe_by_id = {
        item.id: item
        for item in wardrobe_records
    }

    reconstructed_items = []

    # Preserve the order encoded in outfit_id
    for item_id in integer_item_ids:

        item = wardrobe_by_id.get(item_id)

        if item is None:
            continue

        reconstructed_items.append({
            "id": item.id,
            "category": item.category,
            "color": item.color,
            "fit": item.fit,

            # Aggregator expects singular KEY names,
            # but the values themselves are lists.
            "style": item.styles or [],
            "occasion": item.occasions or [],
        })

    if not reconstructed_items:
        return None

    occasion = _get_outfit_occasion(
        db=db,
        user_id=user_id,
        outfit_id=outfit_id
    )

    return {
        "outfit_id": str(outfit_id),
        "occasion": occasion,
        "items": reconstructed_items,
    }

# ============================================================
# SAVE A FEEDBACK EVENT
# ============================================================

def save_feedback_event(feedback_event: dict):
    """
    feedback_event is expected to look like the dict produced by
    agents.feedback_agent.feedback_events (a FeedbackEvent-shaped
    dict): user_id, outfit_id, feedback_type, reason, rating,
    comment, timestamp, status.
    """

    db = SessionLocal()

    try:
        record = FeedbackRecordDB(
            user_id=feedback_event["user_id"],
            outfit_id=str(feedback_event["outfit_id"]),
            feedback_type=feedback_event["feedback_type"],
            reason=feedback_event.get("reason"),
            rating=feedback_event.get("rating"),
            comment=feedback_event.get("comment")
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "user_id": record.user_id,
            "outfit_id": record.outfit_id,
            "feedback_type": record.feedback_type,
            "reason": record.reason,
            "rating": record.rating,
            "comment": record.comment,
            "created_at": (
                record.created_at.isoformat()
                if record.created_at else None
            )
        }

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


# ============================================================
# GET ALL FEEDBACK EVENTS FOR A USER
# ============================================================

def get_user_feedback_events(user_id):
    db = SessionLocal()

    try:
        records = (
            db.query(FeedbackRecordDB)
            .filter(FeedbackRecordDB.user_id == user_id)
            .order_by(FeedbackRecordDB.created_at.asc())
            .all()
        )

        feedback_events = []

        for record in records:
            outfit = _reconstruct_outfit(
                db=db,
                user_id=record.user_id,
                outfit_id=record.outfit_id
            )

            feedback_events.append({
                "user_id": record.user_id,
                "outfit_id": record.outfit_id,
                "feedback_type": record.feedback_type,
                "reason": record.reason,
                "rating": record.rating,
                "comment": record.comment,
                "timestamp": (
                    record.created_at.isoformat()
                    if record.created_at
                    else datetime.now(timezone.utc).isoformat()
                ),
                "status": "recorded",

                # Required by feedback_aggregator.py so it can
                # learn category/color/fit/style/occasion.
                "outfit": outfit,
            })

        return feedback_events

    finally:
        db.close()
