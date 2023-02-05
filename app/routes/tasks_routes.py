from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.project import Project
from app.models.users import User
from app.models.task import Task
from .helper_routes import validate

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    if 'project_id' not in request_body or 'title' not in request_body:
        return make_response({"details": "Project_id and title must be in request body"}, 400)
    try:
        validate(Project, request_body['project_id'])
        new_task = Task.from_dict(request_body)
    except:
        return jsonify({"details": "Invalid Data"}), 404

    db.session.add(new_task)
    db.session.commit()

    response = {'Task': new_task.to_dict()}
    return make_response(jsonify(response)), 201


@tasks_bp.route('/<id>', methods=["PUT"])
def update_task(id):
    update_task = validate(Task, id)
    request_body = request.get_json()

    update_task.title = request_body.get('title', update_task.title)
    update_task.status = request_body.get('status', update_task.status)
    update_task.description = request_body.get(
        'description', update_task.description)
    update_task.due_date = request_body.get('due_date', update_task.due_date)
    update_task.assigned_to_id = request_body.get(
        'assigned_to_id', update_task.assigned_to_id)

    db.session.commit()
    return jsonify({"task": update_task.to_dict()}), 200

#  to especific user by id is not working

@tasks_bp.route('/<id>', methods=['PATCH'])
def assign_task_to_user(id):

    validate(User, id)
    request_body = request.get_json()
    # if 'email' not in request_body:
    #     return make_response({"details": "email must be provided"}, 400)

    new_member = User.from_dict(request_body)

    db.session.add(new_member)
    db.session.commit()

    response = {'user': new_member.to_dict()}

    return make_response(jsonify(response)), 201


@tasks_bp.route('/<id>', methods=['GET'])
def get_one_task(id):

    task = validate(Task, id)
    return jsonify(task.to_dict()), 200
