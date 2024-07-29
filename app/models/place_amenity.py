"""
Module that makes a jonction between the classes Place and Amenity.
Useful to handle 'many to many' relationship"""

from config import db

place_amenities = db.Table('place_amenities',
    db.Column('place_id',
    db.String(36),
    db.ForeignKey('places.id'),
    primary_key=True),

    db.Column('amenity_id',
    db.String(36),
    db.ForeignKey('amenities.id'),
    primary_key=True)
)
