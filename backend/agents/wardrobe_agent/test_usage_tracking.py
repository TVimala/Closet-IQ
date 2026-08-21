from agents.wardrobe_agent.wardrobe_service import mark_item_as_worn


result = mark_item_as_worn(
    item_id=3,
    user_id="U101"
)

print("\nUSAGE TRACKING RESULT:\n")
print(result)