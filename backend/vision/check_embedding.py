import open_clip
import torch
from PIL import Image


model, _, preprocess = open_clip.create_model_and_transforms(
    "hf-hub:Marqo/marqo-fashionCLIP"
)

image = preprocess(
    Image.open("uploads/test.jpg").convert("RGB")
).unsqueeze(0)


with torch.no_grad():
    image_features = model.encode_image(image)

print("Embedding shape:", image_features.shape)
print("Embedding dimension:", image_features.shape[-1])