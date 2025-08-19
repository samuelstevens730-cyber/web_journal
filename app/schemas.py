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
    model_config = {"from_attributes": True}
    #Tell pydantic it can read attributes from ORM objects
    # (e.g. a SQLAlchemy Entry instance) not just plain dicts

class EntryUpdate(BaseModel):
    """
    PATCH payload: both fields optional, but if provided they must meet the same length rules as create.
    """
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
        description="Optional new title; 1-120 chars when present."
    )
    content_md: str | None = Field(
        default=None,
        min_length=1,
        max_length=50_000,
        description="Optional new markdown; up to ~50k chars when present."
    )

# PUT: full replace (both fields required)
class EntryPut(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    content_md: str = Field(min_length = 1, max_length=50000)
