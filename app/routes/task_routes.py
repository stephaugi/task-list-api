from flask import Blueprint, abort, make_response, request, Response
import requests
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_filters, send_slack_complete
from ..db import db
import datetime
import os

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = create_model(Task, request_body)
    # try:
    #     new_task = Task.from_dict(request_body)
    # except KeyError:
    #     response_body = {"details": "Invalid data"}
    #     abort(make_response(response_body, 400))

    # db.session.add(new_task)
    # db.session.commit()

    return new_task.to_dict(), 201

@bp.get("")
def get_all_tasks():
    params = request.args

    return get_models_with_filters(Task, params)

@bp.get("<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return task.to_dict()

@bp.delete("<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.put("<task_id>")
def update_task(task_id):
    request_body = request.get_json()
    task = validate_model(Task, task_id)
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    date = datetime.datetime.now()
    task.completed_at = date

    db.session.commit()
    
    send_slack_complete(Task, task)
    
    return Response(status=204, mimetype="application/json")

@bp.patch("<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

