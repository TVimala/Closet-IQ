from agents.wardrobe_agent.wardrobe_service import find_similar_items


result = find_similar_items(
    item_id=8,
    user_id="U102"
)

print("\nSIMILARITY SEARCH RESULT:\n")
print(result)