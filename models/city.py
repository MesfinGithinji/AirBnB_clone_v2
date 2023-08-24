#!/usr/bin/python3
""" Module city """

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class City(BaseModel, Base):
    """ City definition attributes and columns """

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'
        name = Column(String(128),nullable=False)
        state_id = Column(String(60),ForeignKey('states.id'),nullable=False)
        places = relationship("Place",backref="cities",cascade="all, delete-orphan")
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """set up city"""
        super().__init__(*args, **kwargs)
