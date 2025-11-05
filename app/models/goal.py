from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")


    def to_dict(self):
        response_dict = {
            "id": self.id,
            "title": self.title,
        }
        
        if self.tasks:
            response_dict["tasks"] = self.tasks
            
        return response_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(title=task_data["title"])