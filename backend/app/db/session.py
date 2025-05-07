"""
Database Session Management.

This module sets up the SQLAlchemy database engine and session handling.
It provides a dependency (`get_db`) for FastAPI endpoints to obtain a database session.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# For SQLite, connect_args is needed to enable foreign key support by default
# and to allow the same connection to be used across different threads in FastAPI.
engine_args = {"connect_args": {"check_same_thread": False}} if "sqlite" in settings.SQLALCHEMY_DATABASE_URL else {}

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    **engine_args
)
"""
SQLAlchemy database engine.
Configured using the `SQLALCHEMY_DATABASE_URL` from application settings.
Includes specific arguments for SQLite if it's the selected database.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Factory for creating SQLAlchemy database sessions.
Sessions are configured to not autocommit or autoflush, and are bound to the engine.
"""

# Dependency to get DB session
def get_db():
    """
    FastAPI dependency to get a database session.

    This function creates a new database session for each request that depends on it
    and ensures that the session is closed after the request is finished, even if
    an error occurs.

    Yields:
        sqlalchemy.orm.Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()