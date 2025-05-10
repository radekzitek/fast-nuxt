"""
CRUD (Create, Read, Update, Delete) Operations for User Model.

This module provides a set of functions to interact with the `User` data
in the database. These functions encapsulate the SQLAlchemy query logic
for common user-related database operations.
"""
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union, List

from app.core.security import get_password_hash  # For hashing passwords
from app.models.user import User  # The SQLAlchemy ORM User model
from app.schemas.user import UserCreate, UserUpdate  # Pydantic schemas for user creation and updates


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieves a user from the database by their ID.

    Args:
        db: The SQLAlchemy database session.
        user_id: The ID of the user to retrieve.

    Returns:
        The User object if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieves a user from the database by their email address.

    Args:
        db: The SQLAlchemy database session.
        email: The email address of the user to retrieve.

    Returns:
        The User object if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieves a user from the database by their username.

    Args:
        db: The SQLAlchemy database session.
        username: The username of the user to retrieve.

    Returns:
        The User object if found, otherwise None.
    """
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieves a list of users from the database with pagination.

    Args:
        db: The SQLAlchemy database session.
        skip: The number of users to skip (for pagination).
        limit: The maximum number of users to return (for pagination).

    Returns:
        A list of User objects.
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, *, user_in: UserCreate) -> User:
    """
    Creates a new user in the database.

    The provided password in `user_in` will be hashed before storage.

    Args:
        db: The SQLAlchemy database session.
        user_in: A Pydantic schema (`UserCreate`) containing the data for the new user.
                 The `password` field should be plain text.

    Returns:
        The newly created User object.
    """
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        note=user_in.note,
        active=user_in.active if user_in.active is not None else True,
        team_member_id=user_in.team_member_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh to get DB-generated fields like id, created_at
    return db_user


def update_user(
    db: Session, *, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    """
    Updates an existing user in the database.

    If a new password is provided in `user_in`, it will be hashed.
    Only fields present in `user_in` will be updated.

    Args:
        db: The SQLAlchemy database session.
        db_user: The existing User ORM object to update.
        user_in: A Pydantic schema (`UserUpdate`) or a dictionary containing the
                 fields to update. If `password` is included, it should be plain text.

    Returns:
        The updated User object.
    """
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        # For Pydantic models, dump to dict, excluding unset values to allow partial updates
        update_data = user_in.model_dump(exclude_unset=True)  # Pydantic V2
        # update_data = user_in.dict(exclude_unset=True) # Pydantic V1

    if "password" in update_data and update_data["password"]:
        # If a new password is provided, hash it
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]  # Remove plain password from update_data
        update_data["hashed_password"] = hashed_password  # Add hashed password

    # Update the db_user object with new values
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)  # Add the updated object to the session (marks it as dirty)
    db.commit()  # Commit the changes to the database
    db.refresh(db_user)  # Refresh to get any DB-updated fields (e.g., updated_at)
    return db_user


def delete_user(db: Session, *, user_id: int) -> Optional[User]:
    """
    Deletes a user from the database by their ID.

    Args:
        db: The SQLAlchemy database session.
        user_id: The ID of the user to delete.

    Returns:
        The User object that was deleted, or None if no user was found with that ID.
    """
    user = db.query(User).get(user_id)  # .get() is a shortcut for filtering by primary key
    if user:
        db.delete(user)
        db.commit()
    return user
