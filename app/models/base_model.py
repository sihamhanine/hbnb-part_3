"""
Python module to define "main" class
"""
from config import db
import uuid


class BaseModel(db.Model):
    """
    Class BaseModel inherit from db.model
    """
    __abstract__ = True

    id = db.Column(db.String(36),
                   primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime,
                           default=db.func.current_timestamp(),
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp(),
                           nullable=False)

    def __repr__(self):
        return f'<BaseModel {self.id}>'
