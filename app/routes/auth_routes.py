import os
import requests
from flask import Blueprint, request, jsonify, session, make_response
import google.auth
from google.oauth2.id_token import verify_oauth2_token
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token

auth_bp = Blueprint('auth_bp', __name__)

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

@auth_bp.route("/google/auth", methods=["POST"])
def google_auth():
    credential = request.json.get("id_token")
    request_session = requests.Session()  # creates a new requests session object
    # Google’s public keys are changed once per day, so we can use caching to reduce latency and reduce the potential for network errors
    cached_session = cachecontrol.CacheControl(request_session)
    #We can use the CacheControl library to make our google.auth.transport.Request aware of the cache
    # used to perform requests to Google API endpoint that requires authorization
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credential,
        request=token_request,
        audience=GOOGLE_CLIENT_ID)

    return make_response(jsonify(id_info)), 200