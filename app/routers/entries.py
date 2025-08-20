"""
FastAPI router for journal entry endpoints.

Defines HTTP routes for creating and retrieving entries.
"""

from fastapi import APIRouter, Response, status, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from .. import crud
from fastapi.responses import RedirectResponse

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

# Must stay above @router.get("/id...") or search functino will return "search parsed as int"
@router.get("/search", response_model=list[schemas.EntryRead])
def search_entries(
    q: str = "",
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Search entries by title or Markdown (LIKE), newest-first.
    """
    if not q.strip():
        return []
    results = crud.search_entries(db, q, limit=limit, offset=offset)
    return results

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

@router.get("", response_model=list[schemas.EntryRead])
def list_entries(
    limit: int = 20,
    offset: int = 0, 
    db: Session = Depends(get_db)):
    """
    List entries newest first with basic pagination (JSON).
    """
    items = crud.get_entries(db, limit=limit, offset=offset)
    return items

@router.delete("/{id}")
def delete_entry_json(
    id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_entry(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Entry not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{id}/delete")
def delete_entry_form(
    id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_entry(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Entry not found.")
    # Temporary target until we ship templates and GET "/"
    return RedirectResponse(url="/entries", status_code=status.HTTP_303_SEE_OTHER)


