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

def get_top_prediction(image, labels):

    results = get_predictions(
        image,
        labels
    )

    label, score = results[0]

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
    top_n=3
):

    results = get_predictions(
        image,
        labels
    )

    predictions = []

    for label, score in results[:top_n]:

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
    # CATEGORY
    # -------------------------

    category_labels = [
        "t-shirt",
        "shirt",
        "blouse",
        "dress",
        "jeans",
        "trousers",
        "skirt",
        "shorts",
        "jacket",
        "coat",
        "hoodie",
        "sweater",
        "kurta",
        "saree",
        "shoes",
        "sneakers",
        "sandals",
        "bag",
        "hat",
        "frock",
        "blazer"
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
        color_labels
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
        pattern_labels
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
        top_n=3
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
        fit_labels
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
        top_n=3
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
        season_labels
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