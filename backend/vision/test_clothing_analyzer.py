from vision.clothing_analyzer import analyze_clothing


image_path = "uploads/test.jpg"

result = analyze_clothing(image_path)

print("\nFINAL CLOTHING ANALYSIS:\n")

for key, value in result.items():
    print(f"{key}: {value}")