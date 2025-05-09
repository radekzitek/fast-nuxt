"""
API Endpoints for User Management.

This module defines the FastAPI routes for CRUD operations on users.
It uses the Pydantic schemas for request and response validation and
the CRUD functions for database interactions.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import crud, models, schemas # Application-specific imports
from app.db.session import get_db # Dependency to get a database session
from app.core.security import verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter()
"""
FastAPI router for user-related endpoints.
All routes defined here will be prefixed, e.g., by `/api/v1/users`.
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")

# Utility to get current user from JWT token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create a new user.

    Checks if a user with the same email or username already exists before creation.
    The password provided in `user_in` will be hashed by the CRUD operation.

    Args:
        db: Database session dependency.
        user_in: Pydantic schema (`UserCreate`) containing the new user's data.

    Raises:
        HTTPException (400): If a user with the given email or username already exists.

    Returns:
        The created user object, conforming to the `schemas.User` model.
    """
    user = crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user_by_username = crud.get_user_by_username(db, username=user_in.username)
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user = crud.create_user(db=db, user_in=user_in)
    return user

@router.get("/", response_model=List[schemas.User])
def read_users_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve a list of users with pagination.

    Args:
        db: Database session dependency.
        skip: Number of users to skip (for pagination).
        limit: Maximum number of users to return.

    Returns:
        A list of user objects, conforming to `schemas.User`.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/me", response_model=schemas.User, dependencies=[Depends(oauth2_scheme)])
def read_users_me(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return schemas.User.model_validate(current_user)

@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by their ID.

    Args:
        user_id: The ID of the user to retrieve.
        db: Database session dependency.

    Raises:
        HTTPException (404): If no user is found with the given ID.

    Returns:
        The user object, conforming to `schemas.User`.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
) -> Any:
    """
    Update an existing user.

    Allows partial updates. If email or username is being changed, it checks for conflicts.
    If a new password is provided, it will be hashed by the CRUD operation.

    Args:
        db: Database session dependency.
        user_id: The ID of the user to update.
        user_in: Pydantic schema (`UserUpdate`) containing the fields to update.

    Raises:
        HTTPException (404): If the user with the given ID does not exist.
        HTTPException (400): If the new email or username is already taken by another user.

    Returns:
        The updated user object, conforming to `schemas.User`.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    # Check for email conflict if email is being changed
    if user_in.email and user_in.email != user.email:
        existing_user = crud.get_user_by_email(db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered by another user.")
    # Check for username conflict if username is being changed
    if user_in.username and user_in.username != user.username:
        existing_user = crud.get_user_by_username(db, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken.")

    user = crud.update_user(db=db, db_user=user, user_in=user_in)
    return user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_id: int,
) -> Any:
    """
    Delete a user by their ID.

    Args:
        db: Database session dependency.
        user_id: The ID of the user to delete.

    Raises:
        HTTPException (404): If the user with the given ID does not exist.

    Returns:
        The deleted user object, conforming to `schemas.User`.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return deleted_user

@router.post("/login", response_model=schemas.Token)
def login_user_endpoint(
    *,
    db: Session = Depends(get_db),
    login_in: schemas.UserLogin,
):
    """
    Authorize user by username and password.
    Returns JWT token if authentication is successful.
    """
    user = crud.get_user_by_username(db, username=login_in.username)
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token({"sub": str(user.id), "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=schemas.Token)
def login_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token({"sub": str(user.id), "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
