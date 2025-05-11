"""
TeamMember ORM Model.

This module defines the SQLAlchemy ORM model for a 'TeamMember'.
"""
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(30), nullable=True)
    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    supervisor_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("team_members.id"), nullable=True)

    supervisor = relationship("TeamMember", remote_side="TeamMember.id", backref="subordinates")
