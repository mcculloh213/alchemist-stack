from alchemist_stack.database import create_database, Database
from .models import Base, B, create_tables

from contextlib import contextmanager
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from typing import Any, Type

__author__ = 'H.D. "Chip" McCullough IV'

class Repo(object):
    """
    Repo class template.
    """

    def __init__(self, *args, **kwargs):
        self.__database = create_database()
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """
        Called when an instance of Repo is called, e.g.:
            `x = Database(...)`
            `x(...)`
        """
        pass

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
        pass

    def __str__(self) -> str:
        """
        A informal, User-Friendly representation of the object.

        :returns: User-Friendly String representation of Database.
        """
        pass

    def __unicode__(self):
        """
        An informal, User-Friendly representation of the object.

        :returns: User-Friendly Unicode String representation of Database.
        """
        pass

    def __nonzero__(self):
        """
        Called by built-in function `bool`, or when a truth-value test occurs.
        """
        pass

class RepositoryBase(object):
    """
    Repository Base class
    """

    def __init__(self, database: Database, *args, **kwargs):
        self.__session_factory = database.sessionmaker
        self.__session = None
        self.__args = args
        self.__kwargs = kwargs
        self.__session_is_open = False
        self.__pending_commit = False

    def __call__(self, *args, **kwargs) -> Session:
        """
        Returns an instance of the session.
        """
        if self.__session_is_open:
            __errors = {
                'repo': self.__str__(),
                'session': str(self.__session),
                'pending_commit': self.__pending_commit,
            }
            raise SessionIsOpenException(
                message='Repository {repo} currently has an open session.'
                    .format(repo=self.__str__()),
                errors=__errors,
                repo=self.__class__
            )
        self.__session_is_open = True
        self.__session = self.__session_factory()
        return self.__session

    def __del__(self):
        """
        Called when an instance of the Repository Base is about to be destroyed.
        """
        if self.__session_is_open and isinstance(self.__session, Session):
            self.__session.close()
            self.__session = None
        del self

    def __repr__(self) -> str:
        """
        A String representation of the object, with as much information as possible.

        :returns: String representation of Repository Base object.
        """
        return '<class {class_name} at {id}>'.format(class_name=self.__class__.__name__,
                                                     id=hex(id(self)))

    def __str__(self) -> str:
        """
        A informal, User-Friendly representation of the object.

        :returns: User-Friendly String representation of Repository Base.
        """
        return self.__class__.__name__

    def __unicode__(self):
        """
        An informal, User-Friendly representation of the object.

        :returns: User-Friendly Unicode String representation of Repository Base.
        """
        pass

    def __nonzero__(self):
        """
        Called by built-in function `bool`, or when a truth-value test occurs.
        """
        return isinstance(self.__session, Session)

    def __cmp__(self, other) -> int:
        """
        Repository Base Comparator. Order is defined by __lt__, __gt__, then __cmp__

        :returns:
            -1 => self < other
            0 => self := other
            1 => self > other
        """
        pass

    def __eq__(self, other) -> bool:
        """
        Repository Base Equality Test
        """
        pass

    def __ne__(self, other) -> bool:
        """
        Repository Base Inequality Test
        """
        pass

    def __lt__(self, other) -> bool:
        """
        Repository Base Less Than Test
        """
        pass

    def __le__(self, other) -> bool:
        """
        Repository Base Less Than or Equal To Test
        """
        pass

    def __ge__(self, other) -> bool:
        """
        Repository Base Greater Than or Equal To Test
        """
        pass

    def __gt__(self, other) -> bool:
        """
        Repository Base Greater Than Test
        """
        pass

    @contextmanager
    def __session_scope(self):
        """
        Transactional scope for committing a series of transactions.
        """
        __session = self.__session_factory()

        if isinstance(__session, Session):
            try:
                yield __session
                __session.commit()
            except:
                __session.rollback()
                raise NoPendingCommitException()
            finally:
                __session.close()
        else:
            raise NoOpenSessionException()

    @property
    def session(self) -> Session:
        if not (self.__session_is_open and isinstance(self.__session, Session)):
            raise Exception()
        return self.__session

    @property
    def pending_commit(self) -> bool:
        return self.__pending_commit

    @property
    def dirty(self) -> bool:
        if isinstance(self.__session, Session):
            return self.__session.dirty
        else:
            return False

    def create_session(self):
        if not (self.__session_is_open and self.pending_commit):
            __errors = {
                'repo': self.__str__(),
                'session': str(self.__session),
                'pending_commit': self.__pending_commit,
            }
            raise SessionIsOpenException(
                message='Repository {repo} currently has an open session.'
                    .format(repo=self.__str__()),
                errors=__errors,
                repo=self.__class__
            )
        self.__session = self.__session_factory()
        self.__open_session()

    def commit_session(self):
        if isinstance(self.__session, Session) and self.pending_commit:
            try:
                self.__session.commit()
                self.__pending_commit = False
            except:
                self.__session.rollback()
                raise NoPendingCommitException()
            finally:
                self.__session.close()
                self.__close_session()
        else:
            raise NoPendingCommitException()

    def close_session(self, force: bool = False):
        if self.__session_is_open and isinstance(self.__session, Session):
            if force:
                self.__session.close()
                self.__close_session()
            else:
                if self.__pending_commit:
                    raise PendingCommitException()

    def __open_session(self):
        self.__session_is_open = True

    def __close_session(self):
        self.__session_is_open = False

    def __create_query(self, cls: B):
        if isinstance(cls, B):
            return Query(entities=cls)
        else:
            __errors = {
                'repo': self.__str__(),
                'session': str(self.__session),
                'entity': str(cls),
            }
            raise UnknownModelException(
                message='The entity {cls} does not inherit from the Declarative Base.'
                    .format(cls=str(cls)),
                errors=__errors,
                model=cls)

    def __bind_session_to_query(self, query: Query) -> Query:
        if self.__session_is_open and isinstance(self.__session, Session):
            return query.with_session(session=self.__session)

    def create_object(self, obj: Type[Base], auto_commit: bool = True):
        if isinstance(obj, Base):
            if auto_commit:
                with self.__session_scope() as s:
                    if isinstance(s, Session):
                        s.add(obj)
                    else:
                        raise NoOpenSessionException()
            else:
                if not (self.__session_is_open and isinstance(self.__session, Session)):
                    self.__session = self.create_session()
                self.__session.add(obj)
                self.__pending_commit = True
                if auto_commit:
                    self.commit_session()
        else:
            __errors = {
                'repo': self.__str__(),
                'session': str(self.__session),
                'entity': obj,
            }
            raise UnknownModelException(
                message='The entity {cls} does not inherit from the Declarative Base.'
                    .format(cls=obj.__cls__.__name__),
                errors=__errors,
                model=obj.__cls__.__name__)

    def read_object(self, cls: B) -> Query:
        if isinstance(cls, B):
            return self.__create_query(cls)

    def update_object(self):
        pass

    def delete_object(self):
        pass

class SessionIsOpenException(Exception):
    """
    Exception for Repo Objects: Session Is Open
    """

    def __init__(self, message: str, errors: dict, repo: Type[RepositoryBase], *args):
        super().__init__(message, *args)
        self.__errors = errors
        self.__repo = repo

    @property
    def errors(self) -> dict:
        return self.__errors

    @property
    def repo(self) -> RepositoryBase:
        return self.__repo


class NoOpenSessionException(Exception):
    """
    Exception for Repo Objects: No Open Session
    """

    def __init__(self):
        pass

class PendingCommitException(Exception):
    """
    Exception for Repo Objects: Pending Commit
    """

    def __init__(self):
        pass

class NoPendingCommitException(Exception):
    """
    Exception for Repo Objects: No Pending Commit
    """

    def __init__(self):
        pass

class UnknownModelException(Exception):
    """
    Exception for Repo Objects: Unknown Model
    """

    def __init__(self, message: str, errors: dict, model: Any, *args):
        super().__init__(message, *args)
        self.__errors = errors
        self.__model = model

    @property
    def errors(self) -> dict:
        return self.__errors

    @property
    def model(self) -> Any:
        return self.__model


