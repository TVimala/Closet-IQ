from database.models import UserProfile, UserPreference, UserCurrentPreference

def calculate_generation(birth_year: int):
    if 1883 <= birth_year <= 1900:
        return "Lost Generation"
    elif 1901 <= birth_year <= 1927:
        return "Greatest Generation"
    elif 1928 <= birth_year <= 1945:
        return "Silent Generation"
    elif 1946 <= birth_year <= 1964:
        return "Baby Boomer"
    elif 1965 <= birth_year <= 1980:
        return "Gen X"
    elif 1981 <= birth_year <= 1996:
        return "Millennial"
    elif 1997 <= birth_year <= 2012:
        return "Gen Z"
    elif 2013 <= birth_year <= 2024:
        return "Gen Alpha"
    else:
        return "Gen Beta"

def create_user_profile(db, user_id, gender, birth_year):

    generation = calculate_generation(birth_year)

    profile = UserProfile(
        user_id=user_id,
        gender=gender,
        birth_year=birth_year,
        generation=generation
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

def create_user_preferences(
    db,
    user_id,
    styles,
    colors,
    fits,
    occasions,
    comfort_weight
):

    preferences = UserPreference(
        user_id=user_id,
        styles=styles,
        colors=colors,
        fits=fits,
        occasions=occasions,
        comfort_weight=comfort_weight
    )

    db.add(preferences)
    db.commit()
    db.refresh(preferences)

    return preferences

def get_user_profile(db, user_id):

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user_id)
        .first()
    )

    preferences = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )

    return {
        "user_id": user_id,
        "gender": profile.gender if profile else None,
        "birth_year": profile.birth_year if profile else None,
        "generation": profile.generation if profile else None,

        "styles": preferences.styles if preferences else [],
        "colors": preferences.colors if preferences else [],
        "fits": preferences.fits if preferences else [],
        "occasions": preferences.occasions if preferences else [],
        "comfort_weight": (
            preferences.comfort_weight
            if preferences else None
        )
    }

def update_user_preferences(
    db,
    user_id,
    styles=None,
    colors=None,
    fits=None,
    occasions=None,
    comfort_weight=None
):

    preferences = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )

    if not preferences:
        return None

    if styles is not None:
        preferences.styles = styles

    if colors is not None:
        preferences.colors = colors

    if fits is not None:
        preferences.fits = fits

    if occasions is not None:
        preferences.occasions = occasions

    if comfort_weight is not None:
        preferences.comfort_weight = comfort_weight

    db.commit()
    db.refresh(preferences)

    return preferences

def save_current_preferences(
    db,
    user_id,
    styles,
    colors,
    fits,
    occasions,
    comfort_weight
):
    current_preferences = (
        db.query(UserCurrentPreference)
        .filter(
            UserCurrentPreference.user_id == user_id
        )
        .first()
    )

    # If current preferences already exist, update them
    if current_preferences:

        current_preferences.styles = styles
        current_preferences.colors = colors
        current_preferences.fits = fits
        current_preferences.occasions = occasions
        current_preferences.comfort_weight = comfort_weight

    # Otherwise create new current preferences
    else:

        current_preferences = UserCurrentPreference(
            user_id=user_id,
            styles=styles,
            colors=colors,
            fits=fits,
            occasions=occasions,
            comfort_weight=comfort_weight
        )

        db.add(current_preferences)

    db.commit()
    db.refresh(current_preferences)

    return current_preferences

def get_current_preferences(
    db,
    user_id
):
    current_preferences = (
        db.query(UserCurrentPreference)
        .filter(
            UserCurrentPreference.user_id == user_id
        )
        .first()
    )

    return current_preferences


def get_preference_context(db, user_id):

    # Get basic user profile
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user_id)
        .first()
    )

    # Get permanent preferences
    permanent_preferences = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user_id)
        .first()
    )

    # Get current preferences
    current_preferences = (
        db.query(UserCurrentPreference)
        .filter(UserCurrentPreference.user_id == user_id)
        .first()
    )

    return {
        "user_id": user_id,

        "profile": {
            "gender": profile.gender if profile else None,
            "birth_year": profile.birth_year if profile else None,
            "generation": profile.generation if profile else None
        },

        "permanent_preferences": {
            "styles": permanent_preferences.styles if permanent_preferences else [],
            "colors": permanent_preferences.colors if permanent_preferences else [],
            "fits": permanent_preferences.fits if permanent_preferences else [],
            "occasions": permanent_preferences.occasions if permanent_preferences else [],
            "comfort_weight": (
                permanent_preferences.comfort_weight
                if permanent_preferences else None
            )
        },

        "current_preferences": {
            "styles": current_preferences.styles if current_preferences else [],
            "colors": current_preferences.colors if current_preferences else [],
            "fits": current_preferences.fits if current_preferences else [],
            "occasions": current_preferences.occasions if current_preferences else [],
            "comfort_weight": (
                current_preferences.comfort_weight
                if current_preferences else None
            )
        }
    }