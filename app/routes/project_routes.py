from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.project import Project
from app.models.project_members import ProjectMembers
from app.models.task import Task
from app.models.users import User
from app.routes.helper_routes import validate

project_bp = Blueprint('project_bp', __name__, url_prefix='/project')


@project_bp.route('', methods=['POST'])
def create_project():
    request_body = request.get_json()

    if 'title' not in request_body and 'admin_id' not in request_body:
        return make_response({"details": "title and admin_id must be provided"}, 400)

    new_project = Project.from_dict(request_body)

    db.session.add(new_project)
    db.session.commit()

    response = {'project': new_project.to_dict()}

    return make_response(jsonify(response)), 201


@project_bp.route('', methods=['GET'])
def get_all_projects():
    projects = Project.query.all()

    project_response = [project.to_dict() for project in projects]

    return jsonify(project_response), 200


@project_bp.route('/<id>', methods=['GET'])
def get_one_project(id):
    project = validate(Project, id)
    return jsonify(project.to_dict()), 200


@project_bp.route('/<id>/tasks', methods=['GET'])
def get_project_tasks(id):
    project = validate(Project, id)

    tasks = Task.query.filter(Task.project_id == project.id)
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@project_bp.route('/<id>/status', methods=['GET'])
def get_project_status(id):
    project = validate(Project, id)

    project_status = project.status
    return jsonify(project_status), 200


@project_bp.route('/<id>', methods=['PUT'])
def update_one_project_new_value(id):
    update_project = validate(Project, id)

    request_body = request.get_json()

    update_project.title = request_body.get('title', update_project.title)
    update_project.status = request_body.get('status', update_project.status)
    update_project.description = request_body.get(
        'description', update_project.description)

    db.session.commit()
    return jsonify({"project": update_project.to_dict()}), 200


@project_bp.route('/<id>/members', methods=['GET'])
def get_project_members(id):
    project = validate(Project, id)

    project_members = ProjectMembers.query.filter_by(
        project_id=project.id).all()
    
    members = []
    for project_member in project_members:
        member = User.query.filter_by(id=project_member.user_id).first()
        members.append(member.to_dict())
    return jsonify(members)


@project_bp.route('/<id>/member', methods=['POST'])
def add_user_to_project(id):
    project = validate(Project, id)
    request_body = request.get_json()

    user_id = request_body.get('user_id')
    user = validate(User, user_id)

    project_member = ProjectMembers(project_id=project.id, user_id=user.id)

    db.session.add(project_member)
    db.session.commit()
    return jsonify({'message': 'User added to project'}), 201

# new route


@project_bp.route('/admin/projects', methods=['GET'])
def get_projects_by_admin_id():

    request_body = request.get_json()
    admin_id = request_body.get('admin_id')

    projects = Project.query.filter_by(admin_id=admin_id)

    if not projects:
        return jsonify({'error': 'No projects found for this admin'}), 404

    projects_data = [project.to_dict() for project in projects]

    return jsonify(projects_data), 200


# @project_bp.route('/<id>/tasks', methods=['POST'])
# def create_task_for_project(id):
#     request_body = request.get_json()
#     # if 'project_id' not in request_body or 'title' not in request_body:
#     validate(Project, id)
#     if 'title' not in request_body:
#         return make_response({"details": "title must be in request body"}, 400)
#     try:
#         request_body['project_id'] = int(id)
#         new_task = Task.from_dict(request_body)
#     except:
#         return jsonify({"details": "Invalid Data"}), 400

#     db.session.add(new_task)
#     db.session.commit()

#     response = {'Task': new_task.to_dict()}
#     return make_response(jsonify(response)), 201
