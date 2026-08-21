from schemas.outfit_schema import StylistInput
from agents.stylist_agent.agent import run_stylist_agent


MOCK_WARDROBE = [
    {
        "id": "W001",
        "name": "White Oversized Shirt",
        "category": "top",
        "color": "white",
        "style": ["minimal", "casual"],
        "fit": "oversized",
        "available": True
    },
    {
        "id": "W002",
        "name": "Black T-Shirt",
        "category": "top",
        "color": "black",
        "style": ["casual", "comfortable"],
        "fit": "regular",
        "available": True
    },
    {
        "id": "W003",
        "name": "Light Blue Shirt",
        "category": "top",
        "color": "blue",
        "style": ["casual", "classic"],
        "fit": "regular",
        "available": True
    },
    {
        "id": "W004",
        "name": "Blue Jeans",
        "category": "bottom",
        "color": "blue",
        "style": ["casual"],
        "fit": "regular",
        "available": True
    },
    {
        "id": "W005",
        "name": "Black Trousers",
        "category": "bottom",
        "color": "black",
        "style": ["formal", "minimal"],
        "fit": "regular",
        "available": True
    },
    {
        "id": "W006",
        "name": "Beige Trousers",
        "category": "bottom",
        "color": "beige",
        "style": ["minimal", "casual"],
        "fit": "relaxed",
        "available": True
    },
    {
        "id": "W007",
        "name": "White Sneakers",
        "category": "shoes",
        "color": "white",
        "style": ["casual", "comfortable"],
        "fit": None,
        "available": True
    },
    {
        "id": "W008",
        "name": "Black Formal Shoes",
        "category": "shoes",
        "color": "black",
        "style": ["formal"],
        "fit": None,
        "available": True
    }
]


def process_outfit_request(occasion: str):

    agent_input = StylistInput(
        occasion=occasion,
        wardrobe=MOCK_WARDROBE
    )

    result = run_stylist_agent(agent_input)

    return result