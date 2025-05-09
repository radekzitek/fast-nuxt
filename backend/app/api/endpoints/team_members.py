"""
API Endpoints for Team Member Management.

This module defines the FastAPI routes for CRUD operations on team members.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TeamMember, status_code=status.HTTP_201_CREATED)
def create_team_member_endpoint(
    *,
    db: Session = Depends(get_db),
    member_in: schemas.TeamMemberCreate,
) -> Any:
    member = crud.create_team_member(db=db, member_in=member_in)
    return member

@router.get("/", response_model=List[schemas.TeamMember])
def read_team_members_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    members = crud.get_team_members(db, skip=skip, limit=limit)
    return members

@router.get("/{member_id}", response_model=schemas.TeamMember)
def read_team_member_by_id_endpoint(
    member_id: int,
    db: Session = Depends(get_db),
) -> Any:
    member = crud.get_team_member(db, member_id=member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    return member

@router.put("/{member_id}", response_model=schemas.TeamMember)
def update_team_member_endpoint(
    *,
    db: Session = Depends(get_db),
    member_id: int,
    member_in: schemas.TeamMemberUpdate,
) -> Any:
    member = crud.get_team_member(db, member_id=member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    updated_member = crud.update_team_member(db=db, db_member=member, member_in=member_in)
    return updated_member

@router.delete("/{member_id}", response_model=schemas.TeamMember)
def delete_team_member_endpoint(
    *,
    db: Session = Depends(get_db),
    member_id: int,
) -> Any:
    member = crud.get_team_member(db, member_id=member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    deleted_member = crud.delete_team_member(db=db, member_id=member_id)
    return deleted_member
