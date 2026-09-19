import open_clip
import torch
from PIL import Image


# ============================================================
# LOAD FASHIONCLIP MODEL
# ============================================================

print("Loading FashionCLIP model...")

model, _, preprocess = open_clip.create_model_and_transforms(
    "hf-hub:Marqo/marqo-fashionCLIP"
)

tokenizer = open_clip.get_tokenizer(
    "hf-hub:Marqo/marqo-fashionCLIP"
)

model.eval()


# ============================================================
# CATEGORY NORMALIZATION
#
# FashionCLIP receives natural-language fashion descriptions.
# Closet-IQ receives canonical category names that match
# services/wardrobe_intelligence.py exactly.
# ============================================================

CATEGORY_LABEL_MAP = {

    # --------------------------------------------------------
    # UPPER BODY
    # --------------------------------------------------------

    "a fashion top": "top",
    "a t-shirt": "tshirt",
    "a shirt": "shirt",
    "a blouse": "blouse",
    "a crop top": "crop_top",
    "a tank top": "tank_top",
    "a polo shirt": "polo",
    "a sweater": "sweater",
    "a hoodie": "hoodie",

    # --------------------------------------------------------
    # LOWER BODY
    # --------------------------------------------------------

    "a pair of jeans": "jeans",
    "a pair of trousers": "trousers",
    "a pair of pants": "pants",
    "a pair of shorts": "shorts",
    "a skirt": "skirt",
    "a pair of joggers": "joggers",
    "a pair of leggings": "leggings",

    # --------------------------------------------------------
    # ONE PIECE
    # --------------------------------------------------------

    "a dress": "dress",
    "a jumpsuit": "jumpsuit",
    "a romper": "romper",
    "a co-ord set": "co_ord_set",

    # --------------------------------------------------------
    # OUTER LAYER
    # --------------------------------------------------------

    "a jacket": "jacket",
    "a blazer": "blazer",
    "a coat": "coat",
    "a cardigan": "cardigan",
    "a shrug": "shrug",

    # --------------------------------------------------------
    # TRADITIONAL / ETHNIC
    # --------------------------------------------------------

    "an Indian saree": "saree",
    "an Indian kurti": "kurti",
    "an Indian lehenga": "lehenga",
    "an Indian anarkali dress": "anarkali",
    "an Indian salwar suit": "salwar_suit",
    "an Indian ethnic clothing set": "ethnic_set",

    # --------------------------------------------------------
    # SWIMWEAR
    # --------------------------------------------------------

    "a bikini": "bikini",
    "a swimsuit": "swimsuit",
    "swimwear": "swimwear",

    # --------------------------------------------------------
    # SPECIAL LAYERS
    # --------------------------------------------------------

    "a fashion cover-up": "cover_up",
    "a beach cover-up": "beach_coverup",
    "a kimono": "kimono",

    # --------------------------------------------------------
    # FOOTWEAR
    # --------------------------------------------------------

    "a pair of shoes": "shoes",
    "a pair of sneakers": "sneakers",
    "a pair of high heels": "heels",
    "a pair of sandals": "sandals",
    "a pair of flat shoes": "flats",
    "a pair of boots": "boots",
    "a pair of slippers": "slippers",
    "a pair of loafers": "loafers",

    # --------------------------------------------------------
    # BAGS
    #
    # Wardrobe Intelligence groups all of these under bag.
    # We store canonical "bag" so downstream logic is simple.
    # --------------------------------------------------------

    "a fashion bag": "bag",
    "a handbag": "bag",
    "a tote bag": "bag",
    "a clutch bag": "bag",
    "a crossbody bag": "bag",
    "a backpack": "bag",

    # --------------------------------------------------------
    # STYLE ACCESSORIES
    # --------------------------------------------------------

    "a fashion belt": "belt",
    "a wrist watch": "watch",
    "a pair of sunglasses": "sunglasses",

    # --------------------------------------------------------
    # ETHNIC ACCESSORIES
    # --------------------------------------------------------

    "an Indian dupatta": "dupatta",
    "a fashion scarf": "scarf",

    # --------------------------------------------------------
    # JEWELRY
    # --------------------------------------------------------

    "a necklace": "necklace",
    "a pair of earrings": "earrings",
    "a bracelet": "bracelet",
    "a ring": "ring",
}


# ============================================================
# COLOR NORMALIZATION
# ============================================================

COLOR_LABEL_MAP = {

    "white clothing or accessory": "white",
    "black clothing or accessory": "black",
    "gray clothing or accessory": "gray",
    "silver clothing or accessory": "silver",

    "red clothing or accessory": "red",
    "maroon clothing or accessory": "maroon",
    "burgundy clothing or accessory": "burgundy",

    "blue clothing or accessory": "blue",
    "navy blue clothing or accessory": "navy",
    "light blue clothing or accessory": "light_blue",

    "green clothing or accessory": "green",
    "olive green clothing or accessory": "olive",
    "emerald green clothing or accessory": "emerald",

    "yellow clothing or accessory": "yellow",
    "mustard clothing or accessory": "mustard",
    "gold clothing or accessory": "gold",

    "orange clothing or accessory": "orange",
    "peach clothing or accessory": "peach",

    "pink clothing or accessory": "pink",
    "blush pink clothing or accessory": "blush",

    "purple clothing or accessory": "purple",
    "lavender clothing or accessory": "lavender",

    "brown clothing or accessory": "brown",
    "tan clothing or accessory": "tan",

    "beige clothing or accessory": "beige",
    "cream clothing or accessory": "cream",
    "ivory clothing or accessory": "ivory",
}


# ============================================================
# PATTERN NORMALIZATION
# ============================================================

PATTERN_LABEL_MAP = {

    "plain solid clothing": "solid",
    "striped clothing": "striped",
    "checked clothing": "checked",
    "floral clothing": "floral",
    "printed clothing": "printed",
    "polka dot clothing": "polka_dot",
    "embroidered clothing": "embroidered",
    "block print clothing": "block_print",
    "ribbed clothing": "ribbed",
    "patterned clothing": "patterned",
}


# ============================================================
# STYLE NORMALIZATION
# ============================================================

STYLE_LABEL_MAP = {

    "casual fashion": "casual",
    "comfortable fashion": "comfortable",
    "minimal fashion": "minimal",
    "classic fashion": "classic",

    "formal fashion": "formal",
    "elegant fashion": "elegant",

    "feminine fashion": "feminine",
    "romantic fashion": "romantic",

    "trendy fashion": "trendy",
    "bold fashion": "bold",

    "bohemian fashion": "boho",

    "traditional Indian fashion": "traditional",
    "ethnic Indian fashion": "ethnic",

    "playful fashion": "playful",
    "cozy fashion": "cozy",

    "vacation fashion": "vacation",
    "sporty fashion": "sporty",
}


# ============================================================
# FIT NORMALIZATION
# ============================================================

FIT_LABEL_MAP = {

    "relaxed fit clothing": "relaxed",
    "regular fit clothing": "regular",
    "oversized clothing": "oversized",
    "fitted clothing": "fitted",
    "slim fit clothing": "slim",
    "flowy clothing": "flowy",
    "structured clothing": "structured",
    "wide leg clothing": "wide_leg",
}


# ============================================================
# OCCASION NORMALIZATION
# ============================================================

OCCASION_LABEL_MAP = {

    "clothing for college": "college",
    "clothing for office": "office",
    "clothing for casual everyday wear": "casual",

    "clothing for a date": "date",
    "clothing for dinner": "dinner",

    "clothing for a party": "party",
    "clothing for brunch": "brunch",

    "clothing for travel": "travel",

    "clothing for a formal event": "formal",

    "clothing for an Indian festive occasion": "festive",
    "clothing for an Indian wedding": "wedding",
    "clothing for a family event": "family_event",

    "clothing for vacation": "vacation",
    "clothing for the beach": "beach",
}


# ============================================================
# SEASON NORMALIZATION
# ============================================================

SEASON_LABEL_MAP = {

    "summer clothing": "summer",
    "winter clothing": "winter",
    "spring clothing": "spring",
    "autumn clothing": "autumn",
    "rainy season clothing": "rainy",
    "all season clothing": "all",
}


# ============================================================
# LABEL LISTS
# ============================================================

CATEGORY_LABELS = list(CATEGORY_LABEL_MAP.keys())
COLOR_LABELS = list(COLOR_LABEL_MAP.keys())
PATTERN_LABELS = list(PATTERN_LABEL_MAP.keys())
STYLE_LABELS = list(STYLE_LABEL_MAP.keys())
FIT_LABELS = list(FIT_LABEL_MAP.keys())
OCCASION_LABELS = list(OCCASION_LABEL_MAP.keys())
SEASON_LABELS = list(SEASON_LABEL_MAP.keys())


# ============================================================
# NORMALIZE LABEL
# ============================================================

def normalize_label(label: str, label_map: dict) -> str:

    return label_map.get(
        label,
        label
    )


# ============================================================
# PREPARE IMAGE
# ============================================================

def prepare_image(image_path):

    return preprocess(
        Image.open(
            image_path
        ).convert("RGB")
    ).unsqueeze(0)


# ============================================================
# GENERATE IMAGE EMBEDDING
# ============================================================

def generate_embedding(image_path):

    image = prepare_image(
        image_path
    )

    with torch.no_grad():

        image_features = model.encode_image(
            image
        )

        image_features = (
            image_features
            /
            image_features.norm(
                dim=-1,
                keepdim=True
            )
        )

    return (
        image_features[0]
        .cpu()
        .tolist()
    )


# ============================================================
# GET PREDICTIONS
# ============================================================

def get_predictions(
    image,
    labels
):

    text = tokenizer(
        labels
    )

    with torch.no_grad():

        image_features = model.encode_image(
            image
        )

        text_features = model.encode_text(
            text
        )

        image_features = (
            image_features
            /
            image_features.norm(
                dim=-1,
                keepdim=True
            )
        )

        text_features = (
            text_features
            /
            text_features.norm(
                dim=-1,
                keepdim=True
            )
        )

        similarity = (
            100.0
            *
            image_features
            @
            text_features.T
        ).softmax(
            dim=-1
        )

    results = list(
        zip(
            labels,
            similarity[0].tolist()
        )
    )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results


# ============================================================
# GET SINGLE BEST PREDICTION
# ============================================================

def get_top_prediction(
    image,
    labels,
    label_map=None
):

    results = get_predictions(
        image,
        labels
    )

    label, score = results[0]

    if label_map is not None:

        label = normalize_label(
            label,
            label_map
        )

    return {
        "label": label,
        "confidence": round(
            score,
            4
        )
    }


# ============================================================
# GET MULTIPLE PREDICTIONS
# ============================================================

def get_top_predictions(
    image,
    labels,
    top_n=3,
    label_map=None
):

    results = get_predictions(
        image,
        labels
    )

    predictions = []

    # Prevent normalization aliases from creating duplicate
    # canonical values in the final list.
    seen_labels = set()

    for label, score in results:

        if label_map is not None:

            normalized_label = normalize_label(
                label,
                label_map
            )

        else:

            normalized_label = label

        if normalized_label in seen_labels:
            continue

        seen_labels.add(
            normalized_label
        )

        predictions.append({
            "label": normalized_label,
            "confidence": round(
                score,
                4
            )
        })

        if len(predictions) >= top_n:
            break

    return predictions


# ============================================================
# MAIN CLOTHING ANALYSIS
# ============================================================

def analyze_clothing(image_path):

    image = prepare_image(image_path)

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    category = get_top_prediction(
        image,
        CATEGORY_LABELS,
        label_map=CATEGORY_LABEL_MAP
    )

    # --------------------------------------------------------
    # COLOR
    # --------------------------------------------------------

    color = get_top_prediction(
        image,
        COLOR_LABELS,
        label_map=COLOR_LABEL_MAP
    )

    # --------------------------------------------------------
    # PATTERN
    # --------------------------------------------------------

    pattern = get_top_prediction(
        image,
        PATTERN_LABELS,
        label_map=PATTERN_LABEL_MAP
    )

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    styles = get_top_predictions(
        image,
        STYLE_LABELS,
        top_n=3,
        label_map=STYLE_LABEL_MAP
    )

    # --------------------------------------------------------
    # FIT
    # --------------------------------------------------------

    fit = get_top_prediction(
        image,
        FIT_LABELS,
        label_map=FIT_LABEL_MAP
    )

    # --------------------------------------------------------
    # OCCASION
    # --------------------------------------------------------

    occasions = get_top_predictions(
        image,
        OCCASION_LABELS,
        top_n=3,
        label_map=OCCASION_LABEL_MAP
    )

    # --------------------------------------------------------
    # SEASON
    # --------------------------------------------------------

    season = get_top_prediction(
        image,
        SEASON_LABELS,
        label_map=SEASON_LABEL_MAP
    )

    # --------------------------------------------------------
    # EMBEDDING
    # --------------------------------------------------------

    embedding = generate_embedding(image_path)

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {
        "category": category,
        "color": color,
        "pattern": pattern,
        "styles": styles,
        "fit": fit,
        "occasions": occasions,
        "season": season,
        "embedding": embedding
    }