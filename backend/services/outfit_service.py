from agents.stylist_agent.agent import run_stylist_agent
from schemas.outfit_schema import (
    StylistInput,
    UserPreferences
)
from services.weather_service import get_weather_context

def process_outfit_request(
    occasion: str,
    latitude: float,
    longitude: float
):

    preferences = UserPreferences(
        **MOCK_USER_PREFERENCES
    )

    # =====================================
    # GET REAL-TIME WEATHER
    # =====================================

    weather = get_weather_context(
        latitude,
        longitude
    )

    # =====================================
    # CREATE STYLIST INPUT
    # =====================================


    agent_input = StylistInput(
        occasion=occasion,
        wardrobe=MOCK_WARDROBE,
        preferences=preferences
    )

    # =====================================
    # RUN STYLIST AGENT
    # =====================================

    result = run_stylist_agent(
        agent_input,
        weather
    )

    return result