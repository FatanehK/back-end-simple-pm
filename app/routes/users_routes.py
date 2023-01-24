from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.users import Users
from .helper_routes import validate


users_bp = Blueprint('users_bp', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
def create_user():
    request_body = request.get_json()
    if 'email_address' not in request_body:
        return make_response({"details": "email must be provided"}, 400)

    new_user = Users.from_dict(request_body)
    new_user["is_admin"] = True
    new_user["is_active"] = True

    db.session.add(new_user)
    db.session.commit()

    response = {'User': new_user.to_dict()}

    return make_response(jsonify(response)), 201
