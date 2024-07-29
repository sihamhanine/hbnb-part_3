"""
Python module for place class
"""
from .base_model import BaseModel
from .place_amenity import place_amenities
from config import db


class Place(BaseModel):
    """
    Defines the Place class that inherits from BaseModel
    """
    __tablename__ = 'places'
    # Fields definition
    name = db.Column(db.String(128),
                        nullable=False)
    description = db.Column(db.String(1024),
                            nullable=False)
    address = db.Column(db.String(256),
                        nullable=False)
    latitude = db.Column(db.Float,
                            nullable=False)
    longitude = db.Column(db.Float,
                            nullable=False)
    num_rooms = db.Column(db.Integer,
                            nullable=False)
    num_bathrooms = db.Column(db.Integer,
                                nullable=False)
    price_per_night = db.Column(db.Float,
                                nullable=False)
    max_guests = db.Column(db.Integer,
                            nullable=False)
    # Foreignkey definition
    amenity_ids = db.Column(db.String(36),
                        db.ForeignKey('amenities.id'),
                        nullable=False)
    host_id = db.Column(db.String(36),
                        db.ForeignKey('users.id'),
                        nullable=False)
    city_id = db.Column(db.String(36),
                        db.ForeignKey('cities.id'),
                        nullable=False)
    # 1 to 1 relationship with User
    host = db.relationship('User',
                           back_populates='place')
    # 1 to many relationship with City
    city = db.relationship('City',
                           back_populates='places')

    # Many to many relationship with amenity
    amenities = db.relationship('Amenity',
                                secondary=place_amenities,
                                back_populates='places')

    # 1 to many relationship with Review
    reviews = db.relationship('Review',
                              back_populates='place',
                              cascade='all, delete-orphan')


    def __repr__(self):
        return f'<Place {self.name}>'
