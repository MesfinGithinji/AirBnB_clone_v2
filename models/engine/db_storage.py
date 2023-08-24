#!/usr/bin/python3
"""DBStorage implementation"""

import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class_names = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """Database Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize objects and db storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""
        if not self.__session:
            self.reload()
        objs = {}
        if type(cls) == str:
            cls = class_names.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objs[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in class_names.values():
                for obj in self.__session.query(cls):
                    objs[obj.__class__.__name__ + '.' + obj.id] = obj
        return objs

    def reload(self):
        """reloads objects from the database"""
        my_session = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(my_session)

    def new(self, obj):
        """creates new object in current session"""
        self.__session.add(obj)

    def save(self):
        """commits current session's changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes object during current session"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Terminate current active session """
        self.__session.remove()

    def get(self, cls, id):
        """Returns an object (Get)"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in class_names:
            cls = class_names[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Returns a count of objects in current session"""
        total_num = 0
        if type(cls) == str and cls in class_names:
            cls = class_names[cls]
            total_num = self.__session.query(cls).count()
        elif cls is None:
            for cls in class_names.values():
                total_num += self.__session.query(cls).count()
        return total_num
