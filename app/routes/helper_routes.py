from functools import wraps
from flask import jsonify, abort, make_response, request, current_app
import jwt
from app.models.project import Project
from app.models.project_members import ProjectMembers
from app.models.users import User


def validate(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        abort(make_response(
            jsonify({"message": f"details: invalid data,{obj_id} ID must be an Integer"})))

    matching_obj = cls.query.get(obj_id)
    if not matching_obj:
        response_str = f"{cls.__name__} with id {obj_id} was not found in the database"
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_obj


def validateProjectAccess(project_id, user_id, should_be_admin=False):
    try:
        project_id = int(project_id)
    except ValueError:
        abort(make_response(
            jsonify({"message": f"details: invalid data,{project_id} ID must be an Integer"})))

    project = Project.query.get(project_id)
    if not project:
        response_str = f"Project with id {project_id} was not found in the database"
        abort(make_response(jsonify({"message": response_str}), 404))

    if project.admin_id == user_id:
        return project

    if should_be_admin == True:
        abort(make_response(
            jsonify({"User is not admin for given project."}), 404))

    # query if user_id is one of the project member
    members = ProjectMembers.query.filter_by(project_id=project_id)
    is_member = False
    for member in members:
        if member.id == user_id:
            is_member = True
            break

    if is_member == False:
        abort(make_response(
            jsonify({"User is not member or admin for given project."}), 404))

    return project


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # is_test = current_app.config["TESTING"]
        # if is_test:
        #     current_user = User.query.filter_by(id=1).first()
        #     return f(current_user, *args, **kwargs)

        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:  # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(
                token, current_app.secret_key, algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['public_id']).first()
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
         # Return the user information attached to the token
        return f(current_user, *args, **kwargs)
    return decorator
