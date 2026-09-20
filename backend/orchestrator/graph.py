"""Graph orchestration definitions.

This is the central Orchestrator. It contains NO agent business
logic itself - it only:
  1. Gathers data from existing agents/services
  2. Adapts that data into the shapes existing agents expect
  3. Calls the existing agent functions
  4. Passes outputs between agents
  5. Returns a final result

Every agent function called below already exists in the project
(see the Step 0 audit). None of their internals are duplicated
here.
"""

from datetime import date as date_type
import logging

from database.connection import SessionLocal

from agents.profile_agent.agent import get_preference_context
from agents.wardrobe_agent.agent import get_wardrobe, mark_item_as_worn

from services.weather_service import get_weather_context, get_weekly_weather

from schemas.outfit_schema import (
    StylistInput,
    WardrobeItem as StylistWardrobeItem,
    UserPreferences,
    LongTermPreferences,
    ShortTermPreferences,
    WeeklyOutfitRequest,
    WeeklyDayPlan,
)

from agents.stylist_agent.agent import run_stylist_agent
from agents.stylist_agent.Planning.weekly_planner import generate_weekly_plan

from agents.feedback_agent.models import FeedbackRequest
from agents.feedback_agent.feedback_events import create_feedback_event
from agents.feedback_agent.agent import run_feedback_agent
from agents.feedback_agent.feedback_store import (
    save_feedback_event,
    get_user_feedback_events,
)
from agents.feedback_agent.outfit_history import (
    record_outfit_worn,
    log_outfit_generated,
    get_user_outfit_history,
    has_outfit_worn_today,
    has_outfit_generated_today,
)

from agents.finance_agent.agent import (
    get_budget,
    get_monthly_spending_analysis,
    analyze_purchase,
)

from agents.notifiction_agent.agent import run_notification_agent

from database.models import NotificationDB

from orchestrator.state import OrchestratorState
from orchestrator.router import RequestType


logger = logging.getLogger("orchestrator")


# ============================================================
# LOGGING HELPER (Step 18 requirement - clear, non-sensitive)
# ============================================================

def _log_start(request_type, user_id, **details):
    logger.info("===================================")
    logger.info("ORCHESTRATOR STARTED")
    logger.info("===================================")
    logger.info("Request Type: %s", request_type)
    logger.info("User ID: %s", user_id)
    for key, value in details.items():
        logger.info("%s: %s", key, value)


# ============================================================
# ADAPTERS
#
# The Wardrobe Agent's DB rows use plural field names
# (styles/occasions/seasons) while StylistInput.WardrobeItem
# uses singular names (style/occasion/season) and requires a
# few fields the raw DB dict doesn't always have populated.
# This adapter is the single place that bridges the two -
# nothing inside either agent is changed to do this.
# ============================================================

def _to_stylist_wardrobe_item(item: dict) -> dict:
    return {
        "id": str(item.get("id")),
        "user_id": str(item.get("user_id")),
        "image_url": item.get("image_url"),
        "category": item.get("category") or "unknown",
        "color": item.get("color"),
        "pattern": item.get("pattern"),
        "fit": item.get("fit"),
        "style": item.get("styles") or [],
        "season": item.get("seasons") or [],
        "occasion": item.get("occasions") or [],
        "condition": item.get("condition") or "good",
        "is_available": (
            item.get("is_available")
            if item.get("is_available") is not None
            else True
        ),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "usage_count": item.get("usage_count") or 0,
        "last_worn_at": item.get("last_worn_at"),
        "embedding": item.get("embedding"),
    }


def _build_stylist_wardrobe(raw_wardrobe: list) -> list:
    return [
        StylistWardrobeItem(**_to_stylist_wardrobe_item(item))
        for item in raw_wardrobe
    ]


def _build_user_preferences(preference_context: dict) -> UserPreferences:

    permanent = preference_context.get("permanent_preferences") or {}
    current = preference_context.get("current_preferences") or {}

    long_term = LongTermPreferences(
        styles=permanent.get("styles") or [],
        colors=permanent.get("colors") or [],
        fits=permanent.get("fits") or [],
        comfort_level=permanent.get("comfort_weight") or 3,
    )

    short_term = ShortTermPreferences(
        styles=current.get("styles") or [],
        colors=current.get("colors") or [],
        fits=current.get("fits") or [],
        comfort_level=current.get("comfort_weight"),
    )

    return UserPreferences(long_term=long_term, short_term=short_term)


def _get_learned_preferences(user_id: str):
    events = get_user_feedback_events(user_id)

    if not events:
        return None

    result = run_feedback_agent(events)

    return result.get("learned_preferences")


# ============================================================
# STEP 5/6 - SINGLE OUTFIT REQUEST
# ============================================================

def run_outfit_request(
    user_id: str,
    occasion: str,
    latitude: float,
    longitude: float,
):
    state = OrchestratorState(
        user_id=user_id,
        request_type=RequestType.OUTFIT_REQUEST,
        occasion=occasion,
        latitude=latitude,
        longitude=longitude,
    )

    _log_start(state.request_type, user_id, Occasion=occasion)

    try:
        db = SessionLocal()
        try:
            preference_context = get_preference_context(db, user_id)
        finally:
            db.close()

        raw_wardrobe = get_wardrobe(user_id)
        weather = get_weather_context(latitude, longitude)
        learned_preferences = _get_learned_preferences(user_id)

        logger.info("Profile Loaded: YES")
        logger.info("Wardrobe Loaded: %s", "YES" if raw_wardrobe else "EMPTY")
        logger.info("Weather Loaded: %s", "YES" if weather else "NO")

        if not raw_wardrobe:
            state.status = "error"
            state.error = "Wardrobe unavailable or empty for this user."
            return {"status": "error", "error": state.error}

        stylist_input = StylistInput(
            occasion=occasion,
            wardrobe=_build_stylist_wardrobe(raw_wardrobe),
            preferences=_build_user_preferences(preference_context),
        )

        logger.info("Routing -> STYLIST_AGENT")

        result = run_stylist_agent(
            stylist_input,
            weather,
            learned_preferences=learned_preferences,
        )

        # Log that an outfit was generated today (for the
        # Notification Agent's wear-reminder check). The Stylist
        # Agent's outfit dicts have no stable "outfit_id" field
        # (outfits are identified by their item-id set, the same
        # way is_same_outfit() already does it) - so derive one
        # the same way rather than inventing a new identity scheme.
        top_outfits = result.get("outfits")
        if top_outfits:
            best_outfit = top_outfits[0]
            item_ids = sorted(
                str(i.get("id"))
                for i in best_outfit.get("items", [])
                if i.get("id") is not None
            )
            derived_outfit_id = "-".join(item_ids) if item_ids else "generated"

            log_outfit_generated(
                user_id=user_id,
                outfit_id=derived_outfit_id,
                items=best_outfit.get("items", []),
                occasion=occasion,
            )

            result["outfit_id"] = derived_outfit_id

        logger.info("Stylist Agent Completed")
        logger.info("Final Result: SUCCESS")

        return {"status": "success", **result}

    except Exception as e:
        logger.exception("Orchestrator failed for OUTFIT_REQUEST")
        return {"status": "error", "error": str(e)}


# ============================================================
# STEP 7 - REGENERATION REQUEST
# ============================================================

def run_regeneration_request(
    user_id: str,
    occasion: str,
    latitude: float,
    longitude: float,
    previous_outfit: dict,
    previous_outfits: list = None,
    regeneration_reason: str = None,
):
    _log_start(
        RequestType.REGENERATION_REQUEST, user_id,
        Occasion=occasion, Reason=regeneration_reason
    )

    try:
        db = SessionLocal()
        try:
            preference_context = get_preference_context(db, user_id)
        finally:
            db.close()

        raw_wardrobe = get_wardrobe(user_id)
        weather = get_weather_context(latitude, longitude)
        learned_preferences = _get_learned_preferences(user_id)

        if not raw_wardrobe:
            return {
                "status": "error",
                "error": "Wardrobe unavailable or empty for this user.",
            }

        stylist_input = StylistInput(
            occasion=occasion,
            wardrobe=_build_stylist_wardrobe(raw_wardrobe),
            preferences=_build_user_preferences(preference_context),
            previous_outfit=previous_outfit,
            previous_outfits=previous_outfits or [],
            regeneration_reason=regeneration_reason,
        )

        result = run_stylist_agent(
            stylist_input,
            weather,
            learned_preferences=learned_preferences,
        )

        logger.info("Final Result: %s", result.get("status", "SUCCESS"))

        return {"status": "success", **result}

    except Exception as e:
        logger.exception("Orchestrator failed for REGENERATION_REQUEST")
        return {"status": "error", "error": str(e)}


# ============================================================
# STEP 8 - WEEKLY OUTFIT REQUEST
# ============================================================

def run_weekly_outfit_request(
    user_id: str,
    start_date,
    days: list,
    latitude: float,
    longitude: float,
):
    _log_start(
        RequestType.WEEKLY_OUTFIT_REQUEST, user_id,
        Days=len(days)
    )

    try:
        db = SessionLocal()
        try:
            preference_context = get_preference_context(db, user_id)
        finally:
            db.close()

        raw_wardrobe = get_wardrobe(user_id)

        if not raw_wardrobe:
            return {
                "status": "error",
                "error": "Wardrobe unavailable or empty for this user.",
            }

        wardrobe = _build_stylist_wardrobe(raw_wardrobe)
        preferences = _build_user_preferences(preference_context)

        request = WeeklyOutfitRequest(
            user_id=user_id,
            start_date=start_date,
            days=[WeeklyDayPlan(**day) for day in days],
            latitude=latitude,
            longitude=longitude,
        )

        result = generate_weekly_plan(
            request=request,
            wardrobe=wardrobe,
            preferences=preferences,
        )

        logger.info("Final Result: SUCCESS")

        return {"status": "success", **result} if isinstance(result, dict) else result

    except Exception as e:
        logger.exception("Orchestrator failed for WEEKLY_OUTFIT_REQUEST")
        return {"status": "error", "error": str(e)}


# ============================================================
# STEP 9 - FEEDBACK REQUEST
# ============================================================

def run_feedback_request(
    user_id: str,
    outfit_id: str,
    feedback_type: str,
    reason: str = None,
    rating: int = None,
    comment: str = None,
    items: list = None,
    occasion: str = None,
):
    _log_start(
        RequestType.FEEDBACK_REQUEST, user_id,
        Outfit=outfit_id, Type=feedback_type
    )

    try:
        feedback_request = FeedbackRequest(
            user_id=user_id,
            outfit_id=outfit_id,
            feedback_type=feedback_type,
            reason=reason,
            rating=rating,
            comment=comment,
        )

        # Validate + normalize via the existing Feedback Agent logic.
        event = create_feedback_event(feedback_request)

        saved = save_feedback_event(event.model_dump())

        wardrobe_updates = []

        # --------------------------------------------------
        # "I Wore This" -> update outfit history + wardrobe
        # usage stats, through the EXISTING agent functions
        # only. Generated outfit != worn outfit, so this only
        # happens for feedback_type == "wore_it".
        # --------------------------------------------------

        if feedback_type == "wore_it" and items:

            history_result = record_outfit_worn(
                user_id=user_id,
                outfit_id=outfit_id,
                items=items,
                occasion=occasion,
                source="confirmed_worn",
            )

            for item in items:
                item_id = item.get("id") if isinstance(item, dict) else item
                if item_id is None:
                    continue
                try:
                    updated = mark_item_as_worn(int(item_id), user_id)
                    if updated:
                        wardrobe_updates.append(updated)
                except (TypeError, ValueError):
                    logger.warning(
                        "Skipping non-integer wardrobe item id: %s", item_id
                    )
        else:
            history_result = None

        # --------------------------------------------------
        # Recompute learned preferences from ALL of this
        # user's stored feedback events (not just this one).
        # --------------------------------------------------

        all_events = get_user_feedback_events(user_id)
        learning_result = run_feedback_agent(all_events)

        logger.info("Final Result: SUCCESS")

        return {
            "status": "success",
            "feedback_event": saved,
            "outfit_history_update": history_result,
            "wardrobe_updates": wardrobe_updates,
            "learned_preferences": learning_result.get("learned_preferences"),
        }

    except ValueError as e:
        return {"status": "error", "error": str(e)}

    except Exception as e:
        logger.exception("Orchestrator failed for FEEDBACK_REQUEST")
        return {"status": "error", "error": str(e)}


# ============================================================
# STEP 10 - PURCHASE FLOW
#
# NOTE: BUY / CONSIDER / DON'T BUY decision + the actual
# confirm/cancel database writes (create wardrobe item +
# purchase history, or mark CANCELLED) already exist as a
# complete, working flow in api/finance.py (confirm_purchase /
# cancel_purchase), built directly on the Finance Agent and
# Wardrobe model. Per the "do not duplicate this in graph.py"
# instruction in the spec, the Orchestrator does not re-implement
# that - it only coordinates the analysis step, which is the
# part that legitimately needs Wardrobe + Finance data merged.
# ============================================================

def run_purchase_analysis_request(
    user_id: str,
    category: str,
    color: str,
    styles: list,
    purchase_price: float,
    month: int,
    year: int,
):
    _log_start(
        RequestType.PURCHASE_ANALYSIS_REQUEST, user_id,
        Category=category, Price=purchase_price
    )

    try:
        result = analyze_purchase(
            user_id=user_id,
            category=category,
            color=color,
            styles=styles,
            purchase_price=purchase_price,
            month=month,
            year=year,
        )

        logger.info("Final Result: SUCCESS")

        return {"status": "success", **result} if isinstance(result, dict) else result

    except Exception as e:
        logger.exception("Orchestrator failed for PURCHASE_ANALYSIS_REQUEST")
        return {"status": "error", "error": str(e)}


# ============================================================
# STEP 11/12/15 - NOTIFICATION FLOW
#
# The Orchestrator/scheduler calls this once per user. It only
# GATHERS data (budget/spend/outfit-today) from the existing
# Finance and Feedback/Outfit-History agents, then calls the
# existing Notification Agent to DECIDE what is needed, then
# persists any resulting notification (with dedup, Step 15).
# ============================================================

def _notification_already_sent_today(db, user_id, notification_type, today):
    return db.query(NotificationDB).filter(
        NotificationDB.user_id == user_id,
        NotificationDB.notification_type == notification_type,
        NotificationDB.scheduled_for == today,
    ).first() is not None


def _notification_already_sent_this_month(db, user_id, notification_type, year, month):
    existing = db.query(NotificationDB).filter(
        NotificationDB.user_id == user_id,
        NotificationDB.notification_type == notification_type,
    ).all()

    for record in existing:
        if (
            record.scheduled_for
            and record.scheduled_for.year == year
            and record.scheduled_for.month == month
        ):
            return True

    return False


def run_notification_check(user_id: str, current_date: date_type = None):

    if current_date is None:
        current_date = date_type.today()

    _log_start(RequestType.NOTIFICATION_REQUEST, user_id, Date=current_date)

    try:
        # ------------------------------------------------
        # GATHER FINANCE DATA (existing Finance Agent)
        # ------------------------------------------------

        monthly_budget = None
        current_shopping_spend = 0

        budget = get_budget(
            user_id=user_id,
            category="CLOTHING",
            month=current_date.month,
            year=current_date.year,
        )

        if budget:
            analysis = get_monthly_spending_analysis(
                user_id=user_id,
                category="CLOTHING",
                month=current_date.month,
                year=current_date.year,
            )

            if "error" not in analysis:
                monthly_budget = analysis["monthly_budget"]
                current_shopping_spend = analysis["total_spent"]

        # ------------------------------------------------
        # GATHER OUTFIT HISTORY DATA (existing Feedback Agent)
        # ------------------------------------------------

        outfit_generated_today = has_outfit_generated_today(user_id, current_date)
        outfit_worn_today = has_outfit_worn_today(user_id, current_date)

        # ------------------------------------------------
        # DECIDE (existing Notification Agent - unchanged)
        # ------------------------------------------------

        decision = run_notification_agent(
            current_date=current_date,
            monthly_budget=monthly_budget,
            current_shopping_spend=current_shopping_spend,
            outfit_generated_today=outfit_generated_today,
            outfit_worn_today=outfit_worn_today,
        )

        # ------------------------------------------------
        # PERSIST (Step 15 - dedup so scheduler re-runs don't
        # create duplicate notifications)
        # ------------------------------------------------

        created = []

        db = SessionLocal()

        try:
            for notification in decision.get("notifications", []):

                notification_type = notification["notification_type"]

                if notification_type == "MONTHLY_BUDGET_REMINDER":
                    if _notification_already_sent_this_month(
                        db, user_id, notification_type,
                        current_date.year, current_date.month
                    ):
                        continue

                elif notification_type == "WEAR_REMINDER":
                    if _notification_already_sent_today(
                        db, user_id, notification_type, current_date
                    ):
                        continue

                elif notification_type in ("BUDGET_WARNING", "BUDGET_EXCEEDED"):
                    if _notification_already_sent_today(
                        db, user_id, notification_type, current_date
                    ):
                        continue

                record = NotificationDB(
                    user_id=user_id,
                    notification_type=notification_type,
                    title=notification["title"],
                    message=notification["message"],
                    scheduled_for=current_date,
                    read=False,
                    delivery_status="delivered",
                )

                db.add(record)
                db.commit()
                db.refresh(record)

                created.append({
                    "id": record.id,
                    "notification_type": record.notification_type,
                    "title": record.title,
                    "message": record.message,
                    "scheduled_for": str(record.scheduled_for),
                })

        finally:
            db.close()

        logger.info(
            "Final Result: SUCCESS (%d notification(s) created)", len(created)
        )

        return {"status": "success", "notifications_created": created}

    except Exception as e:
        logger.exception("Orchestrator failed for NOTIFICATION_REQUEST")
        return {"status": "error", "error": str(e)}


# ============================================================
# BACKWARD-COMPATIBLE PLACEHOLDER CLASS
#
# Kept only so any pre-existing import of WorkflowGraph does
# not break. It is not used by the flows above.
# ============================================================

class WorkflowGraph:
    def __init__(self) -> None:
        self.nodes: list = []

    def add_node(self, name: str) -> None:
        self.nodes.append(name)
