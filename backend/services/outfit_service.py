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
    },

    {
        "id": "W037",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "navy",
        "pattern": "striped",
        "fit": "regular",
        "style": ["classic", "casual"],
        "season": ["all"],
        "occasion": ["college", "casual", "travel", "office"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 4,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W038",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "lavender",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["feminine", "minimal", "elegant"],
        "season": ["spring", "summer"],
        "occasion": ["date", "brunch", "casual", "party"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W039",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "beige",
        "pattern": "linen",
        "fit": "relaxed",
        "style": ["minimal", "comfortable", "classic"],
        "season": ["summer", "spring"],
        "occasion": ["travel", "vacation", "casual", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W040",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "gold",
        "pattern": "embellished",
        "fit": "fitted",
        "style": ["party", "elegant", "bold"],
        "season": ["autumn", "winter"],
        "occasion": ["party", "festive", "dinner", "wedding"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # ADDITIONAL BOTTOMS
    # ============================================================

    {
        "id": "W041",
        "user_id": "U001",
        "image_url": None,
        "category": "bottom",
        "color": "navy",
        "pattern": "solid",
        "fit": "straight",
        "style": ["formal", "classic"],
        "season": ["all"],
        "occasion": ["office", "formal", "dinner"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W042",
        "user_id": "U001",
        "image_url": None,
        "category": "bottom",
        "color": "olive",
        "pattern": "solid",
        "fit": "cargo",
        "style": ["casual", "trendy"],
        "season": ["spring", "summer", "autumn"],
        "occasion": ["college", "travel", "casual"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W043",
        "user_id": "U001",
        "image_url": None,
        "category": "bottom",
        "color": "cream",
        "pattern": "pleated",
        "fit": "wide_leg",
        "style": ["elegant", "minimal", "classic"],
        "season": ["summer", "spring", "autumn"],
        "occasion": ["office", "brunch", "date", "formal"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # SHORTS
    # ============================================================

    {
        "id": "W044",
        "user_id": "U001",
        "image_url": None,
        "category": "shorts",
        "color": "beige",
        "pattern": "solid",
        "fit": "relaxed",
        "style": ["casual", "comfortable"],
        "season": ["summer"],
        "occasion": ["vacation", "beach", "travel", "casual"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 3,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # ADDITIONAL SKIRTS
    # ============================================================

    {
        "id": "W045",
        "user_id": "U001",
        "image_url": None,
        "category": "skirt",
        "color": "beige",
        "pattern": "pleated",
        "fit": "midi",
        "style": ["classic", "feminine", "elegant"],
        "season": ["spring", "summer", "autumn"],
        "occasion": ["office", "brunch", "date", "formal"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W046",
        "user_id": "U001",
        "image_url": None,
        "category": "skirt",
        "color": "red",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["bold", "party", "feminine"],
        "season": ["all"],
        "occasion": ["party", "date", "dinner"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # JUMPSUIT
    # ============================================================

    {
        "id": "W047",
        "user_id": "U001",
        "image_url": None,
        "category": "jumpsuit",
        "color": "navy",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["elegant", "minimal", "classic"],
        "season": ["spring", "summer", "autumn"],
        "occasion": ["party", "dinner", "date", "formal"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # MORE DRESSES
    # ============================================================

    {
        "id": "W048",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "navy",
        "pattern": "solid",
        "fit": "midi",
        "style": ["classic", "elegant", "minimal"],
        "season": ["all"],
        "occasion": ["office", "formal", "dinner", "date"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W049",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "green",
        "pattern": "floral",
        "fit": "flowy",
        "style": ["feminine", "romantic", "boho"],
        "season": ["spring", "summer"],
        "occasion": ["vacation", "brunch", "date", "party"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # ETHNIC ADDITIONS
    # ============================================================

    {
        "id": "W050",
        "user_id": "U001",
        "image_url": None,
        "category": "kurti",
        "color": "mustard",
        "pattern": "block_print",
        "fit": "straight",
        "style": ["ethnic", "traditional", "casual"],
        "season": ["summer", "spring", "autumn"],
        "occasion": ["college", "casual", "festive", "family_event"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 5,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W051",
        "user_id": "U001",
        "image_url": None,
        "category": "kurti",
        "color": "white",
        "pattern": "embroidered",
        "fit": "straight",
        "style": ["ethnic", "minimal", "elegant"],
        "season": ["summer", "spring"],
        "occasion": ["college", "casual", "festive", "family_event"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W052",
        "user_id": "U001",
        "image_url": None,
        "category": "saree",
        "color": "navy",
        "pattern": "silk",
        "fit": None,
        "style": ["traditional", "elegant", "formal"],
        "season": ["all"],
        "occasion": ["wedding", "festive", "formal", "family_event"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W053",
        "user_id": "U001",
        "image_url": None,
        "category": "lehenga",
        "color": "pink",
        "pattern": "embroidered",
        "fit": None,
        "style": ["traditional", "feminine", "elegant"],
        "season": ["all"],
        "occasion": ["wedding", "festive", "party"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # LAYERS
    # ============================================================

    {
        "id": "W054",
        "user_id": "U001",
        "image_url": None,
        "category": "jacket",
        "color": "black",
        "pattern": "leather",
        "fit": "fitted",
        "style": ["edgy", "trendy", "bold"],
        "season": ["autumn", "winter"],
        "occasion": ["casual", "date", "party", "travel"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W055",
        "user_id": "U001",
        "image_url": None,
        "category": "blazer",
        "color": "beige",
        "pattern": "solid",
        "fit": "structured",
        "style": ["formal", "minimal", "classic"],
        "season": ["spring", "autumn", "winter"],
        "occasion": ["office", "formal", "brunch", "date"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # ADDITIONAL SHOES
    # ============================================================

    {
        "id": "W056",
        "user_id": "U001",
        "image_url": None,
        "category": "shoes",
        "color": "red",
        "pattern": "solid",
        "fit": None,
        "style": ["bold", "party", "feminine"],
        "season": ["all"],
        "occasion": ["party", "date", "dinner"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W057",
        "user_id": "U001",
        "image_url": None,
        "category": "shoes",
        "color": "brown",
        "pattern": "solid",
        "fit": None,
        "style": ["classic", "formal", "elegant"],
        "season": ["all"],
        "occasion": ["office", "formal", "dinner"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W058",
        "user_id": "U001",
        "image_url": None,
        "category": "shoes",
        "color": "white",
        "pattern": "canvas",
        "fit": None,
        "style": ["casual", "trendy", "comfortable"],
        "season": ["spring", "summer", "autumn"],
        "occasion": ["college", "casual", "travel", "vacation"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 7,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # ACCESSORIES
    # ============================================================

    {
        "id": "W059",
        "user_id": "U001",
        "image_url": None,
        "category": "belt",
        "color": "black",
        "pattern": "solid",
        "fit": None,
        "style": ["minimal", "formal", "classic"],
        "season": ["all"],
        "occasion": ["office", "formal", "casual", "dinner"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 3,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W060",
        "user_id": "U001",
        "image_url": None,
        "category": "watch",
        "color": "gold",
        "pattern": "metallic",
        "fit": None,
        "style": ["elegant", "classic"],
        "season": ["all"],
        "occasion": ["office", "formal", "date", "dinner"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 4,
        "last_worn_at": None,
        "embedding": None
    },

    {
        "id": "W061",
        "user_id": "U001",
        "image_url": None,
        "category": "sunglasses",
        "color": "black",
        "pattern": "solid",
        "fit": None,
        "style": ["casual", "trendy"],
        "season": ["summer", "spring"],
        "occasion": ["travel", "vacation", "casual", "brunch"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 2,
        "last_worn_at": None,
        "embedding": None
    },

    # ============================================================
    # DELIBERATE EDGE CASES
    # ============================================================

    {
        "id": "W062",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "white",
        "pattern": "solid",
        "fit": "regular",
        "style": ["casual"],
        "season": ["all"],
        "occasion": ["college", "casual"],
        "condition": "good",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 30,
        "last_worn_at": None,
        "embedding": None
    },

    # Rarely worn item
    {
        "id": "W063",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "emerald",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["elegant", "bold"],
        "season": ["all"],
        "occasion": ["party", "dinner", "date"],
        "condition": "excellent",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 0,
        "last_worn_at": None,
        "embedding": None
    },

    # Unavailable item
    {
        "id": "W064",
        "user_id": "U001",
        "image_url": None,
        "category": "dress",
        "color": "black",
        "pattern": "solid",
        "fit": "fitted",
        "style": ["elegant", "minimal"],
        "season": ["all"],
        "occasion": ["date", "dinner", "party"],
        "condition": "good",
        "is_available": False,
        "created_at": None,
        "updated_at": None,
        "usage_count": 1,
        "last_worn_at": None,
        "embedding": None
    },

    # Poor-condition item
    {
        "id": "W065",
        "user_id": "U001",
        "image_url": None,
        "category": "top",
        "color": "gray",
        "pattern": "solid",
        "fit": "regular",
        "style": ["casual", "comfortable"],
        "season": ["all"],
        "occasion": ["college", "casual", "travel"],
        "condition": "poor",
        "is_available": True,
        "created_at": None,
        "updated_at": None,
        "usage_count": 12,
        "last_worn_at": None,
        "embedding": None
    }

]

# ============================================================
# MOCK USER PREFERENCES
# ============================================================

MOCK_USER_PREFERENCES = {
    "long_term": {
      "styles": ["casual", "minimal"],
      "colors": ["white", "black"],
      "fits": ["oversized"],
      "comfort_level": 3
    },
    "short_term": {
      "styles": ["elegant", "romantic"],
      "colors": ["red"],
      "fits": ["fitted"],
      "comfort_level": 4,
      "avoid_styles": ["casual"],
      "avoid_colors": ["black"],
      "occasion_note": "I want something special today"
    }
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