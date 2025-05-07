from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# For SQLite, connect_args is needed to enable foreign key support by default
engine_args = {"connect_args": {"check_same_thread": False}} if "sqlite" in settings.SQLALCHEMY_DATABASE_URL else {}
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    **engine_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()