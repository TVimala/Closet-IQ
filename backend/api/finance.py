from fastapi import APIRouter, HTTPException, File, UploadFile, Form

import os
import shutil
import uuid

from vision.clothing_analyzer import analyze_clothing

from agents.finance_agent.agent import (
    analyze_purchase, 
    record_purchase
)

from schemas.finance import (
    FinancialProfileCreate,
    FinancialProfileUpdate,
    BudgetCreate,
    BudgetUpdate, 
    PurchaseCreate,
    PurchaseAnalysisRequest
)

from agents.finance_agent.agent import (
    set_financial_profile,
    get_financial_profile,
    set_budget,
    get_budget,
    record_purchase,
    get_purchase_history,
    get_monthly_spending_analysis,
    analyze_purchase
)

from database.models import (
    FinancialProfile,
    Budget,
    PurchaseHistory,
    PendingPurchase,
    WardrobeItem
)

from database.connection import SessionLocal


router = APIRouter(
    prefix="/api/finance",
    tags=["Finance Agent"]
)


UPLOAD_FOLDER = "uploads/purchase_analysis"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ============================================================
# SET / UPDATE FINANCIAL PROFILE
# ============================================================

@router.post("/profile")
def create_financial_profile(data: FinancialProfileCreate):

    result = set_financial_profile(
        user_id=data.user_id,
        monthly_salary=data.monthly_salary,
        currency=data.currency
    )

    return result


# ============================================================
# GET FINANCIAL PROFILE
# ============================================================

@router.get("/profile/{user_id}")
def fetch_financial_profile(user_id: str):

    profile = get_financial_profile(user_id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Financial profile not found"
        )

    return profile


# ============================================================
# UPDATE FINANCIAL PROFILE
# ============================================================

@router.put("/profile/{user_id}")
def update_financial_profile(
    user_id: str,
    data: FinancialProfileUpdate
):

    existing_profile = get_financial_profile(user_id)

    if not existing_profile:
        raise HTTPException(
            status_code=404,
            detail="Financial profile not found"
        )

    # Keep old values if user doesn't provide new ones
    monthly_salary = (
        data.monthly_salary
        if data.monthly_salary is not None
        else existing_profile["monthly_salary"]
    )

    currency = (
        data.currency
        if data.currency is not None
        else existing_profile["currency"]
    )

    result = set_financial_profile(
        user_id=user_id,
        monthly_salary=monthly_salary,
        currency=currency
    )

    return result


# ============================================================
# SET / UPDATE BUDGET
# ============================================================

@router.post("/budget")
def create_budget(data: BudgetCreate):

    result = set_budget(
        user_id=data.user_id,
        category=data.category,
        monthly_limit=data.monthly_limit,
        month=data.month,
        year=data.year
    )

    return result


# ============================================================
# GET BUDGET
# ============================================================

@router.get("/budget/{user_id}")
def fetch_budget(
    user_id: str,
    category: str,
    month: int,
    year: int
):

    budget = get_budget(
        user_id=user_id,
        category=category,
        month=month,
        year=year
    )

    if not budget:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    return budget


# ============================================================
# UPDATE BUDGET
# ============================================================

@router.put("/budget/{user_id}")
def update_budget(
    user_id: str,
    category: str,
    month: int,
    year: int,
    data: BudgetUpdate
):

    existing_budget = get_budget(
        user_id=user_id,
        category=category,
        month=month,
        year=year
    )

    if not existing_budget:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    result = set_budget(
        user_id=user_id,
        category=category,
        monthly_limit=data.monthly_limit,
        month=month,
        year=year
    )

    return result


# ============================================================
# RECORD PURCHASE
# ============================================================

@router.post("/purchase")
def create_purchase(data: PurchaseCreate):

    result = record_purchase(
        user_id=data.user_id,
        purchase_price=data.purchase_price,
        wardrobe_item_id=data.wardrobe_item_id,
        purchase_date=data.purchase_date,
        brand=data.brand,
        merchant=data.merchant
    )

    return result


# ============================================================
# GET PURCHASE HISTORY
# ============================================================

@router.get("/purchases/{user_id}")
def fetch_purchase_history(user_id: str):

    purchases = get_purchase_history(user_id)

    return {
        "user_id": user_id,
        "total_purchases": len(purchases),
        "purchases": purchases
    }


# ============================================================
# MONTHLY SPENDING ANALYSIS
# ============================================================

@router.get("/monthly-analysis/{user_id}")
def monthly_spending_analysis(
    user_id: str,
    category: str,
    month: int,
    year: int
):

    result = get_monthly_spending_analysis(
        user_id=user_id,
        category=category,
        month=month,
        year=year
    )

    return result


# ============================================================
# ANALYZE PURCHASE
# ============================================================

@router.post("/analyze-purchase")
def analyze_purchase_api(data: PurchaseAnalysisRequest):

    result = analyze_purchase(
        user_id=data.user_id,
        category=data.category,
        color=data.color,
        styles=data.styles,
        purchase_price=data.purchase_price,
        month=data.month,
        year=data.year
    )

    return result



# ============================================================
# ANALYZE PURCHASE IMAGE
# ============================================================

@router.post("/analyze-purchase-image")
async def analyze_purchase_image(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    purchase_price: float = Form(...),
    month: int = Form(...),
    year: int = Form(...),
    brand: str = Form(None),
    merchant: str = Form(None)
):

    # --------------------------------------------------------
    # CREATE PURCHASE UPLOAD FOLDER
    # --------------------------------------------------------

    purchase_upload_folder = "uploads/purchases"

    os.makedirs(
        purchase_upload_folder,
        exist_ok=True
    )

    # --------------------------------------------------------
    # SAVE IMAGE
    # --------------------------------------------------------

    file_extension = os.path.splitext(
        file.filename
    )[1]

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = os.path.join(
        purchase_upload_folder,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        # ----------------------------------------------------
        # ANALYZE CLOTHING USING EXISTING ANALYZER
        # ----------------------------------------------------

        clothing_analysis = analyze_clothing(
            file_path
        )

        # ----------------------------------------------------
        # EXTRACT VALUES
        # ----------------------------------------------------

        styles = [
            item["label"]
            for item in clothing_analysis["styles"]
        ]

        occasions = [
            item["label"]
            for item in clothing_analysis["occasions"]
        ]

        seasons = [
            clothing_analysis["season"]["label"]
        ]

        category = clothing_analysis["category"]["label"]

        color = clothing_analysis["color"]["label"]

        pattern = clothing_analysis["pattern"]["label"]

        fit = clothing_analysis["fit"]["label"]

        embedding = clothing_analysis["embedding"]

        # ----------------------------------------------------
        # SAVE TO PENDING PURCHASE
        # ----------------------------------------------------

        db = SessionLocal()

        try:

            pending_purchase = PendingPurchase(

                user_id=user_id,

                image_url=file_path,

                category=category,
                color=color,
                pattern=pattern,
                fit=fit,

                styles=styles,
                occasions=occasions,
                seasons=seasons,

                embedding=embedding,

                purchase_price=purchase_price,

                brand=brand,
                merchant=merchant,

                status="ANALYZED"
            )

            db.add(pending_purchase)

            db.commit()

            db.refresh(pending_purchase)

        except Exception as e:

            db.rollback()

            raise e

        finally:

            db.close()

        # ----------------------------------------------------
        # ANALYZE PURCHASE USING FINANCE AGENT
        # ----------------------------------------------------

        purchase_analysis = analyze_purchase(
            user_id=user_id,
            category=category,
            purchase_price=purchase_price,
            month=month,
            year=year,
            color=color,
            styles=styles
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {

            "success": True,

            "message": (
                "Purchase image analyzed successfully"
            ),

            "pending_purchase_id": pending_purchase.id,

            "user_id": user_id,

            "purchase_price": purchase_price,

            "month": month,

            "year": year,

            "image_path": file_path,

            "clothing_analysis": {

                "category": clothing_analysis["category"],

                "color": clothing_analysis["color"],

                "pattern": clothing_analysis["pattern"],

                "fit": clothing_analysis["fit"],

                "styles": clothing_analysis["styles"],

                "occasions": clothing_analysis["occasions"],

                "season": clothing_analysis["season"]

            },

            "purchase_analysis": purchase_analysis
        }

    except Exception as e:

        return {

            "success": False,

            "message": "Purchase analysis failed.",

            "error": str(e)
        }


# ============================================================
# CONFIRM PURCHASE
# ============================================================

@router.post("/confirm-purchase")
def confirm_purchase(
    pending_purchase_id: int
):

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # 1. GET PENDING PURCHASE
        # ----------------------------------------------------

        pending_purchase = db.query(
            PendingPurchase
        ).filter(
            PendingPurchase.id == pending_purchase_id
        ).first()

        if not pending_purchase:

            return {
                "success": False,
                "message": "Pending purchase not found."
            }

        # ----------------------------------------------------
        # 2. CHECK IF ALREADY PURCHASED
        # ----------------------------------------------------

        if pending_purchase.status == "PURCHASED":

            return {
                "success": False,
                "message": "This purchase has already been confirmed."
            }

        # ----------------------------------------------------
        # 3. CREATE WARDROBE ITEM
        # ----------------------------------------------------

        wardrobe_item = WardrobeItem(

            user_id=pending_purchase.user_id,

            image_url=pending_purchase.image_url,

            embedding=pending_purchase.embedding,

            category=pending_purchase.category,

            color=pending_purchase.color,

            pattern=pending_purchase.pattern,

            fit=pending_purchase.fit,

            styles=pending_purchase.styles,

            occasions=pending_purchase.occasions,

            seasons=pending_purchase.seasons,

            is_available=True,

            usage_count=0
        )

        db.add(wardrobe_item)

        db.flush()

        # ----------------------------------------------------
        # 4. CREATE PURCHASE HISTORY
        # ----------------------------------------------------

        purchase = PurchaseHistory(

            user_id=pending_purchase.user_id,

            wardrobe_item_id=wardrobe_item.id,

            purchase_price=pending_purchase.purchase_price,

            brand=pending_purchase.brand,

            merchant=pending_purchase.merchant
        )

        db.add(purchase)

        # ----------------------------------------------------
        # 5. UPDATE PENDING PURCHASE STATUS
        # ----------------------------------------------------

        pending_purchase.status = "PURCHASED"

        # ----------------------------------------------------
        # 6. COMMIT EVERYTHING
        # ----------------------------------------------------

        db.commit()

        db.refresh(wardrobe_item)

        db.refresh(purchase)

        return {

            "success": True,

            "message": (
                "Purchase confirmed successfully. "
                "Item added to wardrobe and purchase history."
            ),

            "wardrobe_item": {

                "id": wardrobe_item.id,

                "user_id": wardrobe_item.user_id,

                "category": wardrobe_item.category,

                "color": wardrobe_item.color,

                "pattern": wardrobe_item.pattern,

                "fit": wardrobe_item.fit,

                "styles": wardrobe_item.styles,

                "occasions": wardrobe_item.occasions,

                "seasons": wardrobe_item.seasons,

                "usage_count": wardrobe_item.usage_count
            },

            "purchase": {

                "id": purchase.id,

                "wardrobe_item_id": purchase.wardrobe_item_id,

                "purchase_price": float(
                    purchase.purchase_price
                ),

                "brand": purchase.brand,

                "merchant": purchase.merchant
            }
        }

    except Exception as e:

        db.rollback()

        return {
            "success": False,
            "message": "Failed to confirm purchase.",
            "error": str(e)
        }

    finally:

        db.close()


# ============================================================
# CANCEL PURCHASE
# ============================================================

@router.post("/cancel-purchase")
def cancel_purchase(
    pending_purchase_id: int
):

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # 1. GET PENDING PURCHASE
        # ----------------------------------------------------

        pending_purchase = db.query(
            PendingPurchase
        ).filter(
            PendingPurchase.id == pending_purchase_id
        ).first()

        # ----------------------------------------------------
        # 2. CHECK IF PURCHASE EXISTS
        # ----------------------------------------------------

        if not pending_purchase:

            return {
                "success": False,
                "message": "Pending purchase not found."
            }

        # ----------------------------------------------------
        # 3. CHECK IF ALREADY PURCHASED
        # ----------------------------------------------------

        if pending_purchase.status == "PURCHASED":

            return {
                "success": False,
                "message": (
                    "This purchase has already been confirmed "
                    "and cannot be cancelled."
                )
            }

        # ----------------------------------------------------
        # 4. CHECK IF ALREADY CANCELLED
        # ----------------------------------------------------

        if pending_purchase.status == "CANCELLED":

            return {
                "success": False,
                "message": "This purchase has already been cancelled."
            }

        # ----------------------------------------------------
        # 5. CANCEL PURCHASE
        # ----------------------------------------------------

        pending_purchase.status = "CANCELLED"

        db.commit()

        db.refresh(pending_purchase)

        # ----------------------------------------------------
        # 6. RETURN RESPONSE
        # ----------------------------------------------------

        return {

            "success": True,

            "message": "Purchase cancelled successfully.",

            "pending_purchase": {

                "id": pending_purchase.id,

                "user_id": pending_purchase.user_id,

                "category": pending_purchase.category,

                "purchase_price": float(
                    pending_purchase.purchase_price
                ),

                "status": pending_purchase.status
            }
        }

    except Exception as e:

        db.rollback()

        return {

            "success": False,

            "message": "Failed to cancel purchase.",

            "error": str(e)
        }

    finally:

        db.close()