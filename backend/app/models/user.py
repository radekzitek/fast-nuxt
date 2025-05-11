"""
User ORM Model.

This module defines the SQLAlchemy ORM model for a 'User'.
It inherits common fields from the `Base` class and defines user-specific attributes.
"""
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column  # For SQLAlchemy 2.0 style type hints
from app.db.base_class import Base


class User(Base):
    """
    SQLAlchemy ORM model representing a user in the database.

    Inherits `id`, `active`, `created_at`, and `updated_at` fields from `Base`.

    Attributes:
        __tablename__ (str): The name of the database table, explicitly set to "users".
        username (Mapped[str]): The user's unique username. Indexed for fast lookups.
        email (Mapped[str]): The user's unique email address. Indexed for fast lookups.
        first_name (Mapped[str | None]): The user's first name (optional).
        last_name (Mapped[str | None]): The user's last name (optional).
        hashed_password (Mapped[str]): The user's password, stored in a hashed format.
        note (Mapped[str | None]): An optional note or description for the user.
        team_member_id (Mapped[int | None]): The ID of the associated team member (optional).
    """
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    team_member_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("team_members.id"), nullable=True)

    # If you need a __repr__ method for debugging:
    # def __repr__(self):
    #    return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
