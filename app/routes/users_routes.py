from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.users import User
from app.models.task import Task
from app.models.project_members import ProjectMembers
from .helper_routes import token_required, validate

users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('/tasks', methods=['GET'])
@token_required
def get_user_tasks(user: User):
    tasks = Task.query.filter_by(assigned_to_id=user.id).all()
    user_tasks = [task.to_dict() for task in tasks]
    return jsonify(user_tasks), 200
