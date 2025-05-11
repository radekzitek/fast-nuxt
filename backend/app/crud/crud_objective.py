"""
CRUD (Create, Read, Update, Delete) Operations for Objective Model.
"""
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union, List
from app.models.objective import Objective
from app.schemas.objective import ObjectiveCreate, ObjectiveUpdate

def get_objective(db: Session, objective_id: int) -> Optional[Objective]:
    return db.query(Objective).filter(Objective.id == objective_id).first()

def get_objectives(db: Session, skip: int = 0, limit: int = 100) -> List[Objective]:
    return db.query(Objective).offset(skip).limit(limit).all()

def create_objective(db: Session, *, obj_in: ObjectiveCreate) -> Objective:
    db_obj = Objective(
        title=obj_in.title,
        description=obj_in.description,
        level=obj_in.level,
        owner_id=obj_in.owner_id,
        parent_objective_id=obj_in.parent_objective_id,
        status=obj_in.status,
        priority=obj_in.priority,
        start_date=obj_in.start_date,
        target_completion_date=obj_in.target_completion_date,
        actual_completion_date=obj_in.actual_completion_date,
        last_updated_date=obj_in.last_updated_date,
        alignment_statement=obj_in.alignment_statement,
        tags=','.join(obj_in.tags) if obj_in.tags else None,
        confidentiality=obj_in.confidentiality,
        strategic_perspective=obj_in.strategic_perspective,
        review_cadence=obj_in.review_cadence,
        last_review_date=obj_in.last_review_date,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_objective(db: Session, *, db_obj: Objective, obj_in: Union[ObjectiveUpdate, Dict[str, Any]]) -> Objective:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = ','.join(update_data["tags"])
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_objective(db: Session, *, objective_id: int) -> Optional[Objective]:
    obj = db.query(Objective).get(objective_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
