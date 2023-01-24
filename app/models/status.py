from app import db
from sqlalchemy.dialects.postgresql import ENUM

status_enum = ENUM('New', 'InProgress', 'Completed',
                   'Abandoned', name='status_enum')
