from flask import abort, make_response
from ..db import db
from app.models.goal import Goal
from app.models.task import Task


def validate_model(cls, id):
    try:
        int(id)
    except:
        response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response, 400))
    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {id} not found"}
        abort(make_response(response, 404))

    return model