from agents.stylist_agent.agent import run_stylist_agent
from schemas.outfit_schema import (
    StylistInput,
    UserPreferences
)
from services.weather_service import get_weather_context

MOCK_WARDROBE = [

    # ============================================================
    # TOPS
    # ============================================================

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
        "occasion": ["college", "casual", "travel", "brunch"],
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
        "occasion": ["college", "casual", "travel", "date", "dinner"],
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
        "occasion": ["college", "office", "casual", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 3,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W009",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "pink",
        "pattern": "floral",
        "fit": "regular",
        "style": ["feminine", "romantic", "casual"],
        "season": ["spring", "summer"],
        "occasion": ["date", "brunch", "casual", "vacation"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W010",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "maroon",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["elegant", "romantic"],
        "season": ["autumn", "winter"],
        "occasion": ["date", "dinner", "party"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W011",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "cream",
        "pattern": "ribbed",
        "fit": "fitted",
        "style": ["minimal", "elegant"],
        "season": ["all"],
        "occasion": ["date", "casual", "brunch", "travel"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 4,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # BOTTOMS
    # ============================================================

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
        "occasion": ["college", "casual", "travel", "brunch"],
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
        "occasion": ["office", "formal", "dinner"],
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
        "occasion": ["college", "casual", "office", "travel", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 4,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W012",
        "user_id": "U001",
        "image_url": None,
        "category": "bottom",
        "color": "white",
        "pattern": "solid",
        "fit": "wide_leg",
        "style": ["minimal", "elegant"],
        "season": ["summer", "spring"],
        "occasion": ["brunch", "date", "vacation", "casual"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W013",
        "user_id": "U001",
        "image_url": None,
        "category": "bottom",
        "color": "blue",
        "pattern": "denim",
        "fit": "wide_leg",
        "style": ["casual", "trendy"],
        "season": ["all"],
        "occasion": ["college", "casual", "travel"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 6,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # SKIRTS
    # ============================================================

    {
        "id": "W014",
        "user_id": "U001",
        "image_url": None,
        "category": "skirt",
        "color": "black",
        "pattern": "solid",
        "fit": "a_line",
        "style": ["feminine", "minimal"],
        "season": ["summer", "spring", "autumn"],
        "occasion": ["date", "brunch", "casual", "party"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W015",
        "user_id": "U001",
        "image_url": None,
        "category": "skirt",
        "color": "floral",
        "pattern": "floral",
        "fit": "flowy",
        "style": ["romantic", "feminine"],
        "season": ["spring", "summer"],
        "occasion": ["date", "brunch", "vacation"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # DRESSES / FROCKS
    # ============================================================

    {
        "id": "W016",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "black",
        "pattern": "solid",
        "fit": "bodycon",
        "style": ["elegant", "minimal", "romantic"],
        "season": ["all"],
        "occasion": ["date", "dinner", "party"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W017",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "pastel_pink",
        "pattern": "floral",
        "fit": "flowy",
        "style": ["feminine", "romantic", "elegant"],
        "season": ["spring", "summer"],
        "occasion": ["date", "brunch", "vacation", "party"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W018",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "red",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["bold", "elegant", "romantic"],
        "season": ["all"],
        "occasion": ["date", "party", "dinner"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W019",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "yellow",
        "pattern": "solid",
        "fit": "flowy",
        "style": ["casual", "feminine", "playful"],
        "season": ["summer", "spring"],
        "occasion": ["vacation", "brunch", "casual", "date"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # ETHNIC / TRADITIONAL
    # ============================================================

    {
        "id": "W020",
        "user_id": "U001",
        "image_url": None,
        "category": "kurti",
        "color": "blue",
        "pattern": "printed",
        "fit": "regular",
        "style": ["ethnic", "casual", "traditional"],
        "season": ["summer", "spring"],
        "occasion": ["college", "casual", "festive"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 3,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W021",
        "user_id": "U001",
        "image_url": None,
        "category": "kurti",
        "color": "maroon",
        "pattern": "embroidered",
        "fit": "straight",
        "style": ["ethnic", "elegant", "traditional"],
        "season": ["autumn", "winter"],
        "occasion": ["festive", "wedding", "family_event"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W022",
        "user_id": "U001",
        "image_url": None,
        "category": "saree",
        "color": "green",
        "pattern": "silk",
        "fit": None,
        "style": ["traditional", "elegant", "ethnic"],
        "season": ["all"],
        "occasion": ["wedding", "festive", "formal", "family_event"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W023",
        "user_id": "U001",
        "image_url": None,
        "category": "saree",
        "color": "pink",
        "pattern": "printed",
        "fit": None,
        "style": ["feminine", "traditional", "elegant"],
        "season": ["summer", "spring"],
        "occasion": ["festive", "wedding", "party"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W024",
        "user_id": "U001",
        "image_url": None,
        "category": "ethnic_set",
        "color": "cream",
        "pattern": "embroidered",
        "fit": "regular",
        "style": ["ethnic", "elegant"],
        "season": ["all"],
        "occasion": ["festive", "wedding", "family_event"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # JACKETS / LAYERS
    # ============================================================

    {
        "id": "W025",
        "user_id": "U001",
        "image_url": None,
        "category": "jacket",
        "color": "blue",
        "pattern": "denim",
        "fit": "oversized",
        "style": ["casual", "trendy"],
        "season": ["autumn", "winter", "spring"],
        "occasion": ["college", "casual", "travel"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 4,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W026",
        "user_id": "U001",
        "image_url": None,
        "category": "blazer",
        "color": "black",
        "pattern": "solid",
        "fit": "structured",
        "style": ["formal", "minimal", "elegant"],
        "season": ["autumn", "winter", "spring"],
        "occasion": ["office", "formal", "dinner", "date"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W027",
        "user_id": "U001",
        "image_url": None,
        "category": "cardigan",
        "color": "cream",
        "pattern": "knit",
        "fit": "relaxed",
        "style": ["cozy", "minimal", "casual"],
        "season": ["autumn", "winter"],
        "occasion": ["college", "casual", "travel", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # SHOES
    # ============================================================

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
        "occasion": ["college", "casual", "travel", "brunch"],
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
        "occasion": ["office", "formal", "dinner"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W028",
        "user_id": "U001",
        "image_url": None,
        "category": "shoes",
        "color": "beige",
        "pattern": "solid",
        "fit": None,
        "style": ["elegant", "feminine"],
        "season": ["summer", "spring"],
        "occasion": ["date", "brunch", "party", "formal"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 3,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W029",
        "user_id": "U001",
        "image_url": None,
        "category": "shoes",
        "color": "brown",
        "pattern": "solid",
        "fit": None,
        "style": ["casual", "boho"],
        "season": ["summer", "spring"],
        "occasion": ["vacation", "travel", "casual", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },


    # ============================================================
    # BAGS
    # ============================================================

    {
        "id": "W030",
        "user_id": "U001",
        "image_url": None,
        "category": "bag",
        "color": "black",
        "pattern": "solid",
        "fit": None,
        "style": ["minimal", "elegant"],
        "season": ["all"],
        "occasion": ["office", "date", "dinner", "formal"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 5,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W031",
        "user_id": "U001",
        "image_url": None,
        "category": "bag",
        "color": "beige",
        "pattern": "solid",
        "fit": None,
        "style": ["casual", "minimal"],
        "season": ["all"],
        "occasion": ["college", "travel", "brunch", "casual"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 8,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W032",
        "user_id": "U001",
        "image_url": None,
        "category": "bag",
        "color": "brown",
        "pattern": "woven",
        "fit": None,
        "style": ["boho", "vacation", "casual"],
        "season": ["summer", "spring"],
        "occasion": ["vacation", "beach", "travel", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # SCARVES / DUPATTAS
    # ============================================================

    {
        "id": "W035",
        "user_id": "U001",
        "image_url": None,
        "category": "dupatta",
        "color": "pink",
        "pattern": "printed",
        "fit": None,
        "style": ["ethnic", "feminine"],
        "season": ["summer", "spring"],
        "occasion": ["festive", "casual", "college"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W036",
        "user_id": "U001",
        "image_url": None,
        "category": "scarf",
        "color": "cream",
        "pattern": "printed",
        "fit": None,
        "style": ["casual", "boho"],
        "season": ["autumn", "winter", "spring"],
        "occasion": ["travel", "casual", "college"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    }
]

# ============================================================
# MOCK USER PREFERENCES
# ============================================================

MOCK_USER_PREFERENCES = {
    "styles": [
        "minimal",
        "romantic",
    ],

    "colors": [
        "red",
        "black",
        "beige"
    ],

    "fits": [
        "bodycon",
        "flowy"
    ],

    "comfort_level": 4
}

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