
from app import db
class ProjectUsers(db.Model):
    __tablename__ = 'user_project'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)