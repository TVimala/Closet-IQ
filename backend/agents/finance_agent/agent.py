from database.connection import SessionLocal
from database.models import FinancialProfile, Budget, PurchaseHistory

from datetime import date, datetime
from sqlalchemy import extract, func

from database.models import(
    FinancialProfile,
    Budget,
    PurchaseHistory,
    WardrobeItem
)


# ============================================================
# FINANCIAL PROFILE
# ============================================================

def set_financial_profile(
    user_id,
    monthly_salary,
    currency="INR"
):

    db = SessionLocal()

    try:

        # Check if the user already has a financial profile
        profile = db.query(FinancialProfile).filter(
            FinancialProfile.user_id == user_id
        ).first()

        # If profile exists, update it
        if profile:

            profile.monthly_salary = monthly_salary
            profile.currency = currency

        # Otherwise create a new profile
        else:

            profile = FinancialProfile(
                user_id=user_id,
                monthly_salary=monthly_salary,
                currency=currency
            )

            db.add(profile)

        db.commit()
        db.refresh(profile)

        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "monthly_salary": profile.monthly_salary,
            "currency": profile.currency,
            "message": "Financial profile saved successfully"
        }

    except Exception as e:

        db.rollback()
        raise e

    finally:

        db.close()


# ============================================================
# GET FINANCIAL PROFILE
# ============================================================

def get_financial_profile(user_id):

    db = SessionLocal()

    try:

        profile = db.query(FinancialProfile).filter(
            FinancialProfile.user_id == user_id
        ).first()

        if not profile:
            return None

        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "monthly_salary": profile.monthly_salary,
            "currency": profile.currency
        }

    finally:

        db.close()


# ============================================================
# SET MONTHLY BUDGET
# ============================================================

def set_budget(
    user_id,
    category,
    monthly_limit,
    month,
    year
):

    db = SessionLocal()

    try:

        # Check whether a budget already exists
        # for this user, category, month and year

        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category,
            Budget.month == month,
            Budget.year == year
        ).first()

        # Update existing budget
        if budget:

            budget.monthly_limit = monthly_limit

        # Create new budget
        else:

            budget = Budget(
                user_id=user_id,
                category=category,
                monthly_limit=monthly_limit,
                month=month,
                year=year
            )

            db.add(budget)

        db.commit()
        db.refresh(budget)

        return {
            "id": budget.id,
            "user_id": budget.user_id,
            "category": budget.category,
            "monthly_limit": budget.monthly_limit,
            "month": budget.month,
            "year": budget.year,
            "message": "Budget saved successfully"
        }

    except Exception as e:

        db.rollback()
        raise e

    finally:

        db.close()


# ============================================================
# GET MONTHLY BUDGET
# ============================================================

def get_budget(
    user_id,
    category,
    month,
    year
):

    db = SessionLocal()

    try:

        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category,
            Budget.month == month,
            Budget.year == year
        ).first()

        if not budget:
            return None

        return {
            "id": budget.id,
            "user_id": budget.user_id,
            "category": budget.category,
            "monthly_limit": budget.monthly_limit,
            "month": budget.month,
            "year": budget.year
        }

    finally:

        db.close()


# ============================================================
# RECORD PURCHASE
# ============================================================

def record_purchase(
    user_id,
    purchase_price,
    wardrobe_item_id=None,
    purchase_date=None,
    brand=None,
    merchant=None
):

    db = SessionLocal()

    try:

        # If purchase date is not provided,
        # use today's date
        if purchase_date is None:
            purchase_date = date.today()

        purchase = PurchaseHistory(
            user_id=user_id,
            wardrobe_item_id=wardrobe_item_id,
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            brand=brand,
            merchant=merchant
        )

        db.add(purchase)

        db.commit()
        db.refresh(purchase)

        return {
            "id": purchase.id,
            "user_id": purchase.user_id,
            "wardrobe_item_id": purchase.wardrobe_item_id,
            "purchase_price": purchase.purchase_price,
            "purchase_date": purchase.purchase_date,
            "brand": purchase.brand,
            "merchant": purchase.merchant,
            "message": "Purchase recorded successfully"
        }

    except Exception as e:

        db.rollback()
        raise e

    finally:

        db.close()


# ============================================================
# GET PURCHASE HISTORY
# ============================================================

def get_purchase_history(user_id):

    db = SessionLocal()

    try:

        purchases = db.query(PurchaseHistory).filter(
            PurchaseHistory.user_id == user_id
        ).order_by(
            PurchaseHistory.purchase_date.desc()
        ).all()

        results = []

        for purchase in purchases:

            results.append({
                "id": purchase.id,
                "user_id": purchase.user_id,
                "wardrobe_item_id": purchase.wardrobe_item_id,
                "purchase_price": purchase.purchase_price,
                "purchase_date": purchase.purchase_date,
                "brand": purchase.brand,
                "merchant": purchase.merchant
            })

        return results

    finally:

        db.close()


# ============================================================
# MONTHLY SPENDING ANALYSIS
# ============================================================

def get_monthly_spending_analysis(
    user_id,
    category,
    month,
    year
):

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Get the budget for this category/month/year
        # ----------------------------------------------------

        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category,
            Budget.month == month,
            Budget.year == year
        ).first()

        # If budget doesn't exist
        if not budget:
            return {
                "error": "Budget not found for the selected month."
            }

        # ----------------------------------------------------
        # Calculate total spending for the selected month
        # ----------------------------------------------------

        total_spent = db.query(
            func.coalesce(
                func.sum(PurchaseHistory.purchase_price),
                0
            )
        ).filter(
            PurchaseHistory.user_id == user_id,
            extract("month", PurchaseHistory.purchase_date) == month,
            extract("year", PurchaseHistory.purchase_date) == year
        ).scalar()

        total_spent = float(total_spent)

        # ----------------------------------------------------
        # Calculate remaining budget
        # ----------------------------------------------------

        monthly_limit = float(budget.monthly_limit)

        remaining_budget = monthly_limit - total_spent

        # ----------------------------------------------------
        # Return analysis
        # ----------------------------------------------------

        return {
            "user_id": user_id,
            "category": category,
            "month": month,
            "year": year,

            "monthly_budget": monthly_limit,
            "total_spent": total_spent,
            "remaining_budget": remaining_budget,

            "budget_exceeded": remaining_budget < 0
        }

    finally:
        db.close()


# ============================================================
# WARDROBE SIMILARITY ANALYSIS
# ============================================================

def analyze_similar_wardrobe_items(
    user_id,
    category,
    color=None,
    styles=None
):

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Start with items from the user's available wardrobe
        # ----------------------------------------------------

        query = db.query(WardrobeItem).filter(
            WardrobeItem.user_id == user_id,
            WardrobeItem.is_available == True
        )

        # ----------------------------------------------------
        # Category is the strongest basic filter
        # ----------------------------------------------------

        if category:
            query = query.filter(
                WardrobeItem.category.ilike(f"%{category}%")
            )

        items = query.all()

        similar_items = []

        for item in items:

            similarity_score = 0
            matched_features = []

            # ------------------------------------------------
            # COLOR MATCH
            # ------------------------------------------------

            if color and item.color:

                if item.color.lower() == color.lower():

                    similarity_score += 30
                    matched_features.append("color")

            # ------------------------------------------------
            # STYLE MATCH
            # ------------------------------------------------

            if styles and item.styles:

                # Convert both to lowercase
                requested_styles = [
                    style.lower()
                    for style in styles
                ]

                existing_styles = [
                    style.lower()
                    for style in item.styles
                ]

                common_styles = set(
                    requested_styles
                ).intersection(
                    existing_styles
                )

                if common_styles:

                    similarity_score += 40
                    matched_features.append("style")

            # ------------------------------------------------
            # CATEGORY MATCH
            # ------------------------------------------------

            # Since the database query already filtered
            # by category, category gets a score.

            similarity_score += 30
            matched_features.append("category")

            # ------------------------------------------------
            # Keep only meaningful matches
            # ------------------------------------------------

            if similarity_score >= 30:

                similar_items.append({
                    "id": item.id,
                    "category": item.category,
                    "color": item.color,
                    "styles": item.styles,
                    "usage_count": item.usage_count,
                    "similarity_score": similarity_score,
                    "matched_features": matched_features
                })

        # ----------------------------------------------------
        # Calculate statistics
        # ----------------------------------------------------

        total_similar_items = len(similar_items)

        total_usage = sum(
            item["usage_count"]
            for item in similar_items
        )

        average_usage = (
            total_usage / total_similar_items
            if total_similar_items > 0
            else 0
        )

        return {
            "total_similar_items": total_similar_items,
            "average_usage_count": round(average_usage, 2),
            "similar_items": similar_items
        }

    finally:
        db.close()


# ============================================================
# COST PER USE ANALYSIS
# ============================================================

def analyze_cost_per_use(user_id, similar_items):

    db = SessionLocal()

    try:

        results = []

        total_cost_per_use = 0

        # Items that have purchase records
        items_with_purchase_data = 0

        # Items where CPU can actually be calculated
        items_with_cost_per_use = 0


        for item in similar_items:

            wardrobe_item_id = item["id"]

            # ---------------------------------------------
            # Find purchase record
            # ---------------------------------------------

            purchase = db.query(PurchaseHistory).filter(
                PurchaseHistory.user_id == user_id,
                PurchaseHistory.wardrobe_item_id == wardrobe_item_id
            ).order_by(
                PurchaseHistory.purchase_date.desc()
            ).first()


            # ---------------------------------------------
            # No purchase record
            # ---------------------------------------------

            if not purchase:

                results.append({
                    "wardrobe_item_id": wardrobe_item_id,
                    "usage_count": item["usage_count"],
                    "purchase_price": None,
                    "cost_per_use": None
                })

                continue


            # ---------------------------------------------
            # Purchase record exists
            # ---------------------------------------------

            items_with_purchase_data += 1

            purchase_price = float(
                purchase.purchase_price
            )

            usage_count = item["usage_count"]


            # ---------------------------------------------
            # Calculate Cost Per Use
            # ---------------------------------------------

            if usage_count > 0:

                cost_per_use = (
                    purchase_price / usage_count
                )

                total_cost_per_use += cost_per_use

                items_with_cost_per_use += 1

            else:

                cost_per_use = None


            results.append({

                "wardrobe_item_id": wardrobe_item_id,

                "usage_count": usage_count,

                "purchase_price": purchase_price,

                "cost_per_use": (
                    round(cost_per_use, 2)
                    if cost_per_use is not None
                    else None
                )
            })


        # ---------------------------------------------
        # Calculate Average Cost Per Use
        # ---------------------------------------------

        average_cost_per_use = (

            total_cost_per_use / items_with_cost_per_use

            if items_with_cost_per_use > 0

            else None
        )


        return {

            "items_analyzed": len(results),

            # How many items have purchase records
            "items_with_purchase_data": (
                items_with_purchase_data
            ),

            # How many items have usable CPU values
            "items_with_cost_per_use": (
                items_with_cost_per_use
            ),

            "average_cost_per_use": (

                round(average_cost_per_use, 2)

                if average_cost_per_use is not None

                else None
            ),

            "items": results
        }


    finally:

        db.close()


# ============================================================
# FINANCIAL AFFORDABILITY ANALYSIS
# ============================================================

def analyze_financial_affordability(
    user_id,
    purchase_price,
    category,
    month,
    year
):

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Get user's financial profile
        # ----------------------------------------------------

        financial_profile = db.query(FinancialProfile).filter(
            FinancialProfile.user_id == user_id
        ).first()

        # ----------------------------------------------------
        # Get budget for selected month
        # ----------------------------------------------------

        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category,
            Budget.month == month,
            Budget.year == year
        ).first()

        # ----------------------------------------------------
        # Calculate spending for selected month
        # ----------------------------------------------------

        total_spent = db.query(
            func.coalesce(
                func.sum(PurchaseHistory.purchase_price),
                0
            )
        ).filter(
            PurchaseHistory.user_id == user_id,
            extract("month", PurchaseHistory.purchase_date) == month,
            extract("year", PurchaseHistory.purchase_date) == year
        ).scalar()

        total_spent = float(total_spent)

        purchase_price = float(purchase_price)

        # ----------------------------------------------------
        # Handle missing financial profile
        # ----------------------------------------------------

        if not financial_profile:
            return {
                "error": "Financial profile not found."
            }

        monthly_salary = float(
            financial_profile.monthly_salary
        )

        # ----------------------------------------------------
        # Handle missing budget
        # ----------------------------------------------------

        if not budget:
            return {
                "error": "Budget not found for selected month."
            }

        monthly_budget = float(
            budget.monthly_limit
        )

        # ----------------------------------------------------
        # Calculate remaining budget
        # ----------------------------------------------------

        remaining_before_purchase = (
            monthly_budget - total_spent
        )

        remaining_after_purchase = (
            remaining_before_purchase - purchase_price
        )

        # ----------------------------------------------------
        # Calculate salary percentage
        # ----------------------------------------------------

        salary_percentage = (
            (purchase_price / monthly_salary) * 100
            if monthly_salary > 0
            else None
        )

        # ----------------------------------------------------
        # Affordability result
        # ----------------------------------------------------

        within_budget = remaining_after_purchase >= 0

        return {

            "monthly_salary": monthly_salary,

            "monthly_budget": monthly_budget,

            "total_spent": total_spent,

            "remaining_budget_before_purchase":
                remaining_before_purchase,

            "proposed_purchase_price":
                purchase_price,

            "remaining_budget_after_purchase":
                remaining_after_purchase,

            "within_budget": within_budget,

            "salary_percentage": (
                round(salary_percentage, 2)
                if salary_percentage is not None
                else None
            )
        }

    finally:
        db.close()


# ============================================================
# PURCHASE EXPLANATION GENERATOR
# ============================================================

def generate_purchase_explanation(
    decision,
    purchase_score,
    wardrobe_analysis,
    cost_per_use_analysis,
    financial_analysis
):

    total_similar_items = wardrobe_analysis[
        "total_similar_items"
    ]

    average_usage = wardrobe_analysis[
        "average_usage_count"
    ]

    average_cost_per_use = cost_per_use_analysis[
        "average_cost_per_use"
    ]

    within_budget = financial_analysis[
        "within_budget"
    ]

    purchase_price = financial_analysis[
        "proposed_purchase_price"
    ]

    remaining_after_purchase = financial_analysis[
        "remaining_budget_after_purchase"
    ]


    # ====================================================
    # BUILD EXPLANATION
    # ====================================================

    explanation_parts = []


    # ----------------------------------------------------
    # FINAL DECISION
    # ----------------------------------------------------

    if decision == "BUY":

        explanation_parts.append(
            f"BUY recommended with a purchase score of "
            f"{purchase_score}/100."
        )

    elif decision == "CONSIDER":

        explanation_parts.append(
            f"CONSIDER this purchase with a score of "
            f"{purchase_score}/100."
        )

    else:

        explanation_parts.append(
            f"DON'T BUY recommended with a score of "
            f"{purchase_score}/100."
        )


    # ----------------------------------------------------
    # WARDROBE ANALYSIS
    # ----------------------------------------------------

    if total_similar_items == 0:

        explanation_parts.append(
            "You do not currently own a similar item, "
            "so this purchase could add something new to your wardrobe."
        )

    elif total_similar_items == 1:

        explanation_parts.append(
            "You currently own only one similar item."
        )

    else:

        explanation_parts.append(
            f"You already own {total_similar_items} similar items."
        )


    # ----------------------------------------------------
    # USAGE ANALYSIS
    # ----------------------------------------------------

    if total_similar_items > 0:

        if average_usage < 1:

            explanation_parts.append(
                f"Those similar items are rarely used, with an "
                f"average usage count of {average_usage}."
            )

        elif average_usage < 4:

            explanation_parts.append(
                f"Your similar items are used occasionally, with an "
                f"average usage count of {average_usage}."
            )

        else:

            explanation_parts.append(
                f"You regularly use similar items, with an "
                f"average usage count of {average_usage}."
            )


    # ----------------------------------------------------
    # COST PER USE ANALYSIS
    # ----------------------------------------------------

    if average_cost_per_use is None:

        explanation_parts.append(
            "There is not enough purchase history available to "
            "calculate the cost per use of similar items."
        )

    else:

        explanation_parts.append(
            f"The average cost per use of similar items is "
            f"₹{average_cost_per_use}."
        )


    # ----------------------------------------------------
    # FINANCIAL ANALYSIS
    # ----------------------------------------------------

    if within_budget:

        explanation_parts.append(
            f"The ₹{purchase_price} purchase fits within your budget "
            f"and would leave ₹{remaining_after_purchase} remaining."
        )

    else:

        explanation_parts.append(
            f"The ₹{purchase_price} purchase would exceed your "
            f"monthly shopping budget."
        )


    # ====================================================
    # FINAL EXPLANATION
    # ====================================================

    return " ".join(explanation_parts)


# ============================================================
# MAIN PURCHASE ANALYSIS
# ============================================================

def analyze_purchase(
    user_id,
    category,
    purchase_price,
    month,
    year,
    color=None,
    styles=None
):

    # ----------------------------------------------------
    # 1. ANALYZE SIMILAR WARDROBE ITEMS
    # ----------------------------------------------------

    wardrobe_analysis = analyze_similar_wardrobe_items(
        user_id=user_id,
        category=category,
        color=color,
        styles=styles
    )

    similar_items = wardrobe_analysis["similar_items"]


    # ----------------------------------------------------
    # 2. ANALYZE COST PER USE
    # ----------------------------------------------------

    cost_per_use_analysis = analyze_cost_per_use(
        user_id=user_id,
        similar_items=similar_items
    )


    # ----------------------------------------------------
    # 3. ANALYZE FINANCIAL AFFORDABILITY
    # ----------------------------------------------------

    financial_analysis = analyze_financial_affordability(
        user_id=user_id,
        purchase_price=purchase_price,
        category="CLOTHING",
        month=month,
        year=year
    )

    # Stop if financial information is missing
    if "error" in financial_analysis:

        return {
            "error": financial_analysis["error"]
        }


    # ----------------------------------------------------
    # 4. EXTRACT IMPORTANT VALUES
    # ----------------------------------------------------

    total_similar_items = wardrobe_analysis[
        "total_similar_items"
    ]

    average_usage = wardrobe_analysis[
        "average_usage_count"
    ]

    within_budget = financial_analysis[
        "within_budget"
    ]

    average_cost_per_use = cost_per_use_analysis[
        "average_cost_per_use"
    ]


    # ====================================================
    # 5. PURCHASE SCORING
    # ====================================================

    purchase_score = 0

    score_breakdown = {}

    reasons = []


    # ====================================================
    # A. FINANCIAL AFFORDABILITY — 40 POINTS
    # ====================================================

    if within_budget:

        purchase_score += 40

        score_breakdown["financial_affordability"] = 40

        reasons.append(
            "The purchase fits within your monthly shopping budget."
        )

    else:

        score_breakdown["financial_affordability"] = 0

        reasons.append(
            "This purchase would exceed your monthly shopping budget."
        )


    # ====================================================
    # B. WARDROBE SATURATION — 25 POINTS
    # ====================================================

    if total_similar_items == 0:

        purchase_score += 25

        score_breakdown["wardrobe_saturation"] = 25

        reasons.append(
            "You don't currently own a similar item."
        )

    elif total_similar_items == 1:

        purchase_score += 20

        score_breakdown["wardrobe_saturation"] = 20

        reasons.append(
            "You own only one similar item."
        )

    elif total_similar_items == 2:

        purchase_score += 12

        score_breakdown["wardrobe_saturation"] = 12

        reasons.append(
            "You already own a few similar items."
        )

    elif total_similar_items == 3:

        purchase_score += 5

        score_breakdown["wardrobe_saturation"] = 5

        reasons.append(
            "Your wardrobe already contains several similar items."
        )

    else:

        score_breakdown["wardrobe_saturation"] = 0

        reasons.append(
            "Your wardrobe is already saturated with similar items."
        )


    # ====================================================
    # C. USAGE PATTERN — 20 POINTS
    # ====================================================

    if total_similar_items == 0:

        # No similar items exist, so usage cannot be measured
        purchase_score += 10

        score_breakdown["usage_pattern"] = 10

        reasons.append(
            "There are no existing similar items to evaluate usage."
        )

    elif average_usage >= 8:

        purchase_score += 20

        score_breakdown["usage_pattern"] = 20

        reasons.append(
            "You frequently wear similar items."
        )

    elif average_usage >= 4:

        purchase_score += 14

        score_breakdown["usage_pattern"] = 14

        reasons.append(
            "You regularly use similar items."
        )

    elif average_usage >= 1:

        purchase_score += 7

        score_breakdown["usage_pattern"] = 7

        reasons.append(
            "Similar items are used occasionally."
        )

    else:

        score_breakdown["usage_pattern"] = 0

        reasons.append(
            "Your similar items have rarely or never been worn."
        )


    # ====================================================
    # D. COST PER USE — 15 POINTS
    # ====================================================

    if average_cost_per_use is None:

        # Not enough purchase/usage history
        purchase_score += 7

        score_breakdown["cost_per_use"] = 7

        reasons.append(
            "There isn't enough cost-per-use history yet."
        )

    elif average_cost_per_use <= 300:

        purchase_score += 15

        score_breakdown["cost_per_use"] = 15

        reasons.append(
            "Similar items provide good value based on cost per use."
        )

    elif average_cost_per_use <= 700:

        purchase_score += 10

        score_breakdown["cost_per_use"] = 10

        reasons.append(
            "Similar items provide moderate value based on cost per use."
        )

    else:

        purchase_score += 3

        score_breakdown["cost_per_use"] = 3

        reasons.append(
            "Similar items currently have a relatively high cost per use."
        )


    # ====================================================
    # 6. FINAL DECISION
    # ====================================================

    if purchase_score >= 70:

        decision = "BUY"

    elif purchase_score >= 40:

        decision = "CONSIDER"

    else:

        decision = "DON'T BUY"



    # ====================================================
    # GENERATE HUMAN-FRIENDLY EXPLANATION
    # ====================================================
    explanation = generate_purchase_explanation(
    decision=decision,
    purchase_score=purchase_score,
    wardrobe_analysis=wardrobe_analysis,
    cost_per_use_analysis=cost_per_use_analysis,
    financial_analysis=financial_analysis
)


    # ====================================================
    # 7. RETURN COMPLETE ANALYSIS
    # ====================================================

    return {

        "decision": decision,

        "purchase_score": purchase_score,

        "score_breakdown": score_breakdown,

        "reasons": reasons,

        "explanation": explanation,

        "wardrobe_analysis": {
            "total_similar_items": total_similar_items,
            "average_usage_count": average_usage
        },

        "cost_per_use_analysis": cost_per_use_analysis,

        "financial_analysis": financial_analysis
    }