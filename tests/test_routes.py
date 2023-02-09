
from app.models.project import Project
from app.models.task import Task
import pytest
from app import db


def test_get_project_no_saved_project(client):
    response = client.get("/projects")
    response_body = response.get_json()

    assert response.status_code == 200


def test_create_project_missing_title(client):

    response = client.post(
        "/projects", json={"description": "important to take care of yourself"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details": "title and admin_id must be provided"}


def test_get_one_project_404(client):
    response = client.get("/projects/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "projects" not in response_body
    assert response_body == {
        'message': 'Project with id 1 was not found in the database'}


def test_get_project_by_id(client, one_project):
    response = client.get("/projects/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"id": 1, "title": "Build an app",
                             "description": "app that calculate tips", "status": "New", 'admin': {'email': 'fataneh@test.com', 'full_name': 'Fataneh', 'id': 1, 'is_active': None}}


def test_post_one_project_create_id_1_in_db(client, one_admin):
    response = client.post(
        "/projects", json={"title": "hello world", "description": "today life", "admin_id": 1})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["project"]["id"] == 1
    assert response_body["project"]["description"] == "today life"

    new_project = Project.query.get(1)
    new_project.title == "hello world"
    new_project.admin == {"full_name": "Fataneh",
                          "email": "fataneh@test.com", "is_active": None, "id": 1}


def test_update_project(client, one_project, one_admin):
    response = client.put("/projects/1", json={
        "title": "Updated project Title",
        "description": "Updated Test Description",
    })

    response_body = response.get_json()

    assert response.status_code == 200
    assert "project" in response_body
    assert response_body == {
        "project": {
            'id': 1,
            'title': "Updated project Title",
            'description': "Updated Test Description",
            'status': "New",
            'admin': {'email': 'fataneh@test.com', 'full_name': 'Fataneh', 'id': 1, 'is_active': None}}}

    project = Project.query.get(1)
    # assert project.admin == {'email': 'fataneh@test.com','full_name': 'Fataneh', 'id': 1, 'is_active': None}
    assert project.title == "Updated project Title"

# Task tests ============================================================================
def test_get_task_not_found(client):

    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 404

    assert not "task" in response_body
    assert response_body == {
        "message": "Task with id 1 was not found in the database"}


def test_get_tasks_one_saved_project(client, one_task, one_project):
    response = client.get("/tasks/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Build the enivroment",
        "description": "fix the requirment and dependencies",
        "assigned_to": None,
        "due_date": None,
        "status": "New",
    }


def test_updated_task(client, one_task):
    response = client.put("/tasks/1", json={
        "title": "This is an updated",
        "description": "Updated Test Description"})
    response_body = response.get_json()
    assert response.status_code == 200
    assert response_body == {
        "task": {'assigned_to': None, 'description': 'Updated Test Description',
                 'due_date': None, 'id': 1,
                 'status': 'New',
                 'title': 'This is an updated'}}


def test_update_task_not_found(client):

    response = client.put(
        "/tasks/10", json={"title": "This is my updated new task"})
    response_body = response.get_json()
    assert response.status_code == 404
    assert response_body == {
        'message': 'Task with id 10 was not found in the database'}


