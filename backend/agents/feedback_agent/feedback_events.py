# ============================================================
# FEEDBACK EVENT PROCESSING
# ============================================================

from datetime import datetime

from .models import (
    FEEDBACK_TYPES,
    REGENERATION_REASONS,
    FeedbackEvent,
    FeedbackRequest
)


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(
    value
):

    if not value:
        return None

    return (
        value
        .lower()
        .strip()
    )


# ============================================================
# VALIDATE FEEDBACK TYPE
# ============================================================

def validate_feedback_type(
    feedback_type
):

    feedback_type = normalize_text(
        feedback_type
    )

    if feedback_type not in FEEDBACK_TYPES:

        raise ValueError(
            f"Unsupported feedback type: "
            f"{feedback_type}"
        )

    return feedback_type


# ============================================================
# VALIDATE REGENERATION REASON
# ============================================================

def validate_regeneration_reason(
    reason
):

    if reason is None:

        return None

    reason = normalize_text(
        reason
    )

    if reason not in REGENERATION_REASONS:

        raise ValueError(
            f"Unsupported regeneration reason: "
            f"{reason}"
        )

    return reason


# ============================================================
# VALIDATE RATING
# ============================================================

def validate_rating(
    rating
):

    if rating is None:

        return None

    if not isinstance(
        rating,
        int
    ):

        raise ValueError(
            "Rating must be an integer "
            "between 1 and 5."
        )

    if rating < 1 or rating > 5:

        raise ValueError(
            "Rating must be between 1 and 5."
        )

    return rating


# ============================================================
# VALIDATE FEEDBACK REQUEST
# ============================================================

def validate_feedback_request(
    feedback
):

    feedback_type = validate_feedback_type(
        feedback.feedback_type
    )

    reason = feedback.reason

    rating = feedback.rating


    # --------------------------------------------------------
    # REGENERATE
    # --------------------------------------------------------

    if feedback_type == "regenerate":

        reason = validate_regeneration_reason(
            reason
        )


    # --------------------------------------------------------
    # RATING
    # --------------------------------------------------------

    if feedback_type == "rating":

        if rating is None:

            raise ValueError(
                "Rating is required when "
                "feedback_type is 'rating'."
            )

        rating = validate_rating(
            rating
        )


    # --------------------------------------------------------
    # OTHER FEEDBACK TYPES
    # --------------------------------------------------------

    else:

        if rating is not None:

            rating = validate_rating(
                rating
            )


    return {

        "feedback_type": feedback_type,

        "reason": reason,

        "rating": rating
    }


# ============================================================
# CREATE FEEDBACK EVENT
# ============================================================

def create_feedback_event(
    feedback
):

    validated = validate_feedback_request(
        feedback
    )

    event = FeedbackEvent(

        user_id=feedback.user_id,

        outfit_id=feedback.outfit_id,

        feedback_type=validated[
            "feedback_type"
        ],

        reason=validated[
            "reason"
        ],

        rating=validated[
            "rating"
        ],

        comment=feedback.comment,

        timestamp=(
            datetime.now().isoformat()
        )
    )

    return event