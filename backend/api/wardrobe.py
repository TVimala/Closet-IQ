from fastapi import APIRouter, File, UploadFile
from sqlalchemy.orm import Session

import os
import shutil
import uuid

from database.connection import SessionLocal
from database.models import WardrobeItem

from vision.clothing_analyzer import analyze_clothing

from agents.wardrobe_agent.agent import (
    find_similar_items,
    get_wardrobe,
    search_wardrobe,
    update_wardrobe_item,
    remove_wardrobe_item
)


router = APIRouter(
    prefix="/api/wardrobe",
    tags=["Wardrobe Agent"]
)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_clothing(
    file: UploadFile = File(...),
    user_id: str = "U101"
):
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        analysis = analyze_clothing(file_path)

    except Exception as e:
        return {
            "success": False,
            "message": "Clothing analysis failed.",
            "error": str(e)
        }

    db: Session = SessionLocal()

    try:
        top_style = analysis["styles"][0]["label"]
        top_occasion = analysis["occasions"][0]["label"]

        wardrobe_item = WardrobeItem(
            user_id=user_id,
            image_url=file_path,

            embedding=analysis["embedding"],

            category=analysis["category"]["label"],
            color=analysis["color"]["label"],
            pattern=analysis["pattern"]["label"],
            fit=analysis["fit"]["label"],
            style=top_style,
            season=analysis["season"]["label"],
            occasion=top_occasion,

            is_available=True
        )

        db.add(wardrobe_item)
        db.commit()
        db.refresh(wardrobe_item)

        return {
            "success": True,
            "message": "Clothing analyzed and saved successfully!",

            "item_id": wardrobe_item.id,
            "user_id": wardrobe_item.user_id,

            "analysis": {
                "category": wardrobe_item.category,
                "color": wardrobe_item.color,
                "pattern": wardrobe_item.pattern,
                "fit": wardrobe_item.fit,
                "style": wardrobe_item.style,
                "occasion": wardrobe_item.occasion,
                "season": wardrobe_item.season
            }
        }

    except Exception as e:

        db.rollback()

        return {
            "success": False,
            "message": "Failed to save wardrobe item.",
            "error": str(e)
        }

    finally:
        db.close()


@router.get("/search")
def search_user_wardrobe(
    user_id: str,
    category: str = None,
    color: str = None,
    style: str = None,
    occasion: str = None,
    season: str = None
):

    results = search_wardrobe(
        user_id=user_id,
        category=category,
        color=color,
        style=style,
        occasion=occasion,
        season=season
    )

    return {
        "success": True,
        "user_id": user_id,
        "count": len(results),
        "items": results
    }


@router.get("/{user_id}")
def get_user_wardrobe(user_id: str):

    wardrobe = get_wardrobe(user_id)

    return {
        "success": True,
        "user_id": user_id,
        "count": len(wardrobe),
        "items": wardrobe
    }


@router.put("/{item_id}")
def update_wardrobe(
    item_id: int,
    user_id: str,
    category: str = None,
    color: str = None,
    pattern: str = None,
    fit: str = None,
    style: str = None,
    occasion: str = None,
    season: str = None,
    # brand: str = None,
    condition: str = None,
    is_available: bool = None
):

    updated_item = update_wardrobe_item(
        item_id=item_id,
        user_id=user_id,
        category=category,
        color=color,
        pattern=pattern,
        fit=fit,
        style=style,
        occasion=occasion,
        season=season,
        # brand=brand,
        condition=condition,
        is_available=is_available
    )

    if not updated_item:
        return {
            "success": False,
            "message": "Wardrobe item not found."
        }

    return {
        "success": True,
        "message": "Wardrobe item updated successfully!",
        "item": updated_item
    }


@router.delete("/{item_id}")
def remove_wardrobe(
    item_id: int,
    user_id: str
):

    removed_item = remove_wardrobe_item(
        item_id=item_id,
        user_id=user_id
    )

    if not removed_item:
        return {
            "success": False,
            "message": "Wardrobe item not found."
        }

    return {
        "success": True,
        "message": "Wardrobe item removed successfully!",
        "item": removed_item
    }


@router.get("/{item_id}/similar")
def get_similar_items(
    item_id: int,
    user_id: str = "U101",
    limit: int = 5
):
    result = find_similar_items(
        item_id=item_id,
        user_id=user_id,
        limit=limit
    )

    if result is None:
        return {
            "success": False,
            "message": "Wardrobe item not found."
        }

    if "error" in result:
        return {
            "success": False,
            "message": result["error"]
        }

    return {
        "success": True,
        "target_item_id": result["target_item_id"],
        "similar_items": result["similar_items"]
    }