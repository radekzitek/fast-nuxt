from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ProgressUpdateBase(BaseModel):
    objective_id: int
    progress_date: date
    comment: str
    progress: Optional[float] = None

class ProgressUpdateCreate(ProgressUpdateBase):
    pass

class ProgressUpdateUpdate(BaseModel):
    progress_date: Optional[date] = None
    comment: Optional[str] = None
    progress: Optional[float] = None

class ProgressUpdateInDBBase(ProgressUpdateBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProgressUpdate(ProgressUpdateInDBBase):
    pass

class ProgressUpdateInDB(ProgressUpdateInDBBase):
    pass
