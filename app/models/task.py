from app import db
from datetime import datetime
from .status import status_enum


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    due_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    status = db.Column(status_enum)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id'), nullable=False)
    assigned_to_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_to = db.relationship('User', back_populates='assigned_tasks')
    project = db.relationship('Project', back_populates='tasks')

    def to_dict(self):
        task_dict = {
            'id': self.id,
            'title': self.title,
            'due_date': self.due_date,
            'description': self.description,
            'status': self.status,
            'assigned_to': self.assigned_to.to_dict() if self.assigned_to else None,
        }
        return task_dict

    @classmethod
    def from_dict(cls, data_dict):
        new_obj = cls(
            title=data_dict['title'],
            description=data_dict.get('description'),
            due_date=data_dict. get('due_date'),
            status=data_dict.get('status'),
            assigned_to_id=data_dict.get('assigned_to_id'),
            project_id=data_dict.get('project_id'))
        return new_obj
