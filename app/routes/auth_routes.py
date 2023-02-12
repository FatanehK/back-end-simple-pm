
import os
import requests
from flask import Blueprint, request, jsonify, session, make_response, current_app
import google.auth
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token
from app import db
from app.models.users import User
import jwt

auth_bp = Blueprint('auth_bp', __name__)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


@auth_bp.route("/google/auth", methods=["POST"])
def google_auth():
    credential = request.json.get("id_token")
    request_session = requests.Session()  # creates a new requests session object
    # Google’s public keys are changed once per day, so we can use caching to reduce latency and reduce the potential for network errors
    cached_session = cachecontrol.CacheControl(request_session)
    # We can use the CacheControl library to make our google.auth.transport.Request aware of the cache
    # used to perform requests to Google API endpoint that requires authorization
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credential,
        request=token_request,
        audience=GOOGLE_CLIENT_ID)

    user:User = User.query.filter_by(email=id_info["email"]).first()
    if user:
        if user.full_name != id_info["name"]:
            user_dict = {
                "full_name": id_info["name"],
            }
            user = User.from_dict(user_dict)
            db.session.update(user)
            db.session.commit()
    else:
        user_dict = {
            "full_name": id_info["name"],
            "email": id_info["email"],
        }
        user = User.from_dict(user_dict)
        db.session.add(user)
        db.session.commit()

    token = jwt.encode({'public_id': user.id},current_app.secret_key, 'HS256')

    return make_response(jsonify({"user": user.to_dict(), "token": token})), 200
