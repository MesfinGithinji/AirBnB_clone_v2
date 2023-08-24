#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object

timeString = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """A base class for all future models of the project"""

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Base model initialized """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, timeString)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, timeString)

    def __str__(self):
        """BaseModel class string representation"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updates updated_at with current date time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self,save_to_disk=False):
        """Returns a dict of instance keys an values """
        dict_values = self.__dict__.copy()
        if "created_at" in dict_values:
            dict_values["created_at"] = dict_values["created_at"].isoformat()
        if "updated_at" in dict_values:
            dict_values["updated_at"] = dict_values["updated_at"].isoformat()
        if '_password' in dict_values:
            dict_values['password'] = dict_values['_password']
            dict_values.pop('_password', None)
        if 'amenities' in dict_values:
            dict_values.pop('amenities', None)
        if 'reviews' in dict_values:
            dict_values.pop('reviews', None)
        dict_values["__class__"] = self.__class__.__name__
        dict_values.pop('_sa_instance_state', None)
        if not save_to_disk:
            dict_values.pop('password', None)
        return dict_values


    def delete(self):
        """deletes current instance from storage"""
        models.storage.delete(self)

