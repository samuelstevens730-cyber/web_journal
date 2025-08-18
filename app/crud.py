"""
CRUD (Create, Read, Update, Delete) operations.

Encapsulates all direct database queries used by routers.
"""

from sqlalchemy.orm import Session
from . import models
from .schemas import EntryCreate

def create_entry(db: Session, data: EntryCreate) -> models.Entry:
    """
    Insert a new journal entry.
    For now, content_html mirrors content_md: we'll render/sanitize later.
    """
    entry = models.Entry(
        title=data.title,
        content_md=data.content_md,
        content_html=data.content_md,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry) #populate .id, timestamps
    return entry
    
def get_entry(db: Session, entry_id: int) -> models.Entry | None:
    """
    Return entry by id, or none if not found
    """
    return db.get(models.Entry, entry_id)