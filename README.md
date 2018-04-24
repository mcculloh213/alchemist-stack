# alchemist-stack
**Package Author**: H.D. 'Chip' McCullough IV

**Last Updated**: April 23rd, 2018

**Description**:\
A Flexible Model-Repository-Database stack for use with SQL Alchemy

## Overview
Alchemist Stack is intended to be a thread-safe, multi-session/multi-connection 

## Usage

Example ORM Table:
```python
# table_example.py

from alchemist_stack.repository.models import Base
from sqlalchemy import Column, Integer, DateTime

class ExampleTable(Base):
    __tablename__ = 'example'
    
    primary_key = Column('id', Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return '<Example(timestamp={timestamp})>'.format(timestamp=self.timestamp)
```

Example Model:
```python
# model_example.py

from tables.table_example import ExampleTable

from datetime import datetime, timezone
from typing import TypeVar

E = TypeVar('E', bound="Example")

class Example(object):
    """
        Example Model class.
    """

    def __init__(self, timestamp: datetime = datetime.now(timezone.utc).astimezone(), primary_key: int = None,
                 *args, **kwargs):
        self.__pk = primary_key
        self.__timestamp = timestamp
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, *args, **kwargs) -> ExampleTable:
        """
            Called when an instance of Example is called, e.g.:
                `x = Example(...)`
                `x(...)`
            This is equivalent to calling `to_orm()` on the object instance.
        
        :returns: The ORM of the Example.
        :rtype: ExampleTable
        """
        return self.to_orm()

    def __repr__(self) -> str:
        """
            A detailed String representation of Example.
        
        :returns: String representation of Example object.
        """
        return '<class Test(pk={pk} timestamp={timestamp}) at {hex_id}>'.format(pk=self.__pk,
                                                                                timestamp=self.__timestamp,
                                                                                hex_id=hex(id(self)))

    @property
    def id(self) -> int:
        return self.__pk

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def to_orm(self) -> ExampleTable:
        return ExampleTable(primary_key=self.__pk, timestamp=self.__timestamp)

    @classmethod
    def from_orm(cls, obj: ExampleTable) -> E:
        return cls(timestamp=obj.timestamp, primary_key=obj.primary_key)
```

Example Repository:
```python
# repository_example.py

from alchemist_stack.context import Context
from alchemist_stack.repository import RepositoryBase
from models.model_example import Example
from tables.table_example import ExampleTable

class ExampleRepository(RepositoryBase):
    """

    """

    def __init__(self, context: Context, *args, **kwargs):
        """
            Test Repository Constructor
        :param database: The Database object containing the engine used to connect to the database.
        :param args: Additional Arguments
        :param kwargs: Additional Keyword Arguments
        """
        super().__init__(context=context, *args, **kwargs)

    def __repr__(self):
        """

        :return:
        """
        return '<class ExampleRepository->RepositoryBase(context={context}) at {hex_id}>'\
            .format(context=str(self.context),
                    hex_id=hex(id(self.context)))

    def create_example(self, obj: Example):
        self._create_object(obj=obj.to_orm())

    def get_example_by_id(self, example_id: int) -> Example:
        self._create_session()
        __query = self._read_object(cls=ExampleTable)
        __t = __query.with_session(self.session).get(example_id)
        self._close_session()
        if isinstance(__t, ExampleTable):
            return Example.from_orm(__t)

    def update_example_by_id(self, example_id: int, values: dict, synchronize_session: str = 'evaluate') -> int:
        self._create_session()
        __query = self._update_object(cls=ExampleTable, values=values)
        rowcount = __query.with_session(self.session)\
            .filter(ExampleTable.primary_key == example_id)\
            .update(values=values,
                    synchronize_session=synchronize_session)
        self._commit_session()
        return rowcount
```