import requests


# ============================================================
# WEATHER CODE → CONDITION
# ============================================================

def get_weather_condition(
    weather_code: int
):

    if weather_code == 0:
        return "clear"

    elif weather_code in [1, 2, 3]:
        return "cloudy"

    elif weather_code in [45, 48]:
        return "foggy"

    elif weather_code in [
        51, 53, 55,
        56, 57,
        61, 63, 65,
        66, 67,
        80, 81, 82
    ]:
        return "rainy"

    elif weather_code in [
        71, 73, 75,
        77, 85, 86
    ]:
        return "snowy"

    elif weather_code in [
        95, 96, 99
    ]:
        return "thunderstorm"

    return "unknown"


# ============================================================
# TEMPERATURE → CLOTHING SEASON
# ============================================================

def get_recommended_season(
    temperature: float
):

    if temperature > 30:
        return "summer"

    elif temperature > 20:
        return "spring"

    elif temperature > 10:
        return "autumn"

    return "winter"


# ============================================================
# GET CURRENT WEATHER
# FOR SINGLE OUTFIT GENERATION
# ============================================================

def get_weather_context(
    latitude: float,
    longitude: float
):

    url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current":
            "temperature_2m,weather_code",

        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    temperature = current[
        "temperature_2m"
    ]

    weather_code = current[
        "weather_code"
    ]

    condition = get_weather_condition(
        weather_code
    )

    recommended_season = (
        get_recommended_season(
            temperature
        )
    )

    return {

        "temperature":
            temperature,

        "weather_code":
            weather_code,

        "condition":
            condition,

        "recommended_season":
            recommended_season
    }


# ============================================================
# GET 7-DAY WEATHER FORECAST
# FOR WEEKLY PLANNER
# ============================================================

def get_weekly_weather(
    latitude: float,
    longitude: float
):

    url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "weather_code"
        ),

        "forecast_days": 7,

        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    daily = data["daily"]

    weather = []

    total_days = min(
        7,
        len(daily["time"])
    )


    # ========================================================
    # PROCESS EACH FORECAST DAY
    # ========================================================

    for i in range(total_days):

        temperature_max = daily[
            "temperature_2m_max"
        ][i]

        temperature_min = daily[
            "temperature_2m_min"
        ][i]

        weather_code = daily[
            "weather_code"
        ][i]


        # ====================================================
        # CONDITION
        # ====================================================

        condition = get_weather_condition(
            weather_code
        )


        # ====================================================
        # AVERAGE TEMPERATURE
        # ====================================================

        average_temperature = (
            temperature_max +
            temperature_min
        ) / 2


        # ====================================================
        # RECOMMENDED CLOTHING SEASON
        # ====================================================

        recommended_season = (
            get_recommended_season(
                average_temperature
            )
        )


        # ====================================================
        # STORE DAY WEATHER
        # ====================================================

        weather.append({

            "date":
                daily["time"][i],

            "temperature_max":
                temperature_max,

            "temperature_min":
                temperature_min,

            "weather_code":
                weather_code,

            "condition":
                condition,

            "recommended_season":
                recommended_season
        })


    return weather