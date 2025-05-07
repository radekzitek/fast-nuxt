from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union, List

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, *, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        note=user_in.note,
        active=user_in.active if user_in.active is not None else True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session, *, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]
) -> User:
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True) # Pydantic V2
        # update_data = user_in.dict(exclude_unset=True) # Pydantic V1

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"] # remove plain password
        update_data["hashed_password"] = hashed_password

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, *, user_id: int) -> Optional[User]:
    user = db.query(User).get(user_id)
    if user:
        db.delete(user)
        db.commit()
    return user