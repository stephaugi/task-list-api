from flask import Blueprint, request, abort, make_response, Response
from ..db import db
from app.models.goal import Goal
from .task_routes import validate_model, create_model, get_models_with_filters

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    new_goal = create_model(Goal, request_body)

    return new_goal.to_dict(), 201

@bp.get("")
def get_all_goals():
    params = request.args
    
    return get_models_with_filters(Goal, params)

@bp.get("<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()

@bp.put("<goal_id>")
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    goal.title = request_body["title"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("<goal_id>")
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")