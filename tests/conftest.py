import pytest
from app import create_app
from app.models.project import Project
from app.models.task import Task
from app.models.users import User
from app import db
from flask.signals import request_finished


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        # user_dict = {
        #     "full_name": "test user",
        #     "email": "test@test1.com"
        # }
        # user = User.from_dict(user_dict)
        # db.session.add(user)
        # db.session.commit()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_task_belongs_to_one_project(app, one_project, one_task):
    task = Task.query.first()
    project = Project.query.first()
    project.tasks.append(task)
    db.session.commit()


@pytest.fixture
def one_project(app, one_admin):
    new_project = Project(
        title="Build an app", description="app that calculate tips", status="New", admin_id=1)
    db.session.add(new_project)
    db.session.commit()


@pytest.fixture
def one_task(app, one_admin, one_project):
    new_task = Task(title="Build the enivroment",
                    description="fix the requirment and dependencies",
                    due_date=None,
                    status="New",
                    assigned_to=None,
                    project_id=1)
    db.session.add(new_task)
    db.session.commit()


@pytest.fixture
def one_admin(app):
    new_user = User(full_name="Fataneh", email="fataneh@test.com")
    db.session.add(new_user)
    db.session.commit()
