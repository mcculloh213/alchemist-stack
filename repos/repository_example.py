from alchemist_stack.context import Context
from alchemist_stack.repository import RepositoryBase
from models.model_example import Example
from tables.table_example import ExampleTable

__author__ = 'H.D. "Chip" McCullough IV'

class ExampleRepository(RepositoryBase):
    """

    """

    def __init__(self, context: Context, *args, **kwargs):
        """
            Test Repository Constructor
        :param context: The Database object containing the engine used to connect to the context.
        :param args: Additional Arguments
        :param kwargs: Additional Keyword Arguments
        """
        super().__init__(context=context, *args, **kwargs)

    def __repr__(self):
        """

        :return:
        """
        return '<class ExampleRepository->RepositoryBase(context={database}) at {hex_id}>'\
            .format(database=str(self.context),
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