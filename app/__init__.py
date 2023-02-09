from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    app.secret_key = os.environ.get("SECRET_KEY")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DBHOST = os.environ.get("DBHOST")
    DBNAME = os.environ.get("DBNAME")
    DBPASS = os.environ.get("DBPASS")
    DBUSER = os.environ.get("DBUSER")

    if test_config is None:
        app.config["SQLALCHEMY_TEST_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"

    from app.models.project import Project
    from app.models.task import Task
    from app.models.users import User
    from app.models.project_members import ProjectMembers

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.project_routes import project_bp
    app.register_blueprint(project_bp)

    from .routes.tasks_routes import tasks_bp
    app.register_blueprint(tasks_bp)

    from .routes.users_routes import users_bp
    app.register_blueprint(users_bp)

    @app.route("/")
    def root():
        return "Project Manager Service is running!"

    CORS(app)
    return app
