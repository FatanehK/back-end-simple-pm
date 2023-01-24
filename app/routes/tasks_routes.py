from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.project import Project
from app.models.tasks import Tasks
from .helper_routes import validate

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    if 'project_id' not in request_body or 'title' not in request_body:
        return make_response({"details": "Project_id and title must be in request body"}, 400)
    try:
        validate(Project, request_body['id'])
        new_task = Tasks.from_dict(request_body)
        validate(Tasks, new_task)
    except:
        return jsonify({"details": "Invalid Data"}), 400

    db.session.add(new_task)
    db.session.commit()

    response = {'Task': new_task.to_dict()}
    return make_response(jsonify(response)), 201


@tasks_bp.route("/id/status", methods=["PATCH"])
def change_task_status(id):

    update_task = validate(Tasks, id)
    request_body = request.get_json()

    update_task.status = request_body.get('status', update_task.status)

    db.session.commit()
    return jsonify({"Task": update_task.to_dict()}), 200
