"""
Python module for city class
"""
from config import db
from .base_model import BaseModel


class City(BaseModel):
    """
    Defines the City class that inherits from BaseModel
    """
    __tablename__ = 'cities'
    # Fields definition
    city_name = db.Column(db.String(128),
                     nullable=False)
    # Foreignkey definition
    country_code = db.Column(db.String(2),
                             db.ForeignKey('countries.code'),
                             nullable=False)
    # 1 to many relationship with Country
    country = db.relationship('Country',
                              back_populates='cities')
    # 1 to many relationship with Place
    places = db.relationship('Place',
                             back_populates='city',
                             cascade='all, delete-orphan')


    def __repr__(self):
        return f'<City {self.name}>'
