from schemas.outfit_schema import StylistInput


def run_stylist_agent(data: StylistInput):

    print("\n--- STYLIST AGENT STARTED ---")

    print(f"Occasion received: {data.occasion}")

    print("\nWardrobe received:")

    for item in data.wardrobe:
        print(
            f"- {item.name} "
            f"| Category: {item.category} "
            f"| Available: {item.available}"
        )

    return {
        "status": "success",
        "message": "Stylist Agent successfully received wardrobe and occasion.",
        "occasion": data.occasion,
        "total_wardrobe_items": len(data.wardrobe)
    }