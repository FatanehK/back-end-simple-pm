from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.project import Project
from app.models.project_members import ProjectMembers
from app.models.task import Task
from app.models.users import User
from app.routes.helper_routes import token_required, validate, validateProjectAccess

project_bp = Blueprint('project_bp', __name__, url_prefix='/projects')


@project_bp.route('', methods=['POST'])
@token_required
def create_project(user: User):
    request_body = request.get_json()

    if 'title' not in request_body:
        return make_response({"details": "title must be provided"}, 400)

    request_body["admin_id"] = user.id
    new_project = Project.from_dict(request_body)

    db.session.add(new_project)
    db.session.commit()

    response = {'project': new_project.to_dict()}

    return make_response(jsonify(response)), 201


@project_bp.route('', methods=['GET'])
@token_required
def get_all_projects(user: User):
    projects = Project.query.filter_by(admin_id=user.id)

    project_response = [project.to_dict() for project in projects]

    return jsonify(project_response), 200


@project_bp.route('/<id>', methods=['GET'])
@token_required
def get_one_project(user: User, id):
    project = validateProjectAccess(id, user.id)
    return jsonify(project.to_dict()), 200


@project_bp.route('/<id>/tasks', methods=['GET'])
@token_required
def get_project_tasks(user: User, id):
    project = validateProjectAccess(id, user.id)

    tasks = Task.query.filter(Task.project_id == project.id)
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@project_bp.route('/<id>/status', methods=['GET'])
@token_required
def get_project_status(user: User, id):
    project = validateProjectAccess(id, user.id)

    project_status = project.status
    return jsonify(project_status), 200


@project_bp.route('/<id>', methods=['PUT'])
@token_required
def update_one_project_new_value(user: User, id):
    update_project = validateProjectAccess(id, user.id)

    request_body = request.get_json()

    update_project.title = request_body.get('title', update_project.title)
    update_project.status = request_body.get('status', update_project.status)
    update_project.description = request_body.get(
        'description', update_project.description)

    db.session.commit()
    return jsonify({"project": update_project.to_dict()}), 200


@project_bp.route('/<id>/members', methods=['GET'])
@token_required
def get_project_members(user: User, id):
    project = validateProjectAccess(id, user.id)

    project_members = ProjectMembers.query.filter_by(
        project_id=project.id).all()

    members = []
    for project_member in project_members:
        member = User.query.filter_by(id=project_member.user_id).first()
        members.append(member.to_dict())
    return jsonify(members)


@project_bp.route('/<id>/member', methods=['POST'])
@token_required
def add_user_to_project(user: User, id):
    project = validateProjectAccess(id, user.id, True)
    request_body = request.get_json()

    email = request_body.get('email')
    full_name = request_body.get('full_name', "")

    new_user = User.query.filter_by(email=email).first()
    if new_user:
        project_member = ProjectMembers.query.filter_by(
            project_id=project.id, user_id=new_user.id).first()
        if project_member != None:
            return jsonify({'message': 'User already exist'}), 400
    else:
        user_dict = {
            "full_name": full_name,
            "email": email,
        }
        new_user = User.from_dict(user_dict)
        db.session.add(new_user)
        db.session.commit()

    project_member = ProjectMembers(project_id=project.id, user_id=new_user.id)

    db.session.add(project_member)
    db.session.commit()
    return jsonify({'message': 'User added to project'}), 201


@project_bp.route('/<id>/member', methods=['DELETE'])
@token_required
def remove_user_from_project(user: User, id):
    project = validateProjectAccess(id, user.id, True)
    request_body = request.get_json()

    member_id = request_body.get('member_id')
    project_member = ProjectMembers.query.filter_by(
        project_id=project.id, user_id=member_id).first()

    db.session.delete(project_member)
    db.session.commit()
    return jsonify({'message': 'User removed from project'}), 201
