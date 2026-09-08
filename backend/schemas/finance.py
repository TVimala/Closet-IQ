from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import date

# ============================================================
# FINANCIAL PROFILE SCHEMAS
# ============================================================

class FinancialProfileCreate(BaseModel):

    user_id: str

    monthly_salary: Decimal = Field(
        ...,
        gt=0,
        description="User's monthly salary"
    )

    currency: str = "INR"


class FinancialProfileUpdate(BaseModel):

    monthly_salary: Optional[Decimal] = Field(
        None,
        gt=0
    )

    currency: Optional[str] = None


# ============================================================
# BUDGET SCHEMAS
# ============================================================

class BudgetCreate(BaseModel):

    user_id: str

    category: str = "CLOTHING"

    monthly_limit: Decimal = Field(
        ...,
        gt=0,
        description="Maximum spending limit"
    )

    month: int = Field(
        ...,
        ge=1,
        le=12
    )

    year: int = Field(
        ...,
        ge=2020
    )


class BudgetUpdate(BaseModel):

    monthly_limit: Optional[Decimal] = Field(
        None,
        gt=0
    )


# ============================================================
# PURCHASE HISTORY SCHEMAS
# ============================================================

class PurchaseCreate(BaseModel):

    user_id: str

    wardrobe_item_id: Optional[int] = None

    purchase_price: Decimal = Field(
        ...,
        gt=0,
        description="Price paid for the item"
    )

    purchase_date: Optional[date] = None

    brand: Optional[str] = None

    merchant: Optional[str] = None


# ============================================================
# PURCHASE ANALYSIS SCHEMA
# ============================================================

class PurchaseAnalysisRequest(BaseModel):

    user_id: str

    category: str
    # Dress / Shirt / Jeans

    color: Optional[str] = None

    styles: Optional[list[str]] = None

    purchase_price: Decimal = Field(
        ...,
        gt=0
    )

    budget_category: str = "CLOTHING"

    month: int

    year: int