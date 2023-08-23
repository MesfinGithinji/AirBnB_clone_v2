#!/usr/bin/python3
""" Module city """

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String ,Integer
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from models.place import Place

class City(BaseModel, Base):
    """ City definition attributes and columns """

    __tablename__ = 'cities'
    name = Column(String(128),nullable=False)
    state_id = Column(String(60),ForeignKey('states.id'),nullable=False)
    places = relationship('Place',backref="cities",cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
