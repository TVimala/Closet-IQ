# ============================================================
# FEEDBACK AGENT
#
# STEP 13 + STEP 14
# ============================================================


from .feedback_aggregator import (
    aggregate_feedback_events,
    get_strongest_signals
)

from .learned_preferences import (
    interpret_learned_preferences
)


# ============================================================
# RUN FEEDBACK AGENT
# ============================================================


def run_feedback_agent(
    feedback_events,
    minimum_confidence="medium"
):

    print(
        "\n==================================="
    )

    print(
        "FEEDBACK AGENT STARTED"
    )

    print(
        "==================================="
    )


    print(
        f"\nFeedback Events Received: "
        f"{len(feedback_events)}"
    )


    # ========================================================
    # STEP 13
    # AGGREGATE RAW FEEDBACK
    # ========================================================

    aggregation_result = (

        aggregate_feedback_events(
            feedback_events
        )
    )


    # ========================================================
    # STEP 13
    # GET STRONGEST RAW SIGNALS
    # ========================================================

    strongest_signals = (

        get_strongest_signals(

            aggregation_result,

            minimum_confidence
        )
    )


    # ========================================================
    # STEP 14
    # INTERPRET LEARNED PREFERENCES
    # ========================================================

    learned_preferences = (

        interpret_learned_preferences(

            aggregation_result,

            minimum_confidence
        )
    )


    # ========================================================
    # DISPLAY LEARNED PREFERENCES
    # ========================================================

    print(
        "\n==================================="
    )

    print(
        "LEARNED PREFERENCES"
    )

    print(
        "==================================="
    )


    print(
        "\nPREFERRED:"
    )

    for attribute_group, values in (
        learned_preferences[
            "preferred"
        ].items()
    ):

        if not values:
            continue

        print(
            f"\n{attribute_group.upper()}:"
        )

        for value in values:

            print(
                f" + {value['value']} "
                f"(strength: {value['strength']}, "
                f"confidence: {value['confidence']})"
            )


    print(
        "\nAVOID:"
    )

    for attribute_group, values in (
        learned_preferences[
            "avoid"
        ].items()
    ):

        if not values:
            continue

        print(
            f"\n{attribute_group.upper()}:"
        )

        for value in values:

            print(
                f" - {value['value']} "
                f"(strength: {value['strength']}, "
                f"confidence: {value['confidence']})"
            )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "status":
            "success",

        "total_events_processed":
            aggregation_result[
                "total_events_processed"
            ],

        "signals":
            aggregation_result[
                "signals"
            ],

        "strongest_signals":
            strongest_signals,

        "learned_preferences":
            learned_preferences
    }