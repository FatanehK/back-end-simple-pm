from app import db
from .status import status_enum


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    project_description = db.Column(db.Text)
    status = db.Column(status_enum)
    users = db.relationship(
        'User', secondary="user_project", back_populates="project")
    tasks = db.relationship('Task', back_populates='project')

    def to_dict(self):
        project_dict = {
            'id': self.id,
            'tilte': self.title,
            'project_description': self.project_description,
            'tasks': self.tasks,
            'users': self.users,
            'status_id': self.status_id,
            'status': self.status
        }
        return project_dict

    @classmethod
    def from_dict(cls, data_dict):
        if 'title' in data_dict and 'users' in data_dict:
            new_obj = cls(title=data_dict.get('title'),
                          project_description=data_dict.get('project_description'),
                          users=data_dict['users'],
                          tasks=data_dict['tasks'],
                          status=data_dict['status'])
        return new_obj
