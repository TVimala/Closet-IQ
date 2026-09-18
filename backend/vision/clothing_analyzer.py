import open_clip
import torch
from PIL import Image


# -------------------------
# LOAD FASHIONCLIP MODEL
# -------------------------

print("Loading FashionCLIP model...")

model, _, preprocess = open_clip.create_model_and_transforms(
    "hf-hub:Marqo/marqo-fashionCLIP"
)

tokenizer = open_clip.get_tokenizer(
    "hf-hub:Marqo/marqo-fashionCLIP"
)

model.eval()

# ============================================================
# LABEL NORMALIZATION
#
# FashionCLIP classifies better against natural-sounding prompts
# ("college outfit", "classic clothing") than bare words, so the
# label lists below stay verbose. But that same text was going
# straight into the database, and the stylist agent's scoring
# code (occasion.py, weather.py, preferences.py) does exact
# string matching against short canonical words like "college"
# and "classic". These maps translate CLIP's prediction back to
# the canonical vocabulary BEFORE it's returned/saved.
# ============================================================

COLOR_LABEL_MAP = {
    "white clothing": "white",
    "black clothing": "black",
    "gray clothing": "gray",
    "red clothing": "red",
    "blue clothing": "blue",
    "green clothing": "green",
    "yellow clothing": "yellow",
    "orange clothing": "orange",
    "pink clothing": "pink",
    "purple clothing": "purple",
    "brown clothing": "brown",
    "beige clothing": "beige",
    "cream clothing": "cream",
}

PATTERN_LABEL_MAP = {
    "plain clothing": "plain",
    "striped clothing": "striped",
    "checked clothing": "checked",
    "floral clothing": "floral",
    "printed clothing": "printed",
    "polka dot clothing": "polka dot",
    "patterned clothing": "patterned",
}

STYLE_LABEL_MAP = {
    "casual clothing": "casual",
    "formal clothing": "formal",
    # "smart casual" has no matching key anywhere in
    # OCCASION_STYLE_SCORES yet, so it's folded into "casual"
    # rather than silently scoring zero everywhere.
    "smart casual clothing": "casual",
    "sporty clothing": "sporty",
    "minimal clothing": "minimal",
    "elegant clothing": "elegant",
    # same reasoning: streetwear isn't a scoring key, closest
    # existing concept is trendy.
    "streetwear clothing": "trendy",
    "classic clothing": "classic",
    "trendy clothing": "trendy",
}

FIT_LABEL_MAP = {
    "relaxed fit clothing": "relaxed",
    "regular fit clothing": "regular",
    "oversized clothing": "oversized",
    "fitted clothing": "fitted",
    "slim fit clothing": "slim",
}

OCCASION_LABEL_MAP = {
    "casual everyday clothing": "casual",
    "college outfit": "college",
    "office wear": "office",
    "party outfit": "party",
    "date night outfit": "date",
    "wedding guest outfit": "wedding",
    "traditional wedding outfit": "wedding",
    "beach vacation outfit": "beach",
    "summer casual outfit": "casual",
    "formal event outfit": "formal",
}

SEASON_LABEL_MAP = {
    "summer clothing": "summer",
    "winter clothing": "winter",
    "spring clothing": "spring",
    "autumn clothing": "autumn",
    "all season clothing": "all",
}


def normalize_label(label: str, label_map: dict) -> str:
    # .get(..., label) is a safe fallback: if a label somehow
    # isn't in the map, keep the original text instead of losing
    # data silently.
    return label_map.get(label, label)


def generate_embedding(image_path):

    image = preprocess(
        Image.open(image_path).convert("RGB")
    ).unsqueeze(0)

    with torch.no_grad():

        image_features = model.encode_image(image)

        # Normalize the embedding
        image_features = image_features / image_features.norm(
            dim=-1,
            keepdim=True
        )

    # Convert tensor to Python list
    embedding = image_features[0].cpu().tolist()

    return embedding


# -------------------------
# GET PREDICTIONS
# -------------------------

def get_predictions(image, labels):

    # Convert labels into tokens
    text = tokenizer(labels)

    with torch.no_grad():

        # Extract image features
        image_features = model.encode_image(image)

        # Extract text features
        text_features = model.encode_text(text)

        # Normalize features
        image_features /= image_features.norm(
            dim=-1,
            keepdim=True
        )

        text_features /= text_features.norm(
            dim=-1,
            keepdim=True
        )

        # Calculate similarity
        similarity = (
            100.0 * image_features @ text_features.T
        ).softmax(dim=-1)

    results = list(
        zip(labels, similarity[0].tolist())
    )

    # Sort highest confidence first
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results


# -------------------------
# GET SINGLE BEST RESULT
# -------------------------

def get_top_prediction(image, labels, label_map=None):

    results = get_predictions(
        image,
        labels
    )

    label, score = results[0]

    if label_map is not None:
        label = normalize_label(label, label_map)

    return {
        "label": label,
        "confidence": round(score, 4)
    }


# -------------------------
# GET TOP MULTIPLE RESULTS
# -------------------------

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

    for label, score in results[:top_n]:

        if label_map is not None:
            label = normalize_label(label, label_map)

        predictions.append({
            "label": label,
            "confidence": round(score, 4)
        })

    return predictions


# =================================================
# MAIN CLOTHING ANALYSIS FUNCTION
# =================================================

def analyze_clothing(image_path):

    # Load and preprocess image
    image = preprocess(
        Image.open(image_path).convert("RGB")
    ).unsqueeze(0)

    # -------------------------
    # CATEGORY (already clean, no map needed)
    # -------------------------

    category_labels = [
        "t-shirt",
        "shirt",
        "blouse",

        "dress",
        "frock",

        "jeans",
        "trousers",
        "skirt",
        "shorts",

        "jacket",
        "coat",
        "hoodie",
        "sweater",
        "blazer",

        "kurta",
        "kurti",
        "saree",

        "shoes",
        "sneakers",
        "sandals",

        "bag",
        "hat"
    ]

    category = get_top_prediction(
        image,
        category_labels
    )

    # -------------------------
    # COLOR
    # -------------------------

    color_labels = [
        "white clothing",
        "black clothing",
        "gray clothing",
        "red clothing",
        "blue clothing",
        "green clothing",
        "yellow clothing",
        "orange clothing",
        "pink clothing",
        "purple clothing",
        "brown clothing",
        "beige clothing",
        "cream clothing"
    ]

    color = get_top_prediction(
        image,
        color_labels,
        label_map=COLOR_LABEL_MAP
    )

    # -------------------------
    # PATTERN
    # -------------------------

    pattern_labels = [
        "plain clothing",
        "striped clothing",
        "checked clothing",
        "floral clothing",
        "printed clothing",
        "polka dot clothing",
        "patterned clothing"
    ]

    pattern = get_top_prediction(
        image,
        pattern_labels,
        label_map=PATTERN_LABEL_MAP
    )

    # -------------------------
    # STYLE
    # -------------------------

    style_labels = [
        "casual clothing",
        "formal clothing",
        "smart casual clothing",
        "sporty clothing",
        "minimal clothing",
        "elegant clothing",
        "streetwear clothing",
        "classic clothing",
        "trendy clothing"
    ]

    styles = get_top_predictions(
        image,
        style_labels,
        top_n=3,
        label_map=STYLE_LABEL_MAP
    )

    # -------------------------
    # FIT
    # -------------------------

    fit_labels = [
        "relaxed fit clothing",
        "regular fit clothing",
        "oversized clothing",
        "fitted clothing",
        "slim fit clothing"
    ]

    fit = get_top_prediction(
        image,
        fit_labels,
        label_map=FIT_LABEL_MAP
    )

    # -------------------------
    # OCCASION
    # -------------------------

    occasion_labels = [
        "casual everyday clothing",
        "college outfit",
        "office wear",
        "party outfit",
        "date night outfit",
        "wedding guest outfit",
        "traditional wedding outfit",
        "beach vacation outfit",
        "summer casual outfit",
        "formal event outfit"
    ]

    occasions = get_top_predictions(
        image,
        occasion_labels,
        top_n=3,
        label_map=OCCASION_LABEL_MAP
    )

    # -------------------------
    # SEASON
    # -------------------------

    season_labels = [
        "summer clothing",
        "winter clothing",
        "spring clothing",
        "autumn clothing",
        "all season clothing"
    ]

    season = get_top_prediction(
        image,
        season_labels,
        label_map=SEASON_LABEL_MAP
    )

    embedding = generate_embedding(image_path)

    # -------------------------
    # RETURN FINAL RESULT
    # -------------------------

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