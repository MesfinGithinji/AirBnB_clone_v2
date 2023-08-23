#!/usr/bin/python3
""" State Module"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """State class defined attributes and columns """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref='state',
                          cascade='all, delete, delete-orphan')

    @property
    def cities(self):
        """
        returns a list of City instances where state_id equals
        to current State.id
        """
        from models import storage
        city_states = []
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == self.id:
                city_states.append(city)
        return city_states
