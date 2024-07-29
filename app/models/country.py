"""
Python module for country class
"""
from config import db


class Country(db.Model):
    """
    Defines the Country class that inherits from db.Model
    """
    __tablename__ = 'countries'
    # Fields definition
    name = db.Column(db.String(128),
                     unique=True,
                     nullable=False)
    code = db.Column(db.String(2),
                     primary_key=True)
    # 1 to many relationship with City
    cities = db.relationship('City',
                             back_populates='country',
                             cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Country {self.name}>'
