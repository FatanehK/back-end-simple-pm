from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.project import Project
from app.models.users import User
from app.models.task import Task
from .helper_routes import token_required, validate, validateProjectAccess

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route('', methods=['POST'])
@token_required
def create_task(user: User):
    request_body = request.get_json()
    if 'project_id' not in request_body and 'title' not in request_body:
        return make_response({"details": "Project_id and title must be in request body"}, 400)
    try:
        validateProjectAccess(request_body['project_id'], user.id)
        new_task = Task.from_dict(request_body)
    except:
        return jsonify({"details": "Invalid Data"}), 404

    db.session.add(new_task)
    db.session.commit()

    response = {'Task': new_task.to_dict()}
    return make_response(jsonify(response)), 201


@tasks_bp.route('/<id>', methods=["PUT"])
@token_required
def update_task(user: User, id):
    update_task: Task = validate(Task, id)
    validateProjectAccess(update_task.project_id, user.id)
    if update_task.status == 'Completed':
        return jsonify({'error': "Completed project can't be updated "}), 404

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

#  to specific user by id is not working


@tasks_bp.route('/<id>', methods=['PATCH'])
@token_required
def assign_task_to_user(user: User, id):
    task: Task = validate(Task, id)
    validateProjectAccess(task.project_id, user.id)

    request_body = request.get_json()

    user_id = request_body.get("user_id")
    validate(User, user_id)
    task.assigned_to_id = user_id

    db.session.commit()

    response = {f'Task (id: {task.id} assigned to user (id:{user_id})'}
    return make_response(jsonify(response)), 201


@tasks_bp.route('/<id>', methods=['GET'])
@token_required
def get_one_task(user: User, id):
    task: Task = validate(Task, id)
    validateProjectAccess(task.project_id, user.id)

    return jsonify(task.to_dict()), 200
