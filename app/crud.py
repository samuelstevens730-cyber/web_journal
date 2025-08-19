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

    changed = False

    # PUT = full replace (both fields required)
    if isinstance(data, schemas.EntryPut):
        if entry.title != data.title:
            entry.title = data.title
            changed = True

        if entry.content_md != data.content_md:
            entry.content_md = data.content_md
            entry.content_html = render_md_to_safe_html(data.content_md)  # Markdown → safe HTML
            changed = True

    # PATCH = partial update (only provided fields)
    else:
        if data.title is not None and data.title != entry.title:
            entry.title = data.title
            changed = True

        if data.content_md is not None and data.content_md != entry.content_md:
            entry.content_md = data.content_md
            entry.content_html = render_md_to_safe_html(data.content_md)  # Markdown → safe HTML
            changed = True

    if changed:
        entry.updated_at = datetime.utcnow()  # v0 convention: naive UTC
        db.add(entry)
        db.commit()
        db.refresh(entry)

    return entry