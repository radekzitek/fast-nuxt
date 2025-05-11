"""
CRUD operations for ProgressUpdate model.
"""
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union, List
from app.models.progress_update import ProgressUpdate
from app.schemas.progress_update import ProgressUpdateCreate, ProgressUpdateUpdate

def get_progress_update(db: Session, progress_update_id: int) -> Optional[ProgressUpdate]:
    return db.query(ProgressUpdate).filter(ProgressUpdate.id == progress_update_id).first()

def get_progress_updates_by_objective(db: Session, objective_id: int, skip: int = 0, limit: int = 100) -> List[ProgressUpdate]:
    return db.query(ProgressUpdate).filter(ProgressUpdate.objective_id == objective_id).offset(skip).limit(limit).all()

def create_progress_update(db: Session, *, obj_in: ProgressUpdateCreate) -> ProgressUpdate:
    db_obj = ProgressUpdate(
        objective_id=obj_in.objective_id,
        progress_date=obj_in.progress_date,
        comment=obj_in.comment,
        progress=obj_in.progress,
        active=True,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_progress_update(db: Session, *, db_obj: ProgressUpdate, obj_in: Union[ProgressUpdateUpdate, Dict[str, Any]]) -> ProgressUpdate:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_progress_update(db: Session, *, progress_update_id: int) -> Optional[ProgressUpdate]:
    obj = db.query(ProgressUpdate).get(progress_update_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
