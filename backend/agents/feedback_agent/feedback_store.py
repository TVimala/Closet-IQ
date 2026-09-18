# ============================================================
# FEEDBACK STORE
#
# New, additive module. The Feedback Agent's aggregator
# (feedback_aggregator.py) and models.py already define
# FeedbackEvent / FEEDBACK_TYPES / REGENERATION_REASONS.
#
# This module is only responsible for persistence: saving a
# validated FeedbackEvent to Postgres, and reloading a user's
# events so run_feedback_agent(feedback_events) can be called
# with real, durable data instead of an in-memory list.
#
# It does not replace or rename any existing function.
# ============================================================

from datetime import datetime, timezone

from database.connection import SessionLocal
from database.models import FeedbackRecordDB


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
#
# Returns a list shaped like agents.feedback_agent.models
# .FeedbackEvent, ready to be passed straight into
# run_feedback_agent(feedback_events).
# ============================================================

def get_user_feedback_events(user_id):

    db = SessionLocal()

    try:
        records = db.query(FeedbackRecordDB).filter(
            FeedbackRecordDB.user_id == user_id
        ).order_by(FeedbackRecordDB.created_at.asc()).all()

        return [
            {
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
                "status": "recorded"
            }
            for record in records
        ]

    finally:
        db.close()
