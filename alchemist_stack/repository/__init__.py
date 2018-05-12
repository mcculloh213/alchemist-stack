# System Imports
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Type

# Third-Party Imports
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from sqlalchemy.util import IdentitySet

# Local Source Imports
from alchemist_stack.context import Context
from .models import Base, B, create_tables

__author__ = 'H.D. "Chip" McCullough IV'

class RepositoryBase(ABC):
    """ Repository Base Abstract Base Class for implementing model repositories """

    __scoped_session_factory = None
    __active_scoped_session = False

    def __init__(self, context: Context, *args, **kwargs):
        """ Repository Base Constructor
        
        :param context: The Database :code:`Context <Context>`
        :type context:
        :param args: 
        :param kwargs: 
        """
        self.__context = context
        self.__session_factory = context.sessionmaker
        self.__local_session = None
        self.__args = args
        self.__kwargs = kwargs
        self.__active_local_session = False
        self.__pending_commit = False

    def __call__(self, *args, **kwargs) -> Session:
        """ Calling an instance of RepositoryBase will return a SQL Alchemy Session instance. If the repository doesn't
                have an existing Session, it will create the Session.
        """
        if not self.__active_local_session:
            self.__active_local_session = True
            self.__local_session = self.__session_factory()
        return self.__local_session

    def __del__(self):
        """ Called when an instance of the Repository Base is about to be destroyed. This will forcibly close the
                Session, losing any uncommitted transactions. If you intend to keep those transactions, call
                `commit_session()`, as this will commit the existing transaction, then close the connection.
        """
        if self.__active_local_session and isinstance(self.__local_session, Session):
            self.__local_session.close()
            self.__local_session = None
            self.__session_close()

    def __repr__(self) -> str:
        """ A String representation of the object, with as much information as possible.

        :returns: String representation of Repository Base object.
        """
        return '<class {class_name} at {id}>'.format(class_name=self.__class__.__name__,
                                                     id=hex(id(self)))

    def __str__(self) -> str:
        """ A informal, User-Friendly representation of the object.

        :returns: User-Friendly String representation of Repository Base.
        """
        return self.__class__.__name__

    def __unicode__(self):
        """ An informal, User-Friendly representation of the object.

        :returns: User-Friendly Unicode String representation of Repository Base.
        """
        return self.__class__.__name__

    def __nonzero__(self):
        """ Called by built-in function `bool`, or when a truth-value test occurs. """
        return isinstance(self.__local_session, Session)

    def __cmp__(self, other) -> int:
        """ Repository Base Comparator. Order is defined by __lt__, __gt__, then __cmp__

        :returns:
            -1 => self < other
            0 => self := other
            1 => self > other
        """
        pass

    def __eq__(self, other) -> bool:
        """ Repository Base Equality Test """
        if isinstance(other, RepositoryBase):
            return self.thread_safe_session is other.thread_safe_session
        return False

    def __ne__(self, other) -> bool:
        """ Repository Base Inequality Test """
        if isinstance(other, RepositoryBase):
            return self.thread_safe_session is not other.thread_safe_session
        return True

    def __lt__(self, other) -> bool:
        """ Repository Base Less Than Test """
        pass

    def __le__(self, other) -> bool:
        """ Repository Base Less Than or Equal To Test """
        pass

    def __ge__(self, other) -> bool:
        """ Repository Base Greater Than or Equal To Test """
        pass

    def __gt__(self, other) -> bool:
        """ Repository Base Greater Than Test """
        pass

    @contextmanager
    def session_scope(self):
        """ Transactional scope for committing a series of transactions.
            If there are no pending transactions (create, update, delete), it will raise a NoPendingCommitException.
            If the session instance was not able to be created, it will raise a NoOpenSessionException.

        :raises: NoPendingCommitException, NoOpenSessionException
        """
        __session = self.__session_factory()

        if isinstance(__session, Session):
            try:
                yield __session
                __session.commit()
            except SQLAlchemyError as sqlerror:  # TODO: Catch psycopg2 IntegretyError -> Expand to other dialects.
                __session.rollback()
                print(sqlerror)
                self.__throw_no_pending_commit_exception()
            finally:
                __session.close()
        else:
            self.__throw_no_open_session_exception()

    @property
    def context(self) -> Context:
        """ Gets the current instance of the Database Context.

        :return: Database Context instance
        :rtype: Context
        """
        return self.__context

    @property
    def local_session(self) -> Session:
        """ Gets the current instance of the SQL Alchemy Session.
                If there is no current session, it will raise a NoOpenSessionException.

        :raises: NoOpenSessionException
        :return: SQL Alchemy Session instance
        :rtype: Session
        """
        if not (self.__active_local_session and isinstance(self.__local_session, Session)):
            self.__throw_no_open_session_exception()
        return self.__local_session

    @property
    def thread_safe_session(self) -> Session:
        """ Gets the current thread-safe Scoped Session.

        :return: SQL Alchemy :code`scoped_session <scoped_session>`
        :rtype: scoped_session
        """
        return self.__scoped_session_factory()

    @property
    def pending_commit(self) -> bool:
        """ Gets the boolean value of whether there is a pending transaction in the current SQL Alchemy Session.

        :return:
            True => There is an open Session, and it contains transactions that need to be committed (create, update, delete).
            False => There either is not an open Session, or there are no pending transactions (read).
        :rtype: bool
        """
        return self.__pending_commit

    @property
    def dirty(self) -> IdentitySet:
        """ Gets the IdentitySet of modified objects in the current open SQL Alchemy Session. If there is no open
                Session, it returns an empty IdentitySet.

        :return: IdentitySet of modified objects in the current open Session.
        :rtype: IdentitySet
        """
        if isinstance(self.__local_session, Session):
            return self.__local_session.dirty
        else:
            return IdentitySet()

    @classmethod
    @abstractmethod
    def instance(cls, context: Context, *args, **kwargs):
        """

        :return:
        """
        raise NotImplementedError

    def _create_session(self):
        """ Creates a new SQL Alchemy Session.
            If there is already an open Session, it will raise a SessionIsOpenException.

        :raises: SessionIsOpenException
        """
        if self.__active_local_session:
            self.__throw_session_is_open_exception()
        self.__local_session = self.__session_factory()
        self.__session_open()

    def _create_thread_safe_session(self):
        """ Creates the context to distribute thread-safe Sessions via
            code:`thread_safe_session <thread_safe_session>`.

        """
        if not self.__active_scoped_session:
            self.__scoped_session_factory = scoped_session(self.__session_factory)
            self.__scoped_session_open()

    def _commit_session(self):
        """ Commits the current open SQL Alchemy Session, saving pending transactions to the context.
            If the Session does not have any pending transactions (create, update, delete), it will raise a
                NoPendingCommitException.
            If there is no current open Session, it will raise a NoOpenSessionException.

        :raises: NoPendingCommitException, NoOpenSessionException
        """
        if self.__active_local_session and isinstance(self.__local_session, Session) and self.pending_commit:
            try:
                self.__local_session.commit()
                self.__pending_commit = False
            except SQLAlchemyError as sqlerror:
                print(sqlerror)
                self.__local_session.rollback()
            finally:
                self.__local_session.close()
                self.__session_close()
        else:
            if not self.__active_local_session:
                self.__throw_no_open_session_exception()
            else:
                self.__throw_no_pending_commit_exception()

    def _close_session(self, force: bool = False):
        """ Closes the current open SQL Alchemy Session.

        :param force: Whether to force the Session closed without committing or not.
            Default: False => Session will be committed before closing.
        :type force: bool
        """
        if self.__active_local_session and isinstance(self.__local_session, Session):
            if force:
                self.__local_session.close()
                self.__session_close()
            else:
                if self.__pending_commit:
                    self._commit_session()
                else:
                    self.__local_session.close()
                    self.__session_close()

    def _remove_thread_safe_sessions(self, force: bool = False):
        """ Closes the current SQL Alchemy Scoped Session

        :param force: Whether to force the Session closed without committing or not.
            Default: False => Session will be committed before closing.
        :type force: bool
        """
        if self.__active_scoped_session:
            if force:
                self.__scoped_session_factory.remove()

    def __session_open(self):
        """ Sets the value of `__session_is_open` to True. """
        self.__active_local_session = True

    def __scoped_session_open(self):
        """ Sets the value of `__active_scoped_session` to True. """
        self.__active_scoped_session = True

    def __session_close(self):
        """ Sets the value of `__session_is_open` to False. """
        self.__local_session = None
        self.__active_local_session = False

    def __scoped_session_close(self):
        """ Kills all thread-local sessions, and sets the value of `__active_scoped_session` to False. """
        if isinstance(self.__scoped_session_factory, scoped_session):
            self.__scoped_session_factory.remove()
            self.__scoped_session_factory = None
            self.__active_scoped_session = False

    def __create_query(self, cls: Base) -> Query:
        """ Creates a raw SQL Alchemy Query on table `cls`. This Query is not bound to a session, and therefore must be
                bound at some point using `Query.with_session(session=...)`.

        :param cls: The Table to query on (must inherit from Base/declarative_base()).
        :type: Base
        :return: A SQL Alchemy Query on table `cls`.
        :rtype: Query
        """
        if issubclass(cls, Base):
            return Query(entities=cls)
        else:
            self.__throw_unknown_model_exception(cls=cls)

    def __bind_current_session_to_query(self, query: Query) -> Query:
        """ Binds the current open SQL Alchemy :code:`Session <Session>` to :parameter:`query <Query>`.

            If there is no currently open :code:`Session <Session>`, it will throw a
            :code:`NoOpenSessionException <NoOpenSessionException>`

        :param query:
        :return:
        """
        if self.__active_local_session and isinstance(self.__local_session, Session):
            return query.with_session(session=self.__local_session)
        else:
            self.__throw_no_open_session_exception()

    def __throw_session_is_open_exception(self):
        """ Raise a :code:`SessionIsOpenException <SessionIsOpenException>` """
        __errors = {
            'repo': self.__str__(),
            'session': str(self.__local_session),
            'pending_commit': self.__pending_commit,
        }
        raise SessionIsOpenException(
            message='Repository {repo} currently has an open session.'
                .format(repo=self.__str__()),
            errors=__errors,
            repo=self.__class__
        )

    def __throw_no_open_session_exception(self):
        """ Raise a :code:`NoOpenSessionException <NoOpenSessionException>` """
        __errors = {
            'repo': self.__str__(),
        }
        raise NoOpenSessionException(
            message='Repository {repo} does not have an open session.'
                .format(repo=self.__str__()),
            errors=__errors,
            repo=self.__class__
        )

    def __throw_pending_commit_exception(self):
        """ Raise a :code:`PendingCommitException <PendingCommitException>` """
        pass

    def __throw_no_pending_commit_exception(self):
        """ Raise a :code:`NoPendingCommitException <NoPendingCommitException>` """
        pass

    def __throw_unknown_model_exception(self, cls: Any):
        """ Raise a :code:`UnknownModelException <UnknownModelException>` """
        __errors = {
            'repo': self.__str__(),
            'session': str(self.__local_session),
            'entity': cls,
        }
        raise UnknownModelException(
            message='The entity {cls} does not inherit from the Declarative Base.'
                .format(cls=cls.__name__),
            errors=__errors,
            model=cls
        )

    def __throw_unknown_column_exception(self, cls: Base, column: str):
        """ Raise a :code:`UnknownColumnException <UnknownColumnException>` """
        __errors = {
            'repo': self.__str__(),
            'session': str(self.__local_session),
            'entity': cls,
            'column': column,
        }
        raise UnknownColumnException(
            message='The entity {cls} does not have a column named {column}'
                .format(cls=cls.__name__,
                        column=column),
            errors=__errors,
            cls=cls,
            column=column
        )

    def __throw_unknown_update_key_exception(self, cls: Base, key: Any, value: Any):
        """ Raise a :code:`SessionIsOpenException <SessionIsOpenException>` """
        __errors = {
            'repo': self.__str__(),
            'entity': cls,
            'update': {
                key: value,
            },
        }
        raise UnknownUpdateKeyException(
            message='The entity {cls} cannot perform an update on {key} with value {value}.'
                .format(cls=cls.__name__,
                        key=key,
                        value=value),
            errors=__errors,
            cls=cls,
            key=key,
            value=value,
        )

    def _create_object(self, obj: Type[Base], auto_commit: bool = True):
        """ Simple CREATE (Crud) operation.

        :param obj: The entity model to be created (inserted). This entity model must inherit from `Base`.
        :type obj: Base
        :param auto_commit: Whether to automatically commit the inserted object to the context and close the Session
        or not.
            Default: True => The object will be added to a separate Session, which will be committed and closed on
        completion.
        :type auto_commit: bool
        """
        if isinstance(obj, Base):
            if auto_commit:
                with self.session_scope() as s:
                    if isinstance(s, Session):
                        s.add(obj)
                    else:
                        self.__throw_no_open_session_exception()
            else:
                if not (self.__active_local_session and isinstance(self.__local_session, Session)):
                    self._create_session()
                self.__local_session.add(obj)
                self.__pending_commit = True
                if auto_commit:
                    self._commit_session()
        else:
            self.__throw_unknown_model_exception(cls=obj)

    def _read_object(self, cls: Base) -> Query:
        """ Simple READ (cRud) operation.

            Creates a simple Query on table `cls`. If `cls` does not inherit from Base, it will raise an
            :code:`UnknownModelException <UnknownModelException>`.

        :param cls: The class to use for the Query. `cls` must inherit from Base.
        :type cls: Base
        :raises: UnknownModelException
        :return: SQL Alchemy Query instance.
        :rtype: Query
        """
        if issubclass(cls, Base):
            return self.__create_query(cls)
        else:
            self.__throw_unknown_model_exception(cls=cls)

    def _update_object(self, cls: Base, values: dict) -> Query:
        """ Simple UPDATE (crUd) operation.

            Creates a simple Query on table `cls` and sets value of `__pending_commit` to True. If `cls` does not
            inherit from Base, it will raise an :code:`UnknownModelException <UnknownModelException>`.

        :param cls: The class to use for the Query. `cls` must inherit from Base.
        :type cls: Base
        :param values: Dictionary of `cls` attributes to update. You may use either string keys, or
            InstrumentedAttribute (cls.attribute) keys.
        :type values: dict
        :raises: UnknownColumnException, UnknownUpdateKeyException, UnknownModelException
        :return: SQL Alchemy Query instance.
        :rtype: Query
        """
        if issubclass(cls, Base):
            for value in values.keys():
                if isinstance(value, str):
                    if not hasattr(cls, value):
                        self.__throw_unknown_column_exception(cls=cls, column=value)
                elif isinstance(value, InstrumentedAttribute):
                    if not hasattr(cls, value.key):
                        self.__throw_unknown_update_key_exception(cls=cls, key=value, value=values.get(value))
                else:
                    self.__throw_unknown_column_exception(cls=cls, column=value)
            self.__pending_commit = True
            return self.__create_query(cls=cls)
        else:
            self.__throw_unknown_model_exception(cls=cls)

    def _delete_object(self):
        """ Simple DELETE (cruD) operation.
        :return:
        """
        pass

    def base_query_on(self, cls: Base) -> Query:
        if isinstance(cls, Base):
            if self.__active_scoped_session:
                return self.__scoped_session_factory.query_property(query_cls=cls)
            else:
                self._create_thread_safe_session()
                return self.__scoped_session_factory.query_property(query_cls=cls)
        else:
            self.__throw_unknown_model_exception(cls=cls)

class SessionIsOpenException(Exception):
    """ Exception for Repo Objects: Session Is Open """

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
    """ Exception for Repo Objects: No Open Session"""

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

class PendingCommitException(Exception):
    """ Exception for Repo Objects: Pending Commit """

    def __init__(self):
        pass

class NoPendingCommitException(Exception):
    """ Exception for Repo Objects: No Pending Commit """

    def __init__(self):
        pass

class UnknownModelException(Exception):
    """ Exception for Repo Objects: Unknown Model """

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

class UnknownColumnException(Exception):
    """ Exception for Repo Objects: Unknown Column """

    def __init__(self, message: str, errors: dict, cls: Base, column: str, *args):
        super().__init__(message, *args)
        self.__errors = errors
        self.__cls = cls
        self.__column = column

    @property
    def errors(self) -> dict:
        return self.__errors

    @property
    def cls(self) -> Base:
        return self.__cls

    @property
    def column(self) -> str:
        return self.__column

class UnknownUpdateKeyException(Exception):
    """ Exception for Repo Objects: Unknown Update Key """

    def __init__(self, message: str, errors: dict, cls: Base, key: Any, value: Any, *args):
        super().__init__(message, *args)
        self.__errors = errors
        self.__cls = cls
        self.__key = key
        self.__value = value

    @property
    def errors(self) -> dict:
        return self.__errors

    @property
    def cls(self) -> Base:
        return self.__cls

    @property
    def key(self) -> Any:
        return self.__key

    @property
    def value(self) -> Any:
        return self.__value
