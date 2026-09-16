# ============================================================
# LEARNED PREFERENCE INTERPRETER
# STEP 14
#
# Converts aggregated feedback signals into
# safe, usable learned preferences.
# ============================================================


# ============================================================
# CONFIDENCE LEVELS
# ============================================================


CONFIDENCE_LEVELS = {

    "low": 1,

    "medium": 2,

    "high": 3
}


# ============================================================
# MINIMUM REQUIREMENTS
# ============================================================
#
# We do not learn from one weak signal.
#
# Low confidence:
#   ignored by default
#
# Medium:
#   used with small influence
#
# High:
#   used with stronger influence
# ============================================================


MINIMUM_CONFIDENCE = "medium"


# ============================================================
# SIGNAL STRENGTH
# ============================================================


def get_signal_strength(
    net_score,
    confidence
):

    absolute_score = abs(
        net_score
    )

    confidence_level = CONFIDENCE_LEVELS.get(
        confidence,
        1
    )

    # --------------------------------------------------------
    # HIGH CONFIDENCE
    # --------------------------------------------------------

    if confidence_level >= 3:

        if absolute_score >= 6:
            return "strong"

        return "medium"

    # --------------------------------------------------------
    # MEDIUM CONFIDENCE
    # --------------------------------------------------------

    if confidence_level >= 2:

        if absolute_score >= 4:
            return "medium"

        return "weak"

    return "weak"


# ============================================================
# SHOULD USE SIGNAL
# ============================================================


def should_use_signal(
    signal,
    minimum_confidence=MINIMUM_CONFIDENCE
):

    confidence = signal.get(
        "confidence",
        "low"
    )

    required_level = CONFIDENCE_LEVELS.get(
        minimum_confidence,
        2
    )

    current_level = CONFIDENCE_LEVELS.get(
        confidence,
        1
    )

    net_score = signal.get(
        "net_score",
        0
    )

    # Must have enough confidence
    if current_level < required_level:
        return False

    # Neutral signal is useless
    if net_score == 0:
        return False

    return True


# ============================================================
# CREATE EMPTY LEARNED PREFERENCES
# ============================================================


def create_empty_learned_preferences():

    return {

        "preferred": {

            "styles": [],

            "colors": [],

            "fits": [],

            "categories": [],

            "occasions": []
        },

        "avoid": {

            "styles": [],

            "colors": [],

            "fits": [],

            "categories": [],

            "occasions": []
        },

        "metadata": {

            "total_learned_preferences": 0,

            "source": "feedback_agent"
        }
    }


# ============================================================
# INTERPRET AGGREGATED SIGNALS
# ============================================================


def interpret_learned_preferences(
    aggregation_result,
    minimum_confidence=MINIMUM_CONFIDENCE
):

    learned_preferences = (
        create_empty_learned_preferences()
    )

    signals = aggregation_result.get(
        "signals",
        {}
    )

    # --------------------------------------------------------
    # PROCESS EACH ATTRIBUTE GROUP
    # --------------------------------------------------------

    for attribute_group, attributes in signals.items():

        # Ignore unknown groups safely

        if (
            attribute_group
            not in learned_preferences["preferred"]
        ):
            continue


        # ----------------------------------------------------
        # PROCESS EACH ATTRIBUTE
        # ----------------------------------------------------

        for attribute_value, signal in attributes.items():

            # Skip weak / neutral signals

            if not should_use_signal(

                signal,

                minimum_confidence
            ):

                continue


            net_score = signal.get(
                "net_score",
                0
            )

            confidence = signal.get(
                "confidence",
                "low"
            )

            strength = get_signal_strength(

                net_score,

                confidence
            )


            learned_item = {

                "value":
                    attribute_value,

                "net_score":
                    net_score,

                "confidence":
                    confidence,

                "strength":
                    strength
            }


            # ------------------------------------------------
            # POSITIVE LEARNING
            # ------------------------------------------------

            if net_score > 0:

                learned_preferences[
                    "preferred"
                ][
                    attribute_group
                ].append(
                    learned_item
                )


            # ------------------------------------------------
            # NEGATIVE LEARNING
            # ------------------------------------------------

            elif net_score < 0:

                learned_preferences[
                    "avoid"
                ][
                    attribute_group
                ].append(
                    learned_item
                )


    # --------------------------------------------------------
    # SORT BY STRONGEST SIGNAL
    # --------------------------------------------------------

    for preference_type in [

        "preferred",

        "avoid"
    ]:

        for attribute_group in learned_preferences[
            preference_type
        ]:

            learned_preferences[
                preference_type
            ][
                attribute_group
            ].sort(

                key=lambda item:
                abs(
                    item["net_score"]
                ),

                reverse=True
            )


    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    total = 0

    for preference_type in [

        "preferred",

        "avoid"
    ]:

        for values in learned_preferences[
            preference_type
        ].values():

            total += len(
                values
            )


    learned_preferences[
        "metadata"
    ][
        "total_learned_preferences"
    ] = total


    return learned_preferences


# ============================================================
# GET LEARNED VALUES
# ============================================================
#
# Returns simple values for the Stylist Agent.
#
# Example:
#
# [
#     "minimal",
#     "comfortable"
# ]
# ============================================================


def get_learned_values(
    learned_preferences,
    preference_type,
    attribute_group
):

    values = learned_preferences.get(
        preference_type,
        {}
    ).get(
        attribute_group,
        []
    )

    return [

        item.get(
            "value"
        )

        for item in values

        if item.get(
            "value"
        )
    ]