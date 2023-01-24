from app import db
from .status import status_enum


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    status = db.Column(status_enum)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin = db.relationship('User', backref=db.backref(
        'admin_projects', uselist=True))
    members = db.relationship(
        'User', secondary='project_members', back_populates='member_projects')
    tasks = db.relationship('Task', back_populates='project')

    def to_dict(self):
        project_dict = {
            'id': self.id,
            'tilte': self.title,
            'description': self.description,
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
                          description=data_dict.get(
                              'description'),
                          users=data_dict['users'],
                          tasks=data_dict['tasks'],
                          status=data_dict['status'])
        return new_obj
