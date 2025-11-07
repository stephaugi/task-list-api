from flask import abort, make_response, Response
from ..db import db
import requests
import os


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

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response_body = {"details": "Invalid data"}
        abort(make_response(response_body, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute,value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
        sort_by = filters.get("sort")
        if sort_by == 'asc':
            query = query.order_by(cls.title.asc())
        elif sort_by == 'desc':
            query = query.order_by(cls.title.desc())
        else:
            query = query.order_by(cls.id)

    models = db.session.scalars(query.order_by(cls.id))

    return [model.to_dict() for model in models]

def delete_model(cls, id):
    model = validate_model(cls, id)
    db.session.delete(model)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def send_slack_complete(cls, model):
    json = {
        "channel" : os.environ.get("SLACK_CHANNEL"),
        "text" : f"Someone just completed the {cls.__name__.lower()} {model.title}"
        }
    
    headers = {
        "Authorization":f"Bearer {os.environ.get("SLACK_BOT_TOKEN")}"
    }
    
    requests.post("https://slack.com/api/chat.postMessage", json=json, headers=headers)