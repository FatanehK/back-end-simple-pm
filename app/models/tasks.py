from app import db
from datetime import datetime
from .status import status_enum


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    due_date = db.Column(db.DateTime)
    task_description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    status = db.Column(status_enum)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', back_populates='tasks')
    project = db.relationship('Project', back_populates='tasks')

    def to_dict(self):
        task_dict = {
            'id': self.id,
            'title': self.title,
            'task_description': self.task_description,
            'project_id': self.project_id,
            'status_id': self.status_id,
            'user_id': self.user_id,
            'status': self.status,
            'project': self.project,
            'user': self.user
        }
        return task_dict

    @classmethod
    def from_dict(cls, data_dict):
        if 'title' in data_dict and 'project_id' in data_dict:
            new_obj = cls(
                title=data_dict['title'],
                task_description=data_dict['task_description'],
                project_id=data_dict['project_id'])
        return new_obj
