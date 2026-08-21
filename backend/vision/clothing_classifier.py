from pathlib import Path
from PIL import Image
from transformers import pipeline


# Create the classifier
classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)


def classify_clothing(image_path):
    image = Image.open(image_path).convert("RGB")

    results = classifier(image)

    return results


if __name__ == "__main__":

    # Get the backend folder
    backend_folder = Path(__file__).resolve().parent.parent

    # Build the correct path to uploads/test.jpg
    image_path = backend_folder / "uploads" / "test.jpg"

    print("Looking for image at:")
    print(image_path)

    print("Image exists:", image_path.exists())

    results = classify_clothing(image_path)

    print("\nPredictions:")

    for result in results[:5]:
        print(
            f"{result['label']}: {result['score']:.4f}"
        )