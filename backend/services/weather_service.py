"""Weather service placeholder."""


class WeatherService:
    """Provides weather data for outfit planning."""

    def get_forecast(self, city: str) -> dict:
        return {"city": city, "temperature": 22, "condition": "sunny"}
