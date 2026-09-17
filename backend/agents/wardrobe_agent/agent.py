from database.connection import SessionLocal
from database.models import WardrobeItem

from sqlalchemy import text


def get_wardrobe(user_id):

    db = SessionLocal()

    try:

        items = db.query(WardrobeItem).filter(
            WardrobeItem.user_id == user_id,
            WardrobeItem.is_available == True
        ).all()

        wardrobe = []

        for item in items:

            wardrobe.append({
                "id": item.id,
                "user_id": item.user_id,
                "image_url": item.image_url,
                "category": item.category,
                "color": item.color,
                "pattern": item.pattern,
                "fit": item.fit,
                "styles": item.styles,
                "occasions": item.occasions,
                "seasons": item.seasons
            })

        return wardrobe

    finally:
        db.close()

def search_wardrobe(
    user_id,
    category=None,
    color=None,
    style=None,
    occasion=None,
    season=None
):
    db = SessionLocal()

    try:
        query = db.query(WardrobeItem).filter(
            WardrobeItem.user_id == user_id,
            WardrobeItem.is_available == True
        )

        if category:
            query = query.filter(
                WardrobeItem.category.ilike(f"%{category}%")
            )

        if color:
            query = query.filter(
                WardrobeItem.color.ilike(f"%{color}%")
            )

        if style:
            query = query.filter(
                WardrobeItem.styles.any(style)
            )

        if occasion:
            query = query.filter(
                WardrobeItem.occasions.any(occasion)
            )

        if season:
            query = query.filter(
                WardrobeItem.seasons.any(season)
            )

        items = query.all()

        results = []

        for item in items:
            results.append({
                "id": item.id,
                "user_id": item.user_id,
                "image_url": item.image_url,
                "category": item.category,
                "color": item.color,
                "pattern": item.pattern,
                "fit": item.fit,
                "styles": item.styles,
                "occasions": item.occasions,
                "seasons": item.seasons
            })

        return results

    finally:
        db.close()

def update_wardrobe_item(
    item_id,
    user_id,
    category=None,
    color=None,
    pattern=None,
    fit=None,
    styles=None,
    occasions=None,
    seasons=None,
    brand=None,
    condition=None,
    is_available=None
):
    db = SessionLocal()

    try:
        # Find the item and make sure it belongs to this user
        item = db.query(WardrobeItem).filter(
            WardrobeItem.id == item_id,
            WardrobeItem.user_id == user_id
        ).first()

        # Item not found
        if not item:
            return None

        # Update only the values that were provided
        if category is not None:
            item.category = category

        if color is not None:
            item.color = color

        if pattern is not None:
            item.pattern = pattern

        if fit is not None:
            item.fit = fit

        if styles is not None:
            item.styles = styles

        if occasions is not None:
            item.occasions = occasions

        if seasons is not None:
            item.seasons = seasons

        if brand is not None:
            item.brand = brand

        if condition is not None:
            item.condition = condition

        if is_available is not None:
            item.is_available = is_available

        # Save changes
        db.commit()

        # Refresh updated data
        db.refresh(item)

        return {
            "id": item.id,
            "user_id": item.user_id,
            "image_url": item.image_url,
            "category": item.category,
            "color": item.color,
            "pattern": item.pattern,
            "fit": item.fit,
            "styles": item.styles,
            "occasions": item.occasions,
            "seasons": item.seasons,
            # "brand": item.brand,
            "condition": item.condition,
            "is_available": item.is_available
        }

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

def remove_wardrobe_item(item_id, user_id):
    db = SessionLocal()

    try:
        # Find the item and verify it belongs to the user
        item = db.query(WardrobeItem).filter(
            WardrobeItem.id == item_id,
            WardrobeItem.user_id == user_id
        ).first()

        # Item not found
        if not item:
            return None

        # Soft delete
        item.is_available = False

        db.commit()
        db.refresh(item)

        return {
            "id": item.id,
            "user_id": item.user_id,
            "is_available": item.is_available,
            "message": "Wardrobe item removed successfully"
        }

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

from datetime import datetime


def mark_item_as_worn(item_id, user_id):

    db = SessionLocal()

    try:
        # Find the item and verify it belongs to the user
        item = db.query(WardrobeItem).filter(
            WardrobeItem.id == item_id,
            WardrobeItem.user_id == user_id,
            WardrobeItem.is_available == True
        ).first()

        # Item not found
        if not item:
            return None

        # Increment usage count
        item.usage_count += 1

        # Update last worn time
        item.last_worn_at = datetime.now()

        # Save changes
        db.commit()

        # Refresh updated item
        db.refresh(item)

        return {
            "id": item.id,
            "user_id": item.user_id,
            "usage_count": item.usage_count,
            "last_worn_at": item.last_worn_at,
            "message": "Item marked as worn successfully"
        }

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()

def find_similar_items(
    item_id,
    user_id,
    limit=5
):
    db = SessionLocal()

    try:

        # Get the selected wardrobe item
        target_item = db.query(WardrobeItem).filter(
            WardrobeItem.id == item_id,
            WardrobeItem.user_id == user_id,
            WardrobeItem.is_available == True
        ).first()

        # Item not found
        if not target_item:
            return None

        # Embedding not available
        if target_item.embedding is None:
            return {
                "error": "Embedding not available for this item."
            }

        # Find similar items using cosine distance
        results = db.execute(
            text("""
                SELECT
                    id,
                    user_id,
                    image_url,
                    category,
                    color,
                    pattern,
                    fit,
                    styles,
                    occasions,
                    seasons,

                    1 - (embedding <=> :embedding) AS similarity

                FROM wardrobe_items

                WHERE
                    user_id = :user_id
                    AND is_available = TRUE
                    AND id != :item_id
                    AND embedding IS NOT NULL

                ORDER BY embedding <=> :embedding

                LIMIT :limit
            """),
            {
                "embedding": str(target_item.embedding),
                "user_id": user_id,
                "item_id": item_id,
                "limit": limit
            }
        )

        similar_items = []

        for row in results.mappings():

            similar_items.append({
                "id": row["id"],
                "user_id": row["user_id"],
                "image_url": row["image_url"],
                "category": row["category"],
                "color": row["color"],
                "pattern": row["pattern"],
                "fit": row["fit"],
                "styles": row["styles"],
                "occasions": row["occasions"],
                "seasons": row["seasons"],
                "similarity": float(row["similarity"])
            })

        return {
            "target_item_id": item_id,
            "similar_items": similar_items
        }

    finally:
        db.close()