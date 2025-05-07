from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.sql import func # Import func

@as_declarative()
class Base:
    """
    Base class which provides automated table name
    and surrogate primary key column, plus common audit columns.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    active = Column(Boolean, default=True, nullable=False) # New field
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # New field
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True) # New field