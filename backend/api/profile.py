from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from database.connection import SessionLocal

from agents.profile_agent.agent import (
    create_user_profile,
    create_user_preferences,
    get_user_profile,
    update_user_preferences,
    save_current_preferences,
    get_current_preferences,
    get_preference_context
)

from schemas.profile import (
    UserProfileCreate,
    UserPreferenceCreate,
    UserPreferenceUpdate
)

router = APIRouter(
    prefix="/api/profile",
    tags=["Profile Agent"]
)

@router.post("/")
def create_profile(
    profile_data: UserProfileCreate
):
    db: Session = SessionLocal()

    try:
        profile = create_user_profile(
            db,
            profile_data.user_id,
            profile_data.gender,
            profile_data.birth_year
        )

        return {
            "success": True,
            "message": "User profile created successfully.",
            "profile": {
                "user_id": profile.user_id,
                "gender": profile.gender,
                "birth_year": profile.birth_year,
                "generation": profile.generation
            }
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": "Failed to create user profile.",
            "error": str(e)
        }

    finally:
        db.close()

@router.post("/preferences")
def create_preferences(
    preference_data: UserPreferenceCreate
):
    db: Session = SessionLocal()

    try:
        preferences = create_user_preferences(
            db,
            preference_data.user_id,
            preference_data.styles,
            preference_data.colors,
            preference_data.fits,
            preference_data.occasions,
            preference_data.comfort_weight
        )

        return {
            "success": True,
            "message": "User preferences created successfully.",
            "preferences": {
                "user_id": preferences.user_id,
                "styles": preferences.styles,
                "colors": preferences.colors,
                "fits": preferences.fits,
                "occasions": preferences.occasions,
                "comfort_weight": preferences.comfort_weight
            }
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": "Failed to create user preferences.",
            "error": str(e)
        }

    finally:
        db.close()


@router.get("/{user_id}")
def get_complete_profile(user_id: str):

    db: Session = SessionLocal()

    try:
        profile_data = get_user_profile(
            db,
            user_id
        )

        if not profile_data:
            return {
                "success": False,
                "message": "User profile not found."
            }

        return {
            "success": True,
            "profile": profile_data
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to retrieve user profile.",
            "error": str(e)
        }

    finally:
        db.close()

@router.put("/preferences/{user_id}")
def update_preferences(
    user_id: str,
    preference_data: UserPreferenceUpdate
):
    db: Session = SessionLocal()

    try:
        preferences = update_user_preferences(
            db,
            user_id,
            styles=preference_data.styles,
            colors=preference_data.colors,
            fits=preference_data.fits,
            occasions=preference_data.occasions,
            comfort_weight=preference_data.comfort_weight
        )

        if not preferences:
            return {
                "success": False,
                "message": "User preferences not found."
            }

        return {
            "success": True,
            "message": "User preferences updated successfully.",
            "preferences": {
                "user_id": preferences.user_id,
                "styles": preferences.styles,
                "colors": preferences.colors,
                "fits": preferences.fits,
                "occasions": preferences.occasions,
                "comfort_weight": preferences.comfort_weight
            }
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": "Failed to update user preferences.",
            "error": str(e)
        }

    finally:
        db.close()


@router.post("/current-preferences/{user_id}")
def save_user_current_preferences(
    user_id: str,
    styles: list[str],
    colors: list[str],
    fits: list[str],
    occasions: list[str],
    comfort_weight: int
):
    db: Session = SessionLocal()

    try:
        preferences = save_current_preferences(
            db=db,
            user_id=user_id,
            styles=styles,
            colors=colors,
            fits=fits,
            occasions=occasions,
            comfort_weight=comfort_weight
        )

        return {
            "success": True,
            "message": "Current preferences saved successfully.",
            "preferences": {
                "user_id": preferences.user_id,
                "styles": preferences.styles,
                "colors": preferences.colors,
                "fits": preferences.fits,
                "occasions": preferences.occasions,
                "comfort_weight": preferences.comfort_weight
            }
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": "Failed to save current preferences.",
            "error": str(e)
        }

    finally:
        db.close()


@router.get("/current-preferences/{user_id}")
def get_user_current_preferences(user_id: str):

    db: Session = SessionLocal()

    try:
        preferences = get_current_preferences(
            db=db,
            user_id=user_id
        )

        if not preferences:
            return {
                "success": False,
                "message": "Current preferences not found."
            }

        return {
            "success": True,
            "preferences": {
                "user_id": preferences.user_id,
                "styles": preferences.styles,
                "colors": preferences.colors,
                "fits": preferences.fits,
                "occasions": preferences.occasions,
                "comfort_weight": preferences.comfort_weight
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to retrieve current preferences.",
            "error": str(e)
        }

    finally:
        db.close()


@router.get("/preference-context/{user_id}")
def get_user_preference_context(user_id: str):

    db: Session = SessionLocal()

    try:
        context = get_preference_context(
            db=db,
            user_id=user_id
        )

        return {
            "success": True,
            "context": context
        }

    except Exception as e:

        return {
            "success": False,
            "message": "Failed to retrieve preference context.",
            "error": str(e)
        }

    finally:
        db.close()
