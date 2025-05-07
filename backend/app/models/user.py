from sqlalchemy import Column, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base # Assuming base_class.py is in app/db/

class User(Base):
    __tablename__ = "users" # Explicitly setting tablename, though Base would default to "user"

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # If you need a __repr__ method for debugging:
    # def __repr__(self):
    #    return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"