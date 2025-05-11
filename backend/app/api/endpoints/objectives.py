"""
API Endpoints for Objective Management.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db.session import get_db
from app.schemas.progress_update import ProgressUpdate, ProgressUpdateCreate, ProgressUpdateUpdate
from app.models import objective as objective_models

router = APIRouter()

@router.post("/", response_model=schemas.Objective, status_code=status.HTTP_201_CREATED)
def create_objective_endpoint(
    *,
    db: Session = Depends(get_db),
    obj_in: schemas.ObjectiveCreate,
) -> Any:
    obj = crud.crud_objective.create_objective(db=db, obj_in=obj_in)
    return obj

@router.get("/", response_model=List[schemas.Objective])
def read_objectives_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    objs = crud.crud_objective.get_objectives(db, skip=skip, limit=limit)
    return objs

@router.get("/enums", tags=["objectives"])
def get_objective_enums():
    return {
        "priority": [e.value for e in objective_models.ObjectivePriority],
        "status": [e.value for e in objective_models.ObjectiveStatus],
        "level": [e.value for e in objective_models.ObjectiveLevel],
        "confidentiality": [e.value for e in objective_models.ObjectiveConfidentiality],
        "strategic_perspective": [e.value for e in objective_models.ObjectiveStrategicPerspective],
        "review_cadence": [e.value for e in objective_models.ObjectiveReviewCadence],
    }

@router.get("/{objective_id}", response_model=schemas.Objective)
def read_objective_by_id_endpoint(
    objective_id: int,
    db: Session = Depends(get_db),
) -> Any:
    obj = crud.crud_objective.get_objective(db, objective_id=objective_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objective not found")
    return obj

@router.put("/{objective_id}", response_model=schemas.Objective)
def update_objective_endpoint(
    *,
    db: Session = Depends(get_db),
    objective_id: int,
    obj_in: schemas.ObjectiveUpdate,
) -> Any:
    obj = crud.crud_objective.get_objective(db, objective_id=objective_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objective not found")
    updated_obj = crud.crud_objective.update_objective(db=db, db_obj=obj, obj_in=obj_in)
    return updated_obj

@router.delete("/{objective_id}", response_model=schemas.Objective)
def delete_objective_endpoint(
    *,
    db: Session = Depends(get_db),
    objective_id: int,
) -> Any:
    obj = crud.crud_objective.get_objective(db, objective_id=objective_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objective not found")
    deleted_obj = crud.crud_objective.delete_objective(db=db, objective_id=objective_id)
    return deleted_obj

@router.get("/{objective_id}/progress-updates", response_model=List[ProgressUpdate])
def list_progress_updates_for_objective(
    objective_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return crud.crud_progress_update.get_progress_updates_by_objective(db, objective_id, skip=skip, limit=limit)

@router.post("/{objective_id}/progress-updates", response_model=ProgressUpdate, status_code=status.HTTP_201_CREATED)
def create_progress_update_for_objective(
    objective_id: int,
    progress_update_in: ProgressUpdateCreate,
    db: Session = Depends(get_db),
):
    if progress_update_in.objective_id != objective_id:
        raise HTTPException(status_code=400, detail="objective_id mismatch")
    return crud.crud_progress_update.create_progress_update(db=db, obj_in=progress_update_in)

@router.get("/progress-updates/{progress_update_id}", response_model=ProgressUpdate)
def get_progress_update(
    progress_update_id: int,
    db: Session = Depends(get_db),
):
    obj = crud.crud_progress_update.get_progress_update(db, progress_update_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Progress update not found")
    return obj

@router.put("/progress-updates/{progress_update_id}", response_model=ProgressUpdate)
def update_progress_update(
    progress_update_id: int,
    progress_update_in: ProgressUpdateUpdate,
    db: Session = Depends(get_db),
):
    db_obj = crud.crud_progress_update.get_progress_update(db, progress_update_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Progress update not found")
    return crud.crud_progress_update.update_progress_update(db=db, db_obj=db_obj, obj_in=progress_update_in)

@router.delete("/progress-updates/{progress_update_id}", response_model=ProgressUpdate)
def delete_progress_update(
    progress_update_id: int,
    db: Session = Depends(get_db),
):
    db_obj = crud.crud_progress_update.get_progress_update(db, progress_update_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Progress update not found")
    return crud.crud_progress_update.delete_progress_update(db=db, progress_update_id=progress_update_id)
