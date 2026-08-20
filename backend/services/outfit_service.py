"""Outfit service placeholder."""


class OutfitService:
    """Coordinates outfit recommendation logic."""

    def generate_outfit(self, wardrobe: list[str] | None = None) -> list[str]:
        return wardrobe or ["shirt", "pants", "jacket"]
