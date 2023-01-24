from app import db
from sqlalchemy.dialects.postgresql import ENUM

status_enum = ENUM('New', 'InProgress', 'Completed',
                   'Abandoned', name='status_enum')

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(status_enum)
    projects = db.relationship(
        "Project", uselist=False, back_populates="status")
    tasks = db.relationship("Tasks", back_populates="status")
