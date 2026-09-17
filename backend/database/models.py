from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Numeric,
    Date,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.sql import func

from .connection import Base

from pgvector.sqlalchemy import Vector

from sqlalchemy.dialects.postgresql import ARRAY

from sqlalchemy.orm import relationship

# ============================================================
# USER MODELS
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        String(50),
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

# ============================================================
# WARDROBE AGENT MODELS
# ============================================================

class WardrobeItem(Base):
    __tablename__ = "wardrobe_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    image_url = Column(
        Text,
        nullable=True
    )

    embedding = Column(
    Vector(512),
    nullable=True
    )

    category = Column(
        String(100),
        nullable=True
    )

    # subcategory = Column(
    #     String(100),
    #     nullable=True
    # )

    color = Column(
        String(100),
        nullable=True
    )

    pattern = Column(
        String(100),
        nullable=True
    )

    # material = Column(
    #     String(100),
    #     nullable=True
    # )

    fit = Column(
        String(100),
        nullable=True
    )

    styles = Column(
    ARRAY(String(100)),
    nullable=True
    )

    seasons = Column(
    ARRAY(String(100)),
    nullable=True
    )

    occasions = Column(
    ARRAY(String(100)),
    nullable=True
    )

    # brand = Column(
    #     String(100),
    #     nullable=True
    # )

    # purchase_price = Column(
    #     Numeric(10, 2),
    #     nullable=True
    # )

    # purchase_date = Column(
    #     Date,
    #     nullable=True
    # )

    condition = Column(
        String(50),
        nullable=True
    )

    is_available = Column(
        Boolean,
        default=True
    )

    usage_count = Column(
    Integer,
    default=0,
    nullable=False
    )

    last_worn_at = Column(
    DateTime,
    nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

# ============================================================
# PROFILE AGENT MODELS
# ============================================================

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    gender = Column(String(30))
    birth_year = Column(Integer)
    generation = Column(String(50))

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    styles = Column(ARRAY(String(100)))
    colors = Column(ARRAY(String(100)))
    fits = Column(ARRAY(String(100)))
    occasions = Column(ARRAY(String(100)))

    comfort_weight = Column(Integer)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

class UserCurrentPreference(Base):
    __tablename__ = "user_current_preferences"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    styles = Column(ARRAY(String(100)))
    colors = Column(ARRAY(String(100)))
    fits = Column(ARRAY(String(100)))
    occasions = Column(ARRAY(String(100)))

    comfort_weight = Column(Integer)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

# ============================================================
# FINANCE AGENT MODELS
# ============================================================

class FinancialProfile(Base):
    __tablename__ = "financial_profiles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    monthly_salary = Column(
        Numeric(12, 2),
        nullable=False
    )

    currency = Column(
        String(10),
        nullable=False,
        default="INR"
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False,
        default="CLOTHING"
    )

    monthly_limit = Column(
        Numeric(12, 2),
        nullable=False
    )

    month = Column(
        Integer,
        nullable=False
    )

    year = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )


# ============================================================
# PURCHASE HISTORY MODELS
# ============================================================

class PurchaseHistory(Base):
    __tablename__ = "purchase_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    wardrobe_item_id = Column(
        Integer,
        ForeignKey("wardrobe_items.id", ondelete="SET NULL"),
        nullable=True
    )

    purchase_price = Column(
        Numeric(12, 2),
        nullable=False
    )

    purchase_date = Column(
        Date,
        nullable=False,
        server_default=func.current_date()
    )

    brand = Column(
        String(100),
        nullable=True
    )

    merchant = Column(
        String(150),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


# ============================================================
# PENDING PURCHASE MODEL
# ============================================================

class PendingPurchase(Base):
    __tablename__ = "pending_purchases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(50),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    image_url = Column(
        Text,
        nullable=True
    )

    # --------------------------------------------------------
    # CLOTHING ANALYSIS
    # --------------------------------------------------------

    category = Column(
        String(100),
        nullable=True
    )

    color = Column(
        String(100),
        nullable=True
    )

    pattern = Column(
        String(100),
        nullable=True
    )

    fit = Column(
        String(100),
        nullable=True
    )

    styles = Column(
        ARRAY(String(100)),
        nullable=True
    )

    occasions = Column(
        ARRAY(String(100)),
        nullable=True
    )

    seasons = Column(
        ARRAY(String(100)),
        nullable=True
    )

    # --------------------------------------------------------
    # EMBEDDING
    # --------------------------------------------------------

    embedding = Column(
        Vector(512),
        nullable=True
    )

    # --------------------------------------------------------
    # PURCHASE INFORMATION
    # --------------------------------------------------------

    purchase_price = Column(
        Numeric(12, 2),
        nullable=False
    )

    brand = Column(
        String(100),
        nullable=True
    )

    merchant = Column(
        String(150),
        nullable=True
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status = Column(
        String(30),
        nullable=False,
        default="ANALYZED"
    )

    # --------------------------------------------------------
    # TIMESTAMPS
    # --------------------------------------------------------

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )