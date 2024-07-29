"""
Python module for review class
"""
from .base_model import BaseModel
from config import db


class Review(BaseModel):
    """
    Defines the Review class that inherits from BaseModel
    """
    __tablename__ = 'reviews'
    # Fields definition
    rating = db.Column(db.Integer,
                       nullable=False)
    comment = db.Column(db.String(1024),
                        nullable=False)
    place_id = db.Column(db.String(36),
                        db.ForeignKey('places.id'),
                        nullable=False)
    # Foreignkey definition
    user_id = db.Column(db.String(36),
                        db.ForeignKey('users.id'),
                        nullable=False)

    # 1 to many relationship with User
    user = db.relationship('User',
                           back_populates='reviews')

    # 1 to many relationship with Place
    place = db.relationship('Place', back_populates='reviews')


    def __repr__(self):
        return f'<Review {self.comment}>'
