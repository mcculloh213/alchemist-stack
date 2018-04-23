from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm.session import sessionmaker

from typing import Tuple, Any

__author__ = 'H.D. "Chip" McCullough IV'

class Database(object):
    """
    Database class template.
    """

    def __init__(self, settings: dict, *args, **kwargs):
        self.__engine = create_engine(URL(**settings))
        self.__sessionmaker = sessionmaker(bind=self.__engine, autoflush=True)
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, settings: dict, *args, **kwargs):
        """
        Called when an instace of Database is called, e.g.:
            `x = Database(...)`
            `x(...)`
        """
        return self.__init__(settings, *args, *kwargs)

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
        return '<class Database at {id}>'.format(id=id(self))

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
