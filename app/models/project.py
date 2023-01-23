from app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    project_description = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    users = db.relationship(
        'User', secondary="user_project", back_populates="project")
    status = db.relationship('Status', back_populates='projects')
    tasks = db.relationship('Task', back_populates='project')

    def to_dict(self):
        project_dict = {
            'id': self.id,
            'tilte': self.title,
            'project_description': self.project_description

        }
        return project_dict

    @classmethod
    def from_dict(cls, data_dict):
        if 'title' in data_dict:
            new_obj = cls(title = data_dict['title'],project_description = data_dict['project_description'])
        return new_obj
