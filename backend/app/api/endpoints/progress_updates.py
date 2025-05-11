from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud
from app.schemas.progress_update import ProgressUpdate, ProgressUpdateCreate, ProgressUpdateUpdate
from app.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[ProgressUpdate])
def list_progress_updates(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    # Optionally, add filtering by objective_id as a query param
    return db.query(crud.models.ProgressUpdate).offset(skip).limit(limit).all()

@router.get("/by-objective/{objective_id}", response_model=List[ProgressUpdate])
def list_progress_updates_for_objective(
    objective_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return crud.crud_progress_update.get_progress_updates_by_objective(db, objective_id, skip=skip, limit=limit)

@router.post("/", response_model=ProgressUpdate, status_code=status.HTTP_201_CREATED)
def create_progress_update(
    progress_update_in: ProgressUpdateCreate,
    db: Session = Depends(get_db),
):
    return crud.crud_progress_update.create_progress_update(db=db, obj_in=progress_update_in)

@router.get("/{progress_update_id}", response_model=ProgressUpdate)
def get_progress_update(
    progress_update_id: int,
    db: Session = Depends(get_db),
):
    obj = crud.crud_progress_update.get_progress_update(db, progress_update_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Progress update not found")
    return obj

@router.put("/{progress_update_id}", response_model=ProgressUpdate)
def update_progress_update(
    progress_update_id: int,
    progress_update_in: ProgressUpdateUpdate,
    db: Session = Depends(get_db),
):
    db_obj = crud.crud_progress_update.get_progress_update(db, progress_update_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Progress update not found")
    return crud.crud_progress_update.update_progress_update(db=db, db_obj=db_obj, obj_in=progress_update_in)

@router.delete("/{progress_update_id}", response_model=ProgressUpdate)
def delete_progress_update(
    progress_update_id: int,
    db: Session = Depends(get_db),
):
    db_obj = crud.crud_progress_update.get_progress_update(db, progress_update_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Progress update not found")
    return crud.crud_progress_update.delete_progress_update(db=db, progress_update_id=progress_update_id)
