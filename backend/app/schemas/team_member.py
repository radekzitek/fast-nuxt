from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class TeamMemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    position: Optional[str] = None
    notes: Optional[str] = None
    supervisor_id: Optional[int] = None


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(TeamMemberBase):
    pass


class TeamMemberInDBBase(TeamMemberBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TeamMember(TeamMemberInDBBase):
    pass


class TeamMemberInDB(TeamMemberInDBBase):
    pass
