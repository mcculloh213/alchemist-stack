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
        return '<class ExampleRepository->RepositoryBase(database={database}) at {hex_id}>'\
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