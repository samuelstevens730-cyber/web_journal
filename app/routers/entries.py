"""
FastAPI router for journal entry endpoints.

Defines HTTP routes for creating and retrieving entries.
"""

from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from .. import crud

router = APIRouter(prefix="/entries", tags=["entries"])

@router.post("/", response_model=schemas.EntryRead)
def create_entry_endpoint(
    title: str = Form(...),
    content_md: str = Form(...),
    db: Session = Depends(get_db),
):
    data = schemas.EntryCreate(title=title, content_md=content_md)
    entry = crud.create_entry(db, data)
    return entry

@router.get("/{id}", response_model=schemas.EntryRead)
def read_entry_endpoint(id: int, db: Session = Depends(get_db)):
    entry = crud.get_entry(db, id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found.")
    return entry

@router.patch("/{id}", response_model=schemas.EntryRead)
def patch_entry(
    id: int,
    payload: schemas.EntryUpdate,  # <-- JSON body with optional fields
    db: Session = Depends(get_db),
):
    """
    Partial update an entry (JSON). Only provided fields are applied.
    Returns the updated entry as EntryRead.
    """
    entry = crud.update_entry(db, id, payload)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found.")
    return entry
