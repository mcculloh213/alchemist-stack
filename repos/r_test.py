from alchemist_stack.database import Context
from alchemist_stack.repository import RepositoryBase
from models.m_test import Test
from tables.t_test import TestTable

__author__ = 'H.D. "Chip" McCullough IV'

class TestRepository(RepositoryBase):
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
        return '<class TestRepository->RepositoryBase(database={database}) at {hex_id}>'\
            .format(database=str(self.database),
                    hex_id=hex(id(self.database)))

    def create_test(self, obj: Test):
        self.create_object(obj=obj.to_orm())

    def get_test_by_id(self, test_id: int) -> Test:
        self.create_session()
        __query = self.read_object(cls=TestTable)
        __t = __query.with_session(self.session).get(test_id)
        self.close_session()
        if isinstance(__t, TestTable):
            return Test.from_orm(__t)

    def update_test_by_id(self, test_id: int, values: dict, synchronize_session: str = 'evaluate') -> int:
        self.create_session()
        __query = self.update_object(cls=TestTable, values=values)
        rowcount = __query.with_session(self.session)\
            .filter(TestTable.primary_key == test_id)\
            .update(values=values,
                    synchronize_session=synchronize_session)
        self.commit_session()
        return rowcount
