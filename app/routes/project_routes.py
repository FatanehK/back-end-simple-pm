from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.project import Project
from app.models.task import Task
from app.routes.helper_routes import validate

project_bp = Blueprint('project_bp', __name__, url_prefix='/project')


@project_bp.route('', methods=['POST'])
def create_project():
    request_body = request.get_json()
    if 'title' not in request_body and 'users' not in request_body:
        return make_response({"details": "title and user must be provided"}, 400)

    new_project = Project.from_dict(request_body)

    db.session.add(new_project)
    db.session.commit()

    response = {'Project': new_project.to_dict()}

    return make_response(jsonify(response)), 201


@project_bp.route('', methods=['GET'])
def get_all_projects():
    projects = Project.query.all()

    project_response = [project.to_dict() for project in projects]

    return jsonify(project_response), 200


@project_bp.route('/<id>/tasks', methods=['GET'])
def get_project_tasks(id):
    project = validate(id)

    tasks = Task.query.filter(Task.project_id == project.id)
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@project_bp.route('/<id>/tasks', methods=['PUT'])
def update_one_project_new_value(id):
    update_project = validate(Project, id)

    request_body = request.get_json()

    update_project.title = request_body.get('title', update_project.title)
    update_project.status = request_body.get('status', update_project.status)
    update_project.users = request_body.get('users', update_project.users)
    update_project.tasks = request_body.get('tasks', update_project.tasks)

    db.session.commit()
    return jsonify({"goal": update_project.to_dict()}), 200
