"""
Database configuration and session management.

- Ensures the `data/` directory exists.
- Defines the SQLAlchemy engine, SessionLocal, and Base for models.
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Ensure /data path exists
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

#Single-file SQLite for v0
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/journal.db"

# For SQLite Only: 
# - SQLite enforces "use connection in same thread that created it".
# - FastAPI/Uvicorn may hop threads in dev, this flag relaxes that check
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
    #, echo=True # <- uncomment while debugging to see SQL
)

#Each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for ORM models
Base = declarative_base()

# FastAPI Dependency to hand a DB session into path ops
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Self check for engine url
if __name__ == '__main__':
    print('DEBUG engine.url =', engine.url)



