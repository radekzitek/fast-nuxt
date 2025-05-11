"""
ProgressUpdate ORM Model.
"""
from sqlalchemy import Integer, Text, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class ProgressUpdate(Base):
    __tablename__ = "progress_updates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    objective_id: Mapped[int] = mapped_column(Integer, ForeignKey("objectives.id"), nullable=False, index=True)
    progress_date: Mapped[Date] = mapped_column(Date, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    progress: Mapped[float | None] = mapped_column(Float, nullable=True)

    objective = relationship("Objective", backref="progress_updates")
