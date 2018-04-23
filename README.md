from sqlalchemy.orm import Query# alchemist-stack
**Package Author**: H.D. 'Chip' McCullough IV\
**Last Updated**: April 23rd, 2018

**Description**:\
A Flexible Model-Repository-Database stack for use with SQL Alchemy

## Overview
Here's probably a good place for a descriptive overview.

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
        return '&lt;Example(timestamp={timestamp})&gt;'.format(timestamp=self.timestamp)
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
        return '&lt;class Test(pk={pk} timestamp={timestamp}) at {hex_id}&gt;'.format(pk=self.__pk,
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
from alchemist_stack.database import Context
from alchemist_stack.repository import RepositoryBase
from models.model_example import Example
from tables.table_example import ExampleTable

__author__ = 'H.D. "Chip" McCullough IV'

class ExampleRepository(RepositoryBase):
    """

    """

    def __init__(self, database: Context, *args, **kwargs):
        """
            Test Repository Constructor
        :param database: The Database object containing the engine used to connect to the database.
        :param args: Additional Arguments
        :param kwargs: Additional Keyword Arguments
        """
        super().__init__(database=database, *args, **kwargs)

    def __repr__(self):
        """

        :return:
        """
        return '&lt;class ExampleRepository->RepositoryBase(database={database}) at {hex_id}&gt;'\
            .format(database=str(self.database),
                    hex_id=hex(id(self.database)))

    def create_example(self, obj: Example):
        self.create_object(obj=obj.to_orm())

    def get_example_by_id(self, example_id: int) -> Example:
        self.create_session()
        __query = self.read_object(cls=ExampleTable)
        __t = __query.with_session(self.session).get(example_id)
        self.close_session()
        if isinstance(__t, ExampleTable):
            return Example.from_orm(__t)

    def update_example_by_id(self, example_id: int, values: dict, synchronize_session: str = 'evaluate') -> int:
        self.create_session()
        __query = self.update_object(cls=ExampleTable, values=values)
        rowcount = __query.with_session(self.session)\
            .filter(ExampleTable.primary_key == example_id)\
            .update(values=values,
                    synchronize_session=synchronize_session)
        self.commit_session()
        return rowcount
```