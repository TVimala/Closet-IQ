from agents.wardrobe_agent.wardrobe_service import (
    get_wardrobe,
    search_wardrobe,
    update_wardrobe_item,
    remove_wardrobe_item
)


# Get complete wardrobe
print("\nUSER WARDROBE:\n")

wardrobe = get_wardrobe("U101")

for item in wardrobe:
    print(item)


# Search for t-shirts
print("\nSEARCH: T-SHIRTS\n")

results = search_wardrobe(
    user_id="U101",
    category="t-shirt"
)

for item in results:
    print(item)

# Search by color
print("\nSEARCH: BLACK CLOTHES\n")

results = search_wardrobe(
    user_id="U101",
    color="black"
)

for item in results:
    print(item)


# Search using multiple filters
print("\nSEARCH: BLACK T-SHIRTS\n")

results = search_wardrobe(
    user_id="U101",
    category="t-shirt",
    color="black"
)

for item in results:
    print(item)

print("\nUPDATE WARDROBE ITEM\n")

updated_item = update_wardrobe_item(
    item_id=3,
    user_id="U101",
    style="casual clothing"
)

print(updated_item)

print("\nREMOVE WARDROBE ITEM\n")

removed_item = remove_wardrobe_item(
    item_id=3,
    user_id="U101"
)

print(removed_item)

print("\nRESTORE WARDROBE ITEM\n")

restored_item = update_wardrobe_item(
    item_id=3,
    user_id="U101",
    is_available=True
)

print(restored_item)