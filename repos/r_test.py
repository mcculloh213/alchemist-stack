from alchemist_stack.database import Database
from alchemist_stack.repository import RepositoryBase
from models.m_test import Test

__author__ = 'H.D. "Chip" McCullough IV'

class TestRepository(RepositoryBase):
    """

    """

    def __init__(self, database: Database, *args, **kwargs):
        super().__init__(database=database, *args, **kwargs)

    def create_test(self, obj: Test):
        super().create_object(obj=obj.to_orm())
