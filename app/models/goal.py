from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


    def to_dict(self):
        response_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if not self.completed_at else self.is_complete,
        }
        
        return response_dict

    @classmethod
    def from_dict(cls, task_data):
        params = ["title","description"]
        kwarg_dict = {param:task_data[param] for param in params}

        return cls(**kwarg_dict)