"""Notification API.

New file (no notification API previously existed). Exposes the
in-app notifications created by the Orchestrator's notification
flow (orchestrator.graph.run_notification_check), which is
normally triggered by the scheduler (services/scheduler.py) but
can also be triggered manually here for testing.
"""

from fastapi import APIRouter, HTTPException

from database.connection import SessionLocal
from database.models import NotificationDB

from orchestrator.graph import run_notification_check


router = APIRouter(prefix="/api/notifications", tags=["Notification Agent"])


# ============================================================
# GET ALL NOTIFICATIONS FOR A USER
# ============================================================

@router.get("/{user_id}")
def get_notifications(user_id: str):

    db = SessionLocal()

    try:
        records = (
            db.query(NotificationDB)
            .filter(NotificationDB.user_id == user_id)
            .order_by(NotificationDB.created_at.desc())
            .all()
        )

        return {
            "success": True,
            "user_id": user_id,
            "count": len(records),
            "notifications": [
                {
                    "id": r.id,
                    "notification_type": r.notification_type,
                    "title": r.title,
                    "message": r.message,
                    "created_at": (
                        r.created_at.isoformat() if r.created_at else None
                    ),
                    "scheduled_for": (
                        r.scheduled_for.isoformat() if r.scheduled_for else None
                    ),
                    "read": r.read,
                    "delivery_status": r.delivery_status,
                }
                for r in records
            ],
        }

    finally:
        db.close()


# ============================================================
# GET UNREAD NOTIFICATIONS
# ============================================================

@router.get("/{user_id}/unread")
def get_unread_notifications(user_id: str):

    db = SessionLocal()

    try:
        records = (
            db.query(NotificationDB)
            .filter(
                NotificationDB.user_id == user_id,
                NotificationDB.read == False,  # noqa: E712
            )
            .order_by(NotificationDB.created_at.desc())
            .all()
        )

        return {
            "success": True,
            "user_id": user_id,
            "count": len(records),
            "notifications": [
                {
                    "id": r.id,
                    "notification_type": r.notification_type,
                    "title": r.title,
                    "message": r.message,
                    "created_at": (
                        r.created_at.isoformat() if r.created_at else None
                    ),
                }
                for r in records
            ],
        }

    finally:
        db.close()


# ============================================================
# MARK NOTIFICATION AS READ
# ============================================================

@router.patch("/{notification_id}/read")
def mark_notification_read(notification_id: int):

    db = SessionLocal()

    try:
        record = (
            db.query(NotificationDB)
            .filter(NotificationDB.id == notification_id)
            .first()
        )

        if not record:
            raise HTTPException(status_code=404, detail="Notification not found.")

        record.read = True
        db.commit()
        db.refresh(record)

        return {
            "success": True,
            "message": "Notification marked as read.",
            "notification_id": record.id,
        }

    finally:
        db.close()


# ============================================================
# MANUAL TRIGGER (for testing without waiting for the scheduler)
# ============================================================

@router.post("/{user_id}/check")
def trigger_notification_check(user_id: str):

    result = run_notification_check(user_id)

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("error"))

    return result
