#!/usr/bin/python3
""" Class User defined"""

import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Class attributes for users """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship('Place', cascade='all, delete, delete-orphan',
                          backref='user')

    reviews = relationship('Review', cascade='all, delete, delete-orphan',
                           backref='user')



