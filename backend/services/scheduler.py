"""Local, free scheduler (APScheduler) for the Notification Agent.

The scheduler contains NO notification business logic itself.
It only triggers orchestrator.graph.run_notification_check for
every known user on a schedule. All decision-making happens in
the existing Notification Agent; all dedup happens in the
Orchestrator (backed by the notifications table).
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from database.connection import SessionLocal
from database.models import User

from orchestrator.graph import run_notification_check


logger = logging.getLogger("scheduler")

_scheduler = BackgroundScheduler()


def _get_all_user_ids():
    db = SessionLocal()
    try:
        return [user.id for user in db.query(User).all()]
    finally:
        db.close()


def run_notification_checks_for_all_users():
    """
    Runs once per scheduled tick. Iterates every user and lets
    the Orchestrator (+ existing Notification Agent + dedup
    logic) decide what, if anything, needs to be created.
    """

    user_ids = _get_all_user_ids()

    logger.info("Scheduler: running notification checks for %d user(s)", len(user_ids))

    for user_id in user_ids:
        try:
            run_notification_check(user_id)
        except Exception:
            logger.exception(
                "Scheduler: notification check failed for user_id=%s", user_id
            )


def start_scheduler():
    """
    Called once from main.py's startup/lifespan handler.

    - Daily check near end of day: covers the WEAR_REMINDER case.
    - Daily check is also sufficient for MONTHLY_BUDGET_REMINDER
      (the Notification Agent itself checks current_date.day == 1)
      and for BUDGET_WARNING / BUDGET_EXCEEDED.
    """

    if _scheduler.running:
        return _scheduler

    _scheduler.add_job(
        run_notification_checks_for_all_users,
        trigger="cron",
        hour=21,
        minute=0,
        id="daily_notification_check",
        replace_existing=True,
    )

    _scheduler.start()

    logger.info("Scheduler started: daily notification check at 21:00")

    return _scheduler


def stop_scheduler():
    if _scheduler.running:
        _scheduler.shutdown(wait=False)
