# app/models/project.py
from typing import List, Optional
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # One-to-many relationship
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project {self.id}: {self.name}>"