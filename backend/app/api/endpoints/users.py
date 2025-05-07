from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db.session import get_db # Corrected import

router = APIRouter()

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
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
    Retrieve users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get user by ID.
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
    Update a user.
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
    Delete a user.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return deleted_user
