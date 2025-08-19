"""
CRUD (Create, Read, Update, Delete) operations.

Encapsulates all direct database queries used by routers.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from .schemas import EntryCreate
from . import schemas, models
from .markdown_utils import render_md_to_safe_html

def create_entry(db: Session, data: EntryCreate) -> models.Entry:
    now = datetime.utcnow()
    entry = models.Entry(
        title=data.title,
        content_md=data.content_md,
        created_at=now,
        updated_at=now,
        content_html=render_md_to_safe_html(data.content_md)
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
    
def get_entry(db: Session, entry_id: int) -> models.Entry | None:
    """
    Return entry by id, or none if not found
    """
    return db.get(models.Entry, entry_id)

def update_entry(
    db: Session,
    entry_id: int,
    data: schemas.EntryUpdate | schemas.EntryPut,
) -> models.Entry | None:
    entry = db.get(models.Entry, entry_id)
    if entry is None:
        return None

    # PUT = full replace
    if isinstance(data, schemas.EntryPut):
        entry.title = data.title
        entry.content_md = data.content_md
        entry.content_html = data.content_md #mirror for now
    else:
        # PATCH = full replace
        if data.title is not None:
            entry.title = data.title
        if data.content_md is not None:
            entry.content_md = data.content_md
            entry.content_html = data.content_md #mirror for now

    db.add(entry)
    db.commit() 
    db.refresh(entry)
    return entry          