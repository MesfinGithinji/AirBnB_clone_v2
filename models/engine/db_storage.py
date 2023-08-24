#!/usr/bin/python3
"""DBStorage implementation"""

from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Database Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize objects and db storage"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""

        class_names = [User, State, City, Amenity, Place, Review]
        dict_objs = {}

        if cls is None:
            for name in class_names:
                query = self.__session.query(name)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.name__, obj.id)
                    dict_objs[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                dict_objs[obj_key] = obj
        return dict_objs

    def new(self, obj):
        """ add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all the changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates the tables in database"""
        Base.metadata.create_all(self.__engine)

        ssn = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        my_ssn = scoped_session(ssn)
        self.__session = my_ssn()

    def close(self):
        """close current query question"""
        self.__session.close()
