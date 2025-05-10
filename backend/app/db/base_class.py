"""
SQLAlchemy Declarative Base Class.

This module defines the base class for all SQLAlchemy ORM models in the application.
It includes common columns that will be inherited by all models, such as an 'id'
primary key, 'active' status, and 'created_at'/'updated_at' timestamps.
"""

from datetime import datetime  # <--- Add this import
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Integer, Boolean, DateTime
from sqlalchemy.sql import func  # Import func
from sqlalchemy.orm import Mapped, mapped_column  # Add Mapped and mapped_column


@as_declarative()
class Base:
    """
    Base class for SQLAlchemy ORM models.

    Provides automated table name generation and common columns:
    - `id`: An integer primary key, indexed for fast lookups.
    - `active`: A boolean indicating if the record is active, defaults to True.
    - `created_at`: A datetime field automatically set to the current time on creation.
    - `updated_at`: A datetime field automatically set to the current time on update.

    The `__tablename__` is automatically generated as the lowercase version of the
    class name.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generates the table name automatically based on the class name.

        Returns:
            The lowercase version of the class name.
        """
        return cls.__name__.lower()

    # Update annotations to use Mapped[] and mapped_column
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    """Surrogate primary key for all tables, indexed for efficiency."""

    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    """Boolean flag to indicate if the record is active. Defaults to True."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    """Timestamp indicating when the record was created. Set by the database server."""

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )
    """Timestamp indicating when the record was last updated. Updated by the database server on modification."""
