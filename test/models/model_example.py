from tests.tables.table_example import ExampleTable

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
        Called when an instance of Test is called, e.g.:
            `x = Test(...)`
            `x(...)`
        """
        return self.to_orm()

    def __repr__(self) -> str:
        """
        A String representation of the object, with as much information as possible.

        :returns: String representation of Test object.
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