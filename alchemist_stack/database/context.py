from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm.session import Session, sessionmaker

from typing import Tuple, Any

__author__ = 'H.D. "Chip" McCullough IV'

class Context(object):
    """
    Database class template.
    """

    def __init__(self, settings: dict, *args, **kwargs):
        self.__engine = create_engine(URL(**settings))
        self.__sessionmaker = sessionmaker(bind=self.__engine, autoflush=True)
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self) -> Session:
        """
        Calling an instance of Database will return a new SQL Alchemy `Session` object. This is equivalent to:
            db = Database(settings=__settings__)
            session_factory = db.sessionmaker
            session = session_factory()
        :returns: A new Session instance
        """
        return self.sessionmaker()

    def __del__(self):
        """
        Called when an instance of Database is about to be destroyed.
        """
        pass

    def __repr__(self) -> str:
        """
        A String representation of the object, with as much information as possible.
        
        :returns: String representation of Database object.
        """
        return '<class Database at {hex_id}>'.format(hex_id=hex(id(self)))

    def __str__(self) -> str:
        """
        A informal, User-Friendly representation of the object.
        
        :returns: User-Friendly String representation of Database.
        """
        return str(self.__engine)

    def __unicode__(self):
        """
        An informal, User-Friendly representation of the object.
        
        :returns: User-Friendly Unicode String representation of Database.
        """
        pass

    def __nonzero__(self) -> bool:
        """
        Called by built-in function `bool`, or when a truth-value test occurs.
        """
        pass

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def sessionmaker(self) -> sessionmaker:
        return self.__sessionmaker

    @property
    def arguments(self) -> Tuple[Any, ...]:
        return self.__args

    @property
    def keyword_arguments(self) -> dict:
        return self.__kwargs
