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
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'admin': self.admin.to_dict() if self.admin else None,
        }
        return project_dict

    @classmethod
    def from_dict(cls, data_dict):
        new_obj = cls(
            title=data_dict.get('title'),
            admin_id=data_dict.get('admin_id'),
            description=data_dict.get('description'))
        return new_obj
