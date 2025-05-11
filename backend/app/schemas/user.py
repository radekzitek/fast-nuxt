"""
Pydantic Schemas for User Data.

This module defines Pydantic models (schemas) for validating and serializing
user-related data in API requests and responses. These schemas are used by
FastAPI for data validation, serialization, and documentation generation.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Shared properties


class UserBase(BaseModel):
    """
    Base Pydantic model for user properties shared across different operations.

    Attributes:
        email (EmailStr): The user's email address. Validated as an email string.
        username (str): The user's username.
        first_name (Optional[str]): The user's first name (optional).
        last_name (Optional[str]): The user's last name (optional).
        note (Optional[str]): An optional note for the user.
        active (Optional[bool]): Whether the user account is active. Defaults to True.
        team_member_id (Optional[int]): The user's team member ID (optional).
    """
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    note: Optional[str] = None
    active: Optional[bool] = True
    team_member_id: Optional[int] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    Pydantic model for data required when creating a new user.
    Inherits all fields from `UserBase`.

    Attributes:
        password (str): The user's plain text password. This will be hashed before storage.
    """
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """
    Pydantic model for data that can be provided when updating an existing user.
    All fields are optional, allowing partial updates. Inherits from `UserBase`.

    Attributes:
        password (Optional[str]): A new plain text password, if the user wants to change it.
        email (Optional[EmailStr]): A new email address, if being updated.
        username (Optional[str]): A new username, if being updated.
    """
    password: Optional[str] = None
    email: Optional[EmailStr] = None  # Allow email update
    username: Optional[str] = None  # Allow username update


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    """
    Base Pydantic model representing common properties of a user as stored in the database.
    Includes fields that are typically auto-generated or managed by the database.
    Inherits from `UserBase`.

    Attributes:
        id (int): The unique identifier for the user.
        created_at (datetime): Timestamp of when the user was created.
        updated_at (Optional[datetime]): Timestamp of when the user was last updated.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """
        Pydantic model configuration.

        Attributes:
            from_attributes (bool): Enables creating the Pydantic model from ORM model attributes.
                                    (Equivalent to `orm_mode = True` in Pydantic V1).
        """
        # orm_mode = True # Pydantic V1
        from_attributes = True  # Pydantic V2


# Properties to return to client
class User(UserInDBBase):
    """
    Pydantic model for representing a user in API responses.
    This is typically what the client will receive. It inherits all fields from `UserInDBBase`.
    Excludes sensitive information like `hashed_password`.
    """
    # pass


# Properties stored in DB
class UserInDB(UserInDBBase):
    """
    Pydantic model representing a user as fully stored in the database,
    including potentially sensitive fields like `hashed_password`.
    Inherits from `UserInDBBase`.

    Attributes:
        hashed_password (str): The user's hashed password as stored in the database.
    """
    hashed_password: str


class UserLogin(BaseModel):
    """
    Pydantic model for user login (authorization) requests.
    """
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
