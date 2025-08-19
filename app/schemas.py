"""
Pydantic schemas for request/response validation.

Keeps API layer decoupled from database models.
"""

from pydantic import BaseModel, Field

class EntryCreate(BaseModel):
    #Incoming data when creating an entry (e.g. from a form)
    title: str = Field(min_length=1, max_length=120)
    content_md: str = Field(min_length=1, max_length=50000)

class EntryRead(BaseModel):
    # Outgoing data when returning an entry as JSON
    id: int
    title: str
    content_md: str
    content_html: str
    class Config:
    #Tell pydantic it can read attributes from ORM objects
    # (e.g. a SQLAlchemy Entry instance) not just plain dicts
        from_attributes = True
# PATCH: partial update (both fields optional)
class EntryUpdate(BaseModel):
    title: str | None = None
    content_md: str | None = None

# PUT: full replace (both fields required)
class EntryPut(BaseModel):
    title: str
    content_md: str
