from alchemist_stack.database import create_database
from alchemist_stack.repository.models import create_tables
from models.m_test import Test
from repos.r_test import TestRepository

__author__ = 'H.D. "Chip" McCullough IV'

if __name__ == '__main__':
    db = create_database()
    create_tables(engine=db.engine)
    tr = TestRepository(database=db)
    t = Test()
    print(t)
    tr.create_test(obj=t)
