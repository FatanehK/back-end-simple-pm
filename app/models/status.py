
from app import db
from sqlalchemy.dialects.postgresql import ENUM

status_enum = ENUM('Completed', 'In-Progress',
                   'Abandoned', status_name='status_enum')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True)
    status_name = db.Column(db.status_enum)
    projects = db.relationship(
        "Project", uselist=False, back_populates="status")
    tasks = db.relationship("Task", back_populates="status")
