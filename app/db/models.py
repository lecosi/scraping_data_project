from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Float,
    String,
    DateTime
)

from app.db.connection import Base


"""class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    name = Column(String)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))


class LocationCategoryReviewed(Base):
    __tablename__ = "location_categories_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=False)
    last_verification_date = Column(DateTime, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))"""
