# ============================================================
# WEATHER SCORING
# ============================================================


def calculate_weather_score(
    outfit,
    weather
):

    items = outfit.get(
        "items",
        []
    )

    if not items:

        return 0

    recommended_season = (
        weather.get(
            "recommended_season",
            "all"
        )
        .lower()
    )

    matched_items = 0

    for item in items:

        seasons = [
            season.lower()
            for season in item.get(
                "season",
                []
            )
        ]

        if (
            "all" in seasons
            or recommended_season
            in seasons
        ):

            matched_items += 1

    return round(
        (
            matched_items
            / len(items)
        ) * 100,
        2
    )