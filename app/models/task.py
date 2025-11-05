from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    # is_complete: Mapped[bool] = mapped_column(nullable=True, default=False)
    completed_at: Mapped[datetime] = mapped_column(nullable=True, default=None)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        response_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if not self.completed_at else True
        }
        
        return response_dict

    @classmethod
    def from_dict(cls, task_data):
        params = ["title","description"]
        kwarg_dict = {param:task_data[param] for param in params}

        return cls(**kwarg_dict)

