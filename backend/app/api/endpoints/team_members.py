"""
API Endpoints for Team Member Management.

This module defines the FastAPI routes for CRUD operations on team members.
"""

from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import get_db
from app.models import TeamMember, Objective

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.TeamMember,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new team member",
    response_description="The created team member.",
)
def create_team_member_endpoint(
    *,
    db: Session = Depends(get_db),
    member_in: schemas.TeamMemberCreate,
) -> Any:
    """
    Create a new team member.

    - **first_name**: First name of the team member
    - **last_name**: Last name of the team member
    - **email**: Email address (must be unique)
    - **phone_number**: Phone number (optional)
    - **position**: Position or role (optional)
    - **notes**: Additional notes (optional)
    - **supervisor_id**: ID of the supervisor (optional)
    """
    member = crud.create_team_member(db=db, member_in=member_in)
    return member


@router.get(
    "/",
    response_model=List[schemas.TeamMember],
    summary="List all team members",
    response_description="A list of team members.",
)
def read_team_members_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve a list of all team members.

    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records to return
    """
    members = crud.get_team_members(db, skip=skip, limit=limit)
    return members


@router.get(
    "/{member_id}",
    response_model=schemas.TeamMember,
    summary="Get a team member by ID",
    response_description="The requested team member.",
)
def read_team_member_by_id_endpoint(
    member_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a team member by their unique ID.

    - **member_id**: The ID of the team member to retrieve
    """
    member = crud.get_team_member(db, member_id=member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found"
        )
    return member


@router.get(
    "/by-supervisor/{supervisor_id}",
    response_model=List[schemas.TeamMember],
    summary="List team members by supervisor ID",
    response_description="A list of team members with the given supervisor ID."
)
def read_team_members_by_supervisor_id(
    supervisor_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve all team members who have the given supervisor_id.
    - **supervisor_id**: The ID of the supervisor
    """
    members = db.query(TeamMember).filter(TeamMember.supervisor_id == supervisor_id).all()
    return members


@router.get("/{team_member_id}/objectives", response_model=List[schemas.Objective])
def get_objectives_for_team_member(team_member_id: int, db: Session = Depends(get_db)):
    return db.query(Objective).filter(Objective.owner_id == team_member_id).all()


@router.put(
    "/{member_id}",
    response_model=schemas.TeamMember,
    summary="Update a team member",
    response_description="The updated team member.",
)
def update_team_member_endpoint(
    *,
    db: Session = Depends(get_db),
    member_id: int,
    member_in: schemas.TeamMemberUpdate,
) -> Any:
    """
    Update an existing team member by ID.

    - **member_id**: The ID of the team member to update
    - **member_in**: The updated team member data
    """
    member = crud.get_team_member(db, member_id=member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found"
        )
    updated_member = crud.update_team_member(
        db=db, db_member=member, member_in=member_in
    )
    return updated_member


@router.delete(
    "/{member_id}",
    response_model=schemas.TeamMember,
    summary="Delete a team member",
    response_description="The deleted team member.",
)
def delete_team_member_endpoint(
    *,
    db: Session = Depends(get_db),
    member_id: int,
) -> Any:
    """
    Delete a team member by ID.

    - **member_id**: The ID of the team member to delete
    """
    member = crud.get_team_member(db, member_id=member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found"
        )
    deleted_member = crud.delete_team_member(db=db, member_id=member_id)
    return deleted_member
