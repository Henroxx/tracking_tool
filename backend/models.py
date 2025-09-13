from unicodedata import category
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


Base = declarative_base()

class TrackingEntry(Base):
    """
    Entry into the main database, represents a tracked event or process
    """
    __tablename__ = "tracking_entries"
    
    transaction_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    date = Column(Date)
    unit_id = Column(Integer, ForeignKey("unit.unit_id"))
    type_id = Column(Integer, ForeignKey("type.type_id"))
    quantity = Column(Integer)
    tag_id = Column(Integer, ForeignKey("tag.tag_id"))
    comment = Column(Text)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    

class Category(Base):
    """
    Hierarchical category of the tracked event/process. Allows to group categories for better analysis
    """
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.category_id"))

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Unit(Base):
    """
    Unit of the quantity, for example time/amount.
    """
    __tablename__ = "unit"

    unit_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    unit_type = Column(String)
    conversion_factor = Column(Float, default=1.0)          #Might cause problems later bc float * integer

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Type(Base):
    """
    Entry into the main database
    """
    __tablename__ = "type"

    type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("type.type_id"))

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class Tag(Base):
    """
    Tag to enhance analysis potential
    """
    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)) 
