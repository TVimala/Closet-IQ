"""Notification service placeholder."""


class NotificationService:
    """Handles notifications for user updates."""

    def send(self, user_id: str, message: str) -> dict:
        return {"user_id": user_id, "message": message, "status": "queued"}
