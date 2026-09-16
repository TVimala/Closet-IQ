from services.wardrobe_intelligence import (
    analyze_wardrobe,
    generate_dynamic_outfits
)
from services.outfit_service import MOCK_WARDROBE

def main():

    result = analyze_wardrobe(MOCK_WARDROBE)

    print("\n========== WARDROBE INTELLIGENCE ==========")

    print("\nAvailable Groups:")
    print(result["available_groups"])

    print("\nAvailable Categories:")
    print(result["available_categories"])

    print("\nAvailable Styles:")
    print(result["available_styles"])

    print("\nAvailable Seasons:")
    print(result["available_seasons"])

    print("\nAvailable Occasions:")
    print(result["available_occasions"])

    print("\nTotal Available Items:")
    print(result["total_available_items"])

    print("\nGrouped Items:")

    for group, items in result["grouped_items"].items():

        print(f"\n{group.upper()}")

        for item in items:
            print(f" - {item['id']} : {item['category']}")
    print("\n\n==========================================")
    print("DYNAMIC OUTFIT GENERATION")
    print("==========================================")

    outfits = generate_dynamic_outfits(
        result
    )

    print(
        f"\nTotal Dynamic Outfits Generated: "
        f"{len(outfits)}"
    )

    print("\nFIRST 10 GENERATED OUTFITS:")

    for index, outfit in enumerate(
        outfits[:10],
        start=1
    ):

        print(
            f"\nOutfit #{index}"
        )

        print(
            f"Type: {outfit['outfit_type']}"
        )

        print("Items:")

        for item in outfit["items"]:

            print(
                f" - {item['id']} : "
                f"{item['category']} "
                f"({item.get('color', 'unknown')})"
            )
    


if __name__ == "__main__":
    main()