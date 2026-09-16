# ============================================================
# NOTIFICATION AGENT
# ============================================================

from datetime import date


# ============================================================
# NOTIFICATION TYPES
# ============================================================

NO_NOTIFICATION = "NO_NOTIFICATION"

MONTHLY_BUDGET_REMINDER = "MONTHLY_BUDGET_REMINDER"

BUDGET_WARNING = "BUDGET_WARNING"

BUDGET_EXCEEDED = "BUDGET_EXCEEDED"

WEAR_REMINDER = "WEAR_REMINDER"


# ============================================================
# BUDGET THRESHOLD
# ============================================================

BUDGET_WARNING_THRESHOLD = 90


# ============================================================
# COMMON NOTIFICATION BUILDER
# ============================================================

def create_notification(
    notification_type,
    title,
    message
):
    return {
        "notification_required": True,
        "notification_type": notification_type,
        "title": title,
        "message": message
    }


def create_no_notification():
    return {
        "notification_required": False,
        "notification_type": NO_NOTIFICATION,
        "title": None,
        "message": None
    }


# ============================================================
# 1. FIRST DAY OF MONTH
# ============================================================

def check_monthly_budget_reminder(current_date=None):
    """
    Check whether today is the first day of the month.

    If yes, remind the user to provide/set their
    monthly shopping budget.
    """

    if current_date is None:
        current_date = date.today()

    if current_date.day != 1:
        return create_no_notification()

    return create_notification(
        MONTHLY_BUDGET_REMINDER,
        "Monthly Shopping Budget",
        "🛍️ What's your monthly budget for shopping this month?"
    )


# ============================================================
# 2. SHOPPING BUDGET STATUS
# ============================================================

def check_budget_status(
    monthly_budget,
    current_shopping_spend
):
    """
    Check the user's current shopping spending
    against their monthly shopping budget.
    """

    if monthly_budget is None:
        return create_no_notification()

    if monthly_budget <= 0:
        return create_no_notification()

    if current_shopping_spend is None:
        current_shopping_spend = 0

    budget_percentage = (
        current_shopping_spend / monthly_budget
    ) * 100

    # --------------------------------------------------------
    # BUDGET EXCEEDED
    # --------------------------------------------------------

    if current_shopping_spend > monthly_budget:

        exceeded_amount = (
            current_shopping_spend - monthly_budget
        )

        return create_notification(
            BUDGET_EXCEEDED,
            "Shopping Budget Exceeded",
            (
                f"⚠️ You've exceeded your monthly shopping budget "
                f"by ₹{exceeded_amount:.2f}."
            )
        )

    # --------------------------------------------------------
    # BUDGET WARNING
    # --------------------------------------------------------

    if budget_percentage >= BUDGET_WARNING_THRESHOLD:

        remaining_amount = (
            monthly_budget - current_shopping_spend
        )

        return create_notification(
            BUDGET_WARNING,
            "Shopping Budget Alert",
            (
                f"🛍️ You've used {budget_percentage:.0f}% of your "
                f"monthly shopping budget. "
                f"₹{remaining_amount:.2f} remaining."
            )
        )

    # --------------------------------------------------------
    # NORMAL
    # --------------------------------------------------------

    return create_no_notification()


# ============================================================
# 3. DAILY "WHAT DID YOU WEAR?" REMINDER
# ============================================================

def check_wear_reminder(
    outfit_generated_today,
    outfit_worn_today
):
    """
    Check whether the user needs a daily outfit reminder.

    Important:
    A generated outfit does NOT mean the user wore it.

    The reminder is sent only when:
    - an outfit was generated today
    - no outfit has been marked as worn today
    """

    if not outfit_generated_today:
        return create_no_notification()

    if outfit_worn_today:
        return create_no_notification()

    return create_notification(
        WEAR_REMINDER,
        "What Did You Wear Today?",
        (
            "👗 What did you wear today? "
            "Tell Closet-IQ what you wore so we can improve "
            "your future outfit recommendations."
        )
    )


# ============================================================
# MAIN NOTIFICATION AGENT
# ============================================================

def run_notification_agent(
    current_date=None,
    monthly_budget=None,
    current_shopping_spend=0,
    outfit_generated_today=False,
    outfit_worn_today=False
):
    """
    Main entry point for the Notification Agent.

    Checks all supported notification conditions.

    Returns a list because more than one notification
    can theoretically be required on the same day.
    """

    if current_date is None:
        current_date = date.today()

    notifications = []

    # ========================================================
    # CHECK 1: FIRST DAY OF MONTH
    # ========================================================

    monthly_budget_notification = check_monthly_budget_reminder(
        current_date
    )

    if monthly_budget_notification["notification_required"]:
        notifications.append(monthly_budget_notification)

    # ========================================================
    # CHECK 2: BUDGET STATUS
    # ========================================================

    budget_notification = check_budget_status(
        monthly_budget,
        current_shopping_spend
    )

    if budget_notification["notification_required"]:
        notifications.append(budget_notification)

    # ========================================================
    # CHECK 3: DAILY OUTFIT REMINDER
    # ========================================================

    wear_notification = check_wear_reminder(
        outfit_generated_today,
        outfit_worn_today
    )

    if wear_notification["notification_required"]:
        notifications.append(wear_notification)

    # ========================================================
    # NO NOTIFICATIONS
    # ========================================================

    if not notifications:
        return {
            "status": "success",
            "notification_count": 0,
            "notifications": []
        }

    # ========================================================
    # RETURN NOTIFICATIONS
    # ========================================================

    return {
        "status": "success",
        "notification_count": len(notifications),
        "notifications": notifications
    }