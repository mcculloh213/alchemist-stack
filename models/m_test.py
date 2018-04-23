from tables.t_test import TestTable

from datetime import datetime, timezone
from typing import TypeVar

__author__ = 'H.D. "Chip" McCullough IV'

T = TypeVar('T', bound="Test")

# http://www.siafoo.net/article/57
class Test(object):
    """
    Test class template.
    """

    def __init__(self, timestamp: datetime = datetime.now(timezone.utc).astimezone(), primary_key: int = None,
                 *args, **kwargs):
        self.__pk = primary_key
        self.__timestamp = timestamp
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, *args, **kwargs) -> TestTable:
        """
        Called when an instance of Test is called, e.g.:
            `x = Test(...)`
            `x(...)`
        """
        return self.to_orm()

    def __del__(self):
        """
        Called when an instance of Test is about to be destroyed.
        """
        pass

    def __repr__(self) -> str:
        """
        A String representation of the object, with as much information as possible.
        
        :returns: String representation of Test object.
        """
        return '<class Test(pk={pk} timestamp={timestamp}) at {hex_id}>'.format(pk=self.__pk,
                                                                                timestamp=self.__timestamp,
                                                                                hex_id=hex(id(self)))

    def __str__(self) -> str:
        """
        A informal, User-Friendly representation of the object.
        
        :returns: User-Friendly String representation of Test.
        """
        return self.__timestamp.isoformat()

    def __unicode__(self):
        """
        An informal, User-Friendly representation of the object.
        
        :returns: User-Friendly Unicode String representation of Test.
        """
        pass

    def __nonzero__(self) -> bool:
        """
        Called by built-in function `bool`, or when a truth-value test occurs.
        """
        pass

    def __cmp__(self, other) -> int:
        """
        Test Comparator. Order is defined by __lt__, __gt__, then __cmp__
        
        :returns: 
            -1 => self < other
            0 => self := other
            1 => self > other
        """
        pass

    def __eq__(self, other) -> bool:
        """
        Test Equality Test
        """
        pass

    def __ne__(self, other) -> bool:
        """
        Test Inequality Test
        """
        pass

    def __lt__(self, other) -> bool:
        """
        Test Less Than Test
        """
        pass

    def __le__(self, other) -> bool:
        """
        Test Less Than or Equal To Test
        """
        pass

    def __ge__(self, other) -> bool:
        """
        Test Greater Than or Equal To Test
        """
        pass

    def __gt__(self, other) -> bool:
        """
        Test Greater Than Test
        """
        pass

    @property
    def id(self) -> int:
        return self.__pk

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def to_orm(self) -> TestTable:
        return TestTable(primary_key=self.__pk, timestamp=self.__timestamp)

    @classmethod
    def from_orm(cls, obj: TestTable) -> T:
        return cls.__init__(cls, obj.timestamp, obj.primary_key)

    
    