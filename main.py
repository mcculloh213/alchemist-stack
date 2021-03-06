from alchemist_stack.context import create_context
from alchemist_stack.repository.models import create_tables
from tests.models.m_test import Test
from tests.repos.r_test import TestRepository

from datetime import datetime, timezone

__author__ = 'H.D. "Chip" McCullough IV'

if __name__ == '__main__':
    db = create_context()
    create_tables(engine=db.engine)
    tr = TestRepository(context=db)
    t = Test()
    tr.create_test(obj=t)
    t = tr.get_test_by_id(test_id=2)
    count = tr.update_test_by_id(test_id=3, values={'timestamp': datetime.now(timezone.utc).astimezone()})
    print(count)