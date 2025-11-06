from flask import Blueprint, request, Response
from ..db import db
from app.models.goal import Goal
from app.models.task import Task
from .task_routes import validate_model, create_model, get_models_with_filters

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)

@bp.post("<goal_id>/tasks")
def create_task_with_goal(goal_id):
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    goal = validate_model(Goal, goal_id)

    if task_ids:
        remove_all_task_ids(goal)
        add_task_ids(goal, task_ids)
        db.session.commit()

        response_body = {"id" : goal.id,
                        "task_ids" : task_ids}
        return response_body, 200
    else:
        return create_model(Task, request_body)

@bp.get("")
def get_all_goals():
    params = request.args

    return get_models_with_filters(Goal, params)

@bp.get("<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()

@bp.get("<goal_id>/tasks")
def get_one_goal_with_tasks(goal_id):
    goal = validate_model(Goal, goal_id)

    response = goal.to_dict()
    response["tasks"] = []

    if goal.tasks:
        for task in goal.tasks:

            response["tasks"].append(task.to_dict())

    return response, 200

@bp.put("<goal_id>")
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)

    goal.title = request_body["title"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

def remove_all_task_ids(goal):
    query = db.select(Task).where(Task.goal_id==goal.id)
    current_tasks = db.session.scalars(query)
    for task in current_tasks:
        task.goal_id = None
    
    db.session.flush()

def add_task_ids(goal, task_ids):
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
    
    db.session.flush()