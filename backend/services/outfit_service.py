from agents.stylist_agent.agent import run_stylist_agent
from schemas.outfit_schema import StylistInput


MOCK_WARDROBE = [

    {
        "id": "W001",
        "user_id": "U001",
        "image_url": None,

        "category": "top",
        "color": "white",
        "pattern": "solid",
        "fit": "oversized",

        "style": ["minimal", "casual"],
        "season": ["summer", "spring"],
        "occasion": ["college", "casual"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 5,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W002",
        "user_id": "U001",
        "image_url": None,

        "category": "top",
        "color": "black",
        "pattern": "solid",
        "fit": "regular",

        "style": ["casual", "comfortable"],
        "season": ["all"],
        "occasion": ["college", "casual", "travel"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 8,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W003",
        "user_id": "U001",
        "image_url": None,

        "category": "top",
        "color": "light_blue",
        "pattern": "solid",
        "fit": "regular",

        "style": ["classic", "casual"],
        "season": ["summer", "spring"],
        "occasion": ["college", "office", "casual"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 3,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W004",
        "user_id": "U001",
        "image_url": None,

        "category": "bottom",
        "color": "blue",
        "pattern": "solid",
        "fit": "regular",

        "style": ["casual"],
        "season": ["all"],
        "occasion": ["college", "casual", "travel"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 10,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W005",
        "user_id": "U001",
        "image_url": None,

        "category": "bottom",
        "color": "black",
        "pattern": "solid",
        "fit": "regular",

        "style": ["formal", "minimal"],
        "season": ["all"],
        "occasion": ["office", "formal"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 2,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W006",
        "user_id": "U001",
        "image_url": None,

        "category": "bottom",
        "color": "beige",
        "pattern": "solid",
        "fit": "relaxed",

        "style": ["minimal", "casual"],
        "season": ["summer", "spring"],
        "occasion": ["college", "casual", "office"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 4,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W007",
        "user_id": "U001",
        "image_url": None,

        "category": "shoes",
        "color": "white",
        "pattern": "solid",
        "fit": None,

        "style": ["casual", "comfortable"],
        "season": ["all"],
        "occasion": ["college", "casual", "travel"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 15,
        "last_worn_at": None,

        "embedding": None
    },

    {
        "id": "W008",
        "user_id": "U001",
        "image_url": None,

        "category": "shoes",
        "color": "black",
        "pattern": "solid",
        "fit": None,

        "style": ["formal"],
        "season": ["all"],
        "occasion": ["office", "formal"],

        "condition": "good",
        "is_available": True,

        "created_at": None,
        "updated_at": None,

        "usage_count": 1,
        "last_worn_at": None,

        "embedding": None
    }
]


def process_outfit_request(occasion: str):

    agent_input = StylistInput(
        occasion=occasion,
        wardrobe=MOCK_WARDROBE
    )

    result = run_stylist_agent(agent_input)

    return result