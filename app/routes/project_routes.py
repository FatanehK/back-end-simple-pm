from flask import Blueprint, request, jsonify, make_response
from app import db

project_bp= Blueprint('project_bp', __name__, url_prefix='/projects')

@project_bp.route('',methods=['POST'])
def create_projects():
    pass
