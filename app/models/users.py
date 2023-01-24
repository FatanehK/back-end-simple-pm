from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, nullable=True, default=None)
    email_address = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship(
        "Project", secondary="user_project", back_populates='users')

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'full_name': self.full_name,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'email_address': self.email_address
        }
        return user_dict

    @classmethod
    def from_dict(cls, data_dict):
        if 'email_address' in data_dict:
            new_obj = cls(full_name=data_dict.get('full_name'),
                          is_admin=data_dict.get('is_admin'),
                          is_active=data_dict.get('is_active'),
                          email_address=data_dict.get('email_address'),
                          password=data_dict.get('password'),
                          )
        return new_obj
