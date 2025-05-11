from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class ObjectiveLevel(str, Enum):
    ORGANIZATIONAL = "ORGANIZATIONAL"
    DEPARTMENTAL = "DEPARTMENTAL"
    TEAM = "TEAM"
    INDIVIDUAL = "INDIVIDUAL"

class ObjectiveStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    DELAYED = "DELAYED"
    ACHIEVED = "ACHIEVED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"

class ObjectivePriority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ObjectiveConfidentiality(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"

class ObjectiveStrategicPerspective(str, Enum):
    FINANCIAL = "FINANCIAL"
    CUSTOMER = "CUSTOMER"
    INTERNAL_PROCESS = "INTERNAL_PROCESS"
    LEARNING_GROWTH = "LEARNING_GROWTH"

class ObjectiveReviewCadence(str, Enum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    BI_ANNUALLY = "BI_ANNUALLY"
    ANNUALLY = "ANNUALLY"

class ProgressUpdate(BaseModel):
    date: date
    comment: str
    progress: Optional[float] = None

class ObjectiveBase(BaseModel):
    title: str
    description: str
    level: ObjectiveLevel
    owner_id: int
    parent_objective_id: Optional[int] = None
    status: ObjectiveStatus
    priority: Optional[ObjectivePriority] = None
    start_date: date
    target_completion_date: date
    actual_completion_date: Optional[date] = None
    alignment_statement: Optional[str] = None
    tags: Optional[List[str]] = None
    confidentiality: Optional[ObjectiveConfidentiality] = None
    strategic_perspective: Optional[ObjectiveStrategicPerspective] = None
    # progress_updates: Optional[List[ProgressUpdate]] = None
    review_cadence: Optional[ObjectiveReviewCadence] = None
    last_review_date: Optional[date] = None

class ObjectiveCreate(ObjectiveBase):
    last_updated_date: datetime

class ObjectiveUpdate(ObjectiveBase):
    last_updated_date: datetime

class ObjectiveInDBBase(ObjectiveBase):
    id: int
    last_updated_date: datetime

    class Config:
        from_attributes = True

class Objective(ObjectiveInDBBase):
    pass

class ObjectiveInDB(ObjectiveInDBBase):
    pass
