from flask import Blueprint, request, abort, make_response
from ..db import db
from app.models.goal import Goal
from .task_routes import validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        response_body = {"details": "Invalid data"}
        abort(make_response(response_body, 400))

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201

@bp.get("")
def get_all_goals():
    query = db.select(Goal)
    # params = request.args.get()
    query = query.order_by(Goal.id)
    goals = db.session.scalars(query)
    
    response_body = []
    for goal in goals:
        response_body.append(goal.to_dict())
    
    return response_body

@bp.get("<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict()