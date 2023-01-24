from app import db
from .project_members import ProjectMembers


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, nullable=True, default=None)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    assigned_tasks = db.relationship('Task', back_populates='assigned_to')
    member_projects = db.relationship(
        'Project', secondary='project_members', back_populates='members')

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'email': self.email
        }
        return user_dict

    @classmethod
    def from_dict(cls, data_dict):
        new_obj = cls(full_name=data_dict.get('full_name'),
                      is_active=data_dict.get('is_active'),
                      email=data_dict.get('email'),
                      password=data_dict.get('password'),
                      )
        return new_obj
