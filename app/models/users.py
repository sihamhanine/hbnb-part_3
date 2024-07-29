"""
Python module for User class
"""
from .base_model import BaseModel
from config import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(None)


class User(BaseModel):
    """
    Defines User class that inherits from BaseModel
    """
    __tablename__ = 'users'
    # Fields definition
    email = db.Column(db.String(100),
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(100),
                           nullable=False)
    last_name = db.Column(db.String(100),
                          nullable=False)
    # JWT secure authentification
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean,
                         default=False)
    # 1 to 1 relationship with Place
    place = db.relationship('Place',
                            uselist=False,
                            back_populates='host',
                            cascade='all, delete-orphan')
    # 1 to many relationship with Review
    reviews = db.relationship('Review',
                              back_populates='user',
                              cascade='all, delete-orphan')

    def set_password(password):
        """
        Sets the password hash for the user
        """
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return password_hash

    def check_password(password_hash, password):
        """
        Check the password hash for the user
        """
        return bcrypt.check_password_hash(password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
