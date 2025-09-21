from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime, Numeric, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TrackingEntry(Base):
    """
    Entry into the main database, represents a tracked event or process
    """
    __tablename__ = "tracking_entry"

    transaction_id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"), nullable=False)
    date: Mapped[date] = mapped_column(nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("unit.unit_id"), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("type.type_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    tag_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tag.tag_id"), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps: DB-seitig, TZ-aware
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    category: Mapped["Category"] = relationship(back_populates="entries")
    unit: Mapped["Unit"] = relationship(back_populates="entries")
    type: Mapped["Type"] = relationship(back_populates="entries")
    tag: Mapped[Optional["Tag"]] = relationship(back_populates="entries")


class Category(Base):
    """
    Hierarchical category of the tracked event/process. Allows grouping for better analysis.
    """
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.category_id"), nullable=True)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Self-referential hierarchy
    parent: Mapped[Optional["Category"]] = relationship(
        remote_side="Category.category_id", back_populates="children"
    )
    children: Mapped[List["Category"]] = relationship(back_populates="parent")

    # Backref to entries
    entries: Mapped[List["TrackingEntry"]] = relationship(back_populates="category")


class Unit(Base):
    """
    Unit of the quantity, for example time/amount.
    """
    __tablename__ = "unit"

    unit_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    unit_type: Mapped[Optional[str]] = mapped_column(String)
    # exact arithmetic: Decimal + Numeric
    conversion_factor: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), server_default="1.00"
    )

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    entries: Mapped[List["TrackingEntry"]] = relationship(back_populates="unit")


class Type(Base):
    """
    Type of the tracked entry (hierarchical).
    """
    __tablename__ = "type"

    type_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("type.type_id"))

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    parent: Mapped[Optional["Type"]] = relationship(
        remote_side="Type.type_id", back_populates="children"
    )
    children: Mapped[List["Type"]] = relationship(back_populates="parent")

    entries: Mapped[List["TrackingEntry"]] = relationship(back_populates="type")


class Tag(Base):
    """
    Tag to enhance analysis potential.
    """
    __tablename__ = "tag"

    tag_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    entries: Mapped[List["TrackingEntry"]] = relationship(back_populates="tag")