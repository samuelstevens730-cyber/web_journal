"""
SQLAlchemy ORM models for the journal app.

Defines database tables and relationships.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base

class Entry(Base):
    __tablename__="entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content_md = Column(Text, nullable=False)
    content_html = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    