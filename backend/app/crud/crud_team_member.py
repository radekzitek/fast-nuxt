from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.team_member import TeamMember
from app.schemas.team_member import TeamMemberCreate, TeamMemberUpdate


def get_team_member(db: Session, member_id: int) -> Optional[TeamMember]:
    return db.query(TeamMember).get(member_id)


def get_team_members(db: Session, skip: int = 0, limit: int = 100) -> List[TeamMember]:
    return db.query(TeamMember).offset(skip).limit(limit).all()


def create_team_member(db: Session, *, member_in: TeamMemberCreate) -> TeamMember:
    db_member = TeamMember(**member_in.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def update_team_member(db: Session, *, db_member: TeamMember, member_in: TeamMemberUpdate) -> TeamMember:
    update_data = member_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def delete_team_member(db: Session, *, member_id: int) -> Optional[TeamMember]:
    member = db.query(TeamMember).get(member_id)
    if member:
        db.delete(member)
        db.commit()
    return member
