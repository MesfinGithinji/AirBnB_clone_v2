#!/usr/bin/python3
""" holds class Amenity"""

import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity

class Amenity(BaseModel, Base):
    """Amenity class and table defined"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place',secondary='place_amenity')
