from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.users import User
from app.models.task import Task
from .helper_routes import validate


users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
def create_user():
    request_body = request.get_json()
    if 'email' not in request_body:
        return make_response({"details": "email must be provided"}, 400)

    new_user = User.from_dict(request_body)

    db.session.add(new_user)
    db.session.commit()

    response = {'user': new_user.to_dict()}

    return make_response(jsonify(response)), 201


@users_bp.route("", methods=["GET"])
def get_all_boards():
    users = User.query.all()

    users_response = [user.to_dict() for user in users]
    return jsonify(users_response), 200


@users_bp.route('/<id>/tasks', methods=['GET'])
def get_user_tasks(id):

    validate(User, id)
    tasks = Task.query.filter_by(Task.assigned_to_id == id).all()
    user_tasks = [task.to_dict() for task in tasks]

    return jsonify(user_tasks), 200
