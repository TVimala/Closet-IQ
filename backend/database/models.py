from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Numeric,
    Date,
    ForeignKey
)
from sqlalchemy.sql import func

from .connection import Base

from pgvector.sqlalchemy import Vector


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

    subcategory = Column(
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

    material = Column(
        String(100),
        nullable=True
    )

    fit = Column(
        String(100),
        nullable=True
    )

    style = Column(
        String(100),
        nullable=True
    )

    season = Column(
        String(100),
        nullable=True
    )

    occasion = Column(
        String(100),
        nullable=True
    )

    brand = Column(
        String(100),
        nullable=True
    )

    purchase_price = Column(
        Numeric(10, 2),
        nullable=True
    )

    purchase_date = Column(
        Date,
        nullable=True
    )

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