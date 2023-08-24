#!/usr/bin/python3
""" State Module"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class defined attributes and columns """

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128),nullable=False)
        cities = relationship("City", cascade="all, delete",backref="states")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """sets up state"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """method to return city instances"""
            city_details = models.storage.all("City").values()
            city_val = []
            for detail in city_details:
                if detail.state_id == self.id:
                    city_val.append(detail)
            return city_val
