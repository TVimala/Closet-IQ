# ============================================================
# FEEDBACK AGGREGATOR
# STEP 13
#
# Converts raw feedback events into aggregated
# positive and negative preference signals.
# ============================================================


from collections import defaultdict


# ============================================================
# SIGNAL WEIGHTS
# ============================================================
#
# Different user actions have different strengths.
#
# Example:
#
# WORE + 5 STAR
# is stronger positive feedback than LIKE.
#
# REGENERATE
# is weaker negative feedback than an explicit DISLIKE.
# ============================================================


EVENT_SIGNAL_WEIGHTS = {

    # --------------------------------------------------------
    # POSITIVE EVENTS
    # --------------------------------------------------------

    "like": {
        "positive": 1,
        "negative": 0
    },

    "wore": {
        "positive": 2,
        "negative": 0
    },

    # --------------------------------------------------------
    # NEGATIVE EVENTS
    # --------------------------------------------------------

    "regenerate": {
        "positive": 0,
        "negative": 1
    },

    "dislike": {
        "positive": 0,
        "negative": 2
    }
}


# ============================================================
# RATING SIGNAL WEIGHTS
# ============================================================
#
# 5 stars = strong positive
# 4 stars = positive
# 3 stars = neutral
# 2 stars = negative
# 1 star  = strong negative
# ============================================================


RATING_SIGNAL_WEIGHTS = {

    5: {
        "positive": 3,
        "negative": 0
    },

    4: {
        "positive": 2,
        "negative": 0
    },

    3: {
        "positive": 0,
        "negative": 0
    },

    2: {
        "positive": 0,
        "negative": 2
    },

    1: {
        "positive": 0,
        "negative": 3
    }
}


# ============================================================
# NORMALIZE TEXT
# ============================================================


def normalize_text(value):

    if value is None:
        return None

    return str(
        value
    ).lower().strip()


# ============================================================
# CREATE EMPTY SIGNAL
# ============================================================


def create_empty_signal():

    return {

        "positive": 0,

        "negative": 0,

        "net_score": 0,

        "confidence": "low",

        "total_signals": 0
    }


# ============================================================
# UPDATE SIGNAL
# ============================================================


def update_signal(
    signal,
    positive_points=0,
    negative_points=0
):

    signal["positive"] += positive_points

    signal["negative"] += negative_points

    signal["net_score"] = (

        signal["positive"]

        -

        signal["negative"]
    )

    signal["total_signals"] = (

        signal["positive"]

        +

        signal["negative"]
    )


# ============================================================
# CALCULATE CONFIDENCE
# ============================================================
#
# Confidence is based on how much repeated
# feedback exists.
#
# 0-2 points  -> low
# 3-5 points  -> medium
# 6+ points   -> high
# ============================================================


def calculate_confidence(
    total_signals
):

    if total_signals >= 6:

        return "high"

    elif total_signals >= 3:

        return "medium"

    return "low"


# ============================================================
# FINALIZE SIGNAL
# ============================================================


def finalize_signal(
    signal
):

    signal["net_score"] = (

        signal["positive"]

        -

        signal["negative"]
    )

    signal["total_signals"] = (

        signal["positive"]

        +

        signal["negative"]
    )

    signal["confidence"] = (

        calculate_confidence(
            signal["total_signals"]
        )
    )

    return signal


# ============================================================
# GET EVENT SIGNAL
# ============================================================


def get_event_signal(
    event
):

    event_type = normalize_text(
        event.get("event_type")
    )

    # --------------------------------------------------------
    # NORMAL EVENT
    # --------------------------------------------------------

    if event_type in EVENT_SIGNAL_WEIGHTS:

        return EVENT_SIGNAL_WEIGHTS[
            event_type
        ]

    # --------------------------------------------------------
    # RATING EVENT
    # --------------------------------------------------------

    if event_type == "rating":

        rating = event.get(
            "rating"
        )

        try:

            rating = int(rating)

        except (
            TypeError,
            ValueError
        ):

            return {
                "positive": 0,
                "negative": 0
            }

        return RATING_SIGNAL_WEIGHTS.get(

            rating,

            {
                "positive": 0,
                "negative": 0
            }
        )

    # --------------------------------------------------------
    # UNKNOWN EVENT
    # --------------------------------------------------------

    return {
        "positive": 0,
        "negative": 0
    }


# ============================================================
# ADD SIGNAL TO ATTRIBUTE
# ============================================================


def add_signal_to_attribute(
    signals,
    attribute_name,
    positive_points,
    negative_points
):

    attribute_name = normalize_text(
        attribute_name
    )

    if not attribute_name:
        return

    if attribute_name not in signals:

        signals[
            attribute_name
        ] = create_empty_signal()

    update_signal(

        signals[
            attribute_name
        ],

        positive_points,

        negative_points
    )


# ============================================================
# EXTRACT OUTFIT ATTRIBUTES
# ============================================================
#
# Returns the attributes represented by the outfit.
#
# We learn from:
#
# - styles
# - colors
# - fits
# - categories
# - occasions
# ============================================================


def extract_outfit_attributes(
    outfit
):

    attributes = {

        "styles": set(),

        "colors": set(),

        "fits": set(),

        "categories": set(),

        "occasions": set()
    }

    if not outfit:

        return attributes

    # --------------------------------------------------------
    # OUTFIT OCCASION
    # --------------------------------------------------------

    occasion = normalize_text(
        outfit.get("occasion")
    )

    if occasion:

        attributes[
            "occasions"
        ].add(
            occasion
        )

    # --------------------------------------------------------
    # OUTFIT ITEMS
    # --------------------------------------------------------

    for item in outfit.get(
        "items",
        []
    ):

        # CATEGORY

        category = normalize_text(
            item.get("category")
        )

        if category:

            attributes[
                "categories"
            ].add(
                category
            )

        # COLOR

        color = normalize_text(
            item.get("color")
        )

        if color:

            attributes[
                "colors"
            ].add(
                color
            )

        # FIT

        fit = normalize_text(
            item.get("fit")
        )

        if fit:

            attributes[
                "fits"
            ].add(
                fit
            )

        # STYLES

        for style in item.get(
            "style",
            []
        ):

            style = normalize_text(
                style
            )

            if style:

                attributes[
                    "styles"
                ].add(
                    style
                )

        # ITEM OCCASIONS

        for occasion in item.get(
            "occasion",
            []
        ):

            occasion = normalize_text(
                occasion
            )

            if occasion:

                attributes[
                    "occasions"
                ].add(
                    occasion
                )

    return attributes


# ============================================================
# APPLY EVENT SIGNAL TO OUTFIT ATTRIBUTES
# ============================================================


def apply_event_to_attributes(
    aggregated_signals,
    outfit,
    positive_points,
    negative_points
):

    attributes = extract_outfit_attributes(
        outfit
    )

    for attribute_group, values in attributes.items():

        for value in values:

            add_signal_to_attribute(

                aggregated_signals[
                    attribute_group
                ],

                value,

                positive_points,

                negative_points
            )


# ============================================================
# AGGREGATE FEEDBACK EVENTS
# ============================================================


def aggregate_feedback_events(
    feedback_events
):

    # --------------------------------------------------------
    # MAIN SIGNAL STRUCTURE
    # --------------------------------------------------------

    aggregated_signals = {

        "styles": {},

        "colors": {},

        "fits": {},

        "categories": {},

        "occasions": {}
    }


    # --------------------------------------------------------
    # PROCESS EVERY EVENT
    # --------------------------------------------------------

    for event in feedback_events:

        # Skip invalid events

        if not isinstance(
            event,
            dict
        ):

            continue


        # ----------------------------------------------------
        # GET EVENT SIGNAL
        # ----------------------------------------------------

        event_signal = get_event_signal(
            event
        )

        positive_points = event_signal[
            "positive"
        ]

        negative_points = event_signal[
            "negative"
        ]


        # Neutral event

        if (
            positive_points == 0
            and
            negative_points == 0
        ):

            continue


        # ----------------------------------------------------
        # GET OUTFIT
        # ----------------------------------------------------
        #
        # The event must contain the outfit snapshot
        # or outfit data associated with that feedback.
        # ----------------------------------------------------

        outfit = event.get(
            "outfit"
        )


        if not outfit:

            continue


        # ----------------------------------------------------
        # APPLY SIGNAL
        # ----------------------------------------------------

        apply_event_to_attributes(

            aggregated_signals,

            outfit,

            positive_points,

            negative_points
        )


    # --------------------------------------------------------
    # FINALIZE ALL SIGNALS
    # --------------------------------------------------------

    for attribute_group in (
        aggregated_signals.values()
    ):

        for signal in (
            attribute_group.values()
        ):

            finalize_signal(
                signal
            )


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {

        "status": "success",

        "total_events_processed":
            len(feedback_events),

        "signals":
            aggregated_signals
    }


# ============================================================
# GET STRONGEST SIGNALS
# ============================================================
#
# Helpful for testing and later for the Stylist Agent.
# ============================================================


def get_strongest_signals(
    aggregation_result,
    minimum_confidence="medium"
):

    confidence_order = {

        "low": 1,

        "medium": 2,

        "high": 3
    }


    minimum_level = confidence_order.get(

        minimum_confidence,

        2
    )


    strongest_signals = {

        "positive": {},

        "negative": {}
    }


    signals = aggregation_result.get(

        "signals",

        {}
    )


    for attribute_group, values in signals.items():

        for attribute_name, signal in values.items():

            confidence_level = confidence_order.get(

                signal.get(
                    "confidence",
                    "low"
                ),

                1
            )


            if confidence_level < minimum_level:

                continue


            net_score = signal.get(

                "net_score",

                0
            )


            if net_score > 0:

                strongest_signals[
                    "positive"
                ].setdefault(

                    attribute_group,

                    []
                ).append({

                    "value":
                        attribute_name,

                    "net_score":
                        net_score,

                    "confidence":
                        signal["confidence"]
                })


            elif net_score < 0:

                strongest_signals[
                    "negative"
                ].setdefault(

                    attribute_group,

                    []
                ).append({

                    "value":
                        attribute_name,

                    "net_score":
                        net_score,

                    "confidence":
                        signal["confidence"]
                })


    # --------------------------------------------------------
    # SORT STRONGEST FIRST
    # --------------------------------------------------------

    for direction in [
        "positive",
        "negative"
    ]:

        for attribute_group in strongest_signals[
            direction
        ]:

            strongest_signals[
                direction
            ][
                attribute_group
            ].sort(

                key=lambda item:

                abs(
                    item["net_score"]
                ),

                reverse=True
            )


    return strongest_signals