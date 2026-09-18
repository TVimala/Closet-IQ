"""
One-off backfill script.

This project has never had this script run against it yet (there
was no backfill_wardrobe_labels.py file anywhere in the zip) - that's
why items 54-60 still have old verbose labels like "college outfit"
even though newly uploaded items are clean.

Run this ONCE. New uploads already get normalized labels at
analysis time (vision/clothing_analyzer.py) - this script only
repairs existing rows that were saved before that fix existed.

Usage (from the backend/ folder, same place you run uvicorn from):
    python backfill_wardrobe_labels.py
"""

from database.connection import SessionLocal
from database.models import WardrobeItem

from vision.clothing_analyzer import (
    COLOR_LABEL_MAP,
    PATTERN_LABEL_MAP,
    STYLE_LABEL_MAP,
    FIT_LABEL_MAP,
    OCCASION_LABEL_MAP,
    SEASON_LABEL_MAP,
    normalize_label,
)


def normalize_list(values, label_map):
    if not values:
        return values
    return [normalize_label(v, label_map) for v in values]


def backfill():
    db = SessionLocal()

    updated_count = 0
    skipped_count = 0

    try:
        items = db.query(WardrobeItem).all()

        print(f"Found {len(items)} wardrobe_items row(s) total.\n")

        for item in items:

            original = {
                "color": item.color,
                "pattern": item.pattern,
                "fit": item.fit,
                "styles": list(item.styles) if item.styles else item.styles,
                "occasions": list(item.occasions) if item.occasions else item.occasions,
                "seasons": list(item.seasons) if item.seasons else item.seasons,
            }

            if item.color:
                item.color = normalize_label(item.color, COLOR_LABEL_MAP)

            if item.pattern:
                item.pattern = normalize_label(item.pattern, PATTERN_LABEL_MAP)

            if item.fit:
                item.fit = normalize_label(item.fit, FIT_LABEL_MAP)

            if item.styles:
                item.styles = normalize_list(item.styles, STYLE_LABEL_MAP)

            if item.occasions:
                item.occasions = normalize_list(item.occasions, OCCASION_LABEL_MAP)

            if item.seasons:
                item.seasons = normalize_list(item.seasons, SEASON_LABEL_MAP)

            changed = (
                item.color != original["color"]
                or item.pattern != original["pattern"]
                or item.fit != original["fit"]
                or item.styles != original["styles"]
                or item.occasions != original["occasions"]
                or item.seasons != original["seasons"]
            )

            if changed:
                updated_count += 1
                print(f"[updated] item {item.id} ({item.category}): "
                      f"{original} -> "
                      f"{{'color': {item.color!r}, 'pattern': {item.pattern!r}, "
                      f"'fit': {item.fit!r}, 'styles': {item.styles}, "
                      f"'occasions': {item.occasions}, 'seasons': {item.seasons}}}")
            else:
                skipped_count += 1

        db.commit()

        print(f"\nDone. Updated {updated_count} item(s), "
              f"{skipped_count} already clean or empty.")

    except Exception as e:
        db.rollback()
        print(f"Backfill failed, rolled back: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    backfill()