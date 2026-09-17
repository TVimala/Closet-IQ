import open_clip
import torch
from PIL import Image


# Load FashionCLIP
model, _, preprocess = open_clip.create_model_and_transforms(
    "hf-hub:Marqo/marqo-fashionCLIP"
)

tokenizer = open_clip.get_tokenizer(
    "hf-hub:Marqo/marqo-fashionCLIP"
)


# Load image
image_path = "uploads/test.jpg"

image = preprocess(
    Image.open(image_path).convert("RGB")
).unsqueeze(0)


def predict(labels, title):
    text = tokenizer(labels)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (
            100.0 * image_features @ text_features.T
        ).softmax(dim=-1)

    results = list(zip(labels, similarity[0].tolist()))
    results.sort(key=lambda x: x[1], reverse=True)

    print(f"\n{title}:\n")

    for label, score in results[:5]:
        print(f"{label}: {score:.4f}")


# -------------------------
# CATEGORY DETECTION
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
    "hat"
]

predict(category_labels, "CATEGORY PREDICTIONS")


# -------------------------
# COLOR DETECTION
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

predict(color_labels, "COLOR PREDICTIONS")

# -------------------------
# PATTERN DETECTION
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

predict(pattern_labels, "PATTERN PREDICTIONS")

# -------------------------
# STYLE DETECTION
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

predict(style_labels, "STYLE PREDICTIONS")

# -------------------------
# FIT DETECTION
# -------------------------

fit_labels = [
    "relaxed fit clothing",
    "regular fit clothing",
    "oversized clothing",
    "fitted clothing",
    "slim fit clothing"
]

predict(fit_labels, "FIT PREDICTIONS")

# -------------------------
# OCCASION DETECTION
# -------------------------

occasion_labels = [
    "college clothing",
    "office clothing",
    "casual outing clothing",
    "party clothing",
    "date clothing",
    "wedding clothing",
    "travel clothing",
    "daily wear clothing",
    "formal event clothing"
]

predict(occasion_labels, "OCCASION PREDICTIONS")

# -------------------------
# SEASON DETECTION
# -------------------------

season_labels = [
    "summer clothing",
    "winter clothing",
    "spring clothing",
    "autumn clothing",
    "all season clothing"
]

predict(season_labels, "SEASON PREDICTIONS")