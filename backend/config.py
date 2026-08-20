"""Application configuration settings."""

from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = "Closet-IQ"
    debug: bool = True
    api_prefix: str = "/api"


settings = Settings()
