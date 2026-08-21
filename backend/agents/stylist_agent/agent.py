from schemas.outfit_schema import StylistInput


def generate_outfit_combinations(wardrobe):

    # Keep only items that are currently available
    available_items = [
        item for item in wardrobe
        if item.available
    ]

    # Separate wardrobe items by category
    tops = [
        item for item in available_items
        if item.category == "top"
    ]

    bottoms = [
        item for item in available_items
        if item.category == "bottom"
    ]

    shoes = [
        item for item in available_items
        if item.category == "shoes"
    ]

    print(f"\nAvailable tops: {len(tops)}")
    print(f"Available bottoms: {len(bottoms)}")
    print(f"Available shoes: {len(shoes)}")

    combinations = []

    # Create every possible:
    # top + bottom + shoes combination
    for top in tops:
        for bottom in bottoms:
            for shoe in shoes:

                outfit = {
                    "top": {
                        "id": top.id,
                        "name": top.name
                    },
                    "bottom": {
                        "id": bottom.id,
                        "name": bottom.name
                    },
                    "shoes": {
                        "id": shoe.id,
                        "name": shoe.name
                    }
                }

                combinations.append(outfit)

    return combinations


def run_stylist_agent(data: StylistInput):

    print("\n--- STYLIST AGENT STARTED ---")
    print(f"Occasion received: {data.occasion}")

    combinations = generate_outfit_combinations(
        data.wardrobe
    )

    print(
        f"\nTotal valid outfit combinations: "
        f"{len(combinations)}"
    )

    return {
        "status": "success",
        "occasion": data.occasion,
        "total_combinations": len(combinations),
        "outfits": combinations
    }