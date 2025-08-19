"""
SQLAlchemy ORM models for the journal app.

Defines database tables and relationships.
"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String, Integer, DateTime, func
from . database import Base

class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    content_md: Mapped[str] = mapped_column(Text, nullable=False)
    content_html: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
