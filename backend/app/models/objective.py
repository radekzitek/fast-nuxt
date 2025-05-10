"""
Objective ORM Model.

This module defines the SQLAlchemy ORM model for a 'Objective'.
"""
from sqlalchemy import String, Text, Integer, ForeignKey, Enum, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
import enum

class ObjectiveLevel(enum.Enum):
    ORGANIZATIONAL = "ORGANIZATIONAL"
    DEPARTMENTAL = "DEPARTMENTAL"
    TEAM = "TEAM"
    INDIVIDUAL = "INDIVIDUAL"

class ObjectiveStatus(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    DELAYED = "DELAYED"
    ACHIEVED = "ACHIEVED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"

class ObjectivePriority(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ObjectiveConfidentiality(enum.Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"

class ObjectiveStrategicPerspective(enum.Enum):
    FINANCIAL = "FINANCIAL"
    CUSTOMER = "CUSTOMER"
    INTERNAL_PROCESS = "INTERNAL_PROCESS"
    LEARNING_GROWTH = "LEARNING_GROWTH"

class ObjectiveReviewCadence(enum.Enum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    BI_ANNUALLY = "BI_ANNUALLY"
    ANNUALLY = "ANNUALLY"

class Objective(Base):
    __tablename__ = "objectives"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[ObjectiveLevel] = mapped_column(Enum(ObjectiveLevel), nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("team_members.id"), nullable=False)
    parent_objective_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("objectives.id"), nullable=True)
    status: Mapped[ObjectiveStatus] = mapped_column(Enum(ObjectiveStatus), nullable=False)
    priority: Mapped[ObjectivePriority | None] = mapped_column(Enum(ObjectivePriority), nullable=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    target_completion_date: Mapped[Date] = mapped_column(Date, nullable=False)
    actual_completion_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    # creation_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    last_updated_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    alignment_statement: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)  # Store as comma-separated string
    confidentiality: Mapped[ObjectiveConfidentiality | None] = mapped_column(Enum(ObjectiveConfidentiality), nullable=True)
    strategic_perspective: Mapped[ObjectiveStrategicPerspective | None] = mapped_column(Enum(ObjectiveStrategicPerspective), nullable=True)
    review_cadence: Mapped[ObjectiveReviewCadence | None] = mapped_column(Enum(ObjectiveReviewCadence), nullable=True)
    last_review_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

    owner = relationship("TeamMember", backref="objectives")
    parent_objective = relationship("Objective", remote_side="Objective.id", backref="sub_objectives")
    # progressUpdates will be handled as a separate table/model if needed
